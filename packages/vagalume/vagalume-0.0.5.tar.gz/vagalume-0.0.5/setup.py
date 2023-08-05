from distutils.core import setup

version = '0.0.5'

setup(
    name='vagalume',
    version=version,
    description="Python wrapper for Vagalume API",
    long_description=open("./README.md", "r").read(),
    packages=['vagalume'],
    scripts=['bin/vagalume'],
    install_requires=open('requirements.txt').read().splitlines(),
    license='MIT License',
    author='Diego Teixeira',
    author_email='diegoteixeir4@gmail.com',
    url='https://github.com/diegoteixeir4/python-vagalume',
    keywords='vagalume song lyric translation',
    classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities",
          ],
)
