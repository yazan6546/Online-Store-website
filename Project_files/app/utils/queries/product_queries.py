from sqlalchemy import text


INSERT_PRODUCTS_TABLE = text("""
                                INSERT INTO Product (product_id, product_name, product_description, price, photo, stock_quantity, category_id)
                                VALUES (:product_id, :product_name, :product_description, :price, :photo, :stock_quantity, :category_id); 
                            """)

GET_PRODUCTS_TABLE = text("""
                            SELECT * FROM Prodyct ORDER BY 1 DESC;
                         """)

SELECT_PRODUCT_BY_ID = text("""
                                SELECT * FROM Product
                                WHERE product_id = :product_id;
                            """)


DELETE_FROM_PRODUCTS = text("""
                                DELETE FROM Product 
                                WHERE product_id = :product_id;
                            """)

CREATE_PRODUCTS_TABLE = text("""
                            product_id int AUTO_INCREMENT,
                            supplier_id INT NOT NULL, ,
                            product_name VARCHAR(255) NOT NULL,
                            product_description VARCHAR(255) NOT NULL,
                            price DECIMAL(10,2) NOT NULL,
                            photo varchar(100),
                            stock_quantity INT NOT NULL,
                            category_id INT NOT NULL,
                            FOREIGN KEY (category_id) REFERENCES Category(category_id),
                            FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
                            PRIMARY KEY (product_id)
                        """)

DROP_CUSTOMERS_TABLE = text("""
                                DROP TABLE IF EXISTS Product;
                            """)
