import csv

from sqlalchemy import insert

from ..database import engine
from ..models import metadata, product_category_table, product_table, basket_table


class CreateDB:
    def __init__(self):
        pass

    @staticmethod
    def create_tables():
        metadata.drop_all(bind=engine, tables=[product_category_table, product_table, basket_table])
        # metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)

    @staticmethod
    def insert_catalog_data():
        with engine.connect() as connection:

            # ADD PRODUCT CATEGORIES (CATEGORIES IS PERMANENT)
            product_categories = [
                    {'id': 1, 'category_name': '3D принтеры', 'category_type': 'Оборудование'},
                    {'id': 2, 'category_name': '3D сканеры', 'category_type': 'Оборудование'},
                    {'id': 3, 'category_name': 'Фрезерные станки', 'category_type': 'Оборудование'},
                    {'id': 4, 'category_name': 'Печи', 'category_type': 'Оборудование'},
                    {'id': 5, 'category_name': 'Фотополимеры', 'category_type': 'Материалы'},
                    {'id': 6, 'category_name': 'CAD CAM блоки', 'category_type': 'Материалы'},
                    {'id': 7, 'category_name': 'Фрезы', 'category_type': 'Материалы'},
                ]
            product_category_stmt = insert(product_category_table).values(product_categories)
            connection.execute(product_category_stmt)

            # ADD PRODUCTS (PRODUCTS IS NOT PERMANENT, CAN CHANGE IN CSV FILE)
            product_files = [
                '3D принтеры.csv',
                '3D сканеры.csv',
                'CAD CAM блоки.csv',
                'Печи.csv',
                'Фотополимеры.csv',
                'Фрезерные станки.csv',
                'Фрезы.csv',
            ]

            for file in product_files:
                with open(f'database/catalog/{file}', 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    products = [product for product in reader if product][1:]

                for product in products:
                    title = product[0].strip()
                    description = product[1].strip()
                    image_url = product[2].strip()
                    price = int(product[3])
                    site_url = product[4].strip()
                    category_id = [c['id'] for c in product_categories if c['category_name'] == file.replace('.csv', '')][0]

                    product_stmt = insert(product_table).values(title=title, description=description, image_url=image_url,
                                                                price=price, site_url=site_url, category_id=category_id)
                    connection.execute(product_stmt)

            connection.commit()
