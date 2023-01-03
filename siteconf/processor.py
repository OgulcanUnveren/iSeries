from siteconf.models import TopSiteConf
from pages.models import FooterPages
def secret(request):
    return {
         
         'topconfs': TopSiteConf.objects.first(),
         'footerpages':FooterPages.objects.all(),
         }