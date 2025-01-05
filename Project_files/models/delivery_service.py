from utils.db_utils import get_db_connection
import utils.queries as q

class DeliveryService:
    def __init__(self, delivery_service_id, delivery_service_name, phone_number, email):
        self.delivery_service_id = delivery_service_id
        self.delivery_service_name = delivery_service_name
        self.phone_number = phone_number

    def insert(self):
        conn = get_db_connection()

        try:
            conn.execute(q.delivery_service.ADD_DELIVERY_SERVICE, self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
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

    def delete(self):
        conn = get_db_connection()

        try:
            conn.execute(q.delivery_service.DELETE_DELIVERY_SERVICE, {"delivery_service_id": self.delivery_service_id})
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
        return DeliveryService(
            dict["delivery_service_id"],
            dict["delivery_service_name"],
            dict["phone_number"],
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