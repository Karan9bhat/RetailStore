import mysql.connector
mydb=mysql.connector.connect(host="localhost", user="himansh", passwd="Himansh@10", auth_plugin='mysql_native_password')

# print(mydb)

if (mydb):
    print("connection Succesfull")
else:
    print("connection Unsuccesfull")

mycursor=mydb.cursor()

# mycursor.execute("Create database testing")
# mycursor.execute("Show databases")
#
# for db in mycursor:
#     print(db)

mycursor.execute("Use testing")
# mycursor.execute("Create table Test(name varchar(20))")
mycursor.execute("Show tables")

for table in mycursor:
    print(table)