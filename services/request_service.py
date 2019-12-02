import urllib.request


class ScoreboardConnector(object):
    """
    Object to connect to a Scoreboard Application like
    Dart-O-Mat 3000 (https://github.com/patrickhener/dart-o-mat-3000/)
    using API like requests
    """

    def __init__(self, dst_host:str, dst_port:str):
        self.dst_host = dst_host
        self.dst_port = dst_port

    def send_throw(self, segment, mod):
        url = "http://" + self.dst_host + ":" + self.dst_port + "/game/throw/" + segment + "/" + mod
        request = urllib.request.urlopen(url)
        return request

    def send_next(self):
        url = "http://" + self.dst_host + ":" + self.dst_port + "/game/nextPlayer"
        request = urllib.request.urlopen(url)
        return request
