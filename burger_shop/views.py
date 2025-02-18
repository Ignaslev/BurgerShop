from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import User, MenuItem, Order, OrderItem


def index(request):
    return render(request, 'index.html')

def menu(request):
    burgers = MenuItem.objects.filter(category='Burgers').all()
    sides = MenuItem.objects.filter(category='Sides').all()
    drinks = MenuItem.objects.filter(category='Drinks').all()

    context = {
        'burgers' : burgers,
        'sides' : sides,
        'drinks' : drinks,
    }
    return render(request, 'menu.html', context=context)

@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_nr = request.POST.get('phone_nr')


        if password != password2:
            messages.error(request, "Passwords doesn't match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

        customer_group = Group.objects.get(name='Customer')
        user.groups.add(customer_group)

        user.profile.phone = phone_nr
        user.profile.save()

        messages.info(request, f'Registration of {username} successful')
        return redirect('login')


@login_required
def get_user_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, 'Profile updated')
        else:
            messages.error(request, 'Error')
        return redirect('user-profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form
    }

    return render(request, 'profile.html', context=context)


@login_required
def start_order(request):
    order = Order.objects.create(user=request.user, order_status='d')

    return redirect('order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    burgers = MenuItem.objects.filter(category='Burgers')
    sides = MenuItem.objects.filter(category='Sides')
    drinks = MenuItem.objects.filter(category='Drinks')

    menu_items = MenuItem.objects.all()

    order_items = order.orderitem_set.all()

    total_price = sum(item.menu_item.price * item.quantity for item in order_items)

    if request.method == 'POST':
        remove_item_id = request.POST.get('remove_item_id')
        if remove_item_id:
            order_item_to_remove = get_object_or_404(OrderItem, id=remove_item_id, order=order)
            order_item_to_remove.delete()
            return redirect('order_detail', order_id=order.id)

        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))

        if menu_item_id and quantity > 0:
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)

            # Check if item is already in the order, update quantity
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )

            if not created:
                order_item.quantity += quantity
                order_item.save()

        return redirect('order_detail', order_id=order.id)

    context = {
        'order': order,
        'menu_items': menu_items,
        'order_items': order_items,
        'burgers': burgers,
        'sides': sides,
        'drinks': drinks,
        'total_price' : total_price,
    }
    return render(request, 'order_detail.html', context)


@login_required
def finalize_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)


    if order.order_status != 'd':
        return redirect('order_detail', order_id=order.id)

    order_items = order.orderitem_set.all()

    total_price = sum(item.menu_item.price * item.quantity for item in order_items)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            for item in order_items:
                quantity = int(request.POST.get(f'quantity_{item.id}', item.quantity))
                if quantity > 0:
                    item.quantity = quantity
                    item.save()
                else:
                    item.delete()

        elif action.startswith('remove_'):
            item_id = int(action.split('_')[1])
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)
            order_item.delete()

        elif action == 'confirm':
            if order_items.exists():
                order.order_status = 'co'
                order.save()
                return redirect('order_success')

        return redirect('finalize_order', order_id=order.id)

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'finalize_order.html', context)

def order_success(request):
    return render(request, 'order_success.html')