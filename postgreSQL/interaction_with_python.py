import psycopg2

def insert_sale(cur,order_num,cust_name,prod_num,prod_name,quantity,price,discount):
    order_total = quantity * price
    if discount != 0:
        order_total = order_total*discount
    sale_data = {
        'order_num': order_num,
        'cust_name': cust_name,
        'prod_num': prod_num,
        'prod_name': prod_name,
        'quantity': quantity,
        'price': price,
        'discount': discount,
        'order_total': order_total
    }
    cur.execute('''INSERT INTO sales VALUES (%(order_num)s, %(cust_name)s, %(prod_num)s, %(prod_name)s, %(quantity)s,
                %(price)s, %(discount)s, %(order_total)s)''', sale_data)

if __name__ == '__main__':
    conn = psycopg2.connect(database='red30',
                        user='postgres',
                        password='123',
                        host='localhost',
                        port='5432')

    cursor = conn.cursor()
    print('input sale data:\n')
    order_num = int(input('what is the order number\n'))
    cust_name = input('what is the costumer name\n')
    prod_num = input('what is the product number\n')
    prod_name = input('what is the product name\n')
    quantity = float(input('how many were bought\n'))
    price = float(input('what is the price\n'))
    discount = float(input('what is the discount\n'))
    insert_sale(cursor, order_num, cust_name,prod_num,prod_name,quantity, price, discount)
    conn.commit()
    conn.close()