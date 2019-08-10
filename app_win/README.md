# Building app:
    cd s2pace\app_win
    env\Script\activate
    Install Microsoft Visual C++ 14.0
    pip install --upgrade git+https://github.com/anthony-tuininga/cx_Freeze.git@master
    python setup.py build

TODOs:
1. Add optional config file to store server url
