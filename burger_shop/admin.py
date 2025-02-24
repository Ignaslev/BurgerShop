from django.contrib import admin
from .models import Profile, Order, MenuItem, OrderItem, CustomBurger, Ingredient, CustomBurgerRecipe, BlogPost, BurgerReview


class CustomBurgerRecipeInline(admin.TabularInline):
    '''
    Allows adding and editing burger ingredients directly in the CustomBurger admin panel.
    '''
    model = CustomBurgerRecipe
    extra = 1

class CustomBurgerAdmin(admin.ModelAdmin):
    '''
    Displays burger name, ID, user, and total price in the list view.
    Allows inline editing of associated CustomBurgerRecipe items.
    '''
    list_display = ('name', 'id', 'user', 'total_price', )
    inlines = [CustomBurgerRecipeInline]


class OrderItemInline(admin.TabularInline):
    '''
    Allows adding and editing order items directly in the Order admin panel.
    '''
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    '''
    Displays order ID, user, total price, order status, and timestamp in the list view.
    Allows inline editing of associated OrderItem entries.
    '''
    list_display = ('id', 'time', 'user', 'total_price', 'order_status')
    list_filter = ('time', 'user')
    list_editable = ('order_status',)
    inlines = [OrderItemInline]


class IngredientAdmin(admin.ModelAdmin):
    '''
    Displays ingredient name, category, and price in the list view.
    Allows price editing and filtering by category.
    '''
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    list_editable = ('price',)


class MenuItemAdmin(admin.ModelAdmin):
    '''
    Displays menu item name, category, and price in the list view.
    Allows price editing and filtering by category.
    '''
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    list_editable = ('price',)

class BurgerReviewAdmin(admin.ModelAdmin):
    '''
    Displays burger, user, and rating in the list view.
    Allows filtering by user and burger.
    '''
    list_display = ('burger', 'user', 'rating')
    list_filter = ('user', 'burger')

class ProfileAdmin(admin.ModelAdmin):
    '''
    Displays user ID, first name, last name, and user in the list view.
    Custom methods retrieve related user attributes.
    '''
    def user_id(self, profile):
        return profile.user.id

    def user_name(self, profile):
        return profile.user.first_name

    def user_lname(self, profile):
        return profile.user.last_name

    list_display = ('user_id', 'user_name', 'user_lname', 'user')


class BlogPostAdmin(admin.ModelAdmin):
    '''
    Displays blog post title, creation date, and author in the list view.
    '''
    list_display = ('title', 'created_at', 'author')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(CustomBurger,CustomBurgerAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BurgerReview,BurgerReviewAdmin)
