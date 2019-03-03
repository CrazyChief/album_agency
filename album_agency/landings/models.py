import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

upload_storage = FileSystemStorage(
    location=settings.LANDING_UPLOAD_ROOT, base_url='/landings')

static_upload_storage = FileSystemStorage(
    location=settings.LANDING_UPLOAD_ROOT, base_url='/landings')

def get_upload_path(instance, filename):
    """ Dynamic folder choise.
    """
    UPLOAD_DIRS = (
        (0, 'css/'),
        (1, 'fonts/'),
        (2, 'js/'),
    )
    instance.file_name = filename
    return os.path.join(
      settings.BASE_DIR, 
      'landings/static/', 
      f'{UPLOAD_DIRS[instance.file_type][1]}', 
      filename)


class StaticFile(models.Model):
    CSS_FILE, FONT_FILE, JS_FILE = range(3)
    STATIC_CHOICES = (
        (CSS_FILE, 'CSS File'),
        (FONT_FILE, 'Font'),
        (JS_FILE, 'JavaScript File'),
    )

    file_name = models.CharField(
        _('File name'), unique=True, max_length=100)
    static_file = models.FileField(
        upload_to=get_upload_path,
        verbose_name=_('Static Files (.css, .js, fonts)'),
        max_length=500
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


class TemplateFile(models.Model):
    name = models.CharField(
        _('Name'), max_length=250, 
        help_text=_('Same object name as for uploaded file'))
    template_file = models.FileField(
        upload_to='',
        storage=upload_storage,
        verbose_name=_('Template file (HTML file)'))
    is_active = models.BooleanField(
        default=False, verbose_name=_('Is template active?'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Template File')
        verbose_name_plural = _('Template Files')
    
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


def upload_path(instance, filename):
    """
    Path to files
    :param instance:
    :param filename:
    :return:
    """
    return "landing/{0}".format(filename)

class LandingImage(models.Model):
    image = models.ImageField(
        upload_to=upload_path, verbose_name=_('Cover picture'))
    alternative_text = models.CharField(
        _('Alternative Image Text'), max_length=250)
    landing = models.ForeignKey(
        Landing, on_delete=models.CASCADE, verbose_name=_('Landing Page'))
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Landing Image')
        verbose_name_plural = _('Landing Images')
    
    def __str__(self):
        return f'Image {self.alternative_text} for Landing {self.landing}'


#   deleting uploaded file from file storage,
#   when model object had deleted from db.
#   Template(.html) file in our case.

@receiver(pre_delete, sender=Landing)
def template_delete(sender, instance, **kwargs):
    instance.template_file.delete(False)


@receiver(pre_delete, sender=LandingImage)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
