from setuptools import setup, find_packages
import nicetable

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='nicetable',
    version=nicetable.__version__,
    python_requires='>=3.6',
    author='Ofir Manor',
    author_email='ofir.manor@gmail.com',
    description='A clean and elegant way to print tables with minimal boilerplate code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ofirmanor/nicetable',
    license='MIT',
    keywords='table tabular textual display data formatter ascii',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
    ],
)
