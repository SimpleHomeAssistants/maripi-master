@echo off
REM ���� ��ġ ������ ��ġ�� ���� ��η� ����
cd /d %~dp0

REM ������ ���� Ȯ��
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ������ �������� �����ϼ���!
    pause
    exit /b
)

REM Flask ���� ����
echo Flask ������ �����մϴ�...
python run.py
pause
