# utils.py

# Global variables to store user details
username = None
user_id = None

def set_user_details(name, uid):
    """
    Sets the global user details after successful login.
    """
    global username, user_id
    username = name
    user_id = uid
    print(f"User details set in the utils: {username}, {user_id}")
