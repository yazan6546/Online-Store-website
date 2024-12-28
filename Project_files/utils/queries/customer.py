from sqlalchemy import text

INSERT_CUSTOMERS_TABLE = text("""
                                INSERT INTO Customer (person_id) 
                                VALUES (:person_id);
                            """)

GET_ALL_CUSTOMERS = text("""
                            SELECT
                            c.person_id AS person_id,
                            p.first_name AS first_name,
                            p.last_name AS last_name,
                            p.email AS email,
                            p.passcode AS passcode
                            FROM Customer c
                            JOIN Person p
                            on c.person_id = p.person_id;
                        """)

SELECT_CUSTOMER_BY_ID = text("""
                                SELECT 
                                c.person_id AS person_id,
                                p.first_name AS first_name,
                                p.last_name AS last_name,
                                p.email AS email,
                                p.passcode AS passcode
                                FROM Customer c
                                JOIN Person p
                                on c.person_id = p.person_id
                                WHERE p.person_id = :person_id;
                            """)

SELECT_CUSTOMER_BY_EMAIL = text("""
                                SELECT 
                                c.person_id AS person_id,
                                p.first_name AS first_name,
                                p.last_name AS last_name,
                                p.email AS email,
                                p.passcode AS passcode
                                FROM Customer c
                                JOIN Person p
                                on c.person_id = p.person_id
                                WHERE p.email = :email;
                            """)

SELECT_PASSWORD_FROM_CUSTOMER = text("""
                                SELECT p.passcode FROM Customer c
                                JOIN Person p 
                                on c.person_id = p.person_id
                                WHERE p.email = :email;
                            """)

DELETE_FROM_CUSTOMERS = text("""
                                DELETE FROM Customer c 
                                WHERE c.person_id = :person_id;
                            """)

CREATE_CUSTOMERS_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Customer(
                            person_id int not null,
                            FOREIGN KEY (person_id) REFERENCES Person(person_id),
                            PRIMARY KEY (person_id));
                        """)

DROP_CUSTOMERS_TABLE = text("""
                            DROP TABLE IF EXISTS Customer;
                            """)
