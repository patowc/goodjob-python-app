from django.urls import path

from .views import goodjob_view

urlpatterns = [
    path('', goodjob_view),
]
