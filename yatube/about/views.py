from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Страница автора проекта."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Страница технологий проекта."""
    template_name = 'about/tech.html'
