@echo off
setlocal
goto begin

rem poetry env info

rem If the venv is not local (on Mac), you can delete the one created
rem and use this setting to then create on that's local.
rem
rem poetry config virtualenvs.in-project true

rem Add a dependency:
rem poetry add requests

rem Then remove the a dependency with:
rem poetry remove requests

rem Publishing:
rem poetry config repositories.test-pypi https://test.pypi.org/legacy
rem get the token at the https://test.pypi.org/legacy web site.
rem poetry config pypi-token.test-pypi pypi...token
rem after build, you can publish with
rem poetry publish pypi..
rem To build and publish:
rem poetry publish --build -r test-pypi

rem Build
rem    poetry build

rem hmm... cant ad this:
rem [tool.poetry.entrypoints]
rem console_scripts = "file_set_tool=main:main"

:begin

echo Building...

goto end

:end
    endlocal
