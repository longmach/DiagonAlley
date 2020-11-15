from flask import Flask, redirect, url_for, render_template, request
from db_connector.db_connector import connect_to_database, execute_query
# {% %} allows for native python code to be written
# ex: {% for _ in range(10) %}
##      {% endfor %}
# {{ }} allows for any variable to be sent from backend to front end


app = Flask(__name__)
# index
@app.route("/")
def index():
    return render_template("index.html")
# home
@app.route("/home")
def home():
    return render_template("home.html")
# customer
@app.route("/customer", methods=["POST", "GET"])
def customer():
    # thought process: 
    # have the customer table show up every time the page is GET requested to reflect changes made
    # redirect after update/delete/insert to show changed in DB
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from customers"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("customer.html", customers = result)
    elif request.method == "POST" and "searchByCustomerName" in request.form:
        f_name = request.form['searchByCustomerFirstName']
        l_name = request.form['searchByCustomerLastName']
        # changed your single data select query by added another input so now its one for first name and one for last name
        # TODO: make this change in the sql file too 
        filteredSelectQuery = "SELECT * FROM customers WHERE first_name = %s AND last_name = %s"
        data = (f_name, l_name)
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("customer.html", filteredCustomer = result)

    # TODO: need to figure out a way to update customer in html side for update button to work correctly
    # change update query to %s
    elif request.method == "POST" and "" in request.form:
        updateQuery= "UPDATE customers SET first_name = :first_name_from_update_form, last_name = :last_name_from_update_form, email = :email_from_update_form, username = :username_from_update_form, created_date = :created_date_input WHERE CONCAT(first_name,' ',last_name) = CONCAT(:first_name_from_update_form,' ',:last_name_from_update_form);"
        result = execute_query(db_connection, updateQuery).fetchall()
        return redirect(url_for("customer"))

    elif request.method == "POST" and "addCustomer" in request.form:
        # create variables with values to insert from request.form
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        created_date = request.form['createDateUser']
        # took out convert(date, getdate()) but feel free to fit it in there if you can get it to work
        insertQuery = "INSERT INTO customers (first_name, last_name, email, username, password, created_date) VALUES (%s, %s, %s, %s, %s, %s);"
        data = (f_name, l_name, email, username, password, created_date)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("customer"))
# items
@app.route("/items", methods=["POST", "GET"])
def items():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from items"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("items.html", items = result)
    elif request.method == "POST" and "searchByItemName" in request.form:
        item_name = request.form['itemName']
        # I added item_ID to html so we can just do * now
        # TODO: make this change in sql file
        filteredSelectQuery = "SELECT * FROM items WHERE name = %s"
        data = (item_name)
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("items.html", filteredItems = result)
    elif request.method == "POST" and "insertItem" in request.form:
        itemName = request.form['itemName']
        itemQuantity = request.form['itemQuantity']
        itemCost = request.form['itemCost']
        itemPrice = request.form['itemPrice']
        insertQuery = "INSERT INTO items (name, inventory_quantity, cost, price) VALUES (%s,%s,%s,%s);"
        data = (itemName, itemQuantity, itemCost, itemPrice)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("items"))
# community
@app.route("/communities", methods=["POST", "GET"])
def communities():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from items"
        result = execute_query(db_connection, getAllQuery).fetchall()t)
        return render_template("items.html", communities = result)
    elif request.method == "POST" and "searchByCommunity" in request.form: 
        communityName = request.form["communityName"]
        filteredSelectQuery = "SELECT * FROM communities WHERE name = %s;"
        data = (communityName)
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("items.html", filteredCommunities = result)
    elif request.method == "POST" and "insertNewCommunity" in request.form:
        communityName = request.form["communityName"]
        communityDiscount = request.form["communityDiscount"]
        insertQuery = "INSERT INTO communities (name, discount) VALUES (%s, %s);"
        data = (communityName, communityDiscount)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("items"))

# TODO: create user communities html page, finish the queries below
# format it the same way as the other pages
# below is unfinished
@app.route("/userCommunities", methods=["POST", "GET"])
def userCommunities():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from items"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("userCommunities.html", userCommunities = result)
    # fix queries below to exchange for real data
    elif request.method == "POST" and "searchByUserCommunityName" in request.form:
        userCommunityName = request.form['']
        filteredSelectQuery = ""
        result = execute_query(db_connection, filteredSelectQuery).fetchall()
        return render_template("userCommunities.html", filteredCommunities = result)
    elif request.method == "POST" and "insertUserCommunity" in request.form:
        insertQuery = ""
        result = execute_query(db_connection, insertQuery).fetchall()
        return redirect(url_for("userCommunities"))

# purchase order
@app.route("/purchaseOrder", methods=["POST", "GET"])
def purchaseOrder():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from purchase_orders"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("purchaseOrder.html", purchaseOrders = result)
    elif request.method == "POST" and "searchByPurchaseOrderID" in request.form:
        order_ID = request.form['purchaseOrderID']
        filteredSelectQuery = "SELECT * FROM purchase_orders WHERE order_ID = %s;"
        data = (order_ID)
        result = execute_query(db_connection, filteredSelectQuery,data).fetchall()
        return render_template("purchaseOrder.html", filteredPurchaseOrder = result)
    elif request.method == "POST" and "insertPurchaseOrder" in request.form:
        customerID = request.form['customerID']
        order_date = request.form['orderDate']
        insertQuery = "INSERT INTO purchase_orders (customer_ID, order_date) VALUES (%s, %s);"
        data = (customerID, order_date)
        result = execute_query(db_connection, insertQuery,data).fetchall()
        return redirect(url_for("purchaseOrder"))

# purchase order details 
@app.route("/purchaseOrderDetails", methods=["POST", "GET"])
def purchaseOrderDetails():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from purchase_order_details"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("purchaseOrderDetails.html", purchaseOrderDetails = result)
    elif request.method == "POST" and "insertPurchaseOrder" in request.form:
        orderID = request.form['orderID']
        itemID = request.form['itemID']
        item_quantity = request.form['itemQuantity']
        insertQuery = "INSERT INTO purchase_order_details (oid, iid, quantity_ordered) VALUES (%s, %s, %s);	"
        data = (orderID, itemID, item_quantity)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("purchaseOrderDetails"))

    # TODO: we have to figure out how to make this possible on the html side
    elif request.method == "POST" and "" in request.form:
        deleteQuery = ""
        result = execute_query(db_connection, deleteQuery).fetchall()
        return redirect(url_for("purchaseOrderDetails"))

# allows us to not rerun server everytime we make a change 
if __name__ == "__main__":
    app.run(debug=True)
