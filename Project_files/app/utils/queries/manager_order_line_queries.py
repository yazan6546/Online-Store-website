from sqlalchemy import text


INSERT_MANAGER_ORDER_TABLE = text("""
                                INSERT INTO Manager_Order (orderline_id, , order_id, product_id, quantity, price_at_time_of_order) 
                                VALUES (:orderline_id, :order_id, :product_id, :quantity, :price_at_time_of_order);
                            """)

GET_MANAGER_ORDER_TABLE = text("""
                            SELECT * FROM Manager_Order_Line ORDER BY 1 DESC;
""")

SELECT_MANAGER_ORDER_Line_BY_ID = text("""
                                SELECT * FROM Manager_Order_Line
                                WHERE order_id = :order_id;
                            """)

DELETE_FROM_MANAGER_ORDER_LINE = text("""
                                DELETE FROM Manager_Order_Line
                                WHERE order_id = :order_id);
                            """)

CREATE_MANAGER_ORDER_LINE_TABLE = text("""
                            create table Manager_Order_Line(
                            order_line_id int not null,
                            product_id int not null,
                            order_id int not null,
                            price_at_time_of_order DECIMAL(10,2),
                            quantity INT NOT NULL CHECK (quantity > 0),
                            foreign key (order_id) references Manager_Order(order_id),
	                        foreign key (product_id) references Product(product_id),
                            primary key (order_line_id)
);
                        """)

DROP_MANAGER_ORDER_TABLE = text("""
                                DROP TABLE IF EXISTS Manager_Order;
                            """)
