#!/usr/bin/python3

from setuptools import setup


def main():
    setup(
        name='simpleplugins',
        version='0.1.1',
        packages=[
            'simpleplugins'
        ],
        url='https://github.com/TechnicalBro/simple-python-plugins',
        license='LICENSE.txt',
        author='Brandon Curtis',
        author_email='freebird.brandon@gmail.com',
        description='Extremely simple python plugin framework!',
        test_suite='tests',
        tests_require=[
            'py',
            'pytest',
            'pytest-cov',
            'pytest-random'
        ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4'
        ],
    )


if __name__ == "__main__":
    main()
