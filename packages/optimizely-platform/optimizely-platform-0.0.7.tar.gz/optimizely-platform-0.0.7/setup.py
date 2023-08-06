from setuptools import setup
from setuptools import find_packages
 
 
setup(
    name='optimizely-platform',
    version='0.0.7',
    description='Package providing modules needed to build add-ons that run natively in the Optimizely platform.',
    author='Jon Gaulding, Tyler Jones, Peng-Wen Chen, Ali Rizvi',
    author_email='developers@optimizely.com',
    license='MIT',
    url='https://github.com/optimizely/optimizely-platform',
    download_url='https://github.com/optimizely/optimizely-platform/tarball/0.0.7',
    keywords = ['optimizely', 'platform', 'integration', 'add-on'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(
      exclude=['tests']
    )
)
