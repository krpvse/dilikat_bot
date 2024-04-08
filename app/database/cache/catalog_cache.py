from loader import redis
from settings import settings


async def get_catalog_from_cache():
    product_names = await redis.lrange(name='catalog_product_names', start=0, end=-1)
    catalog = []
    for name in product_names:
        product = await redis.lrange(name=name, start=0, end=-1)
        catalog.append(product)

    return catalog


async def get_product_from_cache(product_id: int):
    name = f'catalog_product_id{product_id}'
    product = await redis.lrange(name=name, start=0, end=-1)
    return product


async def clear_catalog_cache():
    product_names = await redis.lrange(name='catalog_product_names', start=0, end=-1)
    if product_names:
        await redis.delete(*product_names)
        await redis.delete('catalog_product_names')


async def save_products_in_cache(products: list):
    # DELETE OLD VALUES
    await clear_catalog_cache()

    # ADD NEW VALUES
    for product in products:
        product_id = product[0]
        name = f'catalog_product_id{product_id}'
        await redis.rpush('catalog_product_names', name)

        await redis.rpush(name, *product)
        await redis.expire(name=name, time=settings.CATALOG_CACHE_EXPIRE_TIME)

    await redis.expire(name='catalog_product_names', time=settings.CATALOG_CACHE_EXPIRE_TIME)
