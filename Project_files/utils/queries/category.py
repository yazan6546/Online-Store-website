from sqlalchemy import text

INSERT_CATEGORY_TABLE = text("""
    INSERT INTO Category (category_name, category_description) 
    VALUES (:category_name, :category_description);
""")

GET_CATEGORY_TABLE = text("""
    SELECT * FROM Category ORDER BY category_id DESC;
""")

SELECT_CATEGORY_BY_ID = text("""
    SELECT * FROM Category
    WHERE category_id = :category_id;
""")

DELETE_FROM_CATEGORY = text("""
    DELETE FROM Category
    WHERE category_id = :category_id;
""")

UPDATE_CATEGORY_TABLE = text("""
    UPDATE Category
    SET category_name = :category_name,
        category_description = :category_description
    WHERE category_id = :category_id;
""")

CREATE_CATEGORY_TABLE = text("""
    CREATE TABLE IF NOT EXISTS Category(
        category_id INT NOT NULL AUTO_INCREMENT,
        category_name VARCHAR(20) NOT NULL,
        category_description VARCHAR(255),
        PRIMARY KEY (category_id)
    );
""")

DROP_CATEGORY_TABLE = text("""
    DROP TABLE IF EXISTS Category;
""")