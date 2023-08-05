from django.apps import AppConfig
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from ..frontend.apps import ModuleMixin
from ..frontend.urlconf import ModuleURLResolver


class MaterialAdminConfig(ModuleMixin, AppConfig):
    name = 'material.admin'
    label = "material_admin"

    icon = '<i class="mdi mdi-action-settings-applications"></i>'
    verbose_name = _("Administration")
    order = 1000

    @property
    def urls(self):
        return ModuleURLResolver(r'^admin/', admin.site.urls[0], namespace='admin', module=self)

    def index_url(self):
        return reverse('admin:index'.format(self.label))
