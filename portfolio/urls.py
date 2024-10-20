from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from search import views as search_views
from blog.feeds import RssFeed, AtomFeed

urlpatterns = [
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path(settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("rss/", RssFeed(), name="rss_feed"),
    path("atom/", AtomFeed(), name="atom_feed"),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("sitemap.xml", sitemap),
    path("", include(wagtail_urls)),
]
