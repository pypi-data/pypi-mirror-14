import pkgutil
import inspect
import logging
import datetime
import collections
from importlib import import_module
from .exceptions import Misconfigured
import mixins
import config
import es


_elasticsearch_indices = collections.defaultdict(lambda: [])


logger = logging.getLogger(__name__)


def find_search_types(module, base=mixins.ElasticsearchIndexMixin):
    """Returns a list of automatically detected search type
    classes. Useful for populating ELASTICSEARCH_TYPE_CLASSES.

    :param module: The module to search.
    :type module: A Python module.
    :param base: A class that your search type classes inherit from.
    :type base: A Python class.
    :returns:  A list of type classes that inherit from base.
    """
    retrieved_types = []

    for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
        module_to_load = '.'.join([module.__name__, modname])
        obj = import_module(module_to_load)
        if ispkg:
            retrieved_types.extend(find_search_types(obj, base))
        else:
            module_klasses = inspect.getmembers(
                obj,
                lambda x: inspect.isclass(x) and
                issubclass(x, base)
            )

            for name, klass in module_klasses:
                if klass is not base and klass not in retrieved_types:
                    retrieved_types.append(klass)

    return retrieved_types


def get_indices(indices=None):
    """Returns indices and their search type classes

    :param indices: Filter returned indices by this list.
    :type indices: list.
    :returns:  A dictionary containing indices as keys and
               a list of search classes as values.
    :raises: Misconfigured
    """
    if not _elasticsearch_indices:
        type_classes = getattr(
            config.settings,
            'ELASTICSEARCH_TYPE_CLASSES',
            ()
        )

        if not type_classes:
            raise Misconfigured(
                'Missing ELASTICSEARCH_TYPE_CLASSES in settings.'
            )

        for type_class in type_classes:
            if inspect.isclass(type_class):
                klass = type_class
            else:
                package_name, klass_name = type_class.rsplit('.', 1)
                try:
                    package = import_module(package_name)
                    klass = getattr(package, klass_name)
                except (ImportError, AttributeError):
                    logger.error('Unable to import `{}`.'.format(type_class))
                    continue

            _elasticsearch_indices[klass.get_index_name()].append(klass)

    result = {}
    if not indices:
        result = _elasticsearch_indices.copy()
    else:
        for k, v in _elasticsearch_indices.items():
            if k in indices:
                result[k] = v

    if not result:
        raise Misconfigured(
            'ELASTICSEARCH_TYPE_CLASSES configured, but none could be loaded.'
        )

    return result


def get_indices_from_aliases(search_aliases=None):
    """Returns indices associated with aliases

    :param search_aliases: Search aliases to get indices for.
    :type search_aliases: list.
    :returns:  A list of indices
    """
    if not search_aliases:
        search_aliases = []

    indices = []

    for alias in search_aliases:
        indices.extend([
            index
            for index, aliases in es.get_aliases().items()
            if alias in aliases['aliases'].keys()
        ])

    return indices


def get_alias_names(aliases=None):
    """Return unique names from aliases

    :param aliases: A list alias/index tuples to get names of.
    :type search_aliases: list
    :returns:  A unique list of alias names
    """
    return list(set([alias[0] for alias in aliases or []]))


def generate_aliases_for_removal():
    current_aliases = es.get_aliases()
    aliases_for_removal = collections.defaultdict(lambda: [])
    for item, tmp in current_aliases.items():
        for iname in list(tmp.get('aliases', {}).keys()):
            aliases_for_removal[iname].append(item)

    return aliases_for_removal


def generate_actions(indices=None, aliases_for_removal=None):
    actions = []
    indices = indices or []
    aliases_for_removal = aliases_for_removal or collections.defaultdict(lambda: [])

    for index_alias, index_name in indices:
        for item in aliases_for_removal[index_alias]:
            actions.append({
                'remove': {
                    'index': item,
                    'alias': index_alias
                }
            })
        actions.append({
            'add': {
                'index': index_name,
                'alias': index_alias
            }
        })

    return actions


def create_aliases(indices=None):
    indices = indices or []

    aliases_for_removal = generate_aliases_for_removal()
    actions = generate_actions(indices, aliases_for_removal)
    es.update_aliases({'actions': actions})


def create_indices(indices=None, set_aliases=True):
    result = []
    aliases = []
    indices = indices or []

    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    for index_alias, type_classes in get_indices(indices).items():
        index_settings = recursive_dict_update(
            getattr(
                config.settings,
                'ELASTICSEARCH_DEFAULT_INDEX_SETTINGS',
                {}
            ),
            getattr(
                config.settings,
                'ELASTICSEARCH_CUSTOM_INDEX_SETTINGS',
                {}
            ).get(index_alias, {})
        )

        index_name = '{0}-{1}'.format(index_alias, now)

        aliases.append((index_alias, index_name))

        type_mappings = {}
        for type_class in type_classes:
            tmp = type_class.get_type_mapping()
            if tmp:
                type_mappings[type_class.get_type_name()] = tmp

            result.append((
                type_class,
                index_alias,
                index_name
            ))

        # if we got any type mappings, put them in the index settings
        if type_mappings:
            index_settings['mappings'] = type_mappings

        es.create_index(index_name, index_settings)

    if set_aliases:
        create_aliases(aliases)

    return result, aliases


def delete_indices(indices=None):
    es.delete_indices(indices or [])


def rebuild_indices(indices=None, set_aliases=True):
    indices = indices or []
    created_indices, aliases = create_indices(indices, False)

    current_index_name = None

    def change_index():
        if current_index_name:
            es.refresh_index(current_index_name)

    for type_class, index_alias, index_name in created_indices:
        if index_name != current_index_name:
            change_index()
            current_index_name = index_name

        try:
            type_class.bulk_index(index_name)
        except NotImplementedError:
            logger.error(
                'bulk_index not implemented on {} - {}.'.format(
                    type_class.get_index_name(),
                    type_class.__name__
                )
            )
            continue
    else:
        change_index()

    if set_aliases:
        alias_names = get_alias_names(aliases)
        existing_aliased_indices = get_indices_from_aliases(alias_names)

        create_aliases(aliases)

        new_aliased_indices = get_indices_from_aliases(alias_names)

        for index in existing_aliased_indices:
            # Ensure that there are new aliased indices, and that our old
            # index is not somehow in them.
            if new_aliased_indices and index not in new_aliased_indices:
                if config.settings.ELASTICSEARCH_DELETE_OLD_INDICES:
                    delete_indices(get_indices(index))

    return created_indices, aliases


def recursive_dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = recursive_dict_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d
