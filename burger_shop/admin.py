from django.contrib import admin
from .models import Profile, Order, MenuItem, OrderItem, CustomBurger, Ingredient, CustomBurgerRecipe, BlogPost


class CustomBurgerRecipeInline(admin.TabularInline):
    model = CustomBurgerRecipe
    extra = 1

class CustomBurgerAdmin(admin.ModelAdmin):
    inlines = [CustomBurgerRecipeInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuItem)
admin.site.register(CustomBurger,CustomBurgerAdmin)
admin.site.register(Ingredient)
admin.site.register(BlogPost)
