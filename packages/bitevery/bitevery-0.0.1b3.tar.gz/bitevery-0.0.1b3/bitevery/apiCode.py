from . import apiUtil
from apiUtil import *

API_CODE_ENDPOINT = "api_code"
SEPARATOR = "/"
	
def getApiCode(username, password):
	return call_get_api_code(API_CODE_ENDPOINT, username, password)