mode con:cols=50 lines=20
@echo off
setlocal enabledelayedexpansion

if not exist python\python.exe (
	echo Python portable wasn't detected; we'll download and install it for you.
	PowerShell -ExecutionPolicy Unrestricted -File "downloadpython.ps1"
)

python\python.exe stopots-bot.py

pause