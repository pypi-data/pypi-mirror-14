from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='boosterpacks',
      version='0.1.1',
      description='Simple of boosterpack in Star Crusade',
      long_description=readme(),
      author='Andrew Grinevich',
      author_email='andrew.grinevich@gmail.com',
      license='MIT',
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=['boosterpacks'],
      include_package_data=True,
      zip_safe=False)