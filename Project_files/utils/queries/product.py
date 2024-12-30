from sqlalchemy import text


INSERT_PRODUCTS_TABLE = text("""
                                INSERT INTO Product (product_id, product_name, product_description,brand, price, photo, stock_quantity, category_id,supplier_id)
                                VALUES (:product_id, :product_name, :product_description,:brand, :price, :photo, :stock_quantity, :category_id, :supplier_id); 
                            """)

GET_PRODUCTS_TABLE = text("""
                            SELECT * FROM Product ORDER BY 1 DESC;
                         """)

SELECT_PRODUCT_BY_ID = text("""
                                SELECT * FROM Product
                                WHERE product_id = :product_id;
                            """)

SELECT_PRODUCT_BY_CATEGORY = text("""
                                SELECT * FROM Product   
                                WHERE category_id = :category_id;
                            """)

SELECT_PRODUCT_BY_SUPPLIER = text("""
                                SELECT * FROM Product   
                                WHERE supplier_id = :supplier_id;
                            """)

UPDATE_PRODUCTS_TABLE = text("""
                                UPDATE Product
                                SET product_name = :product_name,
                                    product_description = :product_description,
                                    brand = :brand,
                                    price = :price,
                                    photo = :photo,
                                    stock_quantity = :stock_quantity,
                                    category_id = :category_id,
                                    supplier_id = :supplier_id
                                WHERE product_id = :product_id;
                            """)

DELETE_FROM_PRODUCTS = text("""
                                DELETE FROM Product 
                                WHERE product_id = :product_id;
                            """)

CREATE_PRODUCTS_TABLE = text("""
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
                        """)

DROP_PRODUCTS_TABLE = text("""
                                DROP TABLE IF EXISTS Product;
                        """)
