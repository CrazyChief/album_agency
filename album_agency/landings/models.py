import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from subprocess import call

upload_storage = FileSystemStorage(
    location=settings.LANDING_UPLOAD_ROOT, base_url='/landings')

static_upload_storage = FileSystemStorage(
    location=settings.LANDING_UPLOAD_ROOT, base_url='/landings')

static_upload_css = FileSystemStorage(
            location=settings.LANDING_UPLOAD_CSS, base_url='/landings')
static_upload_js = FileSystemStorage(
            location=settings.LANDING_UPLOAD_JS, base_url='/landings')
static_upload_font = FileSystemStorage(
            location=settings.LANDING_UPLOAD_FONTS, base_url='/landings')


def get_upload_path(instance, filename):
    """ Dynamic folder choise.
        keep this func for migrations :D
    """
    UPLOAD_DIRS = (
        (0, 'css/'),
        (1, 'fonts/'),
        (2, 'js/'),
    )
    upl = UPLOAD_DIRS[instance.file_type][1]
    if upl == 'css/':
        static_upload = FileSystemStorage(
            location=settings.LANDING_UPLOAD_CSS, base_url='/landings')
    elif upl == 'js/':
        static_upload = FileSystemStorage(
            location=settings.LANDING_UPLOAD_JS, base_url='/landings')
    else:
        static_upload = FileSystemStorage(
            location=settings.LANDING_UPLOAD_FONTS, base_url='/landings')
    path = os.path.join(
      settings.BASE_DIR,
      'landings/static/',
      f'{UPLOAD_DIRS[instance.file_type][1]}',
      filename)
    return path


class StaticFile(models.Model):
    CSS_FILE, FONT_FILE, JS_FILE = range(3)
    STATIC_CHOICES = (
        (CSS_FILE, 'CSS File'),
        (FONT_FILE, 'Font'),
        (JS_FILE, 'JavaScript File'),
    )

    file_name = models.CharField(
        _('File name'), unique=True, max_length=100,
        help_text=_('Use same name as uploaded file'))
    static_css = models.FileField(
        upload_to='',
        storage=static_upload_css,
        verbose_name=_('Static File (.css)'),
        max_length=500,
        blank=True,
        null=True
    )
    static_js = models.FileField(
        upload_to='',
        storage=static_upload_js,
        verbose_name=_('Static File (.js)'),
        max_length=500,
        blank=True,
        null=True
    )
    static_font = models.FileField(
        upload_to='',
        storage=static_upload_font,
        verbose_name=_('Static File (fonts)'),
        max_length=500,
        blank=True,
        null=True
    )
    file_type = models.SmallIntegerField(
        _('File Type'), choices=STATIC_CHOICES)
    is_active = models.BooleanField(_('Is Active?'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Static File')
        verbose_name_plural = _('Static Files')

    def __str__(self):
        return f'Static file: {self.file_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def is_file_active(self):
        return self.is_active

    is_file_active.admin_order_field = "is_active"
    is_file_active.boolean = True
    is_file_active.short_description = _("Is file active?")

    @property
    def make_file_path(self):
        UPLOAD_DIRS = (
            (0, 'css/'),
            (1, 'fonts/'),
            (2, 'js/'),
        )
        return f'landings/{UPLOAD_DIRS[self.file_type][1]}{self.file_name}'


class TemplateFile(models.Model):
    name = models.CharField(
        _('Name'), max_length=250,
        help_text=_('Same object name as for uploaded file'))
    template_file = models.FileField(
        upload_to='',
        storage=upload_storage,
        verbose_name=_('Template file (HTML file)'))
    static_files = models.ManyToManyField(
        StaticFile, verbose_name=_('Used static files'))
    is_active = models.BooleanField(
        default=False, verbose_name=_('Is template active?'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Template File')
        verbose_name_plural = _('Template Files')

    def __str__(self):
        return f'Template File {self.name}'

    def is_template_active(self):
        return self.is_active

    is_template_active.admin_order_field = "is_active"
    is_template_active.boolean = True
    is_template_active.short_description = _("Is template active?")


class Landing(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    title_page = models.CharField(
        max_length=250, default="", verbose_name=_('Title for page'))
    slug = models.SlugField(null=True, blank=True)
    template = models.ForeignKey(
        TemplateFile, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Template'))
    meta_description = models.TextField(
        null=True, blank=True, verbose_name=_('Meta description'))
    is_active = models.BooleanField(
        default=False, verbose_name=_('Is landing active?'))
    images_count = models.IntegerField(_('Images count'), default=5)
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date added'))
    date_changed = models.DateTimeField(
        auto_now=True, verbose_name=_('Date changed'))

    class Meta:
        ordering = ['-date_added']
        verbose_name = _('Landing')
        verbose_name_plural = _('Landings')

    def __str__(self):
        return "Landing {}".format(self.title_page)

    def is_landing_active(self):
        return self.is_active

    is_landing_active.admin_order_field = "is_active"
    is_landing_active.boolean = True
    is_landing_active.short_description = _("Is landing active?")

    @property
    def get_template_path(self):
        return self.template.template_file.url[1:]


def upload_path(instance, filename):
    """
    Path to files
    :param instance:
    :param filename:
    :return:
    """
    return "landings/{0}".format(filename)


class LandingImage(models.Model):
    image = models.ImageField(
        upload_to=upload_path, verbose_name=_('Cover picture'))
    landing = models.ForeignKey(
        Landing, on_delete=models.CASCADE, verbose_name=_('Landing Page'))
    position = models.IntegerField(_('Image position'), default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Landing Image')
        verbose_name_plural = _('Landing Images')

    def __str__(self):
        return f'Image for Landing {self.landing}'


#   deleting uploaded file from file storage,
#   when model object had deleted from db.
#   Template(.html) file in our case.

@receiver(pre_delete, sender=TemplateFile)
def template_delete(sender, instance, **kwargs):
    instance.template_file.delete(False)


@receiver(pre_delete, sender=LandingImage)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(pre_delete, sender=StaticFile)
def static_file_delete(sender, instance, **kwargs):
    if instance.file_type == 0:
        instance.static_css.delete(False)
    elif instance.file_type == 2:
        instance.static_js.delete(False)
    else:
        instance.static_font.delete(False)


@receiver(post_save, sender=StaticFile)
def collect_static(sender, instance, **kwargs):
    call([
        "python",
        "album_agency/manage.py",
        "collectstatic",
        "-v",
        "0",
        "--no-input"
    ])
