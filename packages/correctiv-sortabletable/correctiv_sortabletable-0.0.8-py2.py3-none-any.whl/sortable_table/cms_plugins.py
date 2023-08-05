import json

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SortableTablePlugin


@plugin_pool.register_plugin
class SortableTableCMSPlugin(CMSPluginBase):
    """
    Plugin for including a selection of entries
    """
    module = _('Table')
    name = _('Sortable Table')
    model = SortableTablePlugin
    render_template = 'sortable_table/render_table.html'
    text_enabled = True

    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ('creator',)

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        context = super(SortableTableCMSPlugin, self).render(
            context, instance, placeholder)
        context['table_id'] = instance.pk
        context['object'] = instance
        context['settings'] = json.dumps(instance.settings)
        context.update(instance.get_table_context())
        return context

    def icon_src(self, instance):
        return settings.STATIC_URL + "cms/img/icons/plugins/link.png"
