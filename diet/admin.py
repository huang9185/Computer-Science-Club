from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Food)
admin.site.register(Foodgroup)
admin.site.register(Subgroup)
admin.site.register(Record)