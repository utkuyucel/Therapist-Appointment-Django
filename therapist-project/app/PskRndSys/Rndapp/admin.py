from django.contrib import admin
from .models import Danisan, Terapist, Randevular

class DanisanAdmin(admin.ModelAdmin):
  list_display = ("name", "second_name", "email", "gender", "price")
  
class TerapistAdmin(admin.ModelAdmin):
  list_display = ("name", "second_name", "email", "gender")
  
  
class RandevularAdmin(admin.ModelAdmin):
  pass

admin.site.register(Danisan, DanisanAdmin)
admin.site.register(Terapist, TerapistAdmin)
admin.site.register(Randevular, RandevularAdmin)
