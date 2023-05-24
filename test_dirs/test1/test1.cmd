@echo off
setlocal
if exist .git goto test2
:test1
  cecho {cyan}Test 1
  if not exist test1.json goto wrong_dir

  set fst=c:\code\Python\projects\file_set_tool\src\file_set_tool.py
  set test1_dir=c:\code\Python\projects\file_set_tool\test_dirs\test1
  set json=%test1_dir%\test1.json
  cecho {yellow}"Current directory: %cd%"
  cecho {magenta}"python %fst% -j %json% -n TEST1 -c DESCRIPTION -s %test1_dir%\source -d %test1_dir%\dest %*"
  python %fst% -j %json% -n TEST1 -c DESCRIPTION -s %test1_dir%\source -d %test1_dir%\dest %*
  if errorlevel 1 goto abort
  call bc source dest
  
  cecho {green}"Done!"
  goto end
:test2
  cecho {cyan}Test 2 - GIT!

  set fst=c:\code\Python\projects\file_set_tool\src\file_set_tool.py
  set test2_dir=c:\code\Python\projects\file_set_tool\test_dirs\test2
  set json=%test2_dir%\test_git.json
  
  cecho {yellow}"Current directory: %cd%"
  cecho {magenta}"python %fst% -j %json% -n TEST_GIT -c DESCRIPTION -d %test2_dir%\dest -g %*"
  python %fst% -j %json% -n TEST_GIT -c DESCRIPTION -d %test2_dir%\dest -g %*
  if errorlevel 1 goto abort
  call bc source dest
  
  cecho {green}"Done!"
  goto end

:wrong_dir
  set BatchDir=%~dp0
  set BatchDir=%BatchDir:~0,-1%
  cecho {red}"Error: run this from %BatchDir%."
  goto end
:abort
  cecho {red}"Aborting!"
  goto end
:end
  endlocal
