from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, select, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship, registry

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/library')

mapper_registry = registry()

base = mapper_registry.generate_base()
class Book(base):
    __tablename__ = 'books'
    book_ID = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    page_num = Column(Integer)
    def __repr__(self):
        return "<Book(book_id={}, book_title={}, page_number={})<".format(self.book_ID, self.tile, self.page_num)
    
class Author(base):
    __tablename__ = 'authors'
    author_ID = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    def __repr__(self):
        return "<Author(author_ID={}, first name={}, last_name={})>".format(self.author_ID, self.first_name, self.last_name)

class AuthorBook(base):
    __tablename__ = 'authorbook'
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
        existing_book = session.execute(select(Book).filter(Book.title==title, Book.page_num==page_num)).scalar()
        if existing_book is not None:
            print('book exits. No action done')
            return
        print("Book doesn't exist. Adding it")
        session.add(book)
        existing_author = session.execute(select(Author).filter(Author.first_name==first_name, last_name==last_name)).scalar()
        if existing_author is not None:
            print("Author exists")
            session.flush()
            pairing = AuthorBook(author_ID=existing_author.author_ID, book_ID=existing_book.book_ID)
            
        else:
            print("Author didn't exist. Adding it")
            session.add(author)
            session.flush()
            pairing = AuthorBook(author_ID=author.author_ID, book_ID=book.book_ID)
        session.add(pairing)
        session.commit()
        print("new pairing added"+str(pairing))

if __name__=="__main__":
    print("enter input data for book")
    title = input("what is the title of the book?\n")
    page_num = int(input("what is the number of pages of this book?\n"))
    first_name = input("what is the first name of the authot of this book?\n")
    last_name = input("what is the last name of the author of this book\n")
    add_book(title, page_num, first_name, last_name)
    print("Done")