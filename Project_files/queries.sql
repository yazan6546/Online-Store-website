# Top 10 selling products
SELECT p.product_id, p.product_name, SUM(col.quantity) AS total_quantity_sold
FROM Product p
JOIN Customer_Order_Line col ON p.product_id = col.product_id
JOIN Customer_Order co ON col.order_id = co.order_id
WHERE co.order_status = 'PLACED'
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 10;

# Pending orders

SELECT co.order_id, co.order_date,co.delivery_date,co.shipping_status,p.first_name,p.last_name
FROM Customer_Order co JOIN Person p ON co.person_id = p.person_id
WHERE co.shipping_status = 'Shipped'
ORDER BY co.delivery_date;


# products with the least quantities

SELECT p.product_id, p.product_name,p.stock_quantity 
FROM Product p
WHERE stock_quantity < 10;


# monthly income report

SELECT DATE_FORMAT(co.order_date, '%Y-%m') AS month, SUM(col.quantity * col.price_at_time_of_order) AS tot
FROM Customer_Order co JOIN Customer_Order_Line col ON co.order_id = col.order_id
WHERE co.order_status = 'PLACED'
GROUP BY DATE_FORMAT(co.order_date, '%Y-%m')
ORDER BY month DESC;

