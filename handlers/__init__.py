from .main_handlers import register_main_handlers
from .product_handlers import register_product_handlers
from .basket_handlers import register_basket_handlers
from .customer_info_handlers import register_customer_info_handlers
from .common_handlers import register_common_handlers


def register_handlers(dp):
    register_product_handlers(dp)
    register_customer_info_handlers(dp)
    register_basket_handlers(dp)
    register_main_handlers(dp)
    register_common_handlers(dp)
