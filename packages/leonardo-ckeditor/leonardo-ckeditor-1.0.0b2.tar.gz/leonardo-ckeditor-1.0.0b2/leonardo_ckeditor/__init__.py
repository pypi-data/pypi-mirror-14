
from django.apps import AppConfig

from .ckeditor_config import DEFAULT_CONFIG

default_app_config = 'leonardo_ckeditor.Config'

LEONARDO_APPS = [
    'leonardo_ckeditor',
    'ckeditor',
    'ckeditor_uploader'
]

LEONARDO_CONFIG = {
    'CKEDITOR_UPLOAD_PATH': ('', ('CKEditor upload directory')),
    'CKEDITOR_CONFIGS': ({'default': DEFAULT_CONFIG}, 'ckeditor config')
}
LEONARDO_OPTGROUP = 'CKEditor'

LEONARDO_JS_FILES = [
    "leonardo_ckeditor/js/ckeditor-modal-init.js",
]
LEONARDO_CSS_FILES = [
    'ckeditor/ckeditor/skins/moono/editor.css'
]
LEONARDO_PUBLIC = True

LEONARDO_URLS_CONF = 'ckeditor_uploader.urls'


class Config(AppConfig):
    name = 'leonardo_ckeditor'
    verbose_name = "leonardo-ckeditor"

    def ready(self):
        from ckeditor_uploader.widgets import CKEditorUploadingWidget
        from leonardo.module.web.widget.htmltext import models
        models.HtmlTextWidget.widgets['text'] = CKEditorUploadingWidget()

        from .utils import monkey_patch_ckeditor
        monkey_patch_ckeditor()
