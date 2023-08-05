from setuptools import setup


setup(name='invocare',
      version=__import__('invocare').__version__,
      author='Justin Bronn',
      author_email='jbronn@gmail.com',
      description='A namespace for invocations.',
      license='Apache License 2.0',
      url='https://github.com/jbronn/invocare',
      download_url='https://pypi.python.org/pypi/invocare/',
      install_requires=[
        'invoke>=0.12.2,<1.0.0',
      ],
      packages=['invocare'],
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
