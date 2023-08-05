from setuptools import setup


setup(name='portcache',
      version='0.2',
      description='A simple cache for port from remote service',
      url='http://github.com/storborg/funniest',
      author='Raghavan',
      author_email='oneraghavan@gmail.com',
      license='MIT',
      packages=['portcache'],
      install_requires=[
          'web.py', 'PyYAML'
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['portcache=portcache.command_line:main'],
      })

print "___________________________________"
print "|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |"
print "|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |"
print "| Succesfully installed portcache |"
print "|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |"
print "|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |"
print "|_________________________________|"

print "\nportcache is a cache for remote calls . In microservices world, we have to work with lots of services which are needed to run our service and \n" \
      "its a pain if the list of these service list grows big .portcache gives you the ability to point to a remote service instance and also cache \n" \
      "the responses for you calls.\n\n" \
      "To start : portcache <config yml file> \n\n" \
      "The config file requires three params localport , remote , cache_file .\n" \
      "localport  - The port you want to run your cache service . you will point your dependent app/service to this port \n" \
      "remote     - The remote url with port that corresponds to the service you would like to cache \n" \
      "cache_file - The location of the cache you want to save \n\n" \
      "A sample config yml file looks like this \n\n" \
      "localport: 9090 \n" \
      "remote: http://myremoteserviceurl.com \n" \
      "cache_file: \"/data/tmp/merch \n\n" \
      "Starting with this config file, starts a server at port 9090.Whenever a request comes to the localhost:9090, it \n" \
      "will check if this request has been already cached ,if yes then it will serve from cache file, else it will call \n" \
      "the http://myremoteserviceurl.com with the request, cache and return the response"
