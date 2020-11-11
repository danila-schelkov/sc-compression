import setuptools

with open('README.md') as fh:
    long_description = fh.read()
    fh.close()

with open('requirements.txt') as fh:
    requirements = [line for line in fh.readlines() if line != '']
    fh.close()

setuptools.setup(
    name='sc-compression',
    version='0.3.0',
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
    install_require=requirements
)
