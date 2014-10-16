# -*- coding: utf-8 -*-
import web
import sys, os
from twisted.python import log
from twisted.internet import defer, reactor


def main(config_file):
    log.startLogging(sys.stdout)
    application = web.Application(config_file)

    port = os.environ.get("PORT", 8888)
    reactor.listenTCP(int(port), application)
    reactor.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        log.error("no config file given")
        sys.exit(-1)
