import socket
import shelve
import sys

import web
import yaml
import requests

urls = (
    '/(.*)', 'index'
)


class index:
    def GET(self, name):
        relative_path = web.ctx.fullpath.__str__()
        if web.store_cache.__contains__(relative_path):
            print "Avaiable in the cache "
            return web.store_cache.get(relative_path)
        else:
            print "Not in cache , hitting the remote"
            response = requests.get(web.config['remote'] + relative_path)
            raw_response = response.text
            try:
                response.raise_for_status()
            except Exception as e:
                print "Request failed with status code " + str(response.status_code) + " ,hence not caching the request"
                print e.message
                return web.InternalError()
                print "coming here"
            web.store_cache[relative_path] = raw_response
            web.store_cache.sync()
        return raw_response


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


def validate(config_file):
    try:
        mandatory_params = ['localport', 'cache_file', 'remote']
        for param in mandatory_params:
            if not param in config_file:
                raise Exception("Config param '" + param + "'  " + "is a mandatory config and is not found in yml file")
    except Exception as e:
        print "Not Starting the cache"
        print e.message
        sys.exit()


def print_startup_message(config):
    print "Starting portcache , the localport:" + str(config['localport']) + " is a cache for remote service " + str(
        web.config[
            'remote'])


def start_port_cache():
    config_file_path = sys.argv[1]
    stream = file(config_file_path, 'r')
    config_file = yaml.load(stream)
    validate(config_file)
    web.config = config_file
    cache = shelve.open(web.config['cache_file'], writeback=True)
    cache.sync()
    web.store_cache = cache

    app = MyApplication(urls, globals())
    print_startup_message(web.config)
    try:
        app.run(port=web.config['localport'])
    except socket.error as e:
        print "There is already an application server running in port : " + str(web.config['localport'])
        print e.message
        sys.exit()


if __name__ == "__main__":
    start_port_cache()
