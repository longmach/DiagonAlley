from flask import Flask, redirect, url_for, render_template, request
from db_connector.db_connector import connect_to_database, execute_query
from datetime import datetime 
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
    getCustomerIDQuery ="SELECT customers.customer_ID from customers"
    created_date = datetime.date(datetime.now())
    db_connection = connect_to_database()
    # get request to show everything in table
    if request.method == "GET":
        getAllQuery = "SELECT * from customers"
        result = execute_query(db_connection, getAllQuery).fetchall()
        customerIDres = execute_query(db_connection, getCustomerIDQuery).fetchall()
        return render_template("customer.html", customers = result, customerIDres= customerIDres)
    # search by first name and last name
    elif request.method == "POST" and "searchByCustomerFirstName" in request.form: 
        f_name = request.form['searchByCustomerFirstName']
        l_name = request.form['searchByCustomerLastName']
        filteredSelectQuery = "SELECT * FROM customers WHERE first_name = %s AND last_name = %s"
        data = (f_name, l_name)
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        customerIDres = execute_query(db_connection, getCustomerIDQuery).fetchall()
        return render_template("customer.html", filteredCustomer = result, customerIDres= customerIDres)
    # update customer
    elif request.method == "POST" and "updateCustomer" in request.form:
        cid = request.form["customer_ID"]
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if cid and f_name and l_name and email and username and password:  
            updateQuery= "UPDATE customers SET first_name = %s, last_name = %s, email = %s, username = %s, password = %s, created_date = %s WHERE customer_ID = %s;"
            data = (f_name, l_name, email, username, password, created_date, cid)
            result = execute_query(db_connection, updateQuery, data).fetchall()
        return redirect(url_for("customer"))
    # insert customer
    elif request.method == "POST" and "addCustomer" in request.form:
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        insertQuery = "INSERT INTO customers (first_name, last_name, email, username, password, created_date) VALUES (%s, %s, %s, %s, %s, %s);"
        data = (f_name, l_name, email, username, password, created_date)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("customer"))
# items
@app.route("/items", methods=["POST", "GET"])
def items():
    db_connection = connect_to_database()
    # select all query
    if request.method == "GET":
        getAllQuery = "SELECT * from items"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("items.html", items = result)
    # search by item name 
    elif request.method == "POST" and "searchByItemName" in request.form:
        item_name = request.form['itemName']
        filteredSelectQuery = "SELECT * FROM items WHERE name = %s"
        data = [item_name]
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("items.html", filteredItems = result)
    # insert new item
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
    # select all query
    if request.method == "GET":
        getAllQuery = "SELECT * from communities"
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("community.html", communities = result)
    # search query
    elif request.method == "POST" and "searchByCommunity" in request.form: 
        communityName = request.form["communityName"]
        filteredSelectQuery = "SELECT * FROM communities WHERE name = %s;"
        data = [communityName]
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("community.html", filteredCommunities = result)
    # insert query
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
    getAllQuery = "SELECT * from purchase_orders"
    getCustomerIDQuery ="SELECT customers.customer_ID from customers"
    orderIDQuery = "SELECT purchase_orders.order_ID from purchase_orders"
     # use this for created date for user
    order_date = datetime.date(datetime.now())
    # select all query
    if request.method == "GET":
        orderIDResults = execute_query(db_connection, orderIDQuery).fetchall()
        customerIDresult = execute_query(db_connection, getCustomerIDQuery).fetchall()
        result = execute_query(db_connection, getAllQuery).fetchall()
        return render_template("purchaseOrder.html", purchaseOrders = result, customerID = customerIDresult, orderID = orderIDResults)
    # search query
    elif request.method == "POST" and "searchByPurchaseOrderID" in request.form:
        order_ID = request.form['purchaseOrderID']
        filteredSelectQuery = "SELECT * FROM purchase_orders WHERE order_ID = %s;"
        data = [order_ID]
        orderIDResults = execute_query(db_connection, orderIDQuery).fetchall()
        customerIDresult = execute_query(db_connection, getCustomerIDQuery).fetchall()
        result = execute_query(db_connection, filteredSelectQuery,data).fetchall()
        return render_template("purchaseOrder.html", filteredPurchaseOrder = result, customerID = customerIDresult, orderID = orderIDResults)
        # update 1:M rel to be nullable
    # update query
    elif request.method == "POST" and "updatePurchaseOrder" in request.form:
        order_ID = request.form["order_ID"]
        customer_ID = request.form["customer_ID"]
        if customer_ID == "NULL":
            customer_ID = None 
        updateQuery= "UPDATE purchase_orders SET customer_ID = %s, order_date = %s WHERE order_ID = %s;"
        data = (customer_ID, order_date, order_ID)
        result = execute_query(db_connection, updateQuery, data).fetchall()
        return redirect(url_for("purchaseOrder"))
    # insert query
    elif request.method == "POST" and "insertPurchaseOrder" in request.form:
        customer_ID = request.form["customerID"]
        insertQuery = "INSERT INTO purchase_orders (customer_ID, order_date) VALUES (%s, %s);"
        data = (customer_ID, order_date)
        result = execute_query(db_connection, insertQuery,data).fetchall()
        return redirect(url_for("purchaseOrder"))

