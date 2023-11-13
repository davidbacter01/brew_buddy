from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UnitOfMeasure, UOMCategory, Ingredient, Reciepe, ReciepeLine, DensityReading, BrewBatch

admin.site.register(User, UserAdmin)
admin.site.register(UnitOfMeasure)
admin.site.register(Reciepe)
admin.site.register(DensityReading)
admin.site.register(Ingredient)
admin.site.register(BrewBatch)
admin.site.register(UOMCategory)
admin.site.register(ReciepeLine)
