from .register_handlers import register_router
from .start_handler import start_router
from .profile_handlers import profile_router
from .admin_handlers import admin_router
from .support_handlers import support_router
from .report_handlers import report_router

__all__ = ["register_router", "start_router",\
    "profile_router", "admin_router", "support_router", "report_router"]

def setup_routers(dp):
    dp.include_router(router=register_router)
    dp.include_router(router=start_router)
    dp.include_router(router=profile_router)
    dp.include_router(router=admin_router)
    dp.include_router(router=support_router)
    dp.include_router(router=report_router)
    
    