from django.urls import path

from projectapp.views import ProjectCreateView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
]