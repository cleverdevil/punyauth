from pecan import expose, redirect

from . import indieauth

class RootController:
    indieauth = indieauth.IndieAuthController()
