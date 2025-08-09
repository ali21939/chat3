@echo off
title منصة تواصل - الموقع والتطبيق المحمول
color 0A

echo.
echo ========================================
echo 🌟 منصة تواصل - الموقع والتطبيق المحمول
echo ========================================
echo.

:: التحقق من Python
echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير متاح، جاري المحاولة بـ py...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python غير مثبت!
        echo.
        echo 💡 لإصلاح المشكلة:
        echo    1. شغل: fix_errors.bat
        echo    2. أو ثبت Python من: https://python.org
        echo.
        pause
        exit /b 1
    ) else (
        echo ✅ تم العثور على Python
        set PYTHON_CMD=py
    )
) else (
    echo ✅ Python متاح
    set PYTHON_CMD=python
)

:: التحقق من المكتبات
echo 🔍 التحقق من المكتبات...
%PYTHON_CMD% -c "import flask, flask_sqlalchemy, flask_cors, jwt" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ بعض المكتبات غير مثبتة، جاري التثبيت...
    %PYTHON_CMD% -m pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow
    if errorlevel 1 (
        echo ❌ فشل في تثبيت المكتبات!
        echo 💡 شغل: fix_errors.bat لإصلاح المشكلة
        pause
        exit /b 1
    )
)

echo ✅ المكتبات متاحة

echo.
echo 🧹 تنظيف قاعدة البيانات...
if exist "database.db" del /f "database.db"
if exist "instance" rmdir /s /q "instance" 2>nul
if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul

echo 📁 إنشاء المجلدات...
if not exist "static" mkdir "static"
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\uploads\messages" mkdir "static\uploads\messages"
if not exist "static\uploads\profiles" mkdir "static\uploads\profiles"

echo ✅ التحضيرات مكتملة!
echo.
echo 🌟 الميزات المتاحة:
echo    🌐 موقع ويب كامل
echo    📱 API للتطبيق المحمول
echo    💬 محادثات متقدمة
echo    🔍 بحث ذكي
echo    🎨 تصميم موحد
echo.
echo 🚀 بدء التشغيل...
echo ========================================
echo 🌐 الموقع: http://127.0.0.1:5000
echo 📱 API: http://127.0.0.1:5000/api/
echo ========================================
echo.

%PYTHON_CMD% app.py

pause