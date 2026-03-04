"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("taggit_autosuggest/", include("taggit_autosuggest.urls")),
    path("", include("cms.urls")),
]
