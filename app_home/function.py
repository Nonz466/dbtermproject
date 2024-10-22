import sqlite3


con = sqlite3.connect('stockdb.db')
cursur = con.cursor()
def insert():
    print("INSERT")
    try :
        input_id = input('product id:')
        input_title = input('product name')
        input_unit = input('unit:')
        input_amount = float(input('amount:'))
        insert_sql = '''INSERT INTO products2 (product_id, product_name,unit_id, amount)
                        VALUES("{0}","{1}","{2}","{3}")'''.format(input_id,input_title,input_amount)
        cursur.execute(insert_sql)
        con.commit()
    except Exception :
        print("Error inserting")
    return input_unit

def search():
    user_input = input('Search:')
    try:
        int(user_input)
        search_sql = '''SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                        FROM products2 as p
                        LEFT JOIN status as st 
                        ON p.status_id = st.id
                        LEFT JOIN unit_table as u 
                        ON p.unit_id = u.id
                        WHERE p.product_id LIKE "%{0}%"
                        '''.format(user_input)
        
    except :
        search_sql = '''SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                        FROM products2 as p
                        LEFT JOIN status as st 
                        ON p.status_id = st.id
                        LEFT JOIN unit_table as u 
                        ON p.unit_id = u.id
                        WHERE p.product_name LIKE "%{0}%"
                        '''.format(user_input)

    cursur.execute(search_sql)
    result = cursur.fetchall()
    for n in range(len(result)):
        print(result[n])
       
def showdb():
    db = '''SELECT * 
            FROM products2; '''
    cursur.execute(db)
    product_table = cursur.fetchall()
    print(product_table)