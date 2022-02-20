class PixivError(Exception):
    pass


class RetryExhaustedError(PixivError):
    def __init__(self, name=None, args=None, kwargs=None):
        self.name = name
        self.reason = '{}, {}'.format(args, kwargs)
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class NoLoginError(PixivError):
    def __init__(self):
        self.reason = 'Require auth() but no password or refresh_token is set.'
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class LoginError(PixivError):
    def __init__(self):
        self.reason = 'Password login is no longer supported, please use `login_web` instead.'
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class AuthCredentialsError(PixivError):
    def __init__(self, code=None, r=None):
        self.reason = 'Run auth() failed! Check username and password.\nHTTP %s: %s' % (code, r)
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class AuthTokenError(PixivError):
    def __init__(self, code=None, r=None):
        self.reason = 'Run auth() failed! Check refresh_token.\nHTTP %s: %s' % (code, r)
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class TokenError(PixivError):
    def __init__(self, token=None, e=None):
        self.reason = 'Get access_token error! \nResponse: %s\nError: %s' % (
            token, e)
        super(PixivError, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class MethodError(PixivError):
    def __init__(self, method=None):
        self.reason = 'Unknown method: %s' % method

    def __str__(self):
        return self.reason


class NoTokenError(PixivError):
    def __init__(self):
        self.reason = 'No access_token Found!'

    def __str__(self):
        return self.reason
