from .main_handlers import register_main_handlers
from .equipment_handlers import register_equipment_handlers
from .material_handlers import register_material_handlers
from .basket_handlers import register_basket_handlers
from .user_info_handlers import register_user_info_handlers
from .common_handlers import register_common_handlers


def register_handlers(dp):
    register_main_handlers(dp)
    register_equipment_handlers(dp)
    register_material_handlers(dp)
    register_basket_handlers(dp)
    register_user_info_handlers(dp)
    register_common_handlers(dp)
