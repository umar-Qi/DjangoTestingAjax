from django.contrib import admin
from .models import Employee, Office, Jobs, Contact, Product
# Register your models here.
admin.site.register((Employee))
admin.site.register((Office))
admin.site.register((Jobs))
admin.site.register((Contact))
admin.site.register((Product))