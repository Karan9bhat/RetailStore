from rest_framework import routers
from django.urls import path, include
from . import views
router = routers.DefaultRouter()

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('addcustomer', views.addcustomer, name='addcustomer'),
    path('newemployee', views.newemployee, name='newemployee'),
    path('customerdetail', views.cdetail, name='customerdetail'),
    path('customer_register', views.c_register, name="customer_register"),
    path('validate', views.accept_login, name='accept_login'),
    path('employee_register', views.emp_register, name="employee_register"),
    path('newproduct', views.newproduct, name='newproduct'),
    path('product_register', views.product_register, name="product_register"),
    path('employeedetail', views.emp_detail, name="employeedetail"),
    path('order', views.order, name="order"),
    path('insert_order', views.insert_order, name="insert_order"),
    path('delete_emp/<int:staff_id>', views.delete_emp, name='delete_emp'),
    path('edit_emp/<int:staff_id>', views.edit_emp, name='edit_emp'),
    path('inventory', views.inventory, name="inventory"),
    path('delete_cust/<int:cust_id>', views.delete_cust, name='delete_cust'),
    path('edit_cust/<int:cust_id>', views.edit_cust, name='edit_cust'),
    path('delete_inv/<int:product_id>', views.delete_inv, name='delete_inv'),
    path('today_sale', views.today_sale, name='today_sale'),
    path('exempting', views.exempting, name='exempting'),
    path('update_cust', views.update_cust, name="update_cust"),
    path('transaction', views.transaction, name='transaction'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('edit_inv/<int:product_id>', views.edit_inv, name='edit_inv'),
    path('update_inv', views.update_inv, name='update_inv'),
    path('edit_emp/<int:staff_id>', views.edit_emp, name='edit_emp'),
    path('update_emp', views.update_emp, name='update_emp'),
    path('add_store', views.add_store, name='add_store'),
    path('new_store', views.new_store, name='new_store'),
    path('list_store', views.list_store, name='list_store')
]