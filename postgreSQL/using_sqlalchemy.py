from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, select

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/red30')

metadata = MetaData()

sales_table = Table('sales', metadata, autoload_with= engine)
metadata.create_all(engine)

with engine.connect() as conn:
    # Read
    for row in conn.execute(select(sales_table)):
        print(row)
    # Create
    insert_instrument = sales_table.insert().values(order_num=1105910,
                                                    cust_name='alen',
                                                    prod_number='ev33',
                                                    prod_name='bed',
                                                    quantity=3,
                                                    price=19.5,
                                                    discount=0,
                                                    order_total=58.5)
    
    conn.execute(insert_instrument)

    # update
    update_statement =  sales_table.update().where(sales_table.c.order_num==1105910).values(cust_name='alec')
    conn.execute(update_statement)

    # confirm the update
    reselect_statement = sales_table.select().where(sales_table.c.order_num==1105910)
    updated_sale = conn.execute(reselect_statement).first()
    print(updated_sale)
    # delete
    delete_statement = sales_table.delete().where(sales_table.c.order_num==1105910)
    conn.execute(delete_statement)

    # confirm delete
    not_found_set = conn.execute(reselect_statement)
    print(not_found_set.rowcount)
