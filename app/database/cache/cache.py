from aioredis import Redis

from settings import settings


class RedisCache:
    def __init__(self, host: str, port: int, decode_responses: bool):
        self.__redis = Redis(host=host, port=port, decode_responses=decode_responses)

    async def get_catalog(self):
        product_names = await self.__redis.lrange(name='catalog_product_names', start=0, end=-1)
        catalog = []
        for name in product_names:
            product = await self.__redis.lrange(name=name, start=0, end=-1)
            catalog.append(product)
        return catalog

    async def get_product(self, product_id: int):
        name = f'catalog_product_id{product_id}'
        product = await self.__redis.lrange(name=name, start=0, end=-1)
        return product

    async def clear_catalog_data(self):
        product_names = await self.__redis.lrange(name='catalog_product_names', start=0, end=-1)
        if product_names:
            await self.__redis.delete(*product_names)
            await self.__redis.delete('catalog_product_names')

    async def update_catalog_data(self, products: list):
        # DELETE OLD VALUES
        await self.clear_catalog_data()

        # ADD NEW VALUES
        for product in products:
            product_id = product[0]
            name = f'catalog_product_id{product_id}'
            await self.__redis.rpush('catalog_product_names', name)

            await self.__redis.rpush(name, *product)
            await self.__redis.expire(name=name, time=settings.CATALOG_CACHE_EXPIRE_TIME)

        await self.__redis.expire(name='catalog_product_names', time=settings.CATALOG_CACHE_EXPIRE_TIME)


redis_cache = RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
