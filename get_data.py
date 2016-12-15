import sqlite3
from sqlite3 import Error
import operator

def create_connection(db_file):
    #Create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def get_input(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM PRODUCTS;")
    products = c.fetchall()
    productsl = len(products)
    print("Welcome to our Genetically Engineered Animals Catalog \nHere you can see our Products and related Products \n")
    print("ID Name")
    for i in products:
        print(i[0], i[1])
    print("\n")
    while True:
        try:
            productid = input("Please insert Product ID for related products, 0 for Catalog or exit to close: ")
            print("\n")
            
            if productid == "exit" :
                conn.close()
                break
            
            else: 
                productid = int(productid)
                
            #Check if the ID is in range of Products
            if productid > productsl:
                print("ID must be between 1 and", productsl, "\n")
                continue
                
            c.execute("SELECT ID FROM ORDER_LINES WHERE PRODUCT_ID=(?);", (productid,))
            isbought = c.fetchall()
            
            
        except ValueError:
            print("Sorry, I didn't understand that. ID must be between 1 and", productsl, "\n")
            continue
        
        #Print out Catalog
        if productid == 0 :
            print("id Name")
            for i in products:
                print(i[0], i[1])
            print("\n")
             
        elif productid <= productsl:
            get_data_from_db(conn, productid, isbought)
            
                 
def get_data_from_db(conn, productid, isbought):
    c = conn.cursor()
    products_list = []
    product_frequency = {}
      
    #What order has this product
    c.execute("SELECT ORDER_ID FROM ORDER_LINES WHERE PRODUCT_ID=(?);", (productid,))
    orders = c.fetchall()
    ordersl= len(orders)
    
    #Check if item has been bought
    if not isbought:
        print("This item has not been bought yet! \n")
        
    else:
        #Get product name for input id  
        c.execute("SELECT NAME FROM PRODUCTS WHERE ID=(?);", (productid,))
        product_name = c.fetchall()
        print("Related products for",product_name[0][0],"\n")
        
        
        #Get Product ids for order
        for i in range(ordersl):
            c.execute("SELECT PRODUCT_ID FROM ORDER_LINES WHERE ORDER_ID=(?);", (orders[i][0],))
            products = c.fetchall()
            productsl = len(products)
            for i in range(productsl):
                if productid != products[i][0]:
                    products_list.append(products[i][0])
                    
        products_listl = len(products_list)
        
        #Count products
        for i in range(products_listl):
            frequency = products_list.count(products_list[i]) 
            product_frequency[products_list[i]] = frequency;
            
        sorted_product_frequency = sorted(product_frequency.items(), key=operator.itemgetter(1))
        
        #Get related products and display top 5
        for i in range(1,6):
            c.execute("SELECT NAME FROM PRODUCTS WHERE ID=(?);", (sorted_product_frequency[-i][0],))
            top5_related_products = c.fetchall()
            if not top5_related_products:
                print("")
            else:
                c.execute("SELECT ID FROM PRODUCTS WHERE NAME=(?);", (top5_related_products[0][0],))
                poid = c.fetchall()
                print(top5_related_products[0][0],"ID", poid[0][0])
        print("\n")


def main():
    database = "database.db"
    
                                
    conn = create_connection(database)
    if conn is not None:
        get_input(conn)
               
    else:
        print("Error! Cannot create the database connection.")
        
        
if __name__ == "__main__": main()
