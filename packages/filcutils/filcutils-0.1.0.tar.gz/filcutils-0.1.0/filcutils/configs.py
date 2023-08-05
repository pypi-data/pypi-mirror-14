import logging
import importlib.util
from .dicts import merge_dict_list, merge_dicts

logger = logging.getLogger(__name__)


def load_configs(config_paths):
    configs = [load_config_dict_py(path) for path in config_paths]
    return merge_dict_list(configs)


def load_config_dict_py(config_path):
    def _read_pyfile(path):
        spec = importlib.util.spec_from_file_location("config", path)
        new_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(new_module)
        return new_module

    def _inspect_module(module):
        return dict([(key, getattr(module, key)) for key in dir(module) if _is_config_option(module, key)])

    def _is_config_option(obj, key):
        val = getattr(obj, key)
        has_opt_type = isinstance(val, (list, str, dict, bool, int, bytes)) or val is None
        return key.isupper() or not key.startswith('_') and has_opt_type

    try:
        return _inspect_module(_read_pyfile(config_path))
    except (FileNotFoundError, AttributeError):
        logger.error('Config file ({0}) does not exists.'.format(config_path))
        return {}
