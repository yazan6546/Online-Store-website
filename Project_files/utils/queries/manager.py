from sqlalchemy import text


INSERT_MANAGER_TABLE = text("""
                                INSERT INTO Manager (person_id, since, role) 
                                VALUES (:person_id, :since, :role);
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
                            p.passcode AS passcode,
                            m.since AS since,
                            m.role AS role
                            FROM Manager m
                            JOIN Person p
                            on m.person_id = p.person_id;
                        """)

SELECT_MANAGER_BY_ID = text("""
                                SELECT 
                                c.person_id AS person_id,
                                p.first_name AS first_name,
                                p.last_name AS last_name,
                                p.email AS email,
                                p.passcode AS passcode,
                                c.role AS role,
                                c.since AS since
                                FROM Manager c
                                JOIN Person p
                                on c.person_id = p.person_id
                                WHERE p.person_id = :person_id;
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


UPDATE_MANAGER_TABLE = text("""
                                UPDATE Manager
                                SET since = :since,
                                role = :role
                                WHERE person_id = :person_id;
                            """)

DELETE_FROM_MANAGER = text("""
                                DELETE FROM Manager 
                                WHERE person_id = :person_id;
                            """)

CREATE_MANAGERS_TABLE = text("""
                            CREATE TABLE IF NOT EXISTS Manager(
                            person_id int NOT NULL,
                            since date ,
                            role varchar(20) not null check (role in ('Financial Manager', 'Assistant Manager', 'Regional Manager')),
                            FOREIGN KEY (person_id) REFERENCES Person(person_id),
                            PRIMARY KEY (person_id)
                            );
                        """)


SEARCH_MANAGERS = text("""
                            SELECT 
                            c.person_id AS person_id,
                            p.first_name AS first_name,
                            p.last_name AS last_name,
                            p.email AS email,
                            p.passcode AS passcode,
                            c.role AS role,
                            c.since AS since
                            FROM Manager c
                            JOIN Person p on c.person_id = p.person_id
                            WHERE p.first_name like :name or p.last_name like :name;
                        """)

DROP_MANAGERS_TABLE = text("""
                                DROP TABLE IF EXISTS Manager;
                            """)
