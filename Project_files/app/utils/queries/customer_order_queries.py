from sqlalchemy import text


INSERT_CUSTOMER_ORDER_TABLE = text("""
                                INSERT INTO Customer_Order (order_id, product_id, order_date, delivery_date, shipping_status, person_id) 
                                VALUES (:order_id, :person_id, :order_date, :delivery_date, :shipping_status, :person_id);
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
                                WHERE order_id = :order_id);
                            """)

CREATE_CUSTOMER_ORDER_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Manager_Order(
                            order_id int NOT NULL,
                            product_id int NOT NULL,
                            person_id int NOT NULL,
                            order_date date,
                            delivery_date date,
                            shipping_status VARCHAR(255),
                            order_status int NOT NULL,
                            FOREIGN KEY (person_id) REFERENCES Manager(person_id),
                            PRIMARY KEY (order_id)
                        """)

DROP_CUSTOMER_ORDER_TABLE = text("""
                                DROP TABLE IF EXISTS Customer_Order;
                            """)
