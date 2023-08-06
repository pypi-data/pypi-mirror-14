from urlparse import urlparse

from erppeek import Client as PeekClient


class Client(PeekClient):
    def __init__(self, url, **kwargs):
        url = urlparse(url)
        server = '{p.scheme}://{p.hostname}:{p.port}'.format(p=url)
        db = url.path.lstrip('/')
        user = url.username
        password = url.password
        super(Client, self).__init__(server, db, user, password, **kwargs)
