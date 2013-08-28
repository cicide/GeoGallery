import deform
import colander
import six

from deform.schema import FileData

from ..models.models import (
    DBSession,
    User,
    )

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token


@colander.deferred
def deferred_csrf_validator(node, kw):
    def validate_csrf(node, value):
        request = kw.get('request')
        csrf_token = request.session.get_csrf_token()

        if six.PY3:
            if not isinstance(csrf_token, str):
                csrf_token = csrf_token.decode('utf-8')

        if value != csrf_token:
            raise colander.Invalid(node,
                                   'Invalid cross-site scripting token')
    return validate_csrf

@colander.deferred
def deferred_choices_widget(node,kw):
    choices = (
    ('', '- Select -'),
    ('admin', 'Admin'),
    )
    return deform.widget.SelectWidget(values=choices)

def user_DoesExist(node,appstruct):
    if DBSession.query(User).filter_by(username=appstruct['username']).count() > 0:
        raise colander.Invalid(node, 'Username already exist.!!')
    
def CheckAuthentication(node,appstruct):
    if DBSession.query(User).filter_by(username=appstruct['username'], pin=appstruct['password']).count() == 0:
        raise colander.Invalid(node, 'Invalid Username or password')
    
def checkUploadFile(node,data):
    AUDIO_EXTS = ['audio/mp3', 'audio/wav']
    if data['mimetype'] not in AUDIO_EXTS:
        raise colander.Invalid(node, 'Invalid file format')
    pass

class CSRFSchema(colander.Schema):
    csrf_token = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        default=deferred_csrf_default,
        validator=deferred_csrf_validator,
    )


class Store(dict):
    def preview_url(self, name):
        return "/tmp"
 
store = Store()

class LoginSchema(CSRFSchema):
    username = colander.SchemaNode(colander.String())
    came_from = colander.SchemaNode(colander.String(),
                    widget = deform.widget.HiddenWidget())
    password = colander.SchemaNode(
                    colander.String(),
                    validator=colander.Length(min=4, max=20),
                    widget=deform.widget.PasswordWidget(size=20),
                    description='Enter a password')

class UserSchema(CSRFSchema):
    username = colander.SchemaNode(colander.String(), 
                   description="Extension of the user")
    name = colander.SchemaNode(colander.String(), 
                   description='Full name')
    email = colander.SchemaNode(colander.String(),
                    validator=colander.Email(),
                    description="Email", missing=None),
    age = colander.SchemaNode(colander.Integer(), 
              description='Age')
    