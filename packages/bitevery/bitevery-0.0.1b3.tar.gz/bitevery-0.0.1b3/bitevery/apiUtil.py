import sys

BASE_URL = "https://www.bitevery.com/api"
SEPARATOR = "/"
CONNECTOR = "&"

py_version = sys.version_info[0]
if py_version >= 3:
    # Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    # Python 2.x
    from urllib2 import urlopen
    from urllib2 import HTTPError

def getParamString(params):
	output = ""
	for param in params:
		output += CONNECTOR
		output += param
	return output
	
def call_api(resource, api_code, params = None, data = None):
	if(params is None):
		request = BASE_URL + SEPARATOR + resource + SEPARATOR + str(api_code)
	else:
		request = BASE_URL + SEPARATOR + resource + SEPARATOR + str(api_code) + getParamString(params)
	try:
		return urlopen(request).read()
	except HTTPError as e:
		return "HTTP error: " + e.read() + ", error code:" + e.code

def call_get_api_code(resource, username, password):
	usernameFull = "username=" + str(username)
	passwordFull = "password=" + str(password)
	request = BASE_URL + SEPARATOR + resource + CONNECTOR + usernameFull + CONNECTOR + passwordFull
	
	try:
		return urlopen(request).read()
	except HTTPError as e:
		return "HTTP error: " + e.read() + ", error code:" + e.code			
	
	