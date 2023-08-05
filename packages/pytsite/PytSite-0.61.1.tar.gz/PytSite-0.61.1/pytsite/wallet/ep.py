"""PytSite Wallet Endpoints
"""
from pytsite import tpl as _tpl, http as _http, router as _router, odm as _odm, lang as _lang, metatag as _metatag, \
    odm_ui as _odm_ui, admin as _admin

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def transactions_cancel(args: dict, inp: dict):
    browse_url = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'})

    ids = inp.get('ids')
    if not ids:
        return _http.response.Redirect(browse_url)

    if isinstance(ids, str):
        ids = (ids,)

    f_action = _router.ep_url('pytsite.wallet.ep.transactions_cancel_submit')
    f = _odm_ui.get_mass_action_form('wallet-transaction-cancel', 'wallet_transaction', ids, f_action)
    f.get_widget('button-submit').color = 'danger'

    _metatag.t_set('title', _lang.t('pytsite.wallet@odm_ui_form_title_delete_wallet_transaction'))

    return _admin.render(_tpl.render('pytsite.odm_ui@delete_form', {'form': f}))


def transactions_cancel_submit(args: dict, inp: dict):
    ids = inp.get('ids')
    if not ids:
        return _http.response.Redirect(inp.get('__redirect'))

    if isinstance(ids, str):
        ids = (ids,)

    for eid in ids:
        entity = _odm.dispense('wallet_transaction', eid)
        """:type: pytsite.wallet._model.Transaction"""
        entity.cancel()

    redirect = inp.get('__redirect', _router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'}))
    return _http.response.Redirect(redirect)
