from __future__ import unicode_literals

from cms.models import CMSPlugin
from cmsplugin_filer_video import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from os.path import basename

class FilerVideo(CMSPlugin):
    # player settings
    movie = FilerFileField(
        verbose_name=_('movie file'),
        help_text=_('use h264 encoded video file or .webm / .ogg files'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    movie_url = models.CharField(_('movie url'), max_length=255, help_text=_('vimeo or youtube (embeddable!) video url. Example: https://www.youtube.com/embed/dd4D8tZPfKE'), blank=True, null=True)
    image = FilerImageField(
        verbose_name=_('image'),
        help_text=_('preview image file'),
        null=True,
        blank=True,
        related_name='filer_video_image',
        on_delete=models.SET_NULL,
    )

    UNIT_CHOICES = (
        ('px', _("pixels (px)")),
        ('%', _("percent (%)")),
        ('em', _("relative to font size (em)")),
    )

    width = models.PositiveSmallIntegerField(_('width'), default=settings.VIDEO_WIDTH)
    width_units = models.CharField(_("width units"), max_length=2, choices=UNIT_CHOICES, default=settings.VIDEO_UNITS)
    height = models.PositiveSmallIntegerField(_('height'), default=settings.VIDEO_HEIGHT)
    height_units = models.CharField(_("height units"), max_length=2, choices=UNIT_CHOICES, default=settings.VIDEO_UNITS)

    controls = models.BooleanField(_('controls'), default=settings.VIDEO_CONTROLS)
    muted = models.BooleanField(_('muted'), default=settings.VIDEO_MUTED)
    auto_play = models.BooleanField(_('auto play'), default=settings.VIDEO_AUTOPLAY)
    loop = models.BooleanField(_('loop'), default=settings.VIDEO_LOOP)

    PRELOAD_CHOICES = (
        ('auto', _("yes")),
        ('metadata', _("metadata only")),
        ('none', _("no")),
    )
    preload = models.CharField(_('preload'), max_length=16, choices=PRELOAD_CHOICES, default=settings.VIDEO_PRELOAD)

    cmsplugin_ptr = models.OneToOneField(
        to=CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.movie:
            name = self.movie.path
        else:
            name = self.movie_url
        return "%s" % basename(name)

    def get_height(self):
        return "%s" % (self.height)

    def get_width(self):
        return "%s" % (self.width)

    def get_movie(self):
        if self.movie:
            return self.movie.url
        else:
            return self.movie_url

    def get_file_extension(self):
        if self.movie:
            return self.__str__().split('.')[-1]
        else:
            return None
