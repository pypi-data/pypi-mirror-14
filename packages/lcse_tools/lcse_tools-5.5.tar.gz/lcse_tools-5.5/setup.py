#import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "lcse_tools",
    version = "5.5",
    author = "Stou Sandalski",
    author_email = "sandalski@astro.umn.edu",
    description = ("Misc tools"),
    scripts = ('src/dpp_server.py', 'src/eval_pp.py', 'src/plot_rprofiles.py', 'src/check_missing.py',
               'src/pngs2movies.py', 'src/layer_images.py'),
    data_files = [('fonts', ['fonts/README.txt', 'fonts/LICENSE.txt', 'fonts/Roboto-Black.ttf',
                              'fonts/Roboto-Bold.ttf', 'fonts/Roboto-Light.ttf', 'fonts/Roboto-Medium.ttf',
                              'fonts/Roboto-Regular.ttf', 'fonts/Roboto-Thin.ttf'])],
    packages = ['lcse_tools'],
    package_dir = {'lcse_tools':'lib'},
#    package_data = {'':['fonts/*.txt', 'fonts/*.ttf']},
    install_requires = ['colorlog', 'numpy', 'lcse', 'lockfile'],
    license = "Apache 2.0",
    keywords = "utils",
    url = "",
    zip_safe=False,
#    long_description=read('README'),
#    classifiers=[
#        "Development Status :: 3 - Alpha",
#        "Topic :: Libraries",
#    ],
)
