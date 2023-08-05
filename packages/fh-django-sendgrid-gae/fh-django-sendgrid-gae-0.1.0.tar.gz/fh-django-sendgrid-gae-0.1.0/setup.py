from setuptools import setup, find_packages

__version__ = None
with open('sgbackend/version.py') as f:
    exec(f.read())

setup(
    name='fh-django-sendgrid-gae',
    version=str(__version__),
    author='Josh Turmel',
    author_email='jt@futurehaus.com',
    url='https://gitlab.com/futurehaus/django-sendgrid-gae',
    packages=find_packages(),
    license='MIT',
    description='SendGrid Backend for Django on GAE using async task queues',
    long_description=open('./README.rst').read(),
    install_requires=["django==1.8", "sendgrid==1.4.0", "fh-django-gae-tasks==0.2.0"],
)
