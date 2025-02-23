from django.contrib import admin
from .models import Profile, Order, MenuItem, OrderItem, CustomBurger, Ingredient, CustomBurgerRecipe, BlogPost, BurgerReview


class CustomBurgerRecipeInline(admin.TabularInline):
    model = CustomBurgerRecipe
    extra = 1

class CustomBurgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'total_price')
    inlines = [CustomBurgerRecipeInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'user', 'total_price', 'order_status')
    list_filter = ('time', 'user')
    inlines = [OrderItemInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    list_editable = ('price',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    list_editable = ('price',)

class BurgerReviewAdmin(admin.ModelAdmin):
    list_display = ('burger', 'user', 'rating')
    list_filter = ('user', 'burger')

class ProfileAdmin(admin.ModelAdmin):
    def user_id(self, obj):
        return obj.user.id

    def user_name(self, obj):
        return obj.user.first_name

    def user_lname(self, obj):
        return obj.user.last_name

    list_display = ('user_id', 'user_name', 'user_lname', 'user')


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(CustomBurger,CustomBurgerAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BurgerReview,BurgerReviewAdmin)
