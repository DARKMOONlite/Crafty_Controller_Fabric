import os
import secrets
import threading
import logging.config

from app.base.handlers import BaseHandler

from app.classes.models import Users, check_role_permission
from app.classes.multiserv import multi
from app.classes.helpers import helper

logger = logging.getLogger(__name__)


class SendCommand(BaseHandler):
    
    def initialize(self, mcserver):
        self.mcserver = mcserver
    
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'svr_control'):
            self.access_denied(user)
        
        command = self.get_body_argument('command', default=None, strip=True)
        server_id = self.get_argument('id')
        if command:
            server = multi.get_server_obj(server_id)
            if server.check_running:
                server.send_command(command)
                self.return_response(200, '', {"run": True}, '')
            else:
                self.return_response(200, {'error':'SER_NOT_RUNNING'}, {}, {})
        else:
            self.return_response(200, {'error':'NO_COMMAND'}, {}, {})
            
class GetHostStats(BaseHandler):
    
    def initialize(self, mcserver):
        self.mcserver = mcserver
    
    def get(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)
        
        stats = multi.get_host_status()
        stats.pop('time') # We dont need the request time 
        self.return_response(200, {}, stats, {})
        
class SearchMCLogs(BaseHandler):
    
    def initialize(self, mcserver):
        self.mcserver = mcserver
        
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)
            
        search_string = self.get_argument('query', default=None, strip=True)
        server_id = self.get_argument('id')
        
        server = multi.get_server_obj(server_id)
        logfile = os.path.join(server.server_path, 'logs', 'latest.log')
        
        data = helper.search_file(logfile, search_string)
        line_list = []
        
        if data:
            for line in data:
                line_list.append({'line_num': line[0], 'message': line[1]})
                
        self.return_response(200, {}, line_list, {})
    
class GetMCLogs(BaseHandler):
    
    def initialize(self, mcserver):
        self.mcserver = mcserver
        
    def get(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)
        
        server_id = self.get_argument('id')
        server = multi.get_server_obj(server_id)

        logfile = os.path.join(server.server_path, 'logs', 'latest.log')
        data = helper.search_file(logfile, '')
        line_list = []
        
        if data:
            for line in data:
                line_list.append({'line_num': line[0], 'message': line[1]})
                
        self.return_response(200, {}, line_list, {})    
        
class GetCraftyLogs(BaseHandler):
        
    def get(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)
            
        filename = self.get_argument('name')
        logfile = os.path.join('logs', filename + '.log')
        
        data = helper.search_file(logfile, '')
        line_list = []
        
        if data:
            for line in data:
                line_list.append({'line_num': line[0], 'message': line[1]})
                
        self.return_response(200, {}, line_list, {}) 
        
class SearchCraftyLogs(BaseHandler):
        
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)
            
        filename = self.get_argument('name')
        query = self.get_argument('query')
        logfile = os.path.join('logs', filename + '.log')
        
        data = helper.search_file(logfile, query)
        line_list = []
        
        if data:
            for line in data:
                line_list.append({'line_num': line[0], 'message': line[1]})
                
        self.return_response(200, {}, line_list, {}) 

class CreateUser(BaseHandler):
    
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'config'):
            self.access_denied(user)
        
        new_username = self.get_argument("username")
        
        # TODO: implement role checking
        #new_role = self.get_argument("role", 'Mod')

        if new_username:
            new_pass = helper.random_string_generator()
            new_token = secrets.token_urlsafe(32)
            result = Users.insert({
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
