from django.contrib import admin
from rango.models import UserProfil
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

class UserProfilAdmin(admin.ModelAdmin):
	list_display = ('name', 'email','website','picture')	

admin.site.register(Category) 
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfil)
