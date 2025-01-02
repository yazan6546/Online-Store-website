drop database Store;
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
    category_name varchar(20) not null,
    category_description varchar(255),
    primary key (category_id)
);

create table Supplier(
    supplier_id int not null auto_increment,
    supplier_name varchar(255) not null,
    phone_number varchar(255) not null,
    primary key (supplier_id)
);


create table Product(
    product_id int auto_increment,
    product_name varchar(255) not null,
    product_description varchar(255) not null,
    brand varchar(30) not null,
    price decimal(10,2) not null,
    photo varchar(100),
    stock_quantity int not null,
    category_id int not null,
    supplier_id int not null,
    foreign key (category_id) references Category(category_id),
    foreign key (supplier_id) references Supplier(supplier_id),
    primary key (product_id)

);




create table Address_Order(
    address_id int,
    city varchar(255) not null,
    street_address varchar(255) not null,
    primary key (address_id)

);

create table Customer_Order(
    order_id int not null auto_increment,
    person_id int not null,
    address_id int,
    order_date date,
    delivery_date date,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    shipping_status varchar(20) check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Customer(person_id) on delete cascade on update cascade,
    foreign key (address_id) references Address(address_id),
    primary key (order_id)
);

create table Customer_Order_Line(
    order_line_id int not null auto_increment,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    quantity int not null,
    foreign key (order_id) references Customer_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);


create table Manager_Order(
    order_id int not null auto_increment,
    person_id int not null,
    order_date date,
    delivery_date date,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    shipping_status varchar(20) check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Manager(person_id),
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


select * from Person;

select * from Customer;

SELECT
                            c.person_id AS person_id,
                            p.first_name AS first_name,
                            p.last_name AS last_name,
                            p.email AS email
                            FROM Customer c
                            JOIN Person p on c.person_id = p.person_id
                            WHERE p.first_name like 'IBRAHIM1' or p.last_name like '%IBRAHIM1%';

select * from Person;

select * from Manager;

select * from Address;

delete from Person where person_id > 20;

select * from Category;

delete from Category;

delete from Customer;
delete from Person;
select * from Customer;
select * from Manager;
select * from Person;

delete from Address;
select COUNT(*) from Customer;
select COUNT(*) from Address;

select * from Category;
select * from Supplier;

select * from Customer_Order;

SELECT p.product_id, p.product_name, SUM(col.quantity) AS total_quantity_sold
    FROM Product p
    JOIN Customer_Order_Line col ON p.product_id = col.product_id
    JOIN Customer_Order co ON col.order_id = co.order_id
    WHERE co.order_status = 'PLACED'
    GROUP BY p.product_id, p.product_name
    ORDER BY total_quantity_sold DESC
    LIMIT 10;


SELECT COUNT(DISTINCT c.person_id) AS customers_with_address
FROM Customer c
JOIN Address a ON c.person_id = a.person_id;