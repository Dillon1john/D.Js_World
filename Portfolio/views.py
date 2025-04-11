from django.shortcuts import render

from django.views.generic import TemplateView
from .models import Project


# Create your views here.



class HomeView(TemplateView):
    template_name = 'Portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProjectListView(TemplateView):
    template_name = 'Portfolio/allProjects.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 6


class ProjectDetailView(TemplateView):
    template_name = 'Portfolio/projectDetail.html'
    model = Project
    context_object_name = 'project'


