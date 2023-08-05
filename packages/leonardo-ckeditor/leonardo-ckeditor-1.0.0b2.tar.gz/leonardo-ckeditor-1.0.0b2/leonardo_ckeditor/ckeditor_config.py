

from ckeditor.widgets import DEFAULT_CONFIG

DEFAULT_CONFIG.update({'allowedContent': True})
DEFAULT_CONFIG.update({'height': 350})

DEFAULT_CONFIG.update({'toolbar_Full': [
    ["Cut", "Copy", "Paste", "PasteText",
     "PasteFromWord", "-", "Undo", "Redo"],
    ["Find", "Replace", "-", "SelectAll", "-", "SpellChecker", "Scayt"],
    ["Form", "Checkbox", "Radio", "TextField", "Textarea",
        "Select", "Button", "ImageButton", "HiddenField"],
    ["Bold", "Italic", "Underline", "Strike",
        "Subscript", "Superscript", "-", "RemoveFormat"],
    ["NumberedList", "BulletedList", "-", "Outdent",
     "Indent", "-", "Blockquote", "CreateDiv",
        "-", "JustifyLeft", "JustifyCenter", "JustifyRight",
        "JustifyBlock", "-", "BidiLtr", "BidiRtl"],
    ["Link", "Unlink", "Anchor"],
    ["Image", "Flash", "Table", "HorizontalRule",
        "Smiley", "SpecialChar", "PageBreak", "Iframe"],
    ["Styles", "Format", "Font", "FontSize"],
    ["TextColor", "BGColor"],
    ["Maximize", "ShowBlocks"],
    ["Source"]]})
