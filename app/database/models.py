from sqlalchemy import MetaData, text, Table, Column, Integer, BigInteger, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint


metadata = MetaData()


# INDEPENDENT TABLES, DON'T DELETE AND DON'T CHANGE WITH CATALOG UPDATING

telegram_user_table = Table(
    'telegram_user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', BigInteger, unique=True, nullable=False),
    Column('username', String(length=32)),
    Column('full_name', String(length=256)),
)

customer_info_table = Table(
    'customer_info',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('telegram_user.user_id'), unique=True, nullable=False),
    Column('first_name', String),
    Column('last_name', String),
    Column('phone_number', String),
    Column('delivery_address', String),
)


# DEPENDS ON CATALOG TABLES, CHANGES WITH CATALOG UPDATING

product_category_table = Table(
    'product_category',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String, nullable=False),
    Column('category_type', String, nullable=False),

)

product_table = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(length=128), nullable=False),
    Column('description', String(length=740)),
    Column('image_url', String),
    Column('price', BigInteger),
    Column('site_url', String),
    Column('category_id', ForeignKey('product_category.id')),
)

basket_table = Table(
    'basket',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product_id', ForeignKey('product.id')),
    Column('quantity', Integer, default=1),
    Column('user_id', ForeignKey('telegram_user.user_id')),
    Column('created_at', DateTime, server_default=text("TIMEZONE('utc', now())")),
    UniqueConstraint('product_id', 'user_id', name='unique_product_id_user_id'),
    CheckConstraint('quantity > 0', name='check_quantity'),
)
