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

if __name__ == "__main__":
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    # создание объектов
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

    sale_kapitanskaya_dochka = Sale(price=200.45, data_sale='09-11-2022', stock=stock_kapitanskaya_dochka, count=1)
    sale_ruslan_i_lyudmila = Sale(price=250.0, data_sale='10-11-2022', stock=stock_ruslan_i_lyudmila, count=3)
    session.add_all([sale_kapitanskaya_dochka, sale_ruslan_i_lyudmila])
    session.commit()

    # извлечение данных
    publisher = input("Введите фамилию автора: ")
    for c in session.query(Publisher, Book, Stock, Sale). \
            filter(Publisher.id == Book.id_publisher). \
            filter(Book.id == Stock.id_book). \
            filter(Stock.id == Sale.id_stock). \
            filter(Publisher.name == publisher).all():
        publisher, book, stock, sale = c
        result = f'{book.name} | {stock.shop.name} | ' \
                 f'{sale.price} | {sale.data_sale}'
        print(result)

    session.close()
