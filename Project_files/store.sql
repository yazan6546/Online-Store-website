drop database if exists Store;
create database Store;
use Store;

create table Person(
    person_id int not null auto_increment,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null unique,
    passcode varchar(255) not null,
    primary key (person_id)
);


create table Customer(
    person_id int not null,
    birth_date date,
    foreign key (person_id) references Person(person_id) on delete cascade on update cascade,

    primary key (person_id)
);



create table Manager(
    person_id int not null,
    since date,
    role varchar(20) not null check (role in ('Financial Manager', 'Assistant Manager', 'Regional Manager')),
    foreign key (person_id) references Person(person_id) on delete cascade on update cascade,
    primary key (person_id)
);


create table Address(
    address_id int not null auto_increment,
    person_id int not null,
    city varchar(255) not null,
    zip_code varchar(255) not null,
    street_address varchar(255) not null,
    foreign key (person_id) references Customer(person_id) on delete cascade on update cascade,
    primary key (address_id)
);

create table Category(
    category_id int not null auto_increment,
    category_name varchar(20) unique not null,
    category_description varchar(255),
    primary key (category_id)
);

create table Supplier(
    supplier_id int not null auto_increment,
    supplier_name varchar(255) not null UNIQUE,
    phone_number varchar(255) not null,
    primary key (supplier_id)
);


create table Product(
    product_id int auto_increment,
    product_name varchar(255) unique not null,
    product_description varchar(255) not null,
    brand varchar(30) not null,
    price decimal(10,2) not null check (price > 0),
    photo varchar(100),
    stock_quantity int not null check ( stock_quantity >= 0),
    category_id int not null,
    supplier_id int not null,
    foreign key (category_id) references Category(category_id),
    foreign key (supplier_id) references Supplier(supplier_id),
    primary key (product_id)

);


CREATE TABLE DeliveryService (
    delivery_service_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each delivery service
    delivery_service_name VARCHAR(255) NOT NULL UNIQUE,                         -- Name of the delivery service (e.g., "DHL", "FedEx")
    phone_number VARCHAR(15)                        -- Contact phone number for the delivery service

);

create table Customer_Order(
    order_id int not null auto_increment,
    person_id int not null,
    address_id int,
    order_date date,
    delivery_date date,
    delivery_service_id int not null,
    order_status varchar(20) not null check (order_status in ('PLACED', 'COMPLETED', 'CANCELLED')),
    foreign key (person_id) references Customer(person_id) on delete cascade on update cascade,
    foreign key (address_id) references Address(address_id),
    foreign key (delivery_service_id) references DeliveryService(delivery_service_id),
    primary key (order_id)
);

create table Customer_Order_Line(
    order_line_id int not null auto_increment,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    quantity INT NOT NULL CHECK (quantity > 0),
    foreign key (order_id) references Customer_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);


create table Manager_Order(
    order_id int not null auto_increment,
    person_id int not null,
    order_date date,
    delivery_date date,
    delivery_service_id int not null,
    order_status varchar(20) not null check (order_status in ('PLACED', 'COMPLETED', 'CANCELLED')),
    foreign key (person_id) references Manager(person_id),
    foreign key (delivery_service_id) references DeliveryService(delivery_service_id),
    primary key (order_id)

);

create table Manager_Order_Line(
    order_line_id int not null auto_increment,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    quantity INT NOT NULL CHECK (quantity > 0),
    foreign key (order_id) references Manager_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);


DELIMITER $$

CREATE TRIGGER after_order_completed
AFTER UPDATE ON Customer_Order
FOR EACH ROW
BEGIN
    -- Check if the order status changed to COMPLETED
    IF NEW.order_status = 'COMPLETED' AND OLD.order_status != 'COMPLETED' THEN
        -- Increment stock for each product in the order
        UPDATE Product p
        JOIN Customer_Order_Line col ON p.product_id = col.product_id
        SET p.stock_quantity = p.stock_quantity - col.quantity
        WHERE col.order_id = NEW.order_id;
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER after_order_completed_insert
AFTER INSERT ON Customer_Order
FOR EACH ROW
BEGIN
    -- Check if the new order is inserted with the status COMPLETED
    IF NEW.order_status = 'COMPLETED' THEN
        -- Increment stock for each product in the order
        UPDATE Product p
        JOIN Customer_Order_Line col ON p.product_id = col.product_id
        SET p.stock_quantity = p.stock_quantity - col.quantity
        WHERE col.order_id = NEW.order_id;
    END IF;
END $$

DELIMITER ;



DELIMITER $$

CREATE TRIGGER after_order_manager_completed_insert
AFTER INSERT ON Manager_Order
FOR EACH ROW
BEGIN
    -- Check if the new order is inserted with the status COMPLETED
    IF NEW.order_status = 'COMPLETED' THEN
        -- Increment stock for each product in the order
