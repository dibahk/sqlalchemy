import psycopg2

conn = psycopg2.connect(database='red30',
                        user='postgres',
                        password='123',
                        host='localhost',
                        port='5432')

cursor = conn.cursor()

sales = [ (1100935, 'spencers', 'dk204','byod-300', 2,89,0,178),
         (1100948, 'ewan','tv810','understanding automation', 1,44.95,0,44.95),
         (1100971,'stehr','ds301','da-sa702',3,399,.1,1077.3),
         (1100972,'hettinger and sons', 'ds306','da-sa702',12,250,.5,1500)]
cursor.executemany("INSERT INTO sales VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",sales)
conn.commit()
conn.close()