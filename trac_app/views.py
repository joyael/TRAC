import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trac_app.auth import get_current_user, role_required
from .forms import RoleForm, RUserForm, RUserLoginForm, ProductForm, ProductUpdateForm
from rest_framework.decorators import api_view
from .serializers import RUserRegistrationSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Product, RUser
from .utils import create_access_token, create_refresh_token, insert_refresh_token, check_refresh_token, make_refresh_token_inactive, is_refresh_token_active
from django.conf import settings
import jwt
from django.contrib.auth import logout


class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)

class JsonHandlerView(View):
    def get(self, request):
        # Render the HTML template for GET requests
        return render(request, 'index.html')

    def post(self, request):
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)  # Directly parse the JSON data
            
            # Access the jsonData field
            json_data = data.get('jsonData')
            parsed_data = json.loads(json_data)
            
            # Process the data (for example, just echoing it back)
            response_data = {
                'received_data': parsed_data,
                'message': 'Data received successfully!'
            }
            
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        # return JsonResponse({'message': 'This is a test response'}, status=200)

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request,"Role Created Successfully1 !") # Save the new role to the database
            return redirect('create_role')  # Redirect to a success page or another view
    else:
        form = RoleForm()
    
    return render(request, 'create_role.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = RUserForm(request.POST)
        if form.is_valid():
            # Save the user, hashing the password if necessary
            user = form.save(commit=False)
            user.hashed_password = make_password(form.cleaned_data['hashed_password'])  # Hash the password
            user.save()
            messages.success(request,"User Created Successfully1 !")
            return redirect('create_user')  # Redirect to a success page or another view
    else:
        form = RUserForm()
    
    return render(request, 'create_user.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('hashed_password')

        user = RUser.objects.filter(username=username).first()
        if not user:
            messages.error(request,"Username error")
            return redirect('login')
        encoded_password=user.hashed_password
        if not check_password(password,encoded_password):  # check password
            messages.error(request,"Password error")
            return redirect('login')
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        insert_refresh_token(refresh_token)

        messages.success(request,"Login Successfull !")
        response =  redirect('adminhome') 
        response.set_cookie('access_token', access_token, httponly=True, secure=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
        return response

    else:
        form = RUserLoginForm()

    return render(request, 'login.html', {'form': form})
  


def logout_view(request):
    # Log the user out
    messages.success(request,"Logged out")
    logout(request)  # This will clear the session data
    # Optionally, you can also delete any tokens stored in cookies
    response = redirect('login')  # Redirect to the home page or login page
    refresh_token = request.COOKIES.get('refresh_token')
    make_refresh_token_inactive(refresh_token)
    response.delete_cookie('access_token')  # Delete access token cookie
    response.delete_cookie('refresh_token')  # Delete refresh token cookie

    return response


def adminhome(request):
    validate_user = role_required(request=request,permission_name="admin")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    return render(request, 'admin_home.html', {'user': user, 'validate_user':validate_user})  # Pass user to the template if needed

def ownerhome(request):
    validate_user = role_required(request=request,permission_name="owner")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    return render(request, 'owner_home.html', {'user': user})

def usergroup1home(request):
    validate_user = role_required(request=request,permission_name="user-group-1")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    return render(request, 'user-group-1_home.html', {'user': user})

def usergroup2home(request):
    validate_user = role_required(request=request,permission_name="user-group-2")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    return render(request, 'user-group-2_home.html', {'user': user})


def insertproduct(request):
    validate_user = role_required(request=request,permission_name="insert-product")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new product to the database
            messages.success(request,"Product Created Successfully1 !")
            return redirect('insertproduct')  # Redirect to a product list page or another page
    else:
        form = ProductForm()
    return render(request, 'insert-product.html', {'form': form})

def viewproducts(request):
    validate_user = role_required(request=request,permission_name="view-products")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'view-products.html', {'products': products})

def updateproduct(request, product_id):
    validate_user = role_required(request=request,permission_name="update-product")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            messages.success(request,"Product Updated Successfully1 !")
            return redirect('updateproduct', product_id=product.id)  # Redirect to a detail view or another page
    else:
        form = ProductUpdateForm(instance=product)  # Populate the form with the existing product data

    return render(request, 'update-product.html', {'form': form, 'product': product})


def deleteproduct(request, product_id):
    validate_user = role_required(request=request,permission_name="update-product")
    if isinstance(validate_user, JsonResponse):
        return validate_user
    user = get_current_user(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully")
        return redirect('viewproducts')
    
    except Exception as e:
        messages.error(request, f"Error deleting product: {str(e)}")
        return redirect('viewproducts')



def refresh_token_view(request):
    refresh_token = request.COOKIES.get('refresh_token')  # Get the refresh token from the cookie
    if not refresh_token:
        return JsonResponse({'error': 'Refresh token not found'}, status=401)
    if check_refresh_token():
        if not is_refresh_token_active:
            return JsonResponse({'error': 'Refresh token Inactivated'}, status=401)
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = RUser.objects.get(id=user_id)

        # Generate a new access token
        new_access_token = create_access_token(user)

        # Set the new access token as a cookie
        response = JsonResponse({'message': 'Access token refreshed successfully'})
        response.set_cookie('access_token', new_access_token, httponly=True, secure=True)  # Set the access token cookie

        return response
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Refresh token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid refresh token'}, status=401)