from sqlalchemy import text
from utils.db_utils import get_db_connection
import utils.queries as q

class Category:
    def __init__(self, category_id=None, category_name=None, category_description=None):
        self.category_id = category_id
        self.category_name = category_name
        self.category_description = category_description

    def insert(self):
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.INSERT_CATEGORY_TABLE, {
                'category_name': self.category_name,
                'category_description': self.category_description
            })
            conn.commit()
            self.category_id = result.lastrowid
            return 1
        except Exception as e:
            print(f"Error in insert(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()
        try:
            conn.execute(q.category.UPDATE_CATEGORY_TABLE, {
                'category_id': self.category_id,
                'category_name': self.category_name,
                'category_description': self.category_description
            })
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in update(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def delete(self):
        conn = get_db_connection()
        try:
            conn.execute(q.category.DELETE_FROM_CATEGORY, {'category_id': self.category_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in delete(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.GET_CATEGORY_TABLE).fetchall()
            categories = [Category(category_id=row['category_id'], category_name=row['category_name'], category_description=row['category_description']) for row in result]
            return categories
        except Exception as e:
            print(f"Error in get_all(): {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.SELECT_CATEGORY_BY_ID, {'category_id': category_id}).fetchone()
            if result:
                return Category(category_id=result['category_id'], category_name=result['category_name'], category_description=result['category_description'])
            return None
        except Exception as e:
            print(f"Error in get_by_id(): {e}")
            return None
        finally:
            conn.close()