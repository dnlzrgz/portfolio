from django import template
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


def has_children(page):
    return page.get_children().live().exists()


def is_active(page, current_page):
    return current_page.url_path.startswith(page.url_path) if current_page else False
