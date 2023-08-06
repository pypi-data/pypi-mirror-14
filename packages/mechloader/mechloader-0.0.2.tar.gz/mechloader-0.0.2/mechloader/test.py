import unittest
from mechloader import Mechloader, AuthFormNotFound, AuthError

class FakeBrowser(object):

    class Form(object):

        def __init__(self):
            self.data = {
                'login': '',
                'password': '',
            }

        def __getitem__(self, item):
            if item in self.data:
                return self.data[item]

        def __setitem__(self, key, value):
            if key in self.data:
                self.data[key] = value

    def __init__(self, prop=None):
        import addict
        self.prop = prop
        self.cookies = {}
        self.forms = ['login']
        self._valid_form = {
            'login': 'user',
            'password': 'pass',
        }

        self.form = self.Form()
        self._ua_handlers = addict.Dict()

    def submit(self):
        if self.form['login'] == self._valid_form['login'] and \
                        self.form['password'] == self._valid_form['password']:
            self.forms = []

    def select_form(self, name):
        if name in self.forms:
            pass
        else:
            import mechanize
            raise mechanize.FormNotFoundError('whoops')

    def set_handle_robots(self, *args, **kwargs):
        pass

    def open(self, url, *args, **kwargs):
        if 'download' in url:
            import StringIO
            s = StringIO.StringIO()
            s.write('tested')
            s.seek(0)
            return s
        else:
            return url


class FakeDownloader(Mechloader):

    browser_class = FakeBrowser


class TestWebDownloader(unittest.TestCase):

    def test_web_downloader(self):

        d = FakeDownloader(main_url='http://example.com')

        self.assertEqual(d.get(), 'http://example.com/')
        self.assertEqual(d.get(path=None), 'http://example.com/')
        self.assertEqual(d.get('/index.html'), 'http://example.com/index.html')

        d = FakeDownloader(main_url='http://example.com:1234')
        self.assertEqual(d.get('/index.html'), 'http://example.com:1234/index.html')

        d.init_browser(prop='tested')
        self.assertEqual(d.browser.prop, 'tested')
        old_b = d.browser

        d.init_browser()
        self.assertEqual(d.browser.prop, 'tested')

        self.assertNotEqual(old_b, d.browser)

        d = FakeDownloader(main_url='http://example.com', browser_properties={'prop': 'fake_prop'})
        self.assertEqual(d.browser.prop, 'fake_prop')

        ok = False
        try:
            FakeDownloader(browser_properties=[])
        except TypeError:
            ok = True
        self.assertTrue(ok)

        d = FakeDownloader(main_url='http://example.com', session_cookie_name='session', session_value='session_value')
        self.assertEqual(d.get_session(), 'session_value')

        d = FakeDownloader(
            main_url='http://example.com',
            username='user', password='pass',
            form_auth='login', input_username='login',
            input_password='password',

        )

        d.auth()

        d = FakeDownloader(
            main_url='http://example.com',
            login='user', password='pass',
            auth_form_name='login1', form_login_name='login',
            form_password_name='password',

        )

        ok = False
        try:
            d.auth()
        except AuthFormNotFound:
            ok = True
        self.assertTrue(ok)

        d = FakeDownloader(
            main_url='http://example.com',
            username='user1', password='pass',
            form_auth='login', input_username='login',
            input_password='password',

        )

        ok = False
        try:
            d.auth()
        except AuthError:
            ok = True
        self.assertTrue(ok)


        self.assertEqual(d.download('download'), 'tested')
        d.set_cookie('1', '2')
        self.assertEqual(d.get_cookie('1'), '2')

