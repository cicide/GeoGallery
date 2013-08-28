from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from geogallery.security import groupfinder
from geogallery.lib import get_user

from models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = session_factory_from_settings(settings)
    authn_policy = AuthTktAuthenticationPolicy( 'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='geogallery.models.models.RootFactory')
    config.set_request_property(get_user, str('user'), reify=True)
    config.include('bag.web.pyramid.flash_msg')
    config.set_session_factory(session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    # Adding the static resources from Deform
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('deform_bootstrap_static', 'deform_bootstrap:static', cache_max_age=3600)
    
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.scan()
    return config.make_wsgi_app()
