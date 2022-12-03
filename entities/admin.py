from django.contrib import admin
from entities.models import Category, Origin, Hero, Villain, HeroAcquaintance

# Register your models here.
admin.site.register(Category)
admin.site.register(Origin)
admin.site.register(Hero)
admin.site.register(Villain)
admin.site.register(HeroAcquaintance)

