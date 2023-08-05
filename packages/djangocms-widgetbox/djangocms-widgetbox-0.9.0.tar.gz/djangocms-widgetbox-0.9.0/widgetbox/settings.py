from django.conf import settings


GALLERY_STYLES = getattr(
    settings, 'WIDGETBOX_GALLERY_STYLES',
    (('widgetbox/gallery.html', 'default'),)
)

FAQ_STYLES = getattr(
    settings, 'WIDGETBOX_FAQ_STYLES',
    (('widgetbox/faq-topic.html', 'default'),)
)

DIVIDER_SIZES = getattr(
    settings, 'WIDGETBOX_DIVIDER_SIZES', ())

CONTAINER_KINDS = getattr(
    settings, 'WIDGETBOX_CONTAINER_KINDS', (
        ('container', 'container'),
        ('container-fluid', 'container-fluid'),
    )
)

LIST_STYLES = getattr(
    settings, 'WIDGETBOX_LIST_STYLES', (
        ('widgetbox/ul.html', 'Unordered list (ul)'),
        ('widgetbox/ol.html', 'Ordered list (ol)'),
    )
)
