class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class CredentialError(Error):
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "Wrong email or password for user: {}".format(self.username)


class ServerError(Error):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __repr__(self):
        return "Server error when processing request on {}".format(self.endpoint)
