from database import get_table
from auth_service import hash_password, check_password

table = get_table()

def register_user(email, password):
    secure_hash = hash_password(password)
    
    try:
        table.put_item(
            Item={
                'email': email,
                'password_hash': secure_hash
            },
            ConditionExpression='attribute_not_exists(email)'
        )
        print(f"\nSUCCESS: User {email} registered with a hashed password.")
    except Exception:
        print("\nERROR: That email is already registered.")

def login_user(email, password):
    
    response = table.get_item(Key={'email': email})
    
    if 'Item' in response:
        stored_hash = response['Item']['password_hash']
        
        if check_password(password, stored_hash):
            print(f"\nWELCOME: Login successful for {email}!")
            return True
            
    print("\nFAILED: Invalid email or password.")
    return False

if __name__ == "__main__":
    print("--- SECURE DYNAMODB LOGIN ---")
    choice = input("1. Register\n2. Login\nChoice: ")
    u_email = input("Enter email: ").strip().lower()
    u_pass = input("Enter password: ").strip()

    if choice == '1':
        register_user(u_email, u_pass)
    elif choice == '2':
        login_user(u_email, u_pass)