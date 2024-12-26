from sqlalchemy import text


INSERT_CUSTOMERS_TABLE = text("""
                                INSERT INTO Customer (person_id) 
                                VALUES (:person_id);
                            """)

GET_CUSTOMERS_TABLE = text("""
                            SELECT * FROM customers ORDER BY 1 DESC;
""")

SELECT_CUSTOMER_BY_ID = text("""
                                SELECT * FROM Customer
                                WHERE person_id = :id;
                            """)

SELECT_CUSTOMER_BY_EMAIL = text("""
                                SELECT * FROM Customer, person
                                JOIN Person on Customer.person_id = person.id
                                WHERE email = :email;
                            """)

SELECT_PASSWORD_FROM_CUSTOMER = text("""
                                SELECT passcode FROM Customer c, Person p
                                JOIN Person on c.person_id = p.person_id
                                WHERE email = :email;
                            """)

DELETE_FROM_CUSTOMERS = text("""
                                DELETE FROM Customer 
                                WHERE perosn_id = :id;
                            """)

CREATE_CUSTOMERS_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Customer(
                            person_id int not null,
                            FOREIGN KEY (person_id) REFERENCES Person(person_id),
                            PRIMARY KEY (person_id)
                        """)

DROP_CUSTOMERS_TABLE = text("""
                                DROP TABLE IF EXISTS Customer;
                            """)
