# @Author: BingWu Yang <detailyang>
# @Date:   2016-03-30T20:27:36+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-03-31T10:42:42+08:00
# @License: The MIT License (MIT)


from setuptools import setup, find_packages

setup(
    name = 'esl',
    version = '0.0.3',
    keywords = ('esl', 'eva-shell-language'),
    description = 'eva shell language for eva-shell',
    license = 'MIT License',
    install_requires = ['ply>=3.8'],

    author = 'detailyang',
    author_email = 'detailyang@gmail.com',

    packages = find_packages(),
    platforms = 'any',
)
