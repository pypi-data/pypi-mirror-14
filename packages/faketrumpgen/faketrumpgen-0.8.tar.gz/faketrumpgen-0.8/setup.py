from setuptools import setup

setup(name='faketrumpgen',
      version='0.8',
      description='Fake trump facebook post generator',
      url='https://github.com/maxcaron/faketrumpgen',
      author='Maxime Caron',
      author_email='maximecaron@live.fr',
      license='MIT',
      packages=['faketrumpgen'],
      install_requires=[
          'Pillow',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)