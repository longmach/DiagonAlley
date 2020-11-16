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
    elif request.method == "POST" and "searchByCustomerFirstName" in request.form:
        f_name = request.form['searchByCustomerFirstName']
        l_name = request.form['searchByCustomerLastName']
        # changed your single data select query by adding another input so now its one for first name and one for last name
        # TODO: i changed the sql in a new file check it out. 
        filteredSelectQuery = "SELECT * FROM customers WHERE first_name = %s AND last_name = %s"
        data = (f_name, l_name)
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("customer.html", filteredCustomer = result)
    # update works finally 
    elif request.method == "POST" and "updateCustomer" in request.form:
        cid = request.form["customer_ID"]
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        created_date = request.form['createDateUser']
        updateQuery= "UPDATE customers SET first_name = %s, last_name = %s, email = %s, username = %s, password = %s, created_date = %s WHERE customer_ID = %s;"
        data = (f_name, l_name, email, username, password, created_date, cid)
        result = execute_query(db_connection, updateQuery, data).fetchall()
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
        # TODO: make this change in sql file or we can just use the one i created 
        filteredSelectQuery = "SELECT * FROM items WHERE name = %s"
        data = [item_name]
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
        getAllQuery = "SELECT * from communities"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("community.html", communities = result)
    elif request.method == "POST" and "searchByCommunity" in request.form: 
        communityName = request.form["communityName"]
        filteredSelectQuery = "SELECT * FROM communities WHERE name = %s;"
        data = [communityName]
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("community.html", filteredCommunities = result)
    elif request.method == "POST" and "insertNewCommunity" in request.form:
        communityName = request.form["communityName"]
        communityDiscount = request.form["communityDiscount"]
        insertQuery = "INSERT INTO communities (name, discount) VALUES (%s, %s);"
        data = [communityName, communityDiscount]
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("communities"))

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
        data = [order_ID]
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
    elif request.method == "POST" and "insertPurchaseOrderDetails" in request.form:
        orderID = request.form['orderID']
        itemID = request.form['itemID']
        item_quantity = request.form['quantity']
        print(orderID, itemID, item_quantity)
        insertQuery = "INSERT INTO purchase_order_details (oid, iid, quantity_ordered) VALUES (%s, %s, %s);"
        data = (orderID, itemID, item_quantity)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("purchaseOrderDetails"))
    # delete works! 
    elif request.method == "POST" and "deleteOrderItemRelationship" in request.form:
        order_ID = request.form['orderID']
        item_ID = request.form['itemID']
        deleteQuery = "DELETE FROM purchase_order_details WHERE oid = %s AND iid = %s;"
        data = (order_ID, item_ID)
        result = execute_query(db_connection, deleteQuery, data).fetchall()
        return redirect(url_for("purchaseOrderDetails"))

# fixed the mistakes made in the rendering and in the html file
# all queries work now. 
@app.route("/customerCommunities", methods=["POST", "GET"])
def customerCommunities():
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * FROM user_communities"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("customerCommunities.html", customerCommunities = result)
    # dude where was your filteredCommunities and customerCommunities in your html. it cant render unless you do this. 
    elif request.method == "POST" and "searchByCustomerID" in request.form:
        # has to be the same name as the form input...
        customer_ID = request.form['searchByCustomerID']
        filteredSelectQuery = "SELECT * FROM user_communities WHERE customer_ID = %s;"
        data = [customer_ID]
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("customerCommunities.html", filteredCommunities=result)
    elif request.method == "POST" and "insertNewCustomerCommunity" in request.form:
        customer_ID = request.form["customer_ID"]
        community_ID = request.form["Community_ID"]
        insertQuery = "INSERT INTO user_communities (customer_ID, community_ID) VALUES (%s, %s);"
        data = (customer_ID, community_ID)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("customerCommunities"))

# above is unfinished

# allows us to not rerun server everytime we make a change 
if __name__ == "__main__":
    app.run(debug=True)

