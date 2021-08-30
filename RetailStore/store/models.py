from django.db import models

# Create your models here.


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    objects = models.Manager()


class Staff:
    staff_id: int
    staff_name: str
    store_id: int
    salary: int
    contact: int
    address: str


class Home:
    sale: int
    employees: int
    exempting: int
    store_name: str


class Cart:
    product_name: str


class Customer:
    cust_id: int
    cust_name: str
    contact: int
    address: str


class Cart_Details:
    product_name: str
    quantity: int
    price: float


class Order:
    tot_price: float
    tot_quantity: int


class Emp:
    id : int


class Inventory:
    product_id: int
    product_name: str
    price: float
    quantity: int
    discout: int


class Tsale:
    order_id: int
    cust_id: int
    staff_id: int
    order_date: str
    amount: int
    transaction_id: int
    transaction: str


class Exempting:
    product_id: int
    product_name: str
    quantity: int


class Store:
    store_id: int
    store_name: str