import utils.password_manager as pm
from models.customers import Customer

# import bcrypt
#
#
# class PasswordManager:
#     """
#     A reusable class for hashing and verifying passwords.
#     """
#
#     def hash_password(self, plain_password):
#         """
#         Hashes the given plain text password.
#         """
#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
#         return hashed_password.decode('utf-8')
#
#     def verify_password(self, plain_password, hashed_password):
#         """
#         Verifies if the given plain text password matches the hashed password.
#         """
#         return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
#
#
# # Example usage
# if __name__ == "__main__":
#     password_manager = PasswordManager()
#
#     # Hash a password
#     password_to_store = password_manager.hash_password("securepassword1233")
#     print("Hashed Password:", password_to_store)
#
#     # Verify the password
#     is_password_correct = password_manager.verify_password("securepassword123", password_to_store)
#     print("Password is correct:", is_password_correct)


user1 = Customer.get_by_email("minifoldrat88@gmail.com")
print(user1.passcode)

print("Test PUSH")