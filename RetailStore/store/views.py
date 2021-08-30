from django.shortcuts import render, get_object_or_404, redirect
import mysql.connector
from .models import Staff, Home, Cart, Customer, Cart_Details, Order, Emp, Inventory, Tsale, Exempting, Store
from json import dumps

# Create your views here.
mydb = mysql.connector.connect(host="localhost", user="himansh", passwd="Himansh@10",database='store',
                               auth_plugin='mysql_native_password')
if mydb:
    print("Connection Successful")
else:
    print("Connection Unsuccessful")
mycursor = mydb.cursor(buffered=True)
store = None
Cart_Items = []
new_order = None


def login(request):
    return render(request, 'store/login.html')


def accept_login(request):
    global store
    if request.method == "POST":
        id = request.POST["store_id"]
        flag = 0
        mycursor.execute("select store_id from store")
        for sid in mycursor:
            if int(id) == int(sid[0]):
                flag = 1
                store = int(id)
                print(store)
                break
        mycursor.reset()
        if flag:
            return redirect('/home')
    return render(request, 'store/login.html')


def index(request):
    global store
    details = Home()
    details.sale = 0
    details.count = 0
    details.exempting = 0
    query = "select sum(amount) as total_amount from ordertable where order_date > DATE(NOW()) and order_date < NOW() and store_id = "+ str(store)
    mycursor.execute(query)
    for am in mycursor:
        try:
            details.sale = float(am[0])
        except:
            details.sale = 0
    query = "select count(*) from staff where store_id = " + str(store)
    mycursor.execute(query)
    for c in mycursor:
        details.count = int(c[0])

    query = "select count(*) from inventory where quantity < 5 and store_id = " + str(store)
    mycursor.execute(query)
    for q in mycursor:
        details.exempting = int(q[0])
    query = "select store_name from store where store_id =" + str(store)
    mycursor.execute(query)
    for s in mycursor:
        details.store_name = s[0]
    return render(request, 'store/index.html', {'details': details})


def cart(request):
    global store, Cart_Items
    products = []
    query = "select product_name from inventory where store_id = " + str(store)
    mycursor.execute(query)
    for pd_name in mycursor:
        name = Cart()
        name.product_name = pd_name[0]
        products.append(name)
    if request.method == "POST":
        New_item = Cart_Details()
        New_item.product_name = request.POST["product_name"]
        New_item.quantity = request.POST["quantity"]
        query = "select price, discount from inventory where product_name = \'{}\'".format(New_item.product_name)
        mycursor.execute(query)
        for item in mycursor:
            New_item.price = int(item[0]) * float(1- (item[1])/100)
        Cart_Items.append(New_item)
    return render(request, 'store/cart.html', {'products': products, 'Cart_Items': Cart_Items})


def addcustomer(request):
    return render(request, 'store/addcustomer.html')


def newemployee(request):
    return render(request, 'store/newemployee.html')


def cdetail(request):
    return render(request, 'store/customerdetail.html')


def c_register(request):
    max_id = 0
    if request.method == 'POST':
        mycursor.execute("select max(cust_id) from customer")
        for id in mycursor:
            max_id = id[0]
        cust_name = request.POST["cust_name"]
        address = request.POST["address"]
        contact = int(request.POST["contact"])
        cust_id = int(max_id)+1
        query = "Insert into customer values({}, \'{}\', {}, \'{}\')".format(cust_id, cust_name, contact, address)
        mycursor.execute(query)
        mycursor.reset()
        mydb.commit()
        print(contact)
    else:
        return redirect(addcustomer)
    return render(request, 'store/addcustomer.html')


def emp_register(request):
    global store
    max_id = 0
    emp_id = None
    details = Emp()
    if request.method == 'POST':
        query = "select max(staff_id) from staff where store_id = " + str(store)
        mycursor.execute(query)
        for id in mycursor:
            max_id = id[0]
        emp_name = request.POST["emp_name"]
        address = request.POST["address"]
        contact = int(request.POST["contact"])
        emp_id = int(max_id) + 1
        salary = request.POST["salary"]
        query = "Insert into staff values({}, \'{}\', {}, {}, \'{}\', {})".format(emp_id, emp_name, contact, salary, address, store)
        mycursor.execute(query)
        mycursor.reset()
        mydb.commit()
    else:
        redirect(newemployee)
    details.id = emp_id
    return redirect('/newemployee', {'details': details})


def newproduct(request):
    return render(request, 'store/addproduct.html')


