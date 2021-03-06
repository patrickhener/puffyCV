import urllib.request
from services.logging_service import initialize_logging

log = initialize_logging()


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
        with urllib.request.urlopen(url) as response:
            log.info("Request {} sent".format(url))
            log.info("HTTP Response Code is: {}".format(response.getcode()))
        log.info("")

    def send_next(self):
        url = "http://" + self.dst_host + ":" + self.dst_port + "/game/nextPlayer"
        with urllib.request.urlopen(url) as response:
            log.info("Request {} sent".format(url))
            log.info("HTTP Response Code is: {}".format(response.getcode()))
