
from django.urls import path
from projects.views import ProjectAboutView, ProjectListView, ProjectPageView


# Маршруты приложения "projects"
urlpatterns = [
    path('projects', ProjectAboutView.as_view(), name='projectsPage'),
    path('all-projects', ProjectListView.as_view(), name='allProjectsPage'),
    path('projects/project/<slug:projectSlug>', ProjectPageView.as_view(), name='projectPage'),
]
