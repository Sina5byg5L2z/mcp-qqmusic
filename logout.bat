@echo off
cd /d "%~dp0"
if exist credential.json (
    del credential.json
    echo 已清除登录凭证。
) else (
    echo 当前未登录，无需登出。
)
pause
