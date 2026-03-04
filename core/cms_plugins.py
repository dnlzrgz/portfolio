from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from core.models import HeroTitle


@plugin_pool.register_plugin
class HeroTitlePlugin(CMSPluginBase):
    model = HeroTitle
    name = _("Hero Title")
    render_template = "plugins/hero_title.html"
    cache = False
