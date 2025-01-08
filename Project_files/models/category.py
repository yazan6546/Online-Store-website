from unicodedata import category

from sqlalchemy import text
from utils.db_utils import get_db_connection
import utils.queries as q

class Category:
    def __init__(self, category_name, category_description, category_id=None):
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

    @classmethod
    def get_all(cls):
        conn = get_db_connection()

        try:
            category_objects = []
            categories = conn.execute(q.category.GET_CATEGORY_TABLE).fetchall()
            categories = [category._mapping for category in categories]
            conn.commit()

            for category in categories:
                category_objects.append(Category(
                    **category
                ))

            return category_objects
        except Exception as e:
            print(f"Error: {e}")
            return 0

        finally:
            conn.close()


    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.SELECT_CATEGORY_BY_ID, {'category_id': category_id}).fetchone()
            result = result._mapping
            return Category(**result)
        except Exception as e:
            print(f"Error in get_by_id(): {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_id_by_name(cls, category_name):
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.GET_ID_BY_NAME, {'category_name': category_name}).fetchone()
            return result[0]
        except Exception as e:
            print(f"Error in get_id_by_name(): {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_names(cls):
        conn = get_db_connection()
        try:
            result = conn.execute(q.category.GET_CATEGORY_NAMES).fetchall()
            return [row[0] for row in result]
        except Exception as e:
            print(f"Error in get_names(): {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def delete_all():
        conn = get_db_connection()
        try:
            conn.execute(q.category.DELETE_ALL_FROM_CATEGORY)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in delete_all(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def __repr__(self):
        return f"{self.category_name} - {self.category_description}"

    def __str__(self):
        return f"{self.category_name} - {self.category_description}"

    def to_dict(self, category_id=True):

        category = {
            'category_name': self.category_name,
            'category_description': self.category_description
        }
        if category_id:
            category['category_id'] = self.category_id

        return category