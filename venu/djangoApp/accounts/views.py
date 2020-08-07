from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .filters import OrderFilter
# Create your views here.


def Home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Deliverd').count()
    pending = orders.filter(status='Pending').count()
    print(total_customers, total_orders, delivered, pending)
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, "accounts/dashboard.html", context)


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


def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})


# // Create order

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


def deleteOrder(request, order_id):
    # form = OrderForm()
    order = Order.objects.get(id=order_id)
    if request.method == 'POST' and request.POST['Confirm']:
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, "accounts/delete.html", context)
