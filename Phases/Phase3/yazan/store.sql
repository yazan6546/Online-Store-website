drop database if exists project;


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
    foreign key (person_id) references Person(person_id),
    primary key (person_id)
);

create table Manager(
    person_id int not null,
    foreign key (person_id) references Person(person_id),
    primary key (person_id)
);

create table Supplier(
    person_id int not null,
    foreign key (person_id) references Person(person_id),
    primary key (person_id)
);


create table Address(
    address_id int not null auto_increment,
    city varchar(255) not null,
    street_address varchar(255) not null,
    primary key (address_id)
);

create table Address_Customer(
    address_id int not null,
    person_id int not null,
    foreign key (address_id) references Address(address_id),
    foreign key (person_id) references Person(person_id),
    primary key (address_id, person_id)
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
    product_id int not null,
    person_id int not null,
    address_id int not null,
    order_date date not null,
    delivery_date date not null,
    shipping_status varchar(20) not null check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Person(person_id),
    foreign key (address_id) references Address_Order(address_id),
    primary key (order_id)
);

create table Customer_Order_Line(
    order_line_id int not null,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    quantity int not null,
    foreign key (order_id) references Customer_Order(order_id),
	foreign key (product_id) references Product(product_id),
    primary key (order_line_id)
);


create table Manager_Order(
    order_id int not null,
    person_id int not null,
    order_date date not null,
    delivery_date date not null,
    shipping_status varchar(20) not null check (shipping_status in ('Shipped', 'Delivered', 'Cancelled')),
    foreign key (person_id) references Person(person_id),
    primary key (order_id)
);

create table Manager_Order_Line(
    order_line_id int not null,
    product_id int not null,
    order_id int not null,
    price_at_time_of_order int not null,
    order_status varchar(20) not null check (order_status in ('IN_CART', 'PLACED')),
    quantity int not null,
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