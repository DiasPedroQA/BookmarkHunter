#  pylint: disable=C, R, E, W
#  pylint: disable=C0114, C0115, C0116

# app/routes/routes.py

from app.controllers.favorite_controller import FavoriteController
from app.services.global_services import GeneralServices

service = GeneralServices()
controller = FavoriteController(service)
