from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='py_easy_async',
      version='0.1.2',
      description='Provides simple interface for threading to easy perform async actions',
      long_description=long_description,
      author='Petrovskyi Anatolii',
      author_email='inbox@toxa.io',
      url='https://github.com/aka-toxa/py_easy_async',
      packages=['py_easy_async'],
      license='MIT',
      package_data={
        # Include readme and license
        '': ['LICENSE', 'README.rst'],
      },
      classifiers=[
                  'License :: OSI Approved :: MIT License',
                  'Intended Audience :: Developers',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
                  'Topic :: Software Development :: Libraries',
                  'Development Status :: 4 - Beta'
      ])
