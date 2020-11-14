-- These are some Database Manipulation queries for a partially implemented Project Website 
-- using the bsg database.
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.

-- get all community name to populate community dropdown
SELECT name FROM communities;					-- customer page
SELECT customer_ID FROM purchase_orders;		-- purchase order page
SELECT order_ID FROM purchase_order_details;	-- purchase order details page
SELECT name FROM items;							-- purchase order details page

-- get a single data for the search form
SELECT first_name,last_name, email, username, password, created_date FROM customers WHERE CONCAT(first_name,' ',last_name) = :name_from_customer_page;	-- customer page
SELECT name, discount FROM communities WHERE name = :name_from_community_page;																			-- communities page
SELECT name, inventory_quantity, cost, price FROM items WHERE name = :name_from_items_page;																-- item page
SELECT order_ID, customer_ID, order_date FROM purchase_orders WHERE order_ID = :order_ID_from_purchase_order_page;										-- purchase_orders page
	
-- get all data from the tables
-- we could do a select*from x_table
SELECT first_name,last_name, email, username, password, created_date FROM customers;																	-- customer page
SELECT name, discount FROM communities;																													-- communities page
SELECT name, inventory_quantity, cost, price FROM items;																								-- item page
SELECT order_ID, customer_ID, order_date FROM purchase_orders; 																							-- purchase_orders page
SELECT oid, ItemName = (SELECT name from item WHERE purchase_order_details.idd = item_ID), quantity_ordered FROM purchase_order_details; 				-- purchase order details page


-- add a new instance in tables
INSERT INTO customers (first_name, last_name, email, username, password, created_date) VALUES (:fname_input, :lname_input, :email_input, :username_input, :password_input, convert(date, getdate()));
INSERT INTO communities (name, discount) VALUES (:comm_name_input, :discount_input);
INSERT INTO items (name, inventory_quantity, cost, price) VALUES (:item_name_input, :quantity_input, :cost_input, :price_input);
INSERT INTO purchase_orders (customer_ID, order_date) VALUES (:customer_ID_input, :order_date_input);
INSERT INTO purchase_order_details (oid, iid, quantity_ordered) VALUES (:oid_input, :iid_input, :quantity_ordered_input);								-- Add new items M-to-M relationship addition

-- update a character's data based on submission of the Update Character form 

UPDATE customers SET first_name = :first_name_from_update_form, last_name = :last_name_from_update_form, email = :email_from_update_form, username = :username_from_update_form, created_date = :created_date_input WHERE CONCAT(first_name,' ',last_name) = CONCAT(:first_name_from_update_form,' ',:last_name_from_update_form);
UPDATE communities SET name = :community_name_from_update_form, discount = :discount_from_update_form WHERE name = :cname_from_update_form);
UPDATE items SET name = :item_name_from_update_form, inventory_quantity = :quantity_from_update_form, cost = :cost_from_update_form, price = price_from_update_form WHERE name = :item_name_from_update_form;
UPDATE purchase_orders SET order_ID = :order_ID_from_update_form, customer_ID = :customer_ID_from_update_form, order_date = order_date_from_update_form WHERE order_ID = :order_ID_from_update_form;
UPDATE purchase_order_details SET oid = :order_ID_from_update_form, iid = :item_ID_from_update_form, quantity_ordered = quantity_ordered_from_update_form WHERE oid = :order_ID_from_update_form;	-- M-to-M relationship update

-- delete a character
DELETE FROM customers WHERE customer_ID = :customer_ID_from_delete_form;
DELETE FROM communities WHERE community_ID = :community_ID_from_delete_form;
DELETE FROM items WHERE item_ID = :item_ID_from_delete_form;
DELETE FROM purchase_orders WHERE order_ID = :order_ID_from_delete_form;
DELETE FROM purchase_order_details WHERE oid = :oid_from_delete_form AND iid = :iid_from_delete_form;												-- M-to-M relationship deletion


