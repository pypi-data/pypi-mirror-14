from setuptools import setup, find_packages

print find_packages()


setup (

        name         = 'MPBS', 

        version      = '0.0.1',

        author       = 'kevin90116',

        author_email = 'kevin90116@gmail.com',

        url          = 'http://www.example.com',

        description  = 'zmq based MultiPublisher-Broker-multiSubscriber framework',

	packages     = find_packages(),

	install_requires = ['pyzmq'],

	platforms    = 'any'

       )
