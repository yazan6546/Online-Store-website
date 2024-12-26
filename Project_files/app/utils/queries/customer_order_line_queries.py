from sqlalchemy import text


INSERT_MANAGER_ORDER_LINE_TABLE = text("""
                                INSERT INTO Manager_Order (order_id, person_id, order_status, order_date, delivery_date, shipping_status, person_id) 
                                VALUES (:order_id, :person_id,:order_status, :order_date, :delivery_date, :shipping_status, :person_id);
                            """)

GET_MANAGER_ORDER_LINE_TABLE = text("""
                            SELECT * FROM Manager_Order ORDER BY 1 DESC;
""")

SELECT_MANAGER_ORDER_BY_ID = text("""
                                SELECT * FROM Manager_Order
                                WHERE person_id = :id;
                            """)

DELETE_FROM_MANAGER_ORDER = text("""
                                DELETE FROM Manager_Order
                                WHERE order_id = :order_id;
                            """)

CREATE_MANAGER_ORDER_TABLE = text("""
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
