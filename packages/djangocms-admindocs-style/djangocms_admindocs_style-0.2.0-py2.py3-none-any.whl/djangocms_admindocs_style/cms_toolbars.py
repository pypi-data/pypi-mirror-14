from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK

@toolbar_pool.register
class AdminDocsToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER
        )
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        url = reverse('django-admindocs-docroot')
        admin_menu.add_sideframe_item(_('Documentation'), url=url, position=position)
