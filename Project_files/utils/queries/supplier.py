from sqlalchemy import text

INSERT_SUPPLIER_TABLE = text("""
                                INSERT INTO Supplier (supplier_name, phone_number)
                                VALUES (:name,:phone); 
                            """)

GET_SUPPLIER_TABLE = text("""
                            SELECT * FROM Supplier ORDER BY 1 ;
                            """)

SELECT_SUPPLIER_BY_SUPPLIER_ID = text("""
                                SELECT * FROM Supplier
                                WHERE supplier_id = :id;
                            """)
GET_SUPPLIER_NAME = text("""
                            SELECT supplier_name FROM Supplier
                            WHERE supplier_id = :supplier_id;
                        """)

GET_ID_BY_SUPPLIER_NAME = text("""
                            SELECT supplier_id FROM Supplier
                            WHERE supplier_name = :name;
                            """)

GET_SUPPLIER_NAMES = text("""
                            SELECT supplier_name FROM Supplier;
                        """)

UPDATE_SUPPLIER_TABLE = text("""
                                UPDATE Supplier
                                SET supplier_name = :name, phone_number = :phone
                                WHERE supplier_id = :supplier_id;
                            """)

Create_SUPPLIER_TABLE = text("""
                            CREATE TABLE Supplier (
                            supplier_id INT AUTO_INCREMENT,
                            name VARCHAR(255) NOT NULL,
                            phone VARCHAR(255) NOT NULL,
                            PRIMARY KEY (supplier_id)
                            );
                        """)

DELETE_FROM_SUPPLIER = text("""
                                DELETE FROM Supplier 
                                WHERE supplier_id = :id;
                            """)

DROP_SUPPLIER_TABLE = text("""
                                DROP TABLE IF EXISTS Supplier;
                        """)

DELETE_ALL_FROM_SUPPLIER = text("""
    DELETE FROM Supplier;
""")
