from sqlalchemy import text

INSERT_CUSTOMER_ORDER_TABLE = text("""
                                INSERT INTO Customer_Order (order_id, person_id, address_id, order_date, delivery_date, shipping_status) 
                                VALUES (:order_id, :person_id, :address_id, :order_date, :delivery_date, :shipping_status);
                            """)

GET_CUSTOMER_ORDER_TABLE = text("""
                            SELECT * FROM Manager_Order ORDER BY 1 DESC;
""")

SELECT_CUSTOMER_ORDER_BY_ID = text("""
                                SELECT * FROM Manager_Order
                                WHERE person_id = :id;
                            """)

DELETE_FROM_CUSTOMER_ORDER = text("""
                                DELETE FROM Manager_Order
                                WHERE order_id = :order_id;
                            """)

CREATE_CUSTOMER_ORDER_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Manager_Order(
                            order_id int NOT NULL,
                            product_id int NOT NULL,
                            address_id int NOT NULL,
                            person_id int NOT NULL,
                            order_date date,
                            delivery_date date,
                            shipping_status VARCHAR(255),
                            order_status int NOT NULL,
                            FOREIGN KEY (person_id) REFERENCES Manager(person_id),
                            PRIMARY KEY (order_id));
                            
                        """)

DROP_CUSTOMER_ORDER_TABLE = text("""
                                DROP TABLE IF EXISTS Customer_Order;
                            """)

GET_ALL_INCART_PRODUCTS_BY_ID = text("""

                                SELECT 
                                    p.product_id,
                                    p.product_name,
                                    p.product_description,
                                    p.price,
                                    col.quantity,
                                    col.price_at_time_of_order
                                FROM 
                                    Customer_Order co
                                JOIN 
                                    Customer_Order_Line col ON co.order_id = col.order_id
                                JOIN 
                                    Product p ON col.product_id = p.product_id
                                WHERE 
                                    co.person_id = :id
                                    AND co.order_status = 'IN_CART';
                            """)
