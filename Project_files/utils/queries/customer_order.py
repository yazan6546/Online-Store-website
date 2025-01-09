from sqlalchemy import text

INSERT_CUSTOMER_ORDER_TABLE = text("""
                                INSERT INTO Customer_Order (person_id, order_status, address_id, delivery_service_id, order_date, delivery_date) 
                                VALUES (:person_id, :order_status, :address_id, :delivery_service_id, :order_date, :delivery_date);
                            """)

GET_CUSTOMER_ORDER_TABLE = text("""
                            SELECT 
                            order_id as order_id,
                            person_id as person_id,
                            order_status as order_status,
                            address_id as address_id,
                            delivery_service_id as delivery_service_id,
                            order_date as order_date,
                            delivery_date as delivery_date
                            FROM Customer_Order ORDER BY 1 ;
""")

SELECT_CUSTOMER_ORDER_BY_ID = text("""
                                SELECT * FROM Manager_Order
                                WHERE person_id = :id;
                            """)

GET_PRODUCTS_FROM_ORDER = text("""
                select col.product_id, col.price_at_time_of_order, col.quantity
                from Customer_Order_Line col
                where col.order_id = :order_id;
            """)

DELETE_FROM_CUSTOMER_ORDER = text("""
                                DELETE FROM Manager_Order
                                WHERE order_id = :order_id;
                            """)


UPDATE_CUSTOMER_ORDER_TABLE = text("""
                            UPDATE Customer_Order
                            SET order_status=:order_status,
                            person_id=:person_id,
                            address_id=:address_id, 
                            delivery_date=:delivery_date, 
                            order_date=:order_date
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
                                    col.quantity
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


GET_ALL_PLACED_ORDERS = text("""

                                SELECT 
                                    co.order_id,
                                    co.order_date,
                                    co.delivery_date,
                                    co.person_id,
                                    co.address_id,
                                    p.product_id,
                                    p.product_name,
                                    p.product_description,
                                    co.delivery_service_id,
                                    co.order_status,
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
                                    co.order_status = 'PLACED';
                            """)


PENDING_ORDERS = text("""
    SELECT co.order_id, co.order_date, co.delivery_date, p.first_name, p.last_name
    FROM Customer_Order co 
    JOIN Person p 
    ON co.person_id = p.person_id
    WHERE co.order_status = 'PLACED
    ORDER BY co.delivery_date;
""")

DELETE_ALL_FROM_CUSTOMER_ORDER = text("""
    DELETE FROM Customer_Order;
""")
