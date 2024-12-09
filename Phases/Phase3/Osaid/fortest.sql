CREATE DATABASE store;

USE store;

CREATE TABLE Product (
    product_ID INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    stock_quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_ID INT NOT NULL,
    description TEXT
);


select * from product ;
