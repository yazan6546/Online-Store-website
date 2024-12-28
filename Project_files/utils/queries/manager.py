from sqlalchemy import text


INSERT_MANAGER_TABLE = text("""
                                INSERT INTO Manager (person_id, since) 
                                VALUES (:person_id, :since);
                            """)

GET_MANAGER_TABLE = text("""
                            SELECT * FROM Manager ORDER BY 1 DESC;
""")

GET_ALL_MANAGERS = text("""
                            SELECT
                            m.person_id AS person_id,
                            p.first_name AS first_name,
                            p.last_name AS last_name,
                            p.email AS email,
                            p.passcode AS passcode
                            FROM Manager m
                            JOIN Person p
                            on m.person_id = p.person_id;
                        """)

SELECT_MANAGER_BY_ID = text("""
                                SELECT * FROM Manager
                                WHERE person_id = :id;
                            """)

SELECT_MANAGER_BY_EMAIL = text("""
                                SELECT 
                                m.person_id AS person_id,
                                p.first_name AS first_name,
                                p.last_name AS last_name,
                                p.email AS email,
                                m.since AS since,
                                p.passcode AS passcode
                                FROM Manager m
                                JOIN Person p
                                 on m.person_id = p.person_id
                                WHERE p.email = :email;
                            """)

SELECT_PASSWORD_FROM_MANAGERS = text("""
                                SELECT p.passcode FROM Manager m, Person p
                                JOIN Person on m.person_id = p.person_id
                                WHERE p.email = :email;
                            """)

DELETE_FROM_MANAGERS = text("""
                                DELETE FROM Manager 
                                WHERE person_id = :id;
                            """)

CREATE_MANAGERS_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Manager(
                            person_id int NOT NULL,
                            since date ,
                            FOREIGN KEY (person_id) REFERENCES Person(person_id),
                            PRIMARY KEY (person_id)
                            );
                        """)

DROP_MANAGERS_TABLE = text("""
                                DROP TABLE IF EXISTS Manager;
                            """)
