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
    since date ,
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

create table Product(
    product_id int auto_increment,
    product_name varchar(255) not null,
    product_description varchar(255) not null,
    price decimal(10,2) not null,
    photo varchar(100),
    stock_quantity int not null,
    category_id int not null,
    foreign key (category_id) references Category(category_id),
    primary key (product_id)

);

create table Address_Order(
    address_id int not null auto_increment,
    city varchar(255) not null,
    street_address varchar(255) not null,
    primary key (address_id)

);

create table Customer_Order(
    order_id int not null,
    person_id int not null,
    address_id int,
    order_date date,
    delivery_date date,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    shipping_status varchar(20) check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Customer(person_id) on delete cascade on update cascade,
    foreign key (address_id) references Address_Order(address_id),
    primary key (order_id)
);

create table Customer_Order_Line(
    order_line_id int not null,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    quantity int not null,
    foreign key (order_id) references Customer_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);


create table Manager_Order(
    order_id int not null,
    person_id int not null,
    order_date date,
    delivery_date date,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    shipping_status varchar(20) check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Manager(person_id),
    primary key (order_id)
);

create table Manager_Order_Line(
    order_line_id int not null,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    quantity INT NOT NULL CHECK (quantity > 0),
    foreign key (order_id) references Manager_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);

create table Supplier(
    supplier_id int not null auto_increment,
    supplier_name varchar(255) not null,
    phone_number varchar(255) not null,
    primary key (supplier_id)
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