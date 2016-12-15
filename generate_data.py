import random
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    #Create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
        
def inserto_db(conn):
    #Generate product names from animals.txt
    lines = [line.rstrip('\n') for line in open("animals.txt")]
    try:
        c = conn.cursor()
        for i in range(0, 226):
            r1 = random.randrange(0, 226)
            r2 = random.randrange(0, 226)
            val = lines[r1] + " " + lines[r2]
            c.execute("INSERT INTO PRODUCTS (NAME) VALUES(?)", (val,))
                       
        conn.commit()

    except Error as e:
        print(e)
        
        
def create_shopping_data(conn):
    try:
        c = conn.cursor()
        for i in range(1, 10001):
            order = i
            purchases = random.randrange(0, 10)
            c.execute("INSERT INTO ORDERS (ID) VALUES(?)", (order,))
            for i in range(0, purchases):
                product = random.randrange(0, 227)
                quantity = random.randrange(1, 11)
                c.execute('''INSERT INTO ORDER_LINES (ORDER_ID, PRODUCT_ID, QUANTITY)
                            VALUES(?, ?, ?)''', (order, product, quantity))
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    

def main():
    database = "database.db"
    
    sql_create_products_table = '''CREATE TABLE IF NOT EXISTS PRODUCTS (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    NAME TEXT NOT NULL
                                    );'''

                                    
    sql_create_order_lines_table = '''CREATE TABLE IF NOT EXISTS ORDER_LINES (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ORDER_ID INTEGER NOT NULL,
                                        PRODUCT_ID INTEGER NOT NULL,
                                        QUANTITY INTEGER NOT NULL,
                                        FOREIGN KEY(ORDER_ID) REFERENCES ORDERS(ID),
                                        FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCTS(ID)
                                        );'''
    
    sql_create_orders_table = '''CREATE TABLE IF NOT EXISTS ORDERS (
                            ID INTEGER
                            );'''

                                
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_products_table)
        create_table(conn, sql_create_orders_table)
        create_table(conn, sql_create_order_lines_table)
        inserto_db(conn)
        create_shopping_data(conn)
        
    else:
        print("Error! Cannot create the database connection.")
        
        
if __name__ == "__main__": main()