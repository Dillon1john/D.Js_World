from django.shortcuts import render

from django.views.generic import TemplateView,  ListView, DetailView
from .models import *


# Create your views here.



class HomeView(TemplateView):
    template_name = 'Portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'Portfolio/allProjects.html'
    ordering = ['title']
    context_object_name = 'projects'
    paginate_by = 6
    if model:
        print('Model found')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProjectDetailView(DetailView):
    template_name = 'Portfolio/projectDetail.html'
    model = Project
    technologies = Project.technologies
    context_object_name = 'project'

    def split_and_sort(self, input_string):
        # Split the string by comma and strip whitespace
        split_list = [item.strip() for item in input_string.split(',')]
        # Return sorted list
        return sorted(split_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        technologies = Project.objects.get(pk=project_id).technologies
        context['technologies'] = self.split_and_sort(technologies)
        return context




