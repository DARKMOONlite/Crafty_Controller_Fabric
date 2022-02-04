import logging
from tornado.web import *
from app.base.handlers import BaseHandler
from app.classes.models import check_role_permission, Remote
from app.classes.multiserv import multi

logger = logging.getLogger(__name__)


class StartServer(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver

    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)

        if user is None:
            self.access_denied('unknown')

        isAccessDenied = check_role_permission(user, 'api_access') and not check_role_permission(user, 'svr_control')

        if not isAccessDenied:
            self.access_denied(user)

        server_id = self.get_argument('id')
        server = multi.get_server_obj(server_id)

        if not server.check_running():
            Remote.insert({
                Remote.command: 'start_mc_server',
                Remote.server_id: server_id,
                Remote.command_source: "localhost"
            }).execute()
            self.return_response(200, {}, {'code':'SER_START_CALLED'}, {})
        else:
            self.return_response(500, {'error':'SER_RUNNING'}, {}, {})

class StopServer(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver
        
    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)
        
        if user is None:
            self.access_denied('unknown')
        
        isAccessDenied = check_role_permission(user, 'api_access') and not check_role_permission(user, 'svr_control')

        if not isAccessDenied:
            self.access_denied(user)
        
        server_id = self.get_argument('id')
        server = multi.get_server_obj(server_id)
        
        if server.check_running():
            Remote.insert({
                Remote.command: 'stop_mc_server',
                Remote.server_id: server_id,
                Remote.command_source: "localhost"
            }).execute()
            
            self.return_response(200, {}, {'code':'SER_STOP_CALLED'}, {})
        else:
            self.return_response(500, {'error':'SER_NOT_RUNNING'}, {}, {})

class RestartServer(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver

    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)

        if user is None:
            self.access_denied('unknown')

        isAccessDenied = check_role_permission(user, 'api_access') and not check_role_permission(user, 'svr_control')

        if not isAccessDenied:
            self.access_denied(user)

        server_id = self.get_argument('id')
        server = multi.get_server_obj(server_id)

        server.restart_threaded_server()
        self.return_response(200, {}, {'code':'SER_RESTART_CALLED'}, {})

class ListServers(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver

    def get(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)

        if user is None:
            self.access_denied('unknown')

        if not check_role_permission(user, 'api_access'):
            self.access_denied(user)

        self.return_response(200, {}, {"code": "COMPLETED", "servers": multi.list_servers()}, {})

        
class GetServerStats(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver

    def get(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)

        if user is None:
            self.access_denied('unknown')

        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'logs'):
            self.access_denied(user)

        stats = multi.get_stats_for_servers()
        data = []

        for server in stats:
            server = stats[server]
            # We dont need the request time 
            server.pop('time')
            data.append(server)

        self.return_response(200, {}, data, {})

class ForceServerBackup(BaseHandler):
    def initialize(self, mcserver):
        self.mcserver = mcserver

    def post(self):
        token = self.get_argument('token')
        user = self.authenticate_user(token)

        if user is None:
            self.access_denied('unknown')

        if not check_role_permission(user, 'api_access') and not check_role_permission(user, 'backups'):
            self.access_denied(user)

        server_id = self.get_argument('id')
        server = multi.get_server_obj(server_id)

        backup_thread = threading.Thread(name='backup', target=server.backup_server, daemon=False)
        backup_thread.start()

        self.return_response(200, {}, {'code':'SER_BAK_CALLED'}, {})
