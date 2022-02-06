import logging.config

from app.base.handlers import BaseHandler
from app.classes.models import check_role_permission
from app.classes.multiserv import multi

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
