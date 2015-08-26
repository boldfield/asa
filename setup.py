from setuptools import setup, find_packages
import os


def load_file(name):
    with open(name) as fs:
        content = fs.read().strip().strip('\n')
    return content


README = load_file('README.md')
VERSION = load_file(os.path.join('asa', 'VERSION'))

with open('requirements.txt', 'r') as fs:
    install_requires = filter(lambda x: bool(x), map(lambda y: y.strip('\n'), fs.readlines()))


tests_require = [
    'nose==1.2.1',
    'mock==1.0.0',
    'coverage==3.5.2',
]

entry_points = {
    'console_scripts': ['asa=asa.cmd:main']
}

setup(name='asa',
      version=VERSION,
      description='Commandline interface to Asana',
      long_description=README,
      keywords='Asana task management',
      author='Brian Oldfield',
      author_email='brian@oldfield.io',
      url='https://github.com/boldfield/asa',
      download_url='https://github.com/boldfield/asa/tarball/{}'.format(VERSION),
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(tests=tests_require),
      install_requires=install_requires,
      entry_points=entry_points,
      scripts=[],
      package_data={'asa': ['VERSION']},
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers'])
