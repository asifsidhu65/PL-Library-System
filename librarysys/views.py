from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class Index(LoginRequiredMixin, TemplateView):

    http_method_names = ['get']
    template_name = 'home/index.html'