# purchase order details 
@app.route("/purchaseOrderDetails", methods=["POST", "GET"])
def purchaseOrderDetails():
    db_connection = connect_to_database()
    # select all query
    if request.method == "GET":
        getAllQuery = "SELECT * from purchase_order_details"
        orderIDQuery = "SELECT purchase_orders.order_ID from purchase_orders"
        itemIDQuery = "SELECT items.item_ID from items" 
        result = execute_query(db_connection, getAllQuery).fetchall()
        orderIDResults = execute_query(db_connection, orderIDQuery).fetchall()
        itemIDResults = execute_query(db_connection, itemIDQuery).fetchall()
        return render_template("purchaseOrderDetails.html", purchaseOrderDetails = result, orderID = orderIDResults, itemID = itemIDResults)
    # insert query
    elif request.method == "POST" and "insertPurchaseOrderDetails" in request.form:
        orderID = request.form['orderID']
        itemID = request.form['itemID']
        item_quantity = request.form['quantity']
        insertQuery = "INSERT INTO purchase_order_details (oid, iid, quantity_ordered) VALUES (%s, %s, %s);"
        data = (orderID, itemID, item_quantity)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("purchaseOrderDetails"))
    # delete query 
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
    # select all query
    if request.method == "GET":
        getAllQueryCustomerCommunities = "SELECT * FROM user_communities"
        getCustomerID = "SELECT customers.customer_ID from customers"
        getCommunityID = "SELECT communities.community_ID from communities"
        result = execute_query(db_connection, getAllQueryCustomerCommunities).fetchall()
        customerIDresult = execute_query(db_connection, getCustomerID).fetchall()
        communityIDresult = execute_query(db_connection, getCommunityID).fetchall()
        return render_template("customerCommunities.html", customerCommunities = result, customersID =customerIDresult, communitiesID = communityIDresult)
    # search query 
    elif request.method == "POST" and "searchByCustomerID" in request.form:
        customer_ID = request.form['searchByCustomerID']
        filteredSelectQuery = "SELECT * FROM user_communities WHERE customer_ID = %s;"
        data = [customer_ID]
        result = execute_query(db_connection, filteredSelectQuery, data).fetchall()
        return render_template("customerCommunities.html", filteredCommunities=result)
    # insert query
    elif request.method == "POST" and "insertNewCustomerCommunity" in request.form:
        customer_ID = request.form["customer_ID"]
        community_ID = request.form["Community_ID"]
        insertQuery = "INSERT INTO user_communities (customer_ID, community_ID) VALUES (%s, %s);"
        data = (customer_ID, community_ID)
        result = execute_query(db_connection, insertQuery, data).fetchall()
        return redirect(url_for("customerCommunities"))

# allows us to not rerun server everytime we make a change 
if __name__ == "__main__":
    app.run(debug=True)

