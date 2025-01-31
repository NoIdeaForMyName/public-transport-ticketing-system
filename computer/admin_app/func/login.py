from config import ADMIN_PASS

def check_login(username, password):
    if username == ADMIN_PASS["login"] and password == ADMIN_PASS["password"]:
        return True
    return False