from django.contrib import admin
from ebid.models import *
from django.contrib.auth.models import Group

admin.site.register(Organization)
admin.site.register(Award)
admin.site.register(BidInformation)
admin.site.register(BidLineItem)
admin.site.register(BiddersList)
admin.site.register(MyUser)
admin.site.unregister(Group)
admin.site.register(BidInstance)