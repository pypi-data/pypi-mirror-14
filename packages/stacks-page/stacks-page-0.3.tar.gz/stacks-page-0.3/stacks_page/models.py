from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField
from versatileimagefield.fields import VersatileImageField, PPOIField

from .managers import (
    StacksPageModelManager,
    StacksPageModelManagerPublishedModelManager
)
from .utils import publish_StacksPage_instance

TEMPLATES_CHOICES = getattr(
    settings,
    'STACKSPAGE_TEMPLATES',
    (
        ('stacks_page/default_page_template.html', 'Default Page Template'),
    )
)


class StacksPageBase(models.Model):
    """
    A base model for shared attributes/logic across stacks_page models
    """
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        auto_now=True
    )
    objects = StacksPageModelManager()
    published = StacksPageModelManagerPublishedModelManager()

    class Meta:
        abstract = True


class StacksPage(StacksPageBase):
    """
    Represents a single HTML page.
    """
    title = models.CharField(
        _('Page Title'),
        max_length=100,
        help_text=(
            'The title of the page. Currently only used for SEO.'
        )
    )
    slug = models.SlugField(
        _('Page Slug'),
        unique=True
    )
    description = models.TextField(
        _('Page Description'),
        help_text=(
            'A short description of the page. The text entered here will be '
            'used for SEO and Facebook share text.'
        )
    )
    keywords = models.CharField(
        _('Keywords'),
        help_text=(
            "Used to populate the 'Keywords' meta tag (used for SEO)."
        ),
        max_length=300,
        blank=True
    )
    twitter_share_text = models.CharField(
        _('Twitter Share Text'),
        max_length=110,
        blank=True,
        help_text=(
            "The text to use when sharing this page to Twitter. Limited to "
            "110 characters."
        )
    )
    canonical_image = VersatileImageField(
        _('Canonical Image'),
        upload_to='images/canonical',
        max_length=300,
        help_text=(
            'An image that represents this page. Is used when this page is '
            'shared on social media.'
        ),
        blank=True,
        ppoi_field='canonical_image_ppoi'
    )
    canonical_image_ppoi = PPOIField()
    publish = models.BooleanField(
        _('Publish Live on Save?'),
        default=False,
        help_text=(
            'Signifies whether this page is viewable to the public.'
        )
    )
    template_path = models.CharField(
        _('Template'),
        max_length=200,
        default='stacks_page/default_page_template.html',
        choices=TEMPLATES_CHOICES,
        help_text=(
            'The path to the template (within this django project) used to '
            'render this page. Used only by developers.'
        )
    )
    live_url = models.URLField(
        _('Live URL'),
        max_length=250,
        blank=True,
        help_text='The URL this page will live at once live in production.'
    )

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        permissions = (
            (
                "can_set_stacks_page_url",
                "Can edit Stacks Page 'Live URL' values"
            ),
        )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stackspage-detail', kwargs={'slug': self.slug})


class StacksPageSection(StacksPageBase):
    """
    Represents a 'section' of content on a page.
    """
    page = models.ForeignKey(
        StacksPage,
        verbose_name=_('Page'),
        related_name='sections'
    )
    title_section = models.CharField(
        _('Title'),
        max_length=140,
        help_text=(
            'The title of this section.'
        )
    )
    title_menu = models.CharField(
        max_length=80,
        help_text=(
            "The 'menu title' of this section."
        )
    )
    slug = models.SlugField(
        _('Section Slug'),
        max_length=80,
    )
    order = models.PositiveIntegerField(
        _('Order'),
        help_text=(
            'The order this page appears on the parent page.'
        )
    )
    content = TextPlusStuffField(
        _('Content'),
        blank=True,
        null=True,
        help_text=('The content of this page section.')
    )
    twitter_share_text = models.CharField(
        _('Twitter Share Text'),
        max_length=110,
        blank=True,
        help_text=(
            "The text to use when sharing this page to Twitter. Limited to "
            "110 characters. If this field is blank the text entered in the "
            "the parent page's Twitter Share Text will be used."
        )
    )

    class Meta:
        verbose_name = _('Page Section')
        verbose_name_plural = _('Page Sections')
        ordering = ('page', 'order')
        unique_together = ('page', 'slug')

    def __unicode__(self):
        return "{page_title} #{order} {section_title}".format(
            page_title=self.page.title,
            order=self.order,
            section_title=self.title_menu
        )


@receiver(models.signals.post_save, sender=StacksPage)
def save_static_rendition(sender, instance, **kwargs):
    """Save a static version of a StacksPage instance."""
    if instance.live_url and instance.publish is True:
        publish_StacksPage_instance(instance)
