from setuptools import setup, find_packages

setup (

        name         = 'zmqf', 

        version      = '0.0.1',

        author       = 'kevin90116',

        author_email = 'kevin90116@gmail.com',

        url          = 'http://www.example.com',

        description  = 'zmq based MultiPublisher-Broker-MultiSubscriber framework',

	    packages     = find_packages(),

	    install_requires = ['pyzmq'],

	    platforms    = 'any'

       )
