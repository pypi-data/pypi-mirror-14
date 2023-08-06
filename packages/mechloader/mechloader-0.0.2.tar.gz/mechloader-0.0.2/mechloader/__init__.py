from urlparse import urlsplit, urlparse
from mechloader.dict_update import dict_update
import logging
import mechanize

class AuthError(RuntimeError):
    pass

class InvalidProto(RuntimeError):
    pass

class AuthFormNotFound(RuntimeError):
    pass

valid_scheme = ('http', 'https')

class Mechloader(object):
    """

    download files from web, use mechanize browser
    """

    browser_class = mechanize.Browser
    _browser = None
    scheme = 'http'
    port = None
    host = None

    def __init__(
            self, main_url=u'', auth_path=u'', username=None, password=None,
            form_auth=None, input_username=None, input_password=None,
            session_cookie_name=None, session_value=None, browser_properties=None, logger=None, **options
    ):
        main_url = self.parse_url(main_url)
        self.logger = logger
        self.main_url = main_url
        self.auth_path = auth_path
        self.username = username
        self.password = password
        self.form_auth = form_auth
        self.input_username = input_username
        self.input_password = input_password
        self.session_cookie_name = session_cookie_name
        if browser_properties is None:
            browser_properties = {}
        elif not isinstance(browser_properties, dict):
            raise TypeError('Browser properties must be a dict')
        self.browser_properties = browser_properties
        if session_value is not None:
            self.set_session(session_value)
        self.options = options
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    @property
    def browser(self):
        if self._browser is None:
            self._browser = self.create_browser(**self.browser_properties)
        return self._browser

    @browser.setter
    def browser(self, value):
        if value is not None and isinstance(value, self.browser_class):
            self._browser = value

    @classmethod
    def create_browser(cls, **kwargs):
        browser = cls.browser_class(**kwargs)
        browser.set_handle_robots(False)
        return browser

    def init_browser(self, **kwargs):
        self.browser_properties = dict_update(self.browser_properties, kwargs)
        self.browser = self.create_browser(**self.browser_properties)
        return self.browser

    def go(self, url, *args, **kwargs):
        url = self.parse_url(url)
        return self.browser.open(url, *args, **kwargs)

    def get(self, path=u'/', *args, **kwargs):
        proto = self.scheme
        host = self.host
        if path is None:
            path = u'/'
        if self.port is not None:
            host = '{}:{}'.format(host, self.port)
        url = '{proto}://{host}{path}'.format(
            proto=proto,
            host=host,
            path=path,
        )
        return self.go(url, *args, **kwargs)

    def parse_url(self, url):
        url = urlsplit(url).geturl()
        parsed_url = urlparse(url=url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.scheme = parsed_url.scheme
        return url

    def update_form(self, form_name, data):
        self.browser.select_form(form_name)

        for key in data:
            self.browser.form[key] = data[key]

    def submit(self, *args, **kwargs):
        return self.browser.submit(*args, **kwargs)

    def update_auth_form(self):
        data = {
            self.input_username: self.username,
            self.input_password: self.password,
        }
        try:
            self.update_form(self.form_auth, data)
        except mechanize.FormNotFoundError as e:
            raise AuthFormNotFound(e)

    def auth(self):
        self.get(path=self.auth_path)
        self.update_auth_form()
        self.submit()
        self.check_auth()

    def check_auth(self):
        try:
            self.update_auth_form()
        except AuthFormNotFound:
            pass
        else:
            raise AuthError('login or password is wrong!')

    def get_cookie(self, name):
        return self.browser._ua_handlers['_cookies'].cookiejar._cookies[self.host]['/'][name].value

    def set_cookie(self, name, value):
        self.browser._ua_handlers['_cookies'].cookiejar._cookies[self.host]['/'][name].value = value

    def get_session(self):
        """Get session key with session_cookie_name

        """
        return self.get_cookie(self.session_cookie_name)

    def set_session(self, value):
        self.set_cookie(self.session_cookie_name, value)

    def download(self, path):
        return self.get(path).read()


