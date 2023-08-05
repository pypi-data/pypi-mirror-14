import sys
import portcache
from .help import print_help

def main():
    if sys.argv[1] == "-help":
        print_help()
    else:
        portcache.start_port_cache()