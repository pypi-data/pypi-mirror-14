from setuptools import setup, find_packages
import ostrich

setup(
    name='ostrichlib',
    version=ostrich.__version__,
    author=ostrich.__author__,
    author_email='python@ostricher.com',
    url='https://www.ostricher.com/python',
    description=ostrich.__oneliner__,
    packages=['ostrich'],
    license='MIT License',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
