from __future__ import print_function
import json
import logging as logging
from botocore.vendored import requests

logger = logging.getLogger(__name__)


def _send_response(response_url, response_body):
    try:
        json_response_body = json.dumps(response_body)
    except Exception as e:
        msg = "Failed to convert response to json: {}".format(str(e))
        logger.error(msg, exc_info=True)
        response_body.update({'Status': 'FAILED', 'Data': {}, 'Reason': msg})
        json_response_body = json.dumps(response_body)
    logger.debug("CFN response URL: {}".format(response_url))
    logger.debug(json_response_body)
    headers = {'content-type': '', 'content-length': str(len(json_response_body))}
    try:
        response = requests.put(response_url, data=json_response_body, headers=headers)
        logger.info("CloudFormation returned status code: {}".format(response.reason))
    except Exception as e:
        logger.error("Unexpected failure sending response to CloudFormation {}".format(e), exc_info=True)
        