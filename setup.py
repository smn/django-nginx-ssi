from setuptools import setup, find_packages

def listify(filename):
    return filter(None, open(filename,'r').read().split('\n'))

setup(
    name = "django-nginx-ssi",
    version = "0.1.1",
    url = 'http://github.com/smn/django-nginx-ssi',
    license = 'BSD',
    description = "Django SSI library for use with Nginx",
    long_description = open('README.rst', 'r').read(),
    author = 'Simon de Haan',
    author_email = "simon@praekeltfoundation.org",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = listify('requirements.pip'),
    classifiers = listify('CLASSIFIERS')
)

