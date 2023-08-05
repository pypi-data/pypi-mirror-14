from setuptools import setup, find_packages

setup(
      name='homework-cli',
      version=0.1,
      packages=find_packages('.'),
      install_requires=['requests', 'PyYAML>=3.1'],
      entry_points={
        'console_scripts': [
          'homework-cli = cli.driver:main']
      },

      author='phantooom',
      author_email='zouruixp@sina.com',
      description='homework-cli',
      license='MIT',
      keywords='homework',
      url='http://fullstack.love',
      package_dir={'homework-cli': 'cli'},
)