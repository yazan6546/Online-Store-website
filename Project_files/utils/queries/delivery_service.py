# utils/queries/delivery_service.py

from sqlalchemy import text

# Query to get all delivery services
GET_ALL_DELIVERY_SERVICES = text("""
    SELECT * FROM DeliveryService;
""")

# Query to get a delivery service by ID
GET_DELIVERY_SERVICE_BY_ID = text("""
    SELECT * FROM DeliveryService WHERE delivery_service_id = :delivery_service_id;
""")

# Query to add a new delivery service
ADD_DELIVERY_SERVICE = text("""
    INSERT INTO DeliveryService (delivery_service_name, phone_number, email)
    VALUES (:delivery_service_name, :phone_number, :email);
""")

# Query to update an existing delivery service
UPDATE_DELIVERY_SERVICE = text("""
    UPDATE DeliveryService
    SET delivery_service_name = :delivery_service_name, phone_number = :phone_number, email = :email
    WHERE delivery_service_id = :delivery_service_id;
""")

# Query to delete a delivery service by ID
DELETE_DELIVERY_SERVICE = text("""
    DELETE FROM DeliveryService WHERE delivery_service_id = :delivery_service_id;
""")