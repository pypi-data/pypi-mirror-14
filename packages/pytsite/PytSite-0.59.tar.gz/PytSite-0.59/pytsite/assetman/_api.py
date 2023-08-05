"""Asset Manager.
"""
from os import path as _path
from importlib.util import find_spec as _find_spec
from pytsite import router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_packages = {}
_locations = {'css': [], 'js': []}
_last_weight = {'css': 0, 'js': 0}
_permanent_last_weight = {'css': 0, 'js': 0}
_inline = []


def register_package(package_name: str, assets_dir: str='res/assets'):
    """Register assets container.
    """
    spec = _find_spec(package_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(package_name))

    dir_path = _path.join(_path.dirname(spec.origin), assets_dir)
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    _packages[package_name] = dir_path


def get_packages() -> dict:
    """Get registered packages.
    """
    return _packages


def add(location: str, collection: str=None, weight=0, permanent=False):
    """Add an asset.
    """
    if not collection:
        if location.endswith('.js'):
            collection = 'js'
        elif location.endswith('.css'):
            collection = 'css'
        else:
            raise ValueError("Cannot detect collection for location '{}'.".format(location))

    if not weight:
        if permanent:
            _permanent_last_weight[collection] += 1
            weight = _permanent_last_weight[collection]
        else:
            _last_weight[collection] += 1
            weight = _last_weight[collection]

    if not [i for i in _locations[collection] if i[0] == location]:
        _locations[collection].append((location, weight, permanent))


def add_inline(s: str, weight=0, forever=False):
    """Add a code which intended to output in the document.
    """
    _inline.append((s, weight, forever))


def remove(location, collection: str=None):
    """Remove an asset location.
    """
    if not collection:
        if isinstance(location, str):
            if location.endswith('.js'):
                collection = 'js'
            elif location.endswith('.css'):
                collection = 'css'
            else:
                raise ValueError("Cannot detect collection of '{}'.".format(location))
        else:
            raise ValueError("Cannot detect collection of '{}'.".format(location))

    if isinstance(location, str):
        _locations[collection] = [l for l in _locations[collection] if l[0] != location]
    elif not isinstance(location, str) and location.__class__.__name__ == 'SRE_Pattern':
        # Compiled regular expression
        _locations[collection] = [l for l in _locations[collection] if not location.match(l[0])]
    else:
        raise TypeError('String or compiled regular expression expected.')


def reset():
    """Remove all previously added locations.
    """
    global _inline

    for location in ('css', 'js'):
        # Filter out all except 'permanent' items
        _locations[location] = [l for l in _locations[location] if l[2]]

    # Filter out all except 'permanent' items
    _inline = [item for item in _inline if item[2]]

    # Reset last weight counter
    global _last_weight
    _last_weight = {'css': 0, 'js': 0}


def get_locations(collection: str) -> list:
    return [l for l in sorted(_locations[collection], key=lambda x: x[1])]


def get_inline() -> list:
    return sorted(_inline, key=lambda x: x[1])


def dump_js() -> str:
    """Dump JS links.
    """
    r = ''
    for loc_url in get_urls('js'):
        r += '<script type="text/javascript" src="{}"></script>\n'.format(loc_url)

    return r


def dump_css() -> str:
    """Dump CSS links.
    """
    r = ''
    for loc_url in get_urls('css'):
        r += '<link rel="stylesheet" href="{}">\n'.format(loc_url)

    return r


def dump_inline() -> str:
    r = ''
    for item in _inline:
        r += item[0]

    return r


def url(location: str) -> str:
    """Get URL of an asset.
    """
    if location.startswith('http') or location.startswith('//'):
        return location
    package_name, asset_path = _split_asset_location_info(location)

    return _router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


def get_urls(collection: str) -> list:
    """Get URLs of all locations in the collection.
    """
    return [url(l[0]) for l in get_locations(collection)]


def _split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    package_name = 'app'
    asset_path = location
    path_parts = location.split('@')
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in _packages:
        raise Exception("Package '{}' is not registered.".format(package_name))

    return package_name, asset_path
