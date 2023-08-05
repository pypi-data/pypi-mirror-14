from django.conf import settings


GALLERY_STYLES = (
    ('widgetbox/gallery.html', 'default'),
)
if hasattr(settings, 'WIDGETBOX_GALLERY_STYLES'):
    GALLERY_STYLES += settings.WIDGETBOX_GALLERY_STYLES

FAQ_STYLES = (
    ('widgetbox/faq-topic.html', 'default'),
)
if hasattr(settings, 'WIDGETBOX_FAQ_STYLES'):
    FAQ_STYLES += settings.WIDGETBOX_FAQ_STYLES

DIVIDER_SIZES = ()
if hasattr(settings, 'WIDGETBOX_DIVIDER_SIZES'):
    DIVIDER_SIZES = settings.WIDGETBOX_DIVIDER_SIZES

CONTAINER_KINDS = (
    ('container', 'container'),
    ('container-fluid', 'container-fluid'),
)
if hasattr(settings, 'WIDGETBOX_CONTAINER_KINDS'):
    CONTAINER_KINDS = settings.WIDGETBOX_CONTAINER_KINDS

LIST_STYLES = (
    ('widgetbox/ul.html', 'Unordered list (ul)'),
    ('widgetbox/ol.html', 'Ordered list (ol)'),
)
if hasattr(settings, 'WIDGETBOX_LIST_STYLES'):
    LIST_STYLES += settings.WIDGETBOX_LIST_STYLES
