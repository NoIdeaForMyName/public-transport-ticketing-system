import database_communication

response, success = database_communication.check_balance("12345")

print(f"Response: {response}, Success: {success}")