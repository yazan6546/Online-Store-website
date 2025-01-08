from utils.db_utils import get_db_connection
import utils.queries as q

class DeliveryService:
    def __init__(self,delivery_service_name, phone_number, delivery_service_id=None):
        self.delivery_service_id = delivery_service_id
        self.delivery_service_name = delivery_service_name
        self.phone_number = phone_number

    def insert(self):
        conn = get_db_connection()
        result = None
        try:
            result = conn.execute(q.delivery_service.ADD_DELIVERY_SERVICE, self.to_dict())
            self.delivery_service_id = result.lastrowid

            conn.commit()

            if result is None:
                raise Exception("Duplicate entry")

        except Exception as e:
            print(f"Error in insert(): {e}")
            conn.rollback()
            raise e

        finally:
            conn.close()

    def to_dict(self, include_id=True):
        temp = {
            "delivery_service_name": self.delivery_service_name,
            "phone_number": self.phone_number,

        }

        if include_id:
            temp["delivery_service_id"] = self.delivery_service_id

        return temp

    @staticmethod
    def delete(delivery_service_id):
        conn = get_db_connection()

        try:
            conn.execute(q.delivery_service.DELETE_DELIVERY_SERVICE, {"delivery_service_id": delivery_service_id})

            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()

        try:
            # Check if the delivery_service_id exists
            service = conn.execute(q.delivery_service.GET_DELIVERY_SERVICE_BY_ID, {"delivery_service_id": self.delivery_service_id}).fetchone()
            if service is None:
                return 0

            # Update the delivery service if it exists
            conn.execute(q.delivery_service.UPDATE_DELIVERY_SERVICE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def delete_all():
        conn = get_db_connection()

        try:
            conn.execute(q.delivery_service.DELETE_DELIVERY_SERVICE)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def from_dict(dict):

        if dict["delivery_service_id"] is None:
            return DeliveryService(
                delivery_service_name=dict["delivery_service_name"],
                phone_number = dict["phone_number"],
            )

        return DeliveryService(
            delivery_service_id=dict["delivery_service_id"],
            delivery_service_name=dict["delivery_service_name"],
            phone_number = dict["phone_number"],

        )

    @staticmethod
    def get_all():
        conn = get_db_connection()

        try:
            services = conn.execute(q.delivery_service.GET_ALL_DELIVERY_SERVICES).fetchall()
            return [DeliveryService.from_dict(service._mapping) for service in services]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()

    def __str__(self):
        return f"DeliveryService: {self.delivery_service_name}"

    @staticmethod
    def get_by_id(delivery_service_id):
        conn = get_db_connection()

        try:
            service = conn.execute(q.delivery_service.SELECT_DELIVERY_BY_DELIVERY_ID, {"delivery_service_id": delivery_service_id}).fetchone()
            return DeliveryService.from_dict(service._mapping) if service else None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()
    @staticmethod
    def get_id_by_name(delivery_service_name):
        conn = get_db_connection()
        try:
            service = conn.execute(q.delivery_service.GET_ID_BY_NAME, {'delivery_service_name' : delivery_service_name}).fetchone()
            return service[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

