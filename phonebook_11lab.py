import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="phonebook_11lab_db", 
            user="postgres", 
            password="arai_olzhas", 
            host="localhost", 
            port="5433"
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None

def create_table():
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS phonebook (
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR(100),
                            last_name VARCHAR(100),
                            phone VARCHAR(20) UNIQUE
                        )''')
        conn.commit()
        print("Table created successfully.")
        cur.close()
        conn.close()

def insert_or_update_user(fname, lname, phone):
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL insert_or_update_user(%s, %s, %s)", (fname, lname, phone))
        conn.commit()
        print(f"User {fname} {lname} inserted/updated successfully.")
        cur.close()
        conn.close()

def insert_many_users(names, surnames, phones):
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL insert_many_users(%s, %s, %s)", (names, surnames, phones))
        conn.commit()
        print("Users inserted/updated successfully.")
        cur.close()
        conn.close()

def search_phonebook(pattern):
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()

def get_paginated(limit, offset):
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()

def delete_by_name_or_phone(query):
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL delete_by_name_or_phone(%s)", (query,))
        conn.commit()
        print(f"Deleted records with query: {query}")
        cur.close()
        conn.close()

def main():
    while True:
        print("\nPhonebook Menu:")
        print("1. Insert or Update User")
        print("2. Insert Multiple Users")
        print("3. Search Phonebook")
        print("4. Get Paginated Data")
        print("5. Delete User by Name or Phone")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            phone = input("Enter phone number: ")
            insert_or_update_user(fname, lname, phone)
        
        elif choice == '2':
            names = input("Enter names (comma separated): ").split(',')
            surnames = input("Enter surnames (comma separated): ").split(',')
            phones = input("Enter phones (comma separated): ").split(',')
            insert_many_users(names, surnames, phones)
        
        elif choice == '3':
            pattern = input("Enter pattern to search: ")
            search_phonebook(pattern)
        
        elif choice == '4':
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            get_paginated(limit, offset)
        
        elif choice == '5':
            query = input("Enter name or phone to delete: ")
            delete_by_name_or_phone(query)
        
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()