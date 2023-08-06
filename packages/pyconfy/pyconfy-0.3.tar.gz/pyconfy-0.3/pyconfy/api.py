"""Functions needed to access the Confluence api."""
import sys

try:
    import requests
except ImportError:
    sys.stderr.write("You do not have the 'requests' module installed. " +
                     "Please see http://docs.python-requests.org/en/latest/ " +
                     "for more information.")
    exit(1)


requests.packages.urllib3.disable_warnings()

token = ""
user = ""
base_url = ""


def load_config():
    """Load variables from the config."""
    try:
        import yaml
    except ImportError:
        sys.stderr.write("You do not have the 'yaml' module installed. "
                         "Please see http://pyyaml.org/wiki/PyYAMLDocumentation"
                         " for more information.")
        exit(1)

    try:
        f = open("confy/confy_config.yml")
        config_data = yaml.safe_load(f)
        f.close()
    except IOError:
        sys.stderr.write("You have not updated your Confluence credentials."
                         "Run update_credentials with appropriate data and try"
                         " again.")
        exit(1)

    global token
    global user
    global base_url
    token = config_data["token"]
    user = config_data["user"]
    base_url = config_data["base_url"]


def rest(url, req='get', data=None):
    """Main function to be called from this module.

    send a request using method 'req' and to the url. the _rest() function
    will add the base_url to this, so 'url' should be something like '/ips'.
    """
    load_config()

    return _rest(req, base_url + url, data)


def _rest(req, url, data=None):
    """Send a rest rest request to the server."""

    if 'HTTPS' not in url.upper():
        print("Secure connection required: Please use HTTPS or https")
        return ""

    cmd = req.upper()
    if cmd != "GET" and cmd != "PUT" and cmd != "POST" and cmd != "DELETE":
        return ""

    status, body = _api_action(cmd, url, data)
    if (int(status) > 200 or int(status) < 226):
        return body
    else:
        print("Oops! Error: status: %s\n%s\n" % (status, body))


def _api_action(cmd, url, data=None):
    url, name, passwd = url, user, token

    requisite_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}
    auth = (name, passwd)

    if cmd == "GET":
        response = requests.get(url, headers=requisite_headers, auth=auth)
    elif cmd == "PUT":
        response = requests.put(url, headers=requisite_headers, auth=auth,
                                params=data)
    elif cmd == "POST":
        response = requests.post(url, headers=requisite_headers, auth=auth,
                                 data=data)
    elif cmd == "DELETE":
        response = requests.delete(url, headers=requisite_headers, auth=auth)

    return response.status_code, response.text
