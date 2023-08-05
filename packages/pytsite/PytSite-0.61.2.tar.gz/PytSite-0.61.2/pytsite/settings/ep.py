"""Settings Plugin Endpoints
"""
import re as _re
from pytsite import auth as _auth, tpl as _tpl, metatag as _metatag, lang as _lang, router as _router, http as _http, \
    form as _form, admin as _admin
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def form(args: dict, inp: dict) -> str:
    """Render settings form.
    """
    uid = args.get('uid')

    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    setting_def = _api.get_definition(uid)
    _metatag.t_set('title', _lang.t(setting_def['title']))

    frm = _api.get_form(uid)

    for k, v in _api.get_setting(uid).items():
        field_name = 'setting_' + k
        if frm.has_widget(field_name):
            frm.get_widget(field_name).set_val(v)

    return _admin.render(_tpl.render('pytsite.settings@form', {'form': frm}))


def form_validate(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """
    uid = inp.get('__setting_uid')

    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    try:
        _api.get_form(uid).fill(inp, mode='validation').validate()
        return {'status': True}
    except _form.error.ValidationError as e:
        return {'status': False, 'messages': {'widgets': e.errors}}


def form_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process settings form submit.
    """
    uid = args.get('uid')
    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    frm = _api.get_form(uid).fill(inp)

    value = {}
    for k, v in frm.values.items():
        if k.startswith('setting_'):
            k = _re.sub('^setting_', '', k)
            value[k] = v

    _api.set_setting(uid, value)
    _router.session().add_success(_lang.t('pytsite.settings@settings_has_been_saved'))

    return _http.response.Redirect(frm.values['__form_location'])


def _check_permissions(uid: str) -> bool:
    section_def = _api.get_definition(uid)
    if section_def['perm_name'] == '*':
        return True

    return _auth.get_current_user().has_permission(section_def['perm_name'])
