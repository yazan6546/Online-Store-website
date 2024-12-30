from models.suppliers import Supplier

def test_supplier_class():
    print("Testing Supplier Class Functionality\n")

    # # Test insert functionality
    # print("Testing Insert:")
    # new_supplier = Supplier(name="Test Supplier", phone="123456789")
    # try:
    #     new_supplier.insert()
    #     print(f"Inserted Supplier with ID: {new_supplier.supplier_id}\n")
    # except Exception as e:
    #     print(f"Insert failed: {e}\n")

    # Test get_by_supplier_id
    print("Testing Get by Supplier ID:")
    try:
        fetched_supplier = Supplier.get_by_supplier_id(2)
        print(f"Fetched Supplier: {fetched_supplier.name}, {fetched_supplier.phone}, ID: {fetched_supplier.supplier_id}\n")
    except Exception as e:
        print(f"Get by Supplier ID failed: {e}\n")

    # Test get_all functionality
    print("Testing Get All Suppliers:")
    try:
        suppliers = Supplier.get_all()
        if suppliers:  # Check if the list is not empty
            print(f"Number of Suppliers: {len(suppliers)}")
            for supplier in suppliers:
                print(f"Supplier ID: {supplier.supplier_id}, Name: {supplier.name}, Phone: {supplier.phone}")
        else:
            print("No suppliers found.")
        print()
    except Exception as e:
        print(f"Get All Suppliers failed: {e}\n")

    # Test delete functionality
    # print("Testing Delete:")
    # try:
    #     result = Supplier.delete(new_supplier.supplier_id)
    #     if result == 1:
    #         print(f"Deleted Supplier with ID: {new_supplier.supplier_id}\n")
    #     else:
    #         print("Delete failed: Supplier not found\n")
    #
    #
    # except Exception as e:
    #     print(f"Delete failed: {e}\n")

    # Test update functionality
    print("Testing Update:")
    try:
        fetched_supplier = Supplier.get_by_supplier_id(4)
        fetched_supplier.name = "New Supplier Name"
        fetched_supplier.phone = "987654321"
        result = fetched_supplier.update()
        if result == 1:
            print(f"Updated Supplier with ID: {fetched_supplier.supplier_id}\n")
        else:
            print("Update failed: Supplier not found\n")

    except Exception as e:
        print(f"Update failed: {e}\n")


if __name__ == "__main__":
    test_supplier_class()
