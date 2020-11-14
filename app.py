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
    db_connection = connect_to_database()
    if request.method == "GET":
        getAllQuery = "SELECT * from customers"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template("customer.html", rows = result)
    # fix queries below to exchange for real data
    # we might not want to send the results back for update/delete/insert
    elif request.method == "POST" and "searchByCustomerName" in request.form:
        filteredSelectQuery = "SELECT first_name,last_name, email, username, password, created_date FROM customers WHERE CONCAT(first_name,' ',last_name) = :name_from_customer_page;"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template("customer.html", filteredCustomer = result)
    elif request.method == "POST" and "" in request.form:
        updateQuery= "UPDATE customers SET first_name = :first_name_from_update_form, last_name = :last_name_from_update_form, email = :email_from_update_form, username = :username_from_update_form, created_date = :created_date_input WHERE CONCAT(first_name,' ',last_name) = CONCAT(:first_name_from_update_form,' ',:last_name_from_update_form);"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return redirect(url_for("customer"))
    elif request.method == "POST" and "" in request.form:
        deleteQuery= "DELETE FROM customers WHERE customer_ID = :customer_ID_from_delete_form;"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return redirect(url_for("customer"))
    elif request.method == "POST" and "" in request.form:
        insertQuery = "INSERT INTO customers (first_name, last_name, email, username, password, created_date) VALUES (:fname_input, :lname_input, :email_input, :username_input, :password_input, convert(date, getdate()));"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return redirect(url_for("customer"))
# items
@app.route("/items", methods=["POST", "GET"])
def items():
    return render_template("items.html")
# community
@app.route("/community", methods=["POST", "GET"])
def community():
    return render_template("community.html")
# user communities
@app.route("/userCommunities", methods=["POST", "GET"])
def userCommunities():
    return render_template("userCommunities.html")
# purchase order
@app.route("/purchaseOrder", methods=["POST", "GET"])
def purchaseOrder():
    return render_template("purchaseOrder.html")
# purchase order details 
@app.route("/purchaseOrderDetails", methods=["POST", "GET"])
def purchaseOrderDetails():
    return render_template("purchaseOrderDetails.html")

# allows us to not rerun server everytime we make a change 
if __name__ == "__main__":
    app.run(debug=True)

