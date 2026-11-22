@echo off
setlocal EnableExtensions
title COIL Group 2 - Lanzador de Pagina Web
cd /d "%~dp0"
if exist "servidor\server_https.py" cd /d "%~dp0.."

set "OPEN_BROWSER=1"
set "STAY_OPEN=1"
set "URL=https://www.coil-group2.com/"
set "DNS_STATUS="
set "WEB_STATUS="

:parse_args
if "%~1"=="" goto :args_done
if /i "%~1"=="--no-browser" set "OPEN_BROWSER=0"
if /i "%~1"=="--no-wait" set "STAY_OPEN=0"
shift
goto :parse_args

:args_done
if not exist "modulo2\servidor\server_https.py" goto :missing_files
if not exist "modulo2\dns\dns_server.py" goto :missing_files
goto :files_ok

:missing_files
echo [ERROR] No se encontraron los archivos requeridos en modulo2\.
if "%STAY_OPEN%"=="1" pause
exit /b 1

:files_ok
set "PYTHON_EXE="
for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%I"
if defined PYTHON_EXE goto :python_ok
for /f "delims=" %%I in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%I"
if defined PYTHON_EXE goto :python_ok

echo [ERROR] Python 3 no encontrado en PATH.
if "%STAY_OPEN%"=="1" pause
exit /b 1

:python_ok
set "PYTHONW_EXE=%PYTHON_EXE:python.exe=pythonw.exe%"
if not exist "%PYTHONW_EXE%" set "PYTHONW_EXE=%PYTHON_EXE%"

echo ============================================================
echo   COIL Group 2 - Lanzador de Pagina Web SD-WAN
echo ============================================================
echo.

netstat -ano -p UDP | findstr /R /C:"0\.0\.0\.0:53 " >nul 2>&1
if not errorlevel 1 goto :dns_already_running

"%PYTHON_EXE%" -c "import dnslib" >nul 2>&1
if errorlevel 1 goto :dns_missing_lib

powershell -NoProfile -Command "$q=[char]34; $w='%PYTHONW_EXE%'; $d=(Get-Location).Path; $c=$q+$w+$q+' -u '+$q+$d+'\modulo2\dns\dns_server.py'+$q; Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$c; CurrentDirectory=$d} | Out-Null" >nul 2>&1
set "DNS_STATUS=[OK] Servidor DNS iniciado en UDP 53."
echo %DNS_STATUS%
goto :check_web

:dns_missing_lib
set "DNS_STATUS=[AVISO] Modulo dnslib no instalado (pip install dnslib). El servidor DNS no se inicio."
echo %DNS_STATUS%
goto :check_web

:dns_already_running
set "DNS_STATUS=[OK] Servidor DNS ya esta activo en UDP 53."
echo %DNS_STATUS%

:check_web
curl.exe -skI --max-time 2 https://127.0.0.1/ 2>nul | findstr /C:"200 OK" >nul 2>&1
if not errorlevel 1 goto :web_already_running

echo [INFO] Reiniciando servidor web HTTP/HTTPS...
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name like ''python%''' | Where-Object { $_.CommandLine -match 'server_https\.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
timeout /t 1 /nobreak >nul

powershell -NoProfile -Command "$q=[char]34; $w='%PYTHONW_EXE%'; $d=(Get-Location).Path; $c=$q+$w+$q+' -u '+$q+$d+'\modulo2\servidor\server_https.py'+$q; Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$c; CurrentDirectory=$d} | Out-Null" >nul 2>&1
set /a TRIES=0

:wait_web
if %TRIES% GEQ 8 goto :web_timeout
timeout /t 1 /nobreak >nul
set /a TRIES+=1
curl.exe -skI --max-time 2 https://127.0.0.1/ 2>nul | findstr /C:"200 OK" >nul 2>&1
if errorlevel 1 goto :wait_web
set "WEB_STATUS=[OK] Servidor Web HTTP/HTTPS iniciado y respondiendo en puertos 80 y 443."
echo %WEB_STATUS%
goto :open_browser_check

:web_timeout
echo [ERROR] No se pudo iniciar el servidor HTTPS en el puerto 443. Verifica que ningun otro programa ocupe el puerto 80 o 443.
if "%STAY_OPEN%"=="1" pause
exit /b 1

:web_already_running
set "WEB_STATUS=[OK] Servidor Web HTTP/HTTPS ya esta activo y respondiendo en puertos 80 y 443."
echo %WEB_STATUS%

:open_browser_check
if "%OPEN_BROWSER%"=="1" start "" "%URL%"
if "%STAY_OPEN%"=="0" exit /b 0

:menu
cls
echo ============================================================
echo   COIL Group 2 - Servicios Activos
echo ============================================================
echo.
echo   %DNS_STATUS%
echo   %WEB_STATUS%
echo.
echo   Portal Principal : https://www.coil-group2.com/
echo   UniLlanos        : https://www.coil-group2.com/unillanos/
echo   Seneca           : https://www.coil-group2.com/seneca/
echo   IP ZeroTier      : https://172.22.201.2/
echo   Certificado CA   : https://www.coil-group2.com/ca.crt
echo.
echo ============================================================
echo   [R] Reabrir pagina en el navegador
echo   [D] Detener servidores DNS y Web y salir
echo   [S] Salir dejando los servidores activos en segundo plano
echo ============================================================
echo.
choice /c RDS /n /m "Selecciona una opcion [R/D/S]: "
if errorlevel 3 goto :exit_keep
if errorlevel 2 goto :stop_servers
if errorlevel 1 goto :reopen_browser
goto :menu

:reopen_browser
start "" "%URL%"
goto :menu

:stop_servers
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name like ''python%''' | Where-Object { $_.CommandLine -match 'dns_server\.py|server_https\.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo.
echo [OK] Servidores COIL detenidos.
timeout /t 2 /nobreak >nul
exit /b 0

:exit_keep
echo.
echo [OK] Los servidores siguen activos en segundo plano.
exit /b 0
