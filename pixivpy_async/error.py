class RetryExhaustedError(Exception):
    def __init__(self, name=None, args=None, kwargs=None):
        self.name = name
        self.reason = '{}, {}'.format(args, kwargs)
        super(Exception, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class NoLoginError(Exception):
    def __init__(self):
        self.reason = 'Require auth() but no password or refresh_token is set.'
        super(Exception, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class AuthCredentialsError(Exception):
    def __init__(self, code=None, r=None):
        self.reason = 'Run auth() failed! Check username and password.\nHTTP %s: %s' % (code, r)
        super(Exception, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class AuthTokenError(Exception):
    def __init__(self, code=None, r=None):
        self.reason = 'Run auth() failed! Check refresh_token.\nHTTP %s: %s' % (code, r)
        super(Exception, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class TokenError(Exception):
    def __init__(self, token=None, e=None):
        self.reason = 'Get access_token error! \nResponse: %s\nError: %s' % (token, e)
        super(Exception, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class MethodError(Exception):
    def __init__(self, method=None):
        self.reason = 'Unknown method: %s' % method

    def __str__(self):
        return self.reason


class NoTokenError(Exception):
    def __init__(self):
        self.reason = 'No access_token Found!'

    def __str__(self):
        return self.reason