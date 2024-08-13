@echo off
:: Enhanced Batch Script for Installing NLTK Version 3.8.1

:: Title of the command prompt window
title NLTK Installation Script

:: Check if Python is installed
echo Checking if Python is installed...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

:: Check if pip is installed
echo Checking if pip is installed...
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip and try again.
    pause
    exit /b
)

:: Install NLTK version 3.8.1
echo Installing NLTK version 3.8.1...
pip install nltk==3.8.1

:: Check if the installation was successful
if %ERRORLEVEL% EQU 0 (
    echo NLTK version 3.8.1 installed successfully!
) else (
    echo Failed to install NLTK. Please check the error messages above.
)

:: Keep the window open to review output
pause