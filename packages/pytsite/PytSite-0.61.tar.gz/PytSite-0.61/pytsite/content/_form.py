"""Content Forms.
"""
from pytsite import form as _form, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Settings(_form.Form):
    """Content Settings Form.
    """
    def _setup(self):
        i = 10
        for lang_code in _lang.langs():
            self.add_widget(_widget.input.Text(
                uid='setting_home_title_' + lang_code,
                label=_lang.t('pytsite.content@home_page_title', {'lang_code': lang_code.upper()},
                              language=lang_code),
                weight=i,
            ))
            i += 10

            self.add_widget(_widget.input.Text(
                uid='setting_home_description_' + lang_code,
                label=_lang.t('pytsite.content@home_page_description', {'lang_code': lang_code.upper()},
                              language=lang_code),
                weight=i,
            ))
            i += 10

            self.add_widget(_widget.input.Tokens(
                uid='setting_home_keywords_' + lang_code,
                label=_lang.t('pytsite.content@home_page_keywords', {'lang_code': lang_code.upper()},
                              language=lang_code),
                weight=i,
            ))
            i += 10

        self.add_widget(_widget.input.TextArea(
            uid='setting_add_js',
            label=_lang.t('pytsite.content@additional_js_code'),
            rows=10,
            weight=i,
        ))
