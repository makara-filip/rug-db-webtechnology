from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.api import api_blueprint

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code

def not_found_response(message=None):
    return error_response(404, message)

def bad_request(message=None):
    return error_response(400, message)

# ensure all API-related errors return API-defined response
@api_blueprint.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code)
