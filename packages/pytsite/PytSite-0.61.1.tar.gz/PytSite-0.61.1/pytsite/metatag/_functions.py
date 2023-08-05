"""PytSite Meta Tags Support.
"""
from pytsite import lang as _lang, util as _util, reg as _reg, events as _events, assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__tags = {'link': []}

__allowed_tags = (
    'title',
    'author',
    'link',
    'description',
    'charset',
    'viewport',
    'keywords',
    'og:title',
    'og:description',
    'og:locale',
    'og:image',
    'og:image:width',
    'og:image:height',
    'og:url',
    'og:type',
    'article:author',
    'article:publisher',
    'twitter:card',
    'twitter:title',
    'twitter:description',
    'twitter:image',
    'twitter:site',
    'fb:app_id',
    'fb:admins',
)


def reset():
    """Reset tags.
    """
    global __tags

    __tags = {'link': []}

    t_set('charset', 'UTF-8')
    t_set('title', _lang.t('pytsite.metatag@untitled_document'))
    t_set('viewport', 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0')
    t_set('link', rel='icon', type='image/png', href=_assetman.url(_reg.get('metatag.favicon.href')))


def t_set(tag: str, value: str=None, **kwargs):
    """Set tag value.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{}'".format(tag))

    if tag in ('link',):
        if tag == 'link':
            if not kwargs.get('rel'):
                raise ValueError("<link> tag must contain 'rel' attribute")
            if not kwargs.get('href'):
                raise ValueError("<link> tag must contain 'href' attribute")

        value = ''
        for k, v in kwargs.items():
            value += ' {}="{}"'.format(k, v)

        __tags['link'].append(value)
    else:
        __tags[tag] = _util.escape_html(value)


def get(tag: str) -> str:
    """Get value of the tag.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    if tag not in __tags:
        return ''

    return __tags[tag]


def dump(tag: str) -> str:
    """ Dump single tag.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    if tag not in __tags:
        return ''

    if tag == 'charset':
        r = '<meta charset="{}">\n'.format(__tags[tag])
    elif tag == 'title':
        r = '<title>{} | {}</title>\n'.format(__tags[tag], _lang.t('app_name'))
    elif tag.startswith('og:') or tag.startswith('author:') or tag.startswith('fb:'):
        r = '<meta property="{}" content="{}">'.format(tag, __tags[tag])
    elif tag == 'link':
        r = ''
        for value in __tags[tag]:
            r += '<{}{}>\n'.format(tag, value)
    else:
        r = '<meta name="{}" content="{}">'.format(tag, __tags[tag])

    return r


def dump_all() -> str:
    """Dump all tags.
    """
    _events.fire('pytsite.metatag.dump_all')

    r = str()
    for tag in __tags:
        r += dump(tag) + '\n'

    return r
