import mysql.connector as sql

def connect_to_database():
    try:
        conn = sql.connect(host='localhost', user="root", passwd='jeevitha', database='mv')
        if conn.is_connected():
            print("Connected successfully")
        return conn
    except sql.Error as e:
        print("Error connecting to database:", e)
        return None

def setup_tables(conn):
    try:
        cursor = conn.cursor()
        # Create regis_info table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regis_info(
                aadhar_no BIGINT PRIMARY KEY,
                name VARCHAR(25), 
                father_name VARCHAR(20),
                mother_name VARCHAR(20),
                examination_applied VARCHAR(40),
                year INT(4),
                gender VARCHAR(11),
                date_of_birth VARCHAR(10),
                nationality VARCHAR(15),
                marital_status VARCHAR(15),
                community VARCHAR(10),
                minority VARCHAR(4),
                add_1 VARCHAR(40),
                add_2 VARCHAR(40),
                add_3 VARCHAR(40),
                dist VARCHAR(20),
                state VARCHAR(20),
                pin_code INT(6),
                pho_no BIGINT,
                mobile_no BIGINT,
                e_mail VARCHAR(45),
                education_qualification VARCHAR(100),
                preference VARCHAR(10),
                p_f_cds_pabt INT(3),
                sainik_milk_sch INT(3),
                son_sainik_mil_sch INT(3)
            )
        """)
        # Create login_info table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_info(
                user VARCHAR(10) PRIMARY KEY,
                passwd VARCHAR(10)
            )
        """)
        conn.commit()
        print("Tables setup completed.")
    except sql.Error as e:
        print("Error setting up tables:", e)

# Insert login credentials
def insert_login_info(cursor, conn, user, passwd):
    try:
        cursor.execute("INSERT INTO login_info (user, passwd) VALUES (%s, %s)", (user, passwd))
        conn.commit()
        print("User registered successfully.")
    except sql.Error as e:
        print("Error inserting login info:", e)

# Authenticate user
def authenticate_user(cursor, user, passwd):
    cursor.execute("SELECT * FROM login_info WHERE user = %s AND passwd = %s", (user, passwd))
    return cursor.fetchone() is not None

# Register details
def add_registration_details(cursor, conn):
    try:
        name = input("Enter your name: ")
        father_name = input("Enter your father's name: ")
        mother_name = input("Enter your mother's name: ")
        examination_applied = input("Enter the examination applied: ")
        year = int(input("Enter the year: "))
        gender = input("Enter your gender: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        nationality = input("Enter your nationality: ")
        marital_status = input("Enter your marital status: ")
        community = input("Enter your community: ")
        minority = input("Do you belong to a minority? (Yes/No): ")
        add_1 = input("Enter address line 1: ")
        add_2 = input("Enter address line 2: ")
        add_3 = input("Enter address line 3: ")
        dist = input("Enter your district: ")
        state = input("Enter your state: ")
        pin_code = int(input("Enter your pincode: "))
        pho_no = int(input("Enter your phone number: "))
        mobile_no = int(input("Enter your mobile number: "))
        e_mail = input("Enter your email ID: ")
        education_qualification = input("Enter your educational qualification: ")
        preference = input("Enter your preference: ")
        p_f_cds_pabt = int(input("Did you fail in CPSS or PABT? (0-No, 1-Yes): "))
        sainik_milk_sch = int(input("Are you from a Sainik/Military school? (0-No, 1-Yes): "))
        son_sainik_mil_sch = int(input("Son of Military person and studying in Sainik school? (0-No, 1-Yes): "))
        aadhar_no = int(input("Enter your Aadhar number: "))

        # Insert into database
        cursor.execute("""
            INSERT INTO regis_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (aadhar_no, name, father_name, mother_name, examination_applied, year, gender, date_of_birth,
              nationality, marital_status, community, minority, add_1, add_2, add_3, dist, state, pin_code,
              pho_no, mobile_no, e_mail, education_qualification, preference, p_f_cds_pabt,
              sainik_milk_sch, son_sainik_mil_sch))
        conn.commit()
        print("Registration completed successfully.")
    except sql.Error as e:
        print("Error adding registration details:", e)

# View registration details
def view_registration_details(cursor):
    try:
        reg_no = int(input("Enter your Aadhar number to view details: "))
        cursor.execute("SELECT * FROM regis_info WHERE aadhar_no = %s", (reg_no,))
        data = cursor.fetchone()
        if data:
            print("Details:")
            for field, value in zip(cursor.column_names, data):
                print(f"{field}: {value}")
        else:
            print("No record found.")
    except sql.Error as e:
        print("Error fetching registration details:", e)

# Main function
def main():
    conn = connect_to_database()
    if conn is None:
        return
    setup_tables(conn)
    cursor = conn.cursor()

    print("Welcome to UPSC Registration System")
    while True:
        print("\n1. Register User")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = input("Enter a username: ")
            passwd = input("Enter a password: ")
            insert_login_info(cursor, conn, user, passwd)
        elif choice == '2':
            user = input("Enter your username: ")
            passwd = input("Enter your password: ")
            if authenticate_user(cursor, user, passwd):
                print("Login successful!")
                print("1. Add Registration Details")
                print("2. View Registration Details")
                print("3. Logout")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1':
                    add_registration_details(cursor, conn)
                elif sub_choice == '2':
                    view_registration_details(cursor)
                elif sub_choice == '3':
                    print("Logging out...")
                else:
                    print("Invalid choice.")
            else:
                print("Invalid username or password.")
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

    conn.close()

main()
