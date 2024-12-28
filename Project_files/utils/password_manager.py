import bcrypt


def hash_password(plain_password):
    """
    Hashes the given plain text password with a salt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password, hashed_password):
    """
    Verifies if the given plain text password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
