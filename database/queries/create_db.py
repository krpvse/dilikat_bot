from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from ..database import engine
from ..models import metadata, product_category_table, product_table, basket_table
from ..catalog import product_categories, get_products_from_csv


class CreateDB:
    def __init__(self):
        pass

    @staticmethod
    def create_tables():
        metadata.create_all(bind=engine)

    @staticmethod
    def update_catalog_data():
        """Function compares catalog in database and catalog in csv-files. If changes exists then updates"""

        print('Checking new catalog data..')

        with engine.connect() as connection:
            # GET ACTUAL CATALOG PRODUCTS FROM DATABASE
            query = select(
                product_table.c.title,
                product_table.c.description,
                product_table.c.image_url,
                product_table.c.price,
                product_table.c.site_url,
                product_table.c.category_id,
            )
            db_catalog = connection.execute(query).all()

            # GET NEW CATALOG PRODUCTS FROM CSV-FILES
            csv_catalog = get_products_from_csv()

            # CHECK NEW PRODUCTS, IF IT EXISTS THEN WRITE NEW DATA
            if db_catalog != csv_catalog:
                print('It is new products. Updating..')

                # ADD PRODUCT CATEGORIES
                product_category_stmt = insert(product_category_table).values(product_categories)
                on_conflict_do_nothing_stmt = product_category_stmt.on_conflict_do_nothing(index_elements=['id'])
                connection.execute(on_conflict_do_nothing_stmt)

                # CLEAR ALL PRODUCTS AND BASKETS
                old_products_stmt = delete(product_table)
                connection.execute(old_products_stmt)
                old_basket_stmt = delete(basket_table)
                connection.execute(old_basket_stmt)

                # ADD NEW PRODUCTS
                for product in csv_catalog:
                    product_stmt = insert(product_table).values(
                        title=product[0],
                        description=product[1],
                        image_url=product[2],
                        price=product[3],
                        site_url=product[4],
                        category_id=product[5],
                    )
                    connection.execute(product_stmt)
            else:
                print('Update is not required')

            connection.commit()
