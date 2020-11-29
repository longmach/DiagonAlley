-- These are some Database Manipulation queries for a partially implemented Project Website 
-- using the bsg database.
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.


-- get a single data for the search form
SELECT * FROM customers WHERE first_name = :first_name_from_customer_page AND last_name = :last_name_from_customer_page;	-- customer page
SELECT * WHERE name = :name_from_community_page;																			-- communities page
SELECT * FROM items WHERE name = :name_from_items_page;																-- item page
SELECT * FROM purchase_orders WHERE order_ID = :order_ID_from_purchase_order_page;										-- purchase_orders page
SELECT * FROM user_communities WHERE customer_ID = :customer_id_from_customer_communities_page;

-- filtered queries for drop downs

-- purchase order
SELECT customers.customer_ID from customers
SELECT purchase_orders.order_ID from purchase_orders

-- purchase order details 
SELECT items.item_ID from items

-- user communities
SELECT user_communities.customer_ID from user_communities
SELECT communities.community_ID from communities

-- get all data from the tables
SELECT * FROM customers;	-- customer page
SELECT * FROM communities; -- communities page
SELECT * FROM items;	-- item page
SELECT * FROM purchase_orders; -- purchase_orders page
SELECT * FROM purchase_order_details; -- purchase order details page
SELECT * FROM user_communities; -- NEW user communities page

-- add a new instance in tables
INSERT INTO customers (first_name, last_name, email, username, password, created_date) VALUES (:fname_input, :lname_input, :email_input, :username_input, :password_input, :date_input);
INSERT INTO communities (name, discount) VALUES (:comm_name_input, :discount_input);
INSERT INTO items (name, inventory_quantity, cost, price) VALUES (:item_name_input, :quantity_input, :cost_input, :price_input);
INSERT INTO purchase_orders (customer_ID, order_date) VALUES (:customer_ID_input, :order_date_input);
INSERT INTO purchase_order_details (oid, iid, quantity_ordered) VALUES (:oid_input, :iid_input, :quantity_ordered_input); -- Add new items M-to-M relationship addition
INSERT INTO user_communities (customer_ID, community_ID) VALUES (:customer_ID_input, :community_ID_input); -- add new communities to user and vice versa M:M

-- update a character's data based on submission of the Update Character form 
UPDATE customers SET first_name = :first_name_from_update_form, last_name = :last_name_from_update_form, email = :email_from_update_form, username = :username_from_update_form, created_date = :created_date_input WHERE first_name = :first_name_from_update_form AND last_name = :last_name_from_update_form;
-- delete M:M purchase order details
DELETE FROM purchase_order_details WHERE oid = :oid_from_delete_form AND iid = :iid_from_delete_form;												-- M-to-M relationship deletion


