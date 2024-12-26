from sqlalchemy import text


INSERT_PERSON_TABLE = text("""
                                INSERT INTO Person (person_id, first_name, last_name, email, passcode) 
                                VALUES (person_id, first_name, last_name, email, passcode);
                           """)

GET_PERSON_TABLE = text("""
                            SELECT * FROM Manager ORDER BY 1 DESC;
""")

SELECT_PERSON_BY_ID = text("""
                                SELECT * FROM Person
                                WHERE person_id = :id;
                            """)

DELETE_FROM_PERSON = text("""
                                DELETE FROM Person 
                                WHERE person_id = :id;
                            """)

CREATE_PERSON_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS person(
                            person_id int NOT NULL auto_increment,
                            first_name VARCHAR(255) NOT NULL,
                            last_name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL UNIQUE,
                            passcode VARCHAR(255) NOT NULL,
                            PRIMARY KEY (person_id)
                            );
                        """)

DROP_PERSON_TABLE = text("""
                                DROP TABLE IF EXISTS Person;
                            """)
