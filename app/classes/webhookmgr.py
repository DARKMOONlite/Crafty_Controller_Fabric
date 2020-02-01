import logging
import requests

from app.classes.models import Webhooks, model_to_dict
from app.classes.helpers import helper

logger = logging.getLogger(__name__)

# Duplicate of commands in remote_coms
commands = {
    "restart_web_server": "Restart Web Server",
    "restart_mc_server": "Restart Minecraft Server",
    "start_mc_server": "Start Minecraft Server",
    "stop_mc_server": "Stop Minecraft Server",
    "exit_crafty": "Stop Crafty",
    "start_ftp": "Start FTPS Server",
    "stop_ftp": "Stop FTPS Server"
}

class WebhookMGR():

    def __init__(self):
        self.commands = commands
        logger.info("WebhookMGR initialised!")

    def add_webhook(self, webhook_name, url, command_name, method="POST", send_data=True):
        logger.info("Adding webhook for command %s to URL %s", command_name, url)
        # make sure command actually exists
        if not self.commands.get(command_name) is None:
            # Ok, we got command
            logger.debug("Specified command exists")
            pass
        else:
            # Oh no, we didn't, seeing if description was specified
            for i in self.commands:
                if self.commands[i] == command_name:
                    # Found it!
                    command_name = i
                    logger.debug("Command found by description")
                    break
                else: 
                    # nope, invalid
                    logger.warning("Command passed to add_webhook is invalid")
                    command_name = None

        if not command_name is None:
            logger.debug("Command name validation passed")
            if helper.validate_url(url) and helper.validate_method(method):
                logger.info("Webhook is valid, adding it to DB")
                try:
                    Webhooks.insert(
                            name=webhook_name,
                            method=method,
                            url=url,
                            on_command=command_name,
                            send_data=send_data
                        ).execute()
                except:
                    logger.exception("Exception occurred while adding webhook. Traceback:")

    def list_webhooks(self):
        data = Webhooks.select()
        webhooks = {}

        for entry in data:
            webhooks[entry.id] = {
                "name": entry.name,
                "method": entry.method,
                "target": entry.url,
                "send_data": entry.send_data, 
                "command_name": entry.on_command,
                "command_desc": self.commands.get(entry.on_command) 
            }
        return webhooks

    def update_webhook(self, id, name, url, command_name, method, send_data):
        # Grab the specified id from the DB
        record = Webhooks.select().where(Webhooks.id == id)

        # Check if it exists
        if not record is None:
            logger.info("Updating webhook info for id %s (%s)", record.id, record.name)

            # Update specified values in DB, if they are the same, nothing will change
            try:
                res = (
                    Webhooks
                    .update(
                        name=name,
                        url=url,
                        method=method,
                        send_data=send_data,
                        on_command=command_name
                    )
                    .where(Webhooks.id == id)
                    .execute()
                )
            except:
                logger.exception("Exception occurred while updating webhook. Traceback:")

            logger.debug("Updated %s rows", res)
        else:
            logger.warning("No result found in DB for webhook ID %s when updating info", id)

    def run_webhooks(self, command_name, data):
        # Grab all hooks from DB
        results = Webhooks.select().where(Webhooks.on_command == command_name)

        if results:
            # Iterate over them
            for result in results:

                # Extract required data
                with_data = result.send_data
                method = result.method
                url = result.url

                if method == "GET":
                    # HTTP/1.1 says body is ignored on GET requests, so not sending it
                    logger.info("Requesting \"GET %s\" webhook due to command \"%s\" being issued", url, command_name)
                    requests.get(url)

                elif method == "POST":
                    if with_data:
                        logger.info("Requesting \"POST %s\" webhook due to command \"%s\" being issued, with data", url, command_name)
                        requests.post(url, data=data)
                    else:
                        logger.info("Requesting \"POST %s\" webhook due to command \"%s\" being issued, without data", url, command_name)
                        requests.post(url)

                elif method == "PUT":
                    if with_data:
                        logger.info("Requesting \"PUT %s\" webhook due to command \"%s\" being issued, with data", url, command_name)
                        requests.put(url, data=data)
                    else:
                        logger.info("Requesting \"PUT %s\" webhook due to command \"%s\" being issued, without data", url, command_name)

                elif method == "DELETE":
                    # HTTP/1.1 says body is ignored on DELETE requests, so not sending it
                    logger.info("Requesting \"DELETE %s\" webhook due to command \"%s\" being issued", url, command_name)
                    requests.delete(url)

                else:
                    # We should never get here
                    pass
        else:
            logger.info("No webhooks to call for command %s", command_name)

    def data_formatter(self, status, errors, data, messages):
        # Define a standardized response
        return {
                "status": status,
                "data": data,
                "errors": errors,
                "messages": messages
                }

webhookmgr = WebhookMGR()