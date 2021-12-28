rem 2020/04/27 21:52

@echo off
set CURRENT_DIR=%~dp0
set DIST_PATH=%CURRENT_DIR%_documents_\_license_\

echo %CURRENT_DIR%
echo %DIST_PATH%
%CURRENT_DIR%\ENV\Scripts\python -m pip install tensorflow seaborn sklearn pygame autopep8 flake8 pip-licenses pipdeptree

%CURRENT_DIR%ENV\Scripts\python -m pip list > %DIST_PATH%pip_list.txt
%CURRENT_DIR%ENV\Scripts\pip-licenses > %DIST_PATH%pip_licenses.txt
%CURRENT_DIR%ENV\Scripts\pipdeptree > %DIST_PATH%pip_tree.txt