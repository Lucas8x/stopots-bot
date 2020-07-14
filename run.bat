@echo off
setlocal enabledelayedexpansion

if not exist python\python.exe (
	echo Python portable wasn't detected; we'll download and install it for you.
	PowerShell -ExecutionPolicy Unrestricted -File "downloadpython.ps1"
)

title Stopots BOT
mode con:cols=50 lines=30
python\python.exe stopots_bot\menu.py