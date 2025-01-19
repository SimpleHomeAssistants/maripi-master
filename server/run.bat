@echo off
REM 현재 배치 파일의 위치를 실행 경로로 설정
cd /d %~dp0

REM 관리자 권한 확인
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 관리자 권한으로 실행하세요!
    pause
    exit /b
)

REM Flask 서버 실행
echo Flask 서버를 실행합니다...
python run.py
pause
