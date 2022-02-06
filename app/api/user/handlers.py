import logging.config
import secrets

from app.base.handlers import BaseHandler
from app.classes.helpers import helper
from app.classes.models import Users, check_role_permission

logger = logging.getLogger(__name__)


class CreateUser(BaseHandler):
    
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'config'):
            self.access_denied(user)
        
        new_username = self.get_argument("username")

        if new_username:
            new_pass = helper.random_string_generator()
            new_token = secrets.token_urlsafe(32)
            _ = Users.insert({
                Users.username: new_username,
                Users.role: 'Mod',
                Users.password: helper.encode_pass(new_pass),
                Users.api_token: new_token
            }).execute()
            
            self.return_response(200, {}, {'code':'COMPLETE', 'username': new_username, 'password': new_pass, 'api_token': new_token}, {})
        else:
            self.return_response(500, {'error':'MISSING_PARAMS'}, {}, {'info':'Some paramaters failed validation'})

class DeleteUser(BaseHandler):
    
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'config'):
            self.access_denied(user)
        
        username = self.get_argument("username", None, True)

        if username == 'Admin':
            self.return_response(500, {'error':'NOT_ALLOWED'}, {}, {'info':'You cannot delete the admin user'})
        else:
            if username:
                Users.delete().where(Users.username == username).execute()
                self.return_response(200, {}, {'code':'COMPLETED'}, {})
