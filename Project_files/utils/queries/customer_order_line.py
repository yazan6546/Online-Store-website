from sqlalchemy import text


INSERT_CUSTOMER_ORDER_LINE_TABLE = text("""
                                INSERT INTO Customer_Order_Line (order_id, product_id, price_at_time_of_order, quantity) 
                                VALUES (:order_id, :product_id, :price_at_time_of_order, :quantity);
                            """)

GET_CUSTOMER_ORDER_LINE_TABLE = text("""
                            SELECT * FROM Manager_Order ORDER BY 1 ;
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
                            person_id int NOT NULL,
                            order_date date NOT NULL,
                            delivery_date date NOT NULL,
                            shipping_status VARCHAR(255) NOT NULL,
                            FOREIGN KEY (person_id) REFERENCES Manager(person_id),
                            PRIMARY KEY (order_id)
                            );
                        """)

DROP_MANAGER_ORDER_TABLE = text("""
                                DROP TABLE IF EXISTS Customer_Order_Line;
                            """)

DELETE_ALL_FROM_CUSTOMER_ORDER_LINE = text("""
    DELETE FROM Customer_Order_Line;
""")