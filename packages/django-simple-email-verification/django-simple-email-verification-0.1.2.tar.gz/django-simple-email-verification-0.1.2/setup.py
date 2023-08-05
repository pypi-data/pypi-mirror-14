from setuptools import setup

setup(
    name='django-simple-email-verification',
    version='0.1.2',
    packages=['simple_email_verification'],
    include_package_data=True,
    url='https://github.com/musashiXXX/django-simple-email-verification',
    download_url='https://github.com/musashiXXX/django-simple-email-verification/tarball/0.1.2',
    license='LICENSE.txt',
    author='Charles Hamilton',
    author_email='musashi@nefaria.com',
    description='A view decorator for verifying e-mail addresses',
    long_description='README.md',
    install_requires=[
        'Django>=1.8'
    ],
    keywords='email django'
)
