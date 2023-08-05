from distutils.core import setup


setup(
    name = 'multidevice',
    packages = ['multidevice'],
    version = '0.1',
    description = 'Application to manage user session across multiple devices.',
    author = 'Hari Kishan',
    author_email = 'hari.kishan81001@gmail.com',
    url = 'https://github.com/harkishan81001/multi-device-login.git',
    keywords = ['User Session', 'Login', 'Django'],
    install_requires = [
        "Django >= 1.6",
        "djangorestframework == 3.3.2",
    ],
)
