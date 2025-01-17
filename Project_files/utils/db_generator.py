import os
import sys

sys.path.append(
    os.path.abspath(
    os.path.join(
    os.path.dirname(__file__), '..')))

import pandas as pd
from models.manager import Manager
from models.customers import Customer
from utils.db_utils import get_db_connection, reset_db




def read_csv_to_objects(file_path, model_class:Customer| Manager):
    df = pd.read_csv(file_path)
    objects = []
    for _, row in df.iterrows():
        print(row.to_dict())

        if model_class == Customer:
            birth_date = pd.to_datetime(row['birth_date'])
            row.drop('birth_date', inplace=True)
            obj = model_class(**row.to_dict(), birth_date=birth_date, hash=True)

        else:
            obj = model_class(**row.to_dict(), hash=True)

        objects.append(obj)
    return objects


def save_objects_to_db(objects):
    for obj in objects:
        obj.insert()

    print(f"Successfully saved {len(objects)} objects to the database.")



def import_data_and_save_to_db(csv_file_path, table_name, engine):
    """
    Reads data from a CSV file into a Pandas DataFrame and inserts it into a specified database table.

    Parameters:
        csv_file_path (str): The path to the CSV file containing the data.
        table_name (str): The name of the database table where the data needs to be inserted.


    """
    try:
        # Step 1: Read data into a Pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Step 2: Save the DataFrame into the specified database table
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',  # Append to the table if it already exists
            index=False  # Do not save the DataFrame index as a column
        )

        print(f"Data from {csv_file_path} successfully inserted into the table '{table_name}'.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")


if __name__ == "__main__":

    reset_db()

    customer_objects = read_csv_to_objects('csv_files/Manager.csv', Manager)
    save_objects_to_db(customer_objects)

    length = len(customer_objects)

    customer_objects = read_csv_to_objects('csv_files/Customer.csv', Customer)
    save_objects_to_db(customer_objects)

    conn = get_db_connection()
    # Hardcoded mapping between CSV file paths and table names
    csv_table_mapping = {
        "csv_files/Address.csv": "Address",
        "csv_files/DeliveryService.csv": "DeliveryService",
        "csv_files/Category.csv": "Category",
        "csv_files/Supplier.csv": "Supplier",
        "csv_files/Product.csv": "Product",
        "csv_files/CustomerOrder.csv": "Customer_Order",
        "csv_files/CustomerOrderLine.csv": "Customer_Order_Line",
        "csv_files/ManagerOrder.csv": "Manager_Order",
        "csv_files/ManagerOrderLine.csv": "Manager_Order_Line",
    }

    # Call the function for each CSV file and corresponding table
    for file_path, table_name in csv_table_mapping.items():
        import_data_and_save_to_db(file_path, table_name, conn)

    conn.close()