def product_register(request):
    global store
    max_id = 0
    if request.method == 'POST':
        query = "select max(product_id) from inventory where store_id = " + str(store)
        mycursor.execute(query)
        for id in mycursor:
            max_id = id[0]
        product_name = request.POST["product_name"]
        query = "select product_name from inventory where store_id = " + str(store)
        mycursor.execute(query)
        for name in  mycursor:
            if str(name[0]) == product_name:
                return render(request, 'store/addproduct.html')
        price = request.POST["price"]
        quantity = int(request.POST["quantity"])
        product_id = int(max_id) + 1
        discount = request.POST["discount"]
        query = "Insert into inventory values({}, \'{}\', {}, {}, {}, {})".format(product_id, product_name, price, quantity, discount, store)
        mycursor.execute(query)
        mycursor.reset()
        mydb.commit()
    return render(request, 'store/addproduct.html')


def emp_detail(request):
    details = []
    query = "select * from staff where store_id = " + str(store)
    mycursor.execute(query)
    for row in mycursor:
        emp = Staff()
        emp.staff_id = int(row[0])
        emp.staff_name = row[1]
        emp.contact = row[2]
        emp.salary = int(row[3])
        emp.address = row[4]
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/emp_detail.html', content)


def cdetail(request):
    details = []
    query = "select * from customer"
    mycursor.execute(query)
    for row in mycursor:
        emp = Customer()
        emp.cust_id = int(row[0])
        emp.cust_name = row[1]
        emp.contact = row[2]
        emp.address = row[3]
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/customerdetail.html', content)


def order(request):
    global Cart_Items, new_order
    if request.method == "POST":
        new_order = Order()
        new_order.tot_price = 0
        new_order.tot_quantity = 0
        for items in Cart_Items:
            p = items.price
            q = items.quantity
            new_order.tot_price += int(p)*int(q)
            new_order.tot_quantity += int(q)
        return render(request, 'store/order.html', {'new_order': new_order})
    return render(request, 'store/order.html')


def insert_order(request):
    global Cart_Items, new_order, store, mycursor
    pname = []
    pquan = []
    max_id = 0
    if request.method == "POST":
        for items in Cart_Items:
            pname.append(items.product_name)
            pquan.append(items.quantity)
        for i in range(len(pname)):

            query = "update inventory set quantity=quantity - {0} where product_name = \'{1}\' and " \
                    "store_id = {2}".format(int(pquan[i]), pname[i], int(store))
            mycursor.execute(query)

        query = "select max(transaction_id) from transaction"
        mycursor.execute(query)
        for id in mycursor:
            max_id = id[0]
        trans_id = max_id + 1
        trans = request.POST["transaction"]
        query = "insert into transaction values ({}, \'{}\' )".format(trans_id, trans)
        mycursor.execute(query)

        query = "select max(order_id) from ordertable"
        mycursor.execute(query)
        for id in mycursor:
            max_id = id[0]
        ord_id = max_id + 1
        cust_id = request.POST["cust_id"]
        emp_id = request.POST["emp_id"]
        store_id = int(store)
        amount = new_order.tot_price
        query = "insert into ordertable values ({}, {}, {}, {}, current_timestamp, {}," \
                " {})".format(ord_id, cust_id, emp_id, amount, store_id, trans_id)
        mycursor.execute(query)
        mydb.commit()
        Cart_Items = []
        new_order = None

    return redirect('/home')

def delete_emp(request, staff_id):
    query = "delete from staff where staff_id = " + str(staff_id)
    mycursor.execute(query)
    mydb.commit()
    return redirect('/employeedetail')


def inventory(request):
    details = []
    query = "select * from inventory where store_id = " + str(store)
    mycursor.execute(query)
    for row in mycursor:
        emp = Inventory()
        emp.product_id = int(row[0])
        emp.product_name = row[1]
        emp.price = float(row[2])
        emp.quantity = int(row[3])
        emp.discount = int(row[4])
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/view_inventory.html', content)


def delete_cust(request, cust_id):
    query = "delete from customer where cust_id = " + str(cust_id)
    mycursor.execute(query)
    mydb.commit()
    return redirect('/customerdetail')


def delete_inv(request, product_id):
    query = "delete from inventory where product_id = " + str(product_id)
    mycursor.execute(query)
    mydb.commit()
    return redirect('/inventory')


