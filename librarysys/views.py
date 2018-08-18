from django.views.generic import TemplateView


class Index(TemplateView):

    http_method_names = ['get']
    template_name = 'index.html'
