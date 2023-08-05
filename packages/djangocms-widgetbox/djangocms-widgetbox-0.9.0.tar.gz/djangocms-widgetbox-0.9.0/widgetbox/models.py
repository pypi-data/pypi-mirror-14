from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from .settings import (
    GALLERY_STYLES, FAQ_STYLES, DIVIDER_SIZES,
    CONTAINER_KINDS, LIST_STYLES
)

from cms.models import CMSPlugin
from cms.models.fields import PageField

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


class LinkMixin(object):
    def get_link(self):
        if self.link_custom:
            return self.link_custom
        elif self.link_to_page:
            return self.link_to_page.get_absolute_url()
        else:
            return ''


@python_2_unicode_compatible
class Button(LinkMixin, CMSPlugin):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)

    link_to_page = PageField(null=True, blank=True)
    link_custom = models.CharField(
        max_length=400, blank=True,
        help_text='Overrides page link if set.')

    icon = models.CharField(
        max_length=50, blank=True,
        help_text='Use it for Font Awesome, GLYPHICONS, or similar icons.')
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to button.')

    class Meta:
        db_table = 'widgetbox_buttons'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Quote(CMSPlugin):
    content = HTMLField()
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=400, blank=True)
    image = FilerImageField(null=True, blank=True)

    class Meta:
        db_table = 'widgetbox_quotes'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Gallery(CMSPlugin):
    style = models.CharField(
        max_length=100,
        choices=GALLERY_STYLES,
        default=GALLERY_STYLES[0][0]
    )

    class Meta:
        db_table = 'widgetbox_galleries'

    def __str__(self):
        return u'Gallery ({})'.format(self.style)

    def get_html_id(self):
        return u'gallery-{}'.format(self.pk)


@python_2_unicode_compatible
class GalleryImage(LinkMixin, CMSPlugin):
    image = FilerImageField()
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    link_to_page = PageField(null=True, blank=True)
    link_custom = models.CharField(max_length=400, blank=True)

    class Meta:
        db_table = 'widgetbox_gallery_images'

    def __str__(self):
        return str(self.image)

    def get_title(self):
        return self.title or self.image.label

    def get_description(self):
        return self.description or self.image.description


@python_2_unicode_compatible
class FaqTopic(CMSPlugin):
    topic = models.CharField(max_length=400)
    style = models.CharField(
        max_length=100,
        choices=FAQ_STYLES, default=FAQ_STYLES[0][0]
    )

    class Meta:
        db_table = 'widgetbox_faq_topics'

    def __str__(self):
        return u'FAQ topic ({})'.format(self.style)


@python_2_unicode_compatible
class Faq(CMSPlugin):
    question = models.CharField(max_length=400)
    answer = HTMLField()

    class Meta:
        db_table = 'widgetbox_faqs'

    def __str__(self):
        return self.question


@python_2_unicode_compatible
class Divider(CMSPlugin):
    size = models.CharField(max_length=10, choices=DIVIDER_SIZES)

    class Meta:
        db_table = 'widgetbox_dividers'

    def __str__(self):
        return self.size


@python_2_unicode_compatible
class HTML(CMSPlugin):
    content = models.TextField(help_text="This is unsafe and potentially dangerous. "
                                         "Be aware of what you are doing.")

    class Meta:
        db_table = 'widgetbox_html'

    def __str__(self):
        return self.content[:80]


@python_2_unicode_compatible
class Row(CMSPlugin):
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to row.')

    class Meta:
        db_table = 'widgetbox_rows'

    def __str__(self):
        return self.extra_css_classes


@python_2_unicode_compatible
class Column(CMSPlugin):
    css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Defines column class, eg col-md-6')
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to column.')

    class Meta:
        db_table = 'widgetbox_columns'

    def __str__(self):
        extra = u' ({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return self.css_classes + extra


@python_2_unicode_compatible
class Container(CMSPlugin):
    kind = models.CharField(
        max_length=20, choices=CONTAINER_KINDS, default=CONTAINER_KINDS[0][0],
        help_text='Container kind, contained or fluid.')
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to column.')

    class Meta:
        db_table = 'widgetbox_containers'

    def __str__(self):
        extra = u' ({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return self.get_kind_display() + extra


@python_2_unicode_compatible
class List(CMSPlugin):
    style = models.CharField(
        max_length=100, choices=LIST_STYLES, default=LIST_STYLES[0][0],
        help_text='Choose list style (template)')
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to list.')

    class Meta:
        db_table = 'widgetbox_lists'

    def __str__(self):
        extra = u' ({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return self.get_style_display() + extra


@python_2_unicode_compatible
class ListItem(CMSPlugin):
    item_text = models.CharField(
        max_length=400, blank=True,
        help_text='Text value for list item, use it for simple lists.')
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to list.')

    class Meta:
        db_table = 'widgetbox_list_items'

    def __str__(self):
        extra = u' ({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return self.item_text[:100] + extra


@python_2_unicode_compatible
class BackgroundImage(CMSPlugin):
    image = FilerImageField()
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to background image.')

    class Meta:
        db_table = 'widgetbox_background_images'

    def __str__(self):
        extra = u'({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return extra


@python_2_unicode_compatible
class Tab(CMSPlugin):
    extra_css_classes = models.CharField(
        max_length=200, blank=True,
        help_text='Use it to add extra CSS classes to tab.')

    class Meta:
        db_table = 'widgetbox_tabs'

    def __str__(self):
        extra = u'({})'.format(self.extra_css_classes) if self.extra_css_classes else u''
        return extra


@python_2_unicode_compatible
class TabPane(CMSPlugin):
    title = models.CharField(max_length=200)
    tabid = models.SlugField(max_length=200, blank=True)

    class Meta:
        db_table = 'widgetbox_tab_panes'

    def __str__(self):
        return self.title

    def get_tabid(self):
        return self.tabid or str(self.pk)
