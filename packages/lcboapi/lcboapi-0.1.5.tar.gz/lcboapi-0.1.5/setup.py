from distutils.core import setup

long_description = open('README.rst').read()

setup(
  name = 'lcboapi',
  packages = ['lcboapi'],
  version = '0.1.5',
  description = 'Python wrapper for the unofficial LCBO API',
  long_description = long_description,
  author = 'Shane Martin',
  author_email = 'dev.sh@nemart.in',
  license='MIT License',
  url = 'https://github.com/shamrt/LCBOAPI',
  download_url = 'https://github.com/shamrt/LCBOAPI/archive/v0.1.5.tar.gz',
  keywords = ['api', 'lcbo'],
  platforms = ['any'],
  classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
