def print_help():
    print "portcache is a cache for remote calls . In microservice world we have to work with lots of services which are needed to run our serviceand \n" \
      "its a pain if the list of these service list grows big . \n" \
      "portcache gives you the ability to point to a remote service instance and also cache the responses for you calls.\n\n" \
      "To start : type portcache <config yml file> \n\n" \
      "The config file requires three params localport , remote , cache_file \n" \
      "localport corresponds to the port you want to run your cache service . you will point your dependent app/service to this port \n" \
      "remote corresponds to the remote url with port that corresponds to the service you would like to cache \n" \
      "cache_file corresponds to the location of the cache you want to save \n" \
      "A sample file looks like this \n\n" \
      "localport: 9090 \n" \
      "remote: http://myremoteserviceurl.com \n" \
      "cache_file: \"/data/tmp/merch \n\n" \
      "Starting with this config file , whenever a request comes to the localhost:9090 , it will check if this request has been already cached \n" \
      ", if yes then it will serve from cache file , else it will call the http://myremoteserviceurl.com with the request , cache and return the response"