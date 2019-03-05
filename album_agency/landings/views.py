import json
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from .models import Landing


class LandingView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.piece = request.META["PATH_INFO"].split('/')[2]
        self.object = Landing.objects.get(slug__exact=self.piece)
        self.template_name = self.object.get_template_path
        return super(LandingView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        css = self.object.template.static_files.filter(file_type=0)
        context['css_static_files'] = [{'file': x.make_file_path} for x in css]
        js = self.object.template.static_files.filter(file_type=2)
        context['js_static_files'] = [{'file': x.make_file_path} for x in js]
        images = self.object.landingimage_set.all()
        for i in images:
            context[f'back{i.position}'] = i
        return context
