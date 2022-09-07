from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, select, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

association_table = Table(
    'association_table', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    author = Column(String(30), nullable=False)
    reviews = relationship('Reviews', backref='book', lazy=True)
    readers = relationship('User', secondary=association_table, back_populates='books', lazy=True)

    def __repr__(self):
        return self.title

class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String(2000), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'От {self.reviewer}'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    reviews = relationship('Reviews', backref='reviewer', lazy=True)
    books = relationship('Book', secondary=association_table, back_populates='readers', lazy=True)

    def __repr__(self):
        return self.name



engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
'''session.add(Book(title='Робинзон Крузо', author='Даниэль Дэфо')) # Создаём книгу 1
session.add(Book(title='Путешествие к центру земли', author='Жуль Верн')) # Создаём книгу 2
session.add(User(name='user1')) # Пользователь 1
session.add(User(name='user2')) # Пользователь 2
session.add(Reviews(text='Замечатьльный роман о приключениях Робинзона', book_id=1, user_id=1)) # Отзыв о книге 1 от пользователя 1
session.add(Reviews(text='Замечатьльный роман о путешествии к центру земли', book_id=2, user_id=2)) # Отзыв о книге 2 от пользователя 2
session.add(Reviews(text='Мне не понравилось', book_id=1, user_id=2)) # Отзыв о книге 1 от пользователя 2
session.commit()'''
stmt = select(Book).where(Book.title == 'Робинзон Крузо')
for book in session.scalars(stmt):
    book.readers = User.id