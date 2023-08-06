# OAuth2Client

## Presentation
*OAuth2Client* is a simple python client library for OAuth2. It is based on the [requests](https://pypi.python.org/pypi/requests).

## Login process
For now it can handle two token process:

- Authorization code
- Credentials  

### Authorization code
Since authorization code process needs the user to accept the access to its data by the application, the library starts localy a http server. You may put the host part of the ```redirect_uri``` parameter in your *hosts* file pointing to your loopback address. The server waits a ```GET``` requests with the  ```code``` as a query parameter.

Getting a couple of access token may be done like this:

```python
scopes = ['scope_1', 'scope_2']

service_information = ServiceInformation('https://authorization-server/oauth/authorize',
                                         'https://token-server/oauth/token',
                                         'client_id',
                                         'client_secret',
                                          scopes)
manager = CredentialManager(service_information,
                            proxies=dict(http='http://localhost:3128', https='http://localhost:3128'))
redirect_uri = 'http://somewhere.io:8080/oauth/code'

# Builds the authorization url and starts the local server according to the redirect_uri parameter
url = manager.init_authorize_code_process(redirect_uri, 'state_test')
_logger.info('Open this url in your browser\n%s', url)

code = manager.wait_and_terminate_authorize_code_process()
# From this point the http server is opened on 8080 port and wait to receive a single GET request
# All you need to do is open the url and the process will go on 
# (as long you put the host part of your redirect uri in your host file)
# when the server gets the request with the code (or error) in its query parameters
_logger.debug('Code got = %s', code)
manager.init_with_authorize_code(redirect_uri, code)
_logger.debug('Access got = %s', manager.access_token)
# Here access and refresh token may be used
```
### Credentials:
Get a couple of access and refresh token is much easier:

```python
scopes = ['scope_1', 'scope_2']

service_information = ServiceInformation('https://authorization-server/oauth/authorize',
                                         'https://token-server/oauth/token',
                                         'client_id',
                                         'client_secret',
                                          scopes)
manager = CredentialManager(service_information,
                            proxies=dict(http='http://localhost:3128', https='http://localhost:3128'))
manager.init_with_credentials('login', 'password')
_logger.debug('Access got = %s', manager.access_token)
# Here access and refresh token may be used
```
 
