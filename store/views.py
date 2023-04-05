from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_categoies()
    categoryId = request.GET.get('category')
    if categoryId:
        products = Product.get_all_product_by_categoryid(categoryId)
    else:
        products = Product.get_all_product()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'index.html', data)

def Validatecustomers(customer):
    error_message = None;
    if not customer.first_name:
        error_message = 'First name must be required!!! '
    elif len(customer.first_name) < 4:
        error_message = 'First name must be 4 char long!'
    elif not customer.last_name:
        error_message = 'Last name must be required!!! '
    elif len(customer.last_name) < 4:
        error_message = 'Last name must be 4 char long!'
    elif not customer.mobile_no:
        error_message = 'Mobile No. must be required!!! '
    elif len(customer.mobile_no) == 10:
        error_message = 'First name must be 10 digit long!'
    elif not customer.password:
        error_message = 'Password must be required!!! '
    elif len(customer.password) < 6:
        error_message = 'Password must be 6 char long!'

    elif customer.isExists():
        error_message = 'This Email is already Registered!'

    return error_message

def registerUser(request):
    PostData = request.POST
    first_name = PostData.get('firstname')
    last_name = PostData.get('lastname')
    mobile_no = PostData.get('mobile_no')
    email = PostData.get('email')
    password = PostData.get('Password')
    # validation
    value = {
        'first_name': first_name,
        'last_name': last_name,
        'mobile_no': mobile_no,
        'email': email
    }
    error_message = None
    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        mobile_no=mobile_no,
                        email=email,
                        password=password)

    error_message = Validatecustomers(customer)

    # saving
    if not error_message:
        print(first_name, last_name, mobile_no, email, password)
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', data)



def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)
