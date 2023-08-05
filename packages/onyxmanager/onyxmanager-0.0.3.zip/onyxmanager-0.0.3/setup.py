from setuptools import setup

setup(name='onyxmanager',
      version='0.0.3',
      description='OnyxManager device fact collector and setting/module manager.',
      url='http://github.com/OnyxChills/onyxmanager',
      author='Brandon Turmel',
      author_email='brandonturmel@gmail.com',
      license='GNU',
      packages=['onyxmanager'],
      install_requires=[
            'pathlib',
      ],
      zip_safe=False)