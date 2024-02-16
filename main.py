import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

LOGIN = 'postgres'
PASSWORD = 'admin'
NAME_SERVER = 'localhost'
PORT_SERVER = 5432
NAME_DB = 'netology_db'
DSN = f'postgresql://{LOGIN}:{PASSWORD}@{NAME_SERVER}:{PORT_SERVER}/{NAME_DB}'

engine = sqlalchemy.create_engine(DSN)


def create_objects(session):
    pushkin = Publisher(name='Pushkin')
    lermantov = Publisher(name='Lermantov')
    session.add_all([pushkin, lermantov])
    session.commit()

    kapitanskaya_dochka = Book(name='Kapitanskaya_dochka', publisher=pushkin)
    ruslan_i_lyudmila = Book(name='Ruslan_i_Lyudmila', publisher=pushkin)
    mcyri = Book(name='Mcyri', publisher=lermantov)
    session.add_all([kapitanskaya_dochka, ruslan_i_lyudmila, mcyri])
    session.commit()

    labirint = Shop(name='Labirint')
    bukvoed = Shop(name='Bukvoed')
    session.add_all([labirint, bukvoed])
    session.commit()

    stock_kapitanskaya_dochka = Stock(book=kapitanskaya_dochka, shop=labirint, count=30)
    stock_ruslan_i_lyudmila = Stock(book=ruslan_i_lyudmila, shop=bukvoed, count=20)
    stock_mcyri = Stock(book=mcyri, shop=bukvoed, count=25)
    session.add_all([stock_kapitanskaya_dochka, stock_ruslan_i_lyudmila, stock_mcyri])
    session.commit()

    sale_kapitanskaya_dochka = Sale(price=200.45, date_sale='09-11-2022', stock=stock_kapitanskaya_dochka, count=1)
    sale_ruslan_i_lyudmila = Sale(price=250.0, date_sale='10-11-2022', stock=stock_ruslan_i_lyudmila, count=3)
    session.add_all([sale_kapitanskaya_dochka, sale_ruslan_i_lyudmila])
    session.commit()


def get_purchases(session, publisher):
    query = session.query(Book.name, Shop.name, Sale.price, Sale.date_sale). \
        join(Publisher, Publisher.id == Book.id_publisher). \
        join(Stock, Stock.id_book == Book.id). \
        join(Shop, Shop.id == Stock.id_shop). \
        join(Sale, Sale.id_stock == Stock.id)
    if publisher.isdigit():
        results = query.filter(Publisher.id == publisher).all()
    else:
        results = query.filter(Publisher.name == publisher).all()

    for book_name, shop_name, price, date_sale in results:
        print(f'{book_name} | {shop_name} | {price} | {date_sale}')


if __name__ == "__main__":
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    # создание объектов
    create_objects(session)

    # извлечение данных
    publisher = input("Enter the publisher's last name or publisher's id: ")
    get_purchases(session, publisher)

    # закрытие сессии
    session.close()