def today_sale(request):
    global store
    details = []
    query = "select * from ordertable natural join transaction where order_date > DATE(NOW()) and order_date < NOW() and store_id = "+ str(store)
    mycursor.execute(query)
    for row in mycursor:
        emp = Tsale()
        emp.order_id = int(row[1])
        emp.cust_id= int(row[2])
        emp.staff_id = int(row[3])
        emp.amount = int(row[4])
        emp.order_date = str(row[5])
        emp.transaction_id = int(row[0])
        emp.transaction = str(row[7])
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/today_sale.html', content)


def exempting(request):
    global store
    details = []
    query = "select product_id, product_name, quantity from inventory where quantity < 5 and store_id = " + str(store)
    mycursor.execute(query)
    for row in mycursor:
        emp = Exempting()
        emp.product_id = int(row[0])
        emp.product_name = str(row[1])
        emp.quantity = int(row[2])
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/exempting.html', content)

def edit_cust(request, cust_id):
    query = "select * from customer where cust_id = " + str(cust_id)
    mycursor.execute(query)
    data = mycursor.fetchone()
    details = list(data)
    return render(request, 'store/edit_cust.html', {'details': details})

def update_cust(request) :
    if request.method == 'POST' :
        cust_id = request.POST['cust_id']
        cust_name = request.POST['cust_name']
        contact = request.POST['contact']
        address = request.POST['address']
        query = "update customer set cust_name = \'{}\', contact = {}, address = \'{}\' where cust_id = {}".format(str(cust_name), int(contact), str(address), str(cust_id))
        mycursor.execute(query)
        mydb.commit()
        return redirect('/customerdetail')
    else:
        return redirect('/customerdetail')


def transaction(request):
    global store
    details = []
    query = "select * from ordertable natural join transaction where store_id = "+ str(store)
    mycursor.execute(query)
    for row in mycursor:
        emp = Tsale()
        emp.order_id = int(row[1])
        emp.cust_id= int(row[2])
        emp.staff_id = int(row[3])
        emp.amount = int(row[4])
        emp.order_date = str(row[5])
        emp.transaction_id = int(row[0])
        emp.transaction = str(row[7])
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/transaction.html', content)


def aboutus(request):
    return render(request, 'store/aboutus.html')


def edit_inv(request, product_id):
    query = "select * from inventory where product_id = " + str(product_id)
    mycursor.execute(query)
    data = mycursor.fetchone()
    details = list(data)
    return render(request, 'store/edit_inv.html', {'details': details})

def update_inv(request) :
    if request.method == 'POST' :
        product_id = request.POST['product_id']
        product_name = request.POST['product_name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        discount = request.POST['discount']
        query = "update inventory set product_name = \'{}\', price = {}, quantity = {}, discount = {} where product_id = {}".format(str(product_name), float(price), int(quantity), int(discount), product_id)
        mycursor.execute(query)
        mydb.commit()
        return redirect('/inventory')
    else:
        return redirect('/inventory')


def edit_emp(request, staff_id):
    query = "select * from staff where staff_id = " + str(staff_id)
    mycursor.execute(query)
    data = mycursor.fetchone()
    details = list(data)
    return render(request, 'store/edit_emp.html', {'details': details})

def update_emp(request) :
    if request.method == 'POST' :
        staff_id = request.POST['staff_id']
        staff_name = request.POST['staff_name']
        contact = request.POST['contact']
        address = request.POST['address']
        salary = request.POST['salary']
        query = "update staff set staff_name = \'{}\', contact = {}, address = \'{}\', salary = {} where staff_id = {}".format(str(staff_name), int(contact), str(address), int(salary), str(staff_id))
        mycursor.execute(query)
        mydb.commit()
        return redirect('/employeedetail')
    else:
        return redirect('/employeedetail')


def new_store(request):
    return render(request, 'store/new_store.html')


def add_store(request):
    if request.method == "POST":
        mycursor.execute("select max(store_id) from store")
        for id in mycursor:
            max_id = id[0]
        store_name = request.POST["store_name"]
        max_id += 1
        query = "Insert into store values({}, \'{}\')".format(max_id, store_name)
        mycursor.execute(query)
        mycursor.reset()
        mydb.commit()
    else:
        return redirect('/new_store')
    return render(request, 'store/new_store.html')


def list_store(request):
    details = []
    query = "select * from store"
    mycursor.execute(query)
    for row in mycursor:
        emp = Store()
        emp.store_id = int(row[0])
        emp.store_name= str(row[1])
        details.append(emp)
    content = {'details': details}
    return render(request, 'store/liststore.html', content)