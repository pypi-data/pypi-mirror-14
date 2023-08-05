from distutils.core import setup

setup(
    name='IgnoreMe_mime',
    version='1.0.0',
    author='David Dworken',
    author_email='david@daviddworken.com',
    packages=['IgnoreMe_mime'],
    url='http://pypi.python.org/pypi/IgnoreMe_mime/',
    license='LICENSE.txt',
    description='Trying to exploit a MIME sniffing vuln...',
    long_description=open('README.rst').read(),
    scripts=['uberPip/nothing.py'],
)
