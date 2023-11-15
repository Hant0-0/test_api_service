from django.contrib import admin

from vpn_service.models import UserProfile, UserSite, SiteStatistic


admin.site.register(UserProfile)


class UserSiteAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_site_name', 'original_site']
    list_filter = ['user']


admin.site.register(UserSite, UserSiteAdmin)


class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'clicks_count', 'data_sent', 'data_received']


admin.site.register(SiteStatistic, SiteStatisticAdmin)

