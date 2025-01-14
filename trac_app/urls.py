from django.urls import path
from .views import JsonHandlerView
from .views import *

urlpatterns = [
    path('json/', JsonHandlerView.as_view(), name='json_handler'),
    path('create-role/', create_role, name='create_role'),
    path('create-user/', create_user, name='create_user'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('adminhome/', adminhome, name='adminhome'),
    path('ownerhome/', ownerhome, name='ownerhome'),
    path('insertproduct/', insertproduct, name='insertproduct'),
    path('viewproducts/', viewproducts, name='viewproducts'),
    path('products/', viewproducts, name='viewproducts'),
    path('products/update/<int:product_id>/', updateproduct, name='updateproduct'),
    path('products/delete/<int:product_id>/', deleteproduct, name='deleteproduct'),
]