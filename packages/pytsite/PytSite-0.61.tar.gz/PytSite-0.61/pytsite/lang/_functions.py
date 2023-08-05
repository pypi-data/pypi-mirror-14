"""PytSite Language Support
"""
import yaml as _yaml
from importlib.util import find_spec as _find_spec
from datetime import datetime as _datetime
from os import path as _path
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__languages = []
__current = None
__fallback = None
__packages = {}

__default_regions = {
    'en': 'US',
    'ru': 'RU',
    'uk': 'UA',
}


def define(languages: list):
    """Define available languages.
    """
    global __languages
    __languages = languages
    set_current(languages[0])
    set_fallback(languages[0])


def langs(include_current=True):
    """Get all available languages.
    :rtype: list[str]
    """
    if include_current:
        return __languages
    else:
        return [lng for lng in __languages if lng != __current]


def set_current(language: str):
    """Set current default language.
    """
    if language not in __languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported.".format(language))

    global __current
    __current = language


def set_fallback(language: str):
    """Set fallback language.
    """
    if language not in __languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported.".format(language))

    global __fallback
    __fallback = language


def get_current() -> str:
    """Get current language.
    """
    if not __languages:
        raise Exception("No languages are defined.")

    return __current


def get_fallback() -> str:
    """Get fallback language.
    """
    if not __languages:
        raise Exception("No languages are defined.")

    return __fallback


def is_package_registered(pkg_name):
    """Check if the package already registered.
    """
    return pkg_name in __packages


def register_package(pkg_name: str, languages_dir: str='res/lang') -> str:
    """Register language container.
    """
    if is_package_registered(pkg_name):
        return

    spec = _find_spec(pkg_name)
    if not spec or not spec.loader:
        raise Exception("Package '{}' is not found.".format(pkg_name))

    lng_dir = _path.join(_path.dirname(spec.origin), languages_dir)
    if not _path.isdir(lng_dir):
        raise Exception("Directory '{}' is not exists.".format(lng_dir))

    __packages[pkg_name] = {'__path': lng_dir}


def get_packages() -> dict:
    """Get info about registered packages.
    """
    return __packages


def is_translation_defined(msg_id: str, language: str=None, use_fallback=True) -> bool:
    """Check if the translation is defined for message ID.
    """
    try:
        t(msg_id, None, language, True, use_fallback)
        return True
    except _error.TranslationError:
        return False


def t(msg_id: str, args: dict=None, language: str=None, exceptions=False, use_fallback=True) -> str:
    """Translate a message ID.
    """
    if not language:
        language = get_current()

    if language not in __languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported.".format(language))

    # Determining package name and message ID
    package_name, msg_id = _split_msg_id(msg_id)

    # Loading language file data
    lang_file_content = load_lang_file(package_name, language)

    if msg_id not in lang_file_content:
        # Searching for fallback translation
        fallback = get_fallback()
        if use_fallback and fallback != language:
            return t(package_name + '@' + msg_id, args, fallback, exceptions, False)
        else:
            if exceptions:
                raise _error.TranslationError("Translation is not found for '{}@{}'".format(package_name, msg_id))
            else:
                return package_name + '@' + msg_id

    msg = lang_file_content[msg_id]

    # Replacing placeholders
    if args:
        for k, v in args.items():
            msg = msg.replace(':' + str(k), str(v))

    return msg


def t_plural(msg_id: str, num: int=2, language: str=None) -> str:
    """Translate a string in plural form.
    """
    if not language:
        language = get_current()

    if language in ['en']:
        if num == 1:
            return t(msg_id + '_plural_one')
        else:
            return t(msg_id + '_plural_two')

    # Language is not english
    if 11 <= num <= 19:
        return t(msg_id + '_plural_zero')
    else:
        last_digit = int(str(num)[-1])
        if last_digit in [0, 5, 6, 7, 8, 9]:
            return t(msg_id + '_plural_zero')
        elif last_digit in [2, 3, 4]:
            return t(msg_id + '_plural_two')
        else:
            return t(msg_id + '_plural_one')


def lang_title(language: str=None) -> str:
    """Get human readable language name.
    """
    if not language:
        language = get_current()
    try:
        return t('lang_title_' + language, exceptions=True)
    except _error.TranslationError:
        return language


def load_lang_file(pkg_name: str, language: str=None):
    """Load package's language file.

    :rtype: dict[str, str]
    """
    # Is the package registered?
    if not is_package_registered(pkg_name):
        raise _error.PackageNotRegistered("Package '{}' is not registered.".format(pkg_name))

    if not language:
        language = get_current()

    # Getting from cache
    if language in __packages[pkg_name]:
        return __packages[pkg_name][language]

    content = {}

    # Actual data loading
    file_path = _path.join(__packages[pkg_name]['__path'], language + '.yml')
    if not _path.exists(file_path):
        return content

    with open(file_path, encoding='utf-8') as f:
        content = _yaml.load(f)

    if content is None:
        content = {}

    # Caching
    __packages[pkg_name][language] = content

    return content


def time_ago(time: _datetime) -> str:
    """Format date/time as 'time ago' phrase.
    """
    diff = _datetime.now() - time
    """:type: datetime.timedelta"""

    if diff.days:
        if diff.days > 365:
            years = diff.days // 365
            return '{} {}'.format(years, t_plural('pytsite.lang@year', years))
        elif diff.days > 31:
            months = diff.days // 12
            return '{} {}'.format(months, t_plural('pytsite.lang@month', months))
        elif diff.days > 7:
            weeks = diff.days // 7
            return '{} {}'.format(weeks, t_plural('pytsite.lang@week', weeks))
        else:
            return '{} {}'.format(diff.days, t_plural('pytsite.lang@day', diff.days))
    else:
        if diff.seconds > 3600:
            hours = diff.seconds // 3600
            return '{} {}'.format(hours, t_plural('pytsite.lang@hour', hours))
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return '{} {}'.format(minutes, t_plural('pytsite.lang@minute', minutes))
        else:
            return '{} {}'.format(diff.seconds, t_plural('pytsite.lang@second', diff.seconds))


def pretty_date(time: _datetime) -> str:
    """Format date as pretty string.
    """
    r = '{} {}'.format(time.day, t_plural('pytsite.lang@month_' + str(time.month)))

    diff = _datetime.now() - time
    if diff.days > 365:
        r += ' ' + str(time.year)

    return r


def pretty_date_time(time: _datetime) -> str:
    """Format date/time as pretty string.
    """
    return '{}, {}'.format(pretty_date(time), time.strftime('%H:%M'))


def ietf_tag(language: str=None, region: str=None, sep: str='-') -> str:
    global __default_regions

    if not language:
        language = get_current()

    if not region:
        if language not in __default_regions:
            raise ValueError("Cannot determine default region for language '{}'.".format(language))
        else:
            region = __default_regions[language]

    return language.lower() + sep + region.upper()


def _split_msg_id(msg_id: str) -> tuple:
    """Split message ID into message ID and package name.
    """
    package_name = 'app'
    msg_id = msg_id.split('@')
    if len(msg_id) == 2:
        package_name = msg_id[0]
        msg_id = msg_id[1]
    else:
        msg_id = msg_id[0]

    return package_name, msg_id
