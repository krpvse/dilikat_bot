import csv


product_categories = [
    {'id': 1, 'category_name': '3D принтеры', 'category_type': 'Оборудование'},
    {'id': 2, 'category_name': '3D сканеры', 'category_type': 'Оборудование'},
    {'id': 3, 'category_name': 'Фрезерные станки', 'category_type': 'Оборудование'},
    {'id': 4, 'category_name': 'Печи', 'category_type': 'Оборудование'},
    {'id': 5, 'category_name': 'Фотополимеры', 'category_type': 'Материалы'},
    {'id': 6, 'category_name': 'CAD CAM блоки', 'category_type': 'Материалы'},
    {'id': 7, 'category_name': 'Фрезы', 'category_type': 'Материалы'},
]

product_files = [
    '3D принтеры.csv',
    '3D сканеры.csv',
    'CAD CAM блоки.csv',
    'Печи.csv',
    'Фотополимеры.csv',
    'Фрезерные станки.csv',
    'Фрезы.csv',
]


async def get_products_from_csv() -> list:
    catalog_products = []

    for file in product_files:
        with open(f'database/catalog/data/{file}', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            products = [product for product in reader if product][1:]

        for p in products:
            title = p[0].strip()
            description = p[1].strip()
            image_url = p[2].strip()
            price = int(p[3])
            site_url = p[4].strip()
            category_id = [c['id'] for c in product_categories if c['category_name'] == file.replace('.csv', '')][0]

            catalog_products.append((title, description, image_url, price, site_url, category_id))

    return catalog_products
