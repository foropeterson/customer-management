from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
#from .forms import CustomerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
#from accounts.views import chatbox
 #Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Customer

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')


	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

#@login_required(login_url='login')
#@admin_only
def home(request):
    orders = Order.objects.filter(status='deliverd')
    customers = Customer.objects.order_by('-id')[:5] 

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)
#@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)
def chatbox(request):
    # Retrieve chat history from the database or any other source
    chat_history = [
        {'sender': 'User', 'content': 'Hello!'},
        {'sender': 'Bot', 'content': 'Hi there! How can I assist you?'},
        # Add more chat messages as needed
    ]

    context = {
        'chat_history': chat_history,
    }

    return render(request, 'accounts/chatbox.html', context)
#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

login_required(login_url='login')
allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        
        if formset.is_valid():
            formset.save()
            
            # Fetch the updated list of orders for the dashboard
            orders = Order.objects.filter(status='deliverd')
            customers = Customer.objects.order_by('-id')[:5]
            total_orders = orders.count()
            delivered = orders.count()
            pending = Order.objects.filter(status='Pending').count()
            
            context = {
                'orders': orders,
                'customers': customers,
                'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending
            }
            
            # Render the dashboard template with the updated context
            return render(request, 'accounts/dashboard.html', context)
    
    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def place_order(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    products = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            product = Product.objects.get(id=product_id)

            # Create the order
            order = Order(customer=customer, product=product, quantity=quantity)
            order.save()

            messages.success(request, "Order placed successfully.")
            return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'accounts/place_order.html', {'customer': customer, 'products': products, 'form': form})

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])

def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('order_list')  # Redirect to the order list page or a custom error page

    if request.method == 'POST':
        order.delete()
        return redirect('remaining_orders')
    
    context = {
        'order': order
    }
    return render(request, 'accounts/delete_order.html', context)

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        confirm_delete_customer(customer)
        return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL name or path
    
    context = {
        'customer': customer
    }
    return render(request, 'accounts/delete_customer.html', context)
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'accounts/add_customer.html', {'form': form})
def update_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return redirect('customer_list')  # Redirect to the customer list page or a custom error page

    if request.method == 'POST':
        # Process the form data and update the customer object
        # ...

        return redirect('customer_detail', customer_id=customer.id)

    context = {
        'customer': customer
    }
    return render(request, 'accounts/update_customer.html', context)
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm()

    return render(request, 'create_customer.html', {'form': form})
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Perform server-side operations, such as adding to the cart or creating an order

        # Prepare the response data to send back to the client
        response_data = {
            'product_name': 'Example Product',
            'quantity': 1
        }

        return JsonResponse(response_data)
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


# Add the error handler URL pattern
def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'accounts/customer_list.html', context)
