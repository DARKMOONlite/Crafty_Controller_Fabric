import logging
from tornado.web import RequestHandler

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    # TODO: Override RequestHandler.prepare for common functionality
    
    def check_xsrf_cookie(self): 
        # Disable CSRF protection on API routes
        pass
    
    def return_response(self, status, errors, data, messages):
        # Define a standardized response 
        self.write({ 
                "status": status,
                "data": data,
                "errors": errors,
                "messages": messages
        })
    
    def access_denied(self, user):
        logger.info("User %s was denied access to API route", user)

        self.set_status(403)
        self.finish(self.return_response(
            403,
            {'error':'ACCESS_DENIED'}, 
            {}, 
            {'info':'You were denied access to the requested resource'})
        )
    
    def authenticate_user(self, token):
        try:
            logger.debug("Searching for specified token")
            user_data = Users.get(api_token=token)
            logger.debug("Checking results")
            if user_data:
                # Login successful! Return the username
                logger.info("User {} has authenticated to API".format(user_data.username))
                return user_data.username
            else:
                logging.debug("Auth unsuccessful")
                return None
                
        except:
            logger.warning("Traceback occurred when authenticating user to API. Most likely wrong token")
            return None