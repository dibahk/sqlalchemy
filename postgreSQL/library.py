from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, select, registry, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship, F

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/red30')

mapper_registry = registry()

base = mapper_registry.generate_base()
class Book(base):
    __tablename__ = 'books directory'
    book_ID = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    page_num = Column(Integer)
    def __repr__(self):
        return "<Book(book_id={}, book_title={}, page_number={})<".format(self.book_ID, self.tile, self.page_num)
    
class Author(base):
    __tablename__ = 'author directory'
    author_ID = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    def __repr__(self):
        return "<Author(author_ID={}, first name={}, last_name={})>".format(self.author_ID, self.first_name, self.last_name)

class AuthorBook(base):
    __tablename__ = 'book author directory'
    bookauthor_ID = Column(Integer, primary_key=True)
    author_ID = Column(Integer, ForeignKey('authors.author_ID'))
    book_ID = Column(Integer, ForeignKey('books.book_ID'))
    author = relationship("Author")
    book = relationship("Book")
    
    def __repr__(self):
        return "<BookAuthor (bookauthor_ID={}, author_ID={}, book_ID={}".format(self.bookauthor_ID, self.author_ID, self.author_ID)

    
base.metadata.create_all(engine)

def add_book(title, page_num, first_name, last_name):
    author = Author(first_name=first_name, last_name=last_name)
    book = Book(title=title, page_num=page_num)
    with Session(engine) as session:
        existing_book = session.execute(select(Book).filter(Book.title==title, Book.page_num==page_num))
        if existing_book is not None:
            print('book exits no action done')
            return
        print("Book doesn't exist")
        session.add(book)
        existing_author = session.execute(select(Author).filter(Author.first_name==first_name, last_name==last_name))
        if existing_author is not None:
            print("Author exists")
            session.flush()
            pairing = AuthorBook(author_ID=existing_author.author_ID, book_ID=existing_book.book_ID)
            
        else:
            print("Author didn't exist")
            session.add(author)
            session.flush()
            pairing = AuthorBook(author_ID=author.author_ID, book_ID=book.book_ID)
        session.add(pairing)
        session.commit()
        print("new pairing added"+str(pairing))
        
with Session(engine) as session:
    # Read
    smallest_sale_query = select(Sales).order_by(Sales.order_total)
    smallest_sale = session.execute(smallest_sale_query).scalar()
    print(smallest_sale.order_total)

    # Insert
    recent_sale = Sales(order_num=1105910,cust_name='alen',prod_number='ev33',prod_name='bed',quantity=3,price=19.5,discount=0,order_total=58.5)
    session.add(recent_sale)
    session.commit()

    # update
    recent_sale.quantity = 2
    recent_sale.order_total = 39
    updated_sale = session.execute(select(Sales).filter(Sales.order_num==1105910)).scalar()
    print(updated_sale.cust_name)
    print(updated_sale.quantity)
    print(updated_sale.order_total)

    # delete
    returned_sale = session.execute(select(Sales).filter(Sales.order_num ==1105910)).scalar()
    session.delete(returned_sale)
    session.commit()
