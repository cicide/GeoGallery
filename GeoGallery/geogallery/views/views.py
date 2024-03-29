import deform
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from geogallery.models import (
    DBSession,
    )
from geogallery.schemas import (
    LoginSchema,
    CheckAuthentication,
    )

import logging
log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='home.mako')
def home(request):
    if request.user is None:
        return HTTPFound(location = request.route_url('login'))
    return dict(user= request.user,)

@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    login_url = request.route_url('login')  
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    schema = LoginSchema(validator=CheckAuthentication).bind(request=request)
    form = deform.Form(schema, action=login_url, buttons=('Login',))
    defaults = {}
    defaults['came_from'] = request.params.get('came_from', referrer)
    if request.POST:
        appstruct = None
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            log.exception('in form validated')
            return {'form':e.render()}
 
        login = appstruct['username']
        password = appstruct['password']
        came_from = appstruct['came_from']
        user = DBSession.query(User).filter_by(username=login, pin = password).first()
        if user:
            headers = remember(request, user.id)
            user.last_login = datetime.datetime.utcnow()
            request.user = user
            return HTTPFound(location = came_from, headers = headers)
        return dict( form= form.render(appstruct=appstruct),
                   )

    return dict(
            url = request.application_url + '/login',
            form = form.render(appstruct=defaults)
        )
    
conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_GeoGallery_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

