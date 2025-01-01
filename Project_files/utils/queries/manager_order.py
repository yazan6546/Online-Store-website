from sqlalchemy import text


INSERT_MANAGER_ORDER_TABLE = text("""
                                INSERT INTO Manager_Order (order_id, person_id, order_status, order_date, delivery_date, shipping_status, person_id) 
                                VALUES (:order_id, :person_id, :order_date, :delivery_date, :order_status, :shipping_status, :person_id);
                            """)

GET_MANAGER_ORDER_TABLE = text("""
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

UPDATE_MANAGER_ORDER_TABLE = text("""
                            UPDATE Manager_Order
                            SET order_status=:order_status,
                            person_id=:person_id,
                            delivery_date=:delivery_date, 
                            shipping_status=:shipping_status, 
                            order_date=:order_date
                            WHERE order_id = :order_id;
                            """)

CREATE_MANAGER_ORDER_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Manager_Order(
                            order_id int NOT NULL,
                            person_id int NOT NULL,
                            order_status varchar(20) NOT NULL CHECK (order_status in ('IN_CART', 'PLACED')),
                            order_date date,
                            delivery_date date,
                            shipping_status VARCHAR(255),
                            FOREIGN KEY (person_id) REFERENCES Manager(person_id),
                            PRIMARY KEY (order_id));
                        """)

DROP_MANAGER_ORDER_TABLE = text("""
                                DROP TABLE IF EXISTS Manager_Order;
                            """)

DELETE_ALL_FROM_MANAGER_ORDER = text("""
    DELETE FROM Manager_Order;
""")

                                        