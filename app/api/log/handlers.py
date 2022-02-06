import logging.config
import os

from app.base.handlers import BaseHandler
from app.classes.helpers import helper
from app.classes.models import check_role_permission
from app.classes.multiserv import multi

logger = logging.getLogger(__name__)


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
