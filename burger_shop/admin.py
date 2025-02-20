from django.contrib import admin
from .models import Profile, Order, MenuItem, OrderItem, CustomBurger, Ingredient, CustomBurgerRecipe, BlogPost, BurgerReview


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


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price')
    list_filter = ('category',)
    list_editable = ('price',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price')
    list_filter = ('category',)
    list_editable = ('price',)

admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(CustomBurger,CustomBurgerAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(BlogPost)
admin.site.register(BurgerReview)
