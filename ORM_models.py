import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), unique=True)


stock = Table(
    'stock',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_book', Integer, ForeignKey('book.id')),
    Column('id_shop', Integer, ForeignKey('shop.id')),
    Column('count', Integer, nullable=False)
)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref="books")
    shop = relationship('Shop', secondary=stock, back_populates='book')


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)

    book = relationship('Book', secondary=stock, back_populates='shop')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    prise = sq.Column(sq.Numeric(precision=10, scale=2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(stock, backref='count')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
