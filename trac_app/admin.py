from django.contrib import admin
from .models import Role, RUser , Product, Permission, Favourite

# Register your models here

admin.site.register(Role)
admin.site.register(RUser)
admin.site.register(Product)
admin.site.register(Permission)
admin.site.register(Favourite)