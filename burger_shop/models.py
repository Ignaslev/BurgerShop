from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Phone number', max_length=50)
    picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user} profile'

    @property
    def picture_url(self):
        if self.picture:
            return self.picture.url
        return '/media/default-user.png'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    ORDER_STATUS = (
        ('d', 'Draft'),
        ('co', 'Confirmed'),
        ('f', 'Finished'),
        ('ca', 'Cancelled')
    )

    order_status = models.CharField('Order status',
                                max_length=2,
                                choices= ORDER_STATUS,
                                default='d',
                                help_text='Status of order')

    PAYMENT_STATUS = (
        ('p', 'Pending'),
        ('pd', 'Paid'),
        ('f', 'Failed'),
        ('ca', 'Cancelled')
    )

    payment_status = models.CharField('Payment status',
                                    max_length=2,
                                    choices=PAYMENT_STATUS,
                                    default='p',
                                    help_text='Status of payment')


    @property
    def total_price(self):
        return sum(item.total_price for item in self.orderitem_set.all())

    def __str__(self):
        user_info = f'{self.user.id}. {self.user}' if self.user else 'No user'
        return f'{user_info}, {self.time}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class MenuItem(models.Model):
    category = models.CharField('Category', max_length=50)
    name = models.CharField('Name', max_length=50)
    description = models.TextField('Description', max_length=150)
    price = models.DecimalField('Price', max_digits=30, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}, {self.price}eur'

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, blank=True, null=True)
    custom_burger = models.ForeignKey('CustomBurger', on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField('Quantity')


    @property
    def total_price(self):
        if self.menu_item:
            return self.menu_item.price * self.quantity
        elif self.custom_burger:
            return self.custom_burger.total_price * self.quantity
        return 0

    def __str__(self):
        if self.menu_item:
            return f'{self.menu_item.name} x {self.quantity}'
        elif self.custom_burger:
            return f'{self.custom_burger.name} x {self.quantity}'


    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class CustomBurger(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Name', max_length=50)
    image = models.ImageField(upload_to='users_burgers', blank=True, null=True)

    @property
    def total_price(self):
        recipe_items = self.customburgerrecipe_set.all()
        return sum(item.price for item in recipe_items)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Custom Burger'
        verbose_name_plural = 'Custom Burgers'


class Ingredient(models.Model):
    category = models.CharField('Category', max_length=50)
    name = models.CharField('Name', max_length=50)
    description = models.CharField('Description', max_length=150)
    price = models.DecimalField('Price', max_digits=30, decimal_places=2)
    part_image = models.ImageField(upload_to='burger_components/', blank=True)

    def __str__(self):
        return f'{self.name}, {self.price}eur'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class CustomBurgerRecipe(models.Model):
    custom_burger = models.ForeignKey(CustomBurger, on_delete=models.CASCADE, null=True, blank=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('Quantity')

    def __str__(self):
        return f'{self.ingredient.name} x {self.quantity}'

    @property
    def price(self):
        if self.ingredient and self.quantity:
            return self.ingredient.price * self.quantity
        return 0


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BurgerReview(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Content', max_length=2000)
    burger = models.ForeignKey(CustomBurger, on_delete=models.CASCADE, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.date}, {self.user}, {self.burger}, {self.rating}/5, {self.content}'