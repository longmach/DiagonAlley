-- part A -- 
-- create tables -- 
DROP TABLE IF EXISTS customers;
CREATE TABLE customers(
	customer_ID INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_date DATE NOT NULL
);
DROP TABLE IF EXISTS purchase_orders;
CREATE TABLE purchase_orders(
	order_ID INT(11) AUTO_INCREMENT PRIMARY KEY,
	customer_ID INT(11) NOT NULL, -- foreign key 
    order_date DATE NOT NULL,
	FOREIGN KEY (customer_ID) REFERENCES customers(customer_ID)
);

DROP TABLE IF EXISTS items;
CREATE TABLE items(
	item_ID INT(11) AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL, 
    inventory_quantity INT(11) NOT NULL, 
    cost INT(11) NOT NULL,
    price INT(11) NOT NULL
);

DROP TABLE IF EXISTS communities;
CREATE TABLE communities(
	community_ID INT(11) AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL, 
    discount INT(11) NOT NULL
);

-- composite entity showing M:M between items and purchase_orders
DROP TABLE IF EXISTS purchase_order_details;
CREATE TABLE purchase_order_details(
	oid INT(11) NOT NULL, -- foreign key, oid = order_ID
	iid INT(11) NOT NULL, -- foreign key, iid = item_ID
    quantity_ordered INT(11) NOT NULL,
    PRIMARY KEY(oid,iid),
	FOREIGN KEY (oid) REFERENCES purchase_orders(order_ID), -- the name pod_fk_order = purchase_order_details foreign key order
    FOREIGN KEY (iid) REFERENCES items(item_ID) --  the name pod_fk_item = purchase_order_details foreign key item
);

-- composite entity showing M:M between customers and communities
DROP TABLE IF EXISTS user_communities;
CREATE TABLE user_communities(
	customer_ID INT(11) NOT NULL , 
	community_ID INT(11) NULL, -- make this nullable
    PRIMARY KEY(customer_ID, community_ID), -- primary key is a combo between customer_ID and community_ID
	CONSTRAINT uc_fk_customer FOREIGN KEY (customer_ID) REFERENCES customers(customer_ID), --  the name uc_fk_customer = user_communities foreign key customer
    CONSTRAINT uc_fk_community FOREIGN KEY (community_ID) REFERENCES communities(community_ID) --  the name uc_fk_community = user_communities foreign key community
);

-- part B -- 
-- insert into customers  -- 
INSERT INTO customers(username, password, email, first_name, last_name, created_date) VALUES 
("potterH", "password", "potterh@hogwarts.edu", "Harry", "Potter", "2020-11-10"),
("weasleyR", "contrasena", "weasleyr@hogwarts.edu", "Ron", "Weasley", "2020-12-10"),
("grangerH", "parola", "grangerh@hogwarts.edu", "Hermione", "Granger", "2020-11-14")
;
-- insert into purchase order -- 
INSERT INTO purchase_orders(customer_ID, order_date) VALUES
((SELECT customer_ID from customers WHERE username = "potterH"), "2020-11-12"),
((SELECT customer_ID from customers WHERE username = "weasleyR"), "2020-12-12"),
((SELECT customer_ID from customers WHERE username = "grangerH"), "2020-12-12")
;
-- insert into items-- 
INSERT INTO items(name, inventory_quantity, cost, price) VALUES
("Firebolt", 1000, 250, 900),
("Robes", 1000, 1, 5), 
("Cauldron", 1000,3, 25), 
("Toy Elder Wand", 1000,1, 7), 
("Remembrall", 1000,2, 7),
("Official Guide to Quidditch World Cup", 1000, 15, 39),
("Skiving Snackbox", 1000, 2, 8),
("Deluminator", 1000, 4, 9),
("Sneakoscope", 1000, 11, 25);
-- insert into communities -- 
INSERT INTO communities(name, discount) VALUES
("Hogwarts", 15),
("Beauxbatons", 7), 
("Durmstrang", 2), 
("Ilvermorny", 5),
("Uagadou", 5), 
("Mahoutokoro", 5);
-- insert into purchase_order_details -- 
INSERT INTO purchase_order_details(oid, iid, quantity_ordered) VALUES
((SELECT purchase_orders.order_ID from purchase_orders WHERE purchase_orders.customer_ID = (SELECT customer_ID FROM customers WHERE customers.username = "potterH")), (SELECT item_ID FROM items WHERE items.item_ID = 1), 1),
((SELECT purchase_orders.order_ID from purchase_orders WHERE purchase_orders.customer_ID = (SELECT customer_ID FROM customers WHERE customers.username = "weasleyR")), (SELECT item_ID FROM items WHERE items.item_ID = 2), 5),
((SELECT purchase_orders.order_ID from purchase_orders WHERE purchase_orders.customer_ID = (SELECT customer_ID FROM customers WHERE customers.username = "grangerH")), (SELECT item_ID FROM items WHERE items.item_ID = 4), 1);
-- insert into user_communities -- 
INSERT INTO user_communities(customer_ID, community_ID) VALUES
((SELECT customers.customer_ID from customers WHERE username = "potterH"), (SELECT communities.community_ID FROM communities WHERE communities.name = "Hogwarts")),
((SELECT customers.customer_ID from customers WHERE username = "weasleyR"), (SELECT communities.community_ID FROM communities WHERE communities.name = "Hogwarts")),
((SELECT customers.customer_ID from customers WHERE username = "grangerH"), (SELECT communities.community_ID FROM communities WHERE communities.name = "Hogwarts"));

