import sqlite3

MASTER_PASSWORD="123456"

SQLITE_DB_FILE="passwords.db"

pwd = raw_input("Insert your master password: ")

if pwd != MASTER_PASSWORD:
    print("Wrong password! Finishing...")
    exit()
else:
    print("continue...")

conn = sqlite3.connect(SQLITE_DB_FILE)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

def menu():
    print("");
    print("*******************************************")
    print("* i : insert new password")
    print("* l : list recorded services")
    print("* r : recover a password")
    print("* e : exit")
    print("*******************************************")

def get_password(service):
    cursor.execute('''
        SELECT username, password FROM users WHERE service=?
    ''',
    (service,)
    )
    if cursor.rowcount == 0:
        print("Service not found. (use 'l' for list services).")
    else:
        data = cursor.fetchall()
        for row in data:
            print(row)

def insert_password(service, username, password):
    cursor.execute('''
        INSERT INTO users (service, username, password)
        VALUES (?,?,?);
    ''',
    (service, username, password)
    )
    conn.commit()

def show_services():
    cursor.execute('''
        SELECT service from users;
    ''')
    for service in cursor.fetchall():
        print(service)

while True:
    menu()
    op = raw_input("What do you want to do? ")
    print(op)
    if op not in ['l','i','r','e']:
        print("Invalid option!")
        continue

    if op == 'l':
        show_services()

    if op == 'e':
        break

    if op == 'i':
        service = raw_input("What is the name of the service? ")
        username = raw_input("What is the name of user? ")
        password = raw_input("What is the password?")
        insert_password(service, username, password)

    if op == 'r':
        service = raw_input("What service do you want the password for? ")
        print("")
        get_password(service)

conn.close()