#         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Order is marked as COMPLETED';
        UPDATE Product p
        JOIN Manager_Order_Line col ON p.product_id = col.product_id
        SET p.stock_quantity = p.stock_quantity + col.quantity
        WHERE col.order_id = NEW.order_id;

#         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Order status is not COMPLETED';
    END IF;
END $$

DELIMITER ;



DELIMITER $$

CREATE TRIGGER after_order_manager_completed
AFTER UPDATE ON Manager_Order
FOR EACH ROW
BEGIN
    -- Check if the order status changed to COMPLETED
    IF NEW.order_status = 'COMPLETED' AND OLD.order_status != 'COMPLETED' THEN
#         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Order is marked as COMPLETED';
        -- Increment stock for each product in the order
        UPDATE Product p
        JOIN Manager_Order_Line col ON p.product_id = col.product_id
        SET p.stock_quantity = p.stock_quantity + col.quantity
        WHERE col.order_id = NEW.order_id;

#         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Order status is not COMPLETED';
    END IF;
END $$

DELIMITER ;






   -- Trigger for Customer table
   DELIMITER $$

   CREATE TRIGGER before_insert_customer
   BEFORE INSERT ON Customer
   FOR EACH ROW
   BEGIN
       -- Check if person_id exists in Manager
       IF EXISTS (SELECT 1 FROM Manager WHERE person_id = NEW.person_id) THEN
           SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'This person_id already exists in Manager. A person cannot be both a Manager and a Customer.';
       END IF;
   END $$

   DELIMITER ;

   -- Trigger for Manager table
   DELIMITER $$

   CREATE TRIGGER before_insert_manager
   BEFORE INSERT ON Manager
   FOR EACH ROW
   BEGIN
       -- Check if person_id exists in Customer
       IF EXISTS (SELECT 1 FROM Customer WHERE person_id = NEW.person_id) THEN
           SIGNAL SQLSTATE '45000'
           SET MESSAGE_TEXT = 'This person_id already exists in Customer. A person cannot be both a Customer and a Manager.';
       END IF;
   END $$

   DELIMITER ;



# SELECT
#     c.person_id AS person_id,
#     p.first_name AS first_name,
#     p.last_name AS last_name,
#     p.email AS email,
#     p.passcode AS passcode,
#     c.birth_date AS birth_date
# FROM Customer c
# JOIN Person p
# ON c.person_id = p.person_id
# WHERE p.email = :email;


UPDATE Product p
JOIN Manager_Order_Line col ON p.product_id = col.product_id
SET p.stock_quantity = p.stock_quantity + col.quantity
WHERE col.order_id = 351;


delete from Product
where product_id > 101;


select * from Address
where person_id = 205;

select * from Manager_Order_Line where order_id = 353;

SELECT
    CASE
        WHEN age BETWEEN 18 AND 30 THEN '18-30'
        WHEN age BETWEEN 31 AND 40 THEN '31-40'
        WHEN age BETWEEN 41 AND 50 THEN '41-50'
        WHEN age > 50 THEN '50+'
    END AS age_group,
    COUNT(*) AS count
FROM (
    SELECT
        TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
    FROM Customer
) AS age_data
GROUP BY age_group
ORDER BY FIELD(age_group, '18-30', '31-40', '41-50', '50+');


select * from Manager_Order_Line where order_id=182;


SELECT
    month,
    product_name,
    total_quantity_sold
FROM (
    SELECT
        DATE_FORMAT(co.order_date, '%Y-%m') AS month,
        p.product_name,
        SUM(col.quantity) AS total_quantity_sold,
        ROW_NUMBER() OVER (PARTITION BY DATE_FORMAT(co.order_date, '%Y-%m') ORDER BY SUM(col.quantity) DESC) AS rn
    FROM
        Customer_Order co
    JOIN
        Customer_Order_Line col ON co.order_id = col.order_id
    JOIN
        Product p ON col.product_id = p.product_id
    WHERE
        co.order_status = 'COMPLETED' AND YEAR(co.order_date) = 2024
    GROUP BY
        month, p.product_name
) subquery
WHERE rn = 1
ORDER BY month;


SELECT
        MONTH(co.order_date) AS month,
        p.product_name,
        SUM(col.quantity) AS total_quantity_sold,
        ROW_NUMBER() OVER (PARTITION BY MONTH(co.order_date, '%Y-%m') ORDER BY SUM(col.quantity) DESC) AS rn

    FROM
        Customer_Order co
    JOIN
        Customer_Order_Line col ON co.order_id = col.order_id
    JOIN
        Product p ON col.product_id = p.product_id
    WHERE
        co.order_status = 'COMPLETED' AND YEAR(co.order_date) = 2024
    GROUP BY
        month, p.product_name