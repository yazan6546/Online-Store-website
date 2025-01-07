from models.products import Product

def test_product_class():
    # print("=== Testing Product Class ===")
    #
    # Step 1: Insert a new product
    print("\nTesting Product Insertion...")
    new_product = Product(
        product_name="Test Product 3",
        product_description="A sample product for testing.",
        brand="Test Brand",
        price=100,
        photo="product.jpg",
        stock_quantity=50,
        category_id=1,
        supplier_id=1
    )

    try:
        new_product.insert()
        print(f"Product inserted successfully with ID: {new_product.product_id}")
    except Exception as e:
        print(f"Error inserting product: {e}")

    # Step 2: Fetch the product by ID
    # print("\nTesting Fetch by Product ID...")
    # fetched_product = Product.get_by_product_id(3)
    # if fetched_product:
    #     print(f"Fetched Product: {fetched_product}")
    # else:
    #     print("Failed to fetch product.")



    # # Step 3: Update the product
    # print("\nTesting Product Update...")
    # new_product.price = 159.8  # Update the price
    # try:
    #     update_result = new_product.update()
    #     if update_result:
    #         print("Product updated successfully.")
    #     else:
    #         print("Failed to update product.")
    # except Exception as e:
    #     print(f"Error updating product: {e}")

    # Step 4: Fetch all products
    # print("\nTesting Fetch All Products...")
    # all_products = Product.get_all()
    # if all_products:
    #     print(f"Total Products: {len(all_products)}")
    #     for product in all_products:
    #         print(product)
    # else:
    #     print("Failed to fetch products.")

    # Step 5: Delete the product
    # print("\nTesting Product Deletion...")
    # try:
    #     delete_result = Product.delete(7)
    #     if delete_result:
    #         print("Product deleted successfully.")
    #     else:
    #         print("Failed to delete product.")
    # except Exception as e:
    #     print(f"Error deleting product: {e}")

    # # Step 6: Verify Deletion
    # print("\nVerifying Product Deletion...")
    # deleted_product = Product.get_by_product_id(new_product.product_id)
    # if not deleted_product:
    #     print("Product deletion verified.")
    # else:
    #     print("Product still exists after deletion.")

if __name__ == "__main__":
    test_product_class()
