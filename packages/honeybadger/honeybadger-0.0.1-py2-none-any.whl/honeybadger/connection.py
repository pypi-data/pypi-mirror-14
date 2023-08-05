import logging
import urllib2
import json
import threading
from .utils import StringReprJSONEncoder

logger = logging.getLogger(__name__)

def send_notice(config, payload):
    request = urllib2.Request(url="{}/v1/notices/".format(config.endpoint))

    if not config.api_key:
        logger.error("Honeybadger API key missing from configuration: cannot report errors.")
        return

    request.add_header('X-Api-Key', config.api_key)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_data(json.dumps(payload, cls=StringReprJSONEncoder)) # request.add_data(str(payload))

    def send_request():
        response = urllib2.urlopen(request)

        status = response.getcode()
        if status != 201:
            logger.error("Received error response [{}] from Honeybadger API.".format(status))

    t = threading.Thread(target=send_request)
    t.start()
