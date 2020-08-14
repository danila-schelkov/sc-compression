@ECHO off
SET FOLDER="dist"
DEL /F/Q/S "%FOLDER%" > NUL
RMDIR /Q/S "%FOLDER%"

python setup.py sdist bdist_wheel
python -m twine upload --repository testpypi dist/*