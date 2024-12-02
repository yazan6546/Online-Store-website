DROP DATABASE IF EXISTS Store;
CREATE DATABASE Store;
use Store;

create table Customer(
    customer_id int not null auto_increment,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null,
    primary key (customer_id)
);

create table Address(
    address_id int not null auto_increment,
    customer_id int not null,
    address varchar(255) not null,
    city varchar(255) not null,
    state varchar(255) not null,
    zip varchar(255) not null,
    foreign key (customer_id) references Customer(customer_id),
    primary key (address_id)

);

create table Address_customer(
    address_id int not null,
    customer_id int not null,
    foreign key (address_id) references Address(address_id),
    foreign key (customer_id) references Customer(customer_id),
    primary key (address_id, customer_id)
);

create table Category(
    category_id int not null auto_increment,
    name varchar(20) not null,
    description varchar(255),
    primary key (category_id)
);

create table Product(
    product_id int auto_increment,
    name varchar(255) not null,
    description varchar(255) not null,
    price decimal(10,2) not null,
    stock_quantity int not null,
    category_id int not null,
    foreign key (category_id) references Category(category_id),
    primary key (product_id)

);


create table Cart(
    customer_id int not null,
    product_id int not null,
    quantity int not null,
    foreign key (customer_id) references Customer(customer_id),
    foreign key (product_id) references Product(product_id),
    primary key (customer_id, product_id)
);

create table `Orders`(
    order_id int not null,
    customer_id int not null,
    address_id int not null,
    order_date date not null,
    delivery_date date not null,
    shipping_status varchar(20) not null check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (customer_id) references Customer(customer_id),
    foreign key (address_id) references Address(address_id),
    primary key (order_id)
);

create table Order_product(
    order_id int not null,
    product_id int not null,
    quantity int not null,
    foreign key (order_id) references `Orders`(order_id),
    foreign key (product_id) references Product(product_id),
    primary key (order_id, product_id)
);

create table Discount(
    discount_id int not null auto_increment,
    name varchar(255) not null,
    discount decimal(10,2) not null,
    start_date date not null,
    end_date date not null,
    description varchar(255),
    customer_id int,
    product_id int,
    foreign key (product_id) references Product(product_id),
    foreign key (customer_id) references Customer(customer_id),
    primary key (discount_id)
);


