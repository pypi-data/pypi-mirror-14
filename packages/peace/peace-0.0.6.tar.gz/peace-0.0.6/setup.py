from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(name='peace',
      version='0.0.6',
      description='REST client',
      long_description=long_description,
      url='https://bitbucket.org/garymonson/peace',
      author='Gary Monson',
      author_email='gary.monson@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='rest client',
      packages=['peace'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
