import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ORM_models import create_tables, Publisher, Stock, Shop, Sale, Book

DSN = 'postgresql://postgres:123@localhost:5432/bookstore_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as ft:
    data = json.load(ft)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


publisher_name_or_id = input('Введите имя или идентификатор издателя: ')
sales = session.query(Sale).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_name_or_id).all()

for sale in sales:
    print(f"Книга: {sale.stock.book.title} | Магазин: {sale.stock.shop.name} | "
          f"Цена: {sale.price} | Дата продажи: {sale.date_sale}")

session.close()
