# -*- encoding: utf-8 -*-

from setuptools import setup

setup(
    name='yuntongxun-restapi-asyncio',
    version='0.1',
    packages=['yuntongxun_aiorest'],
    package_dir={'': 'src'},
    url='https://github.com/tanbro/yuntongxun-restapi-asyncio',
    license='GPL',
    author='Liu Xue Yan',
    author_email='realtanbro@gmail.com',
    description='asyncio python helper library for yuntongxun.com Restful Web API',
    keywords='yuntongxun',
    long_description=open('README.rst', encoding='utf-8').read(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Telephony',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
