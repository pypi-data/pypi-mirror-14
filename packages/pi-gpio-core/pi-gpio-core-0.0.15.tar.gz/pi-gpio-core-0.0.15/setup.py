from distutils.core import setup

setup(
    name='pi-gpio-core',
    version='0.0.15',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['pi_gpio_core'],
    package_data={
        'pi_gpio_core': [
            'client/*',
            'server/*'
        ]
    },
    url='https://github.com/exitcodezero/pi-gpio-core',
    license='LICENSE',
    description='A ZeroMQ-based service for interacting with GPIO pins',
    long_description='A ZeroMQ-based service for interacting with GPIO pins',
    install_requires=[
        "coverage==4.0.3",
        "gpiozero==1.1.0",
        "json-rpc==1.10.3",
        "nose==1.3.7",
        "pyzmq==15.2.0",
        "RPi.GPIO==0.6.2"
    ],
)
