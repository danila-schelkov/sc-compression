import setuptools

with open('README.md') as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name='sc-compression',
    version='0.2.6',
    author='Vorono4ka',
    author_email='crowo4ka@gmail.com',
    description='SC Compression',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vorono4ka/sc-compression',
    license='GPLv3',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
