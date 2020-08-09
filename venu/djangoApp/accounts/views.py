from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
# // Models
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
# Create your views here.
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def Home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Deliverd').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, customer_id):
    # orders = Order.objects.all()
    customer = Customer.objects.get(id=customer_id)
    # orders = Order.objects.filter(customer=customer)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'orders': orders,
        'customer': customer,
        'total_orders': total_orders,
        'filter': myFilter
    }

    return render(request, "accounts/customer.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})


# // Create order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, c_id):
    customer = Customer.objects.get(id=c_id)
    form = OrderForm(initial={'customer': customer})
    if(request.method == 'POST'):
        # print(request.POST)
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)


# // update view
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if(request.method == 'POST'):
        form = OrderForm(request.POST, instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/order_form.html", context)

# // update view


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, order_id):
    # form = OrderForm()
    order = Order.objects.get(id=order_id)
    if request.method == 'POST' and request.POST['Confirm']:
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, "accounts/delete.html", context)


# LOGIN AND REGISTER
@unauthenticated_user
def registerPage(request):
    # if(request.user.is_authenticated):
    #     return redirect('/')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username)
            messages.success(request, 'User has been created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# LOGIN


def loginPage(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request=request, username=username, password=password)
        if(user != None):
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR Password Incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

# LOGOUT USER


def logoutUser(request):
    logout(request)
    return redirect('login')


# //----------- USER PAGE VIEWS ----------//

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    # total orders
    total_orders = orders.count()
    # deliver
    delivered = orders.filter(status='Deliverd').count()
    # pending
    pending = orders.filter(status='Pending').count()
    # // context
    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, "accounts/user/user.html", context)


# /////////  User Account  //////////
@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userAccount(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if(form.is_valid()):
            form.save()

    context = {'form': form}
    return render(request, "accounts/user/account.html", context)
