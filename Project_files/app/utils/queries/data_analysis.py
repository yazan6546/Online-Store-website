from sqlalchemy import text

TOP_10_SELLING_PRODUCTS = text("""
    SELECT p.product_id, p.product_name, SUM(col.quantity) AS total_quantity_sold
    FROM Product p
    JOIN Customer_Order_Line col ON p.product_id = col.product_id
    JOIN Customer_Order co ON col.order_id = co.order_id
    WHERE co.order_status = 'PLACED'
    GROUP BY p.product_id, p.product_name
    ORDER BY total_quantity_sold DESC
    LIMIT 10;
""")


LOW_STOCK_PRODUCTS = text("""
    SELECT p.product_id, p.product_name, p.stock_quantity
    FROM Product p
    WHERE stock_quantity < 10;
""")

MONTHLY_INCOME_REPORT = text("""
    SELECT DATE_FORMAT(co.order_date, '%Y-%m') AS month, 
           SUM(col.quantity * col.price_at_time_of_order) AS tot
    FROM Customer_Order co 
    JOIN Customer_Order_Line col ON co.order_id = col.order_id
    WHERE co.order_status = 'PLACED'
    GROUP BY DATE_FORMAT(co.order_date, '%Y-%m')
    ORDER BY month DESC;
""")
