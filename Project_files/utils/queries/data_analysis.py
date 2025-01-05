from sqlalchemy import text

TOP_10_SELLING_PRODUCTS = text("""
    SELECT p.product_id, p.product_name, c.category_name, s.supplier_name, p.price, SUM(col.quantity) AS total_quantity_sold
    FROM Product p
    JOIN Customer_Order_Line col ON p.product_id = col.product_id
    JOIN Customer_Order co ON col.order_id = co.order_id
    JOIN Category c ON p.category_id = c.category_id
    JOIN Supplier s ON p.supplier_id = s.supplier_id
    WHERE co.order_status = 'COMPLETED'
    GROUP BY p.product_id, p.product_name
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
    WHERE co.order_status = 'COMPLETED'
    GROUP BY DATE_FORMAT(co.order_date, '%Y-%m')
    ORDER BY month DESC;
""")

CATEGORY_COUNT = text("""SELECT 
    c.category_name,
    SUM(col.quantity) AS total_quantity_sold
FROM 
    Category c
JOIN 
    Product p ON c.category_id = p.category_id
JOIN 
    Customer_Order_Line col ON p.product_id = col.product_id
JOIN 
    Customer_Order co ON col.order_id = co.order_id
WHERE 
    co.order_status = 'COMPLETED'
GROUP BY 
    c.category_name
ORDER BY 
    total_quantity_sold DESC;
""")


yearly_revenue = text("""
SELECT
    DATE_FORMAT(co.order_date, '%Y-%m') AS month,
    SUM(col.price_at_time_of_order * col.quantity) AS total_revenue
FROM
    Customer_Order co
JOIN
    Customer_Order_Line col ON co.order_id = col.order_id
WHERE
    YEAR(co.order_date) = :year AND co.order_status = 'COMPLETED'
GROUP BY
    month
ORDER BY
    month;
    """)


all_revenues = text("""
    SELECT
        YEAR(co.order_date) AS year,
        MONTH(co.order_date) AS month,
        SUM(col.price_at_time_of_order * col.quantity) AS total_revenue
    FROM
        Customer_Order co
    JOIN
        Customer_Order_Line col ON co.order_id = col.order_id
    WHERE
        co.order_status = 'COMPLETED'
    GROUP BY
        YEAR(co.order_date), MONTH(co.order_date)
    ORDER BY
        year, month;
    """)


best_customers = text("""
SELECT
    p.first_name,
    p.last_name,
    SUM(col.price_at_time_of_order * col.quantity) AS total_paid
FROM
    Customer_Order co
JOIN
    Customer_Order_Line col ON co.order_id = col.order_id
JOIN
    Customer c ON co.person_id = c.person_id
JOIN
    Person p ON c.person_id = p.person_id
WHERE
    co.order_status = 'COMPLETED'
GROUP BY
    p.first_name, p.last_name
ORDER BY
    total_paid DESC
LIMIT 10;
""")

customer_demographics = text("""
SELECT
    a.city,
    COUNT(c.person_id) AS customer_count
FROM
    Customer c
JOIN
    Address a ON c.person_id = a.person_id
GROUP BY
    a.city
ORDER BY
    customer_count DESC;
""")


best_selling_product_by_month = text("""
SELECT
    month,
    product_name,
    total_quantity_sold
FROM (
    SELECT
        DATE_FORMAT(co.order_date, '%%Y-%%m') AS month,
        p.product_name,
        SUM(col.quantity) AS total_quantity_sold,
        ROW_NUMBER() OVER (PARTITION BY DATE_FORMAT(co.order_date, '%%Y-%%m') ORDER BY SUM(col.quantity) DESC) AS rn
    FROM
        Customer_Order co
    JOIN
        Customer_Order_Line col ON co.order_id = col.order_id
    JOIN
        Product p ON col.product_id = p.product_id
    WHERE
        co.order_status = 'COMPLETED' AND YEAR(co.order_date) = %(year)s
    GROUP BY
        month, p.product_name
) subquery
WHERE rn = 1
ORDER BY month;
""")


COUNT_CUSTOMERS = text("""
    SELECT COUNT(*) FROM Customer;
""")
COUNT_ORDERS = text("""
    SELECT COUNT(*) FROM Customer_Order
    WHERE order_status = 'COMPLETED';
""")
COUNT_PRODUCTS = text("""
    SELECT COUNT(*) FROM Product;
""")

TOTAL_REVENUE = text("""
    SELECT SUM(price_at_time_of_order * quantity) AS total_revenue
    FROM Customer_Order_Line
    JOIN Customer_Order ON Customer_Order.order_id = Customer_Order_Line.order_id
    WHERE order_status = 'COMPLETED';
""")

CUSTOMER_RECENT_ORDERS = text("""
        SELECT 
            co.order_id,
            p.first_name,
            p.last_name,
            co.order_date,
            co.delivery_date,
            co.order_status
        FROM 
            Customer_Order co
        JOIN 
            Customer c ON co.person_id = c.person_id
        JOIN 
            Person p ON c.person_id = p.person_id
        WHERE 
            co.order_status = 'COMPLETED'
        ORDER BY 
            co.order_date DESC
        LIMIT 5;
""")



