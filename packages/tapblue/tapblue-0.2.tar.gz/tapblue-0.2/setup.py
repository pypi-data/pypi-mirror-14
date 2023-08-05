from setuptools import setup

setup(name='tapblue',
      version='0.2',
      description='The button for hackers and techies',
      url='https://github.com/nchafni/tapblue',
      author='Nezare Chafni',
      author_email='nchafni@tap.blue',
      license='MIT',
      packages=['tapblue'],
      install_requires=[
                'pubnub',
            ],
      zip_safe=False)