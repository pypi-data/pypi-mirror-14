from setuptools import setup


_locals = {}
with open('invocare/puppet/_version.py') as fh:
    exec(fh.read(), None, _locals)
version = _locals['__version__']


setup(name='invocare-puppet',
      version=version,
      author='Justin Bronn',
      author_email='jbronn@gmail.com',
      description='Puppet Invocations',
      long_description='Implementations of Puppet-related invoke tasks.',
      license='Apache License 2.0',
      url='https://github.com/jbronn/invocare-puppet',
      download_url='https://pypi.python.org/pypi/invocare-puppet/',
      install_requires=[
        'invocare-ssh>=0.2.0,<1.0.0',
      ],
      packages=['invocare.puppet'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)
