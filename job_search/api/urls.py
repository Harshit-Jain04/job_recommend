from django.urls import path

from .views import JobView, SkillView

urlpatterns = [
    path('job/', JobView.as_view(),name = 'job'),
    path('skill', SkillView.as_view(),name = 'skill'),
]