@echo off
title منصة تواصل - الموقع والتطبيق المحمول
color 0A

echo.
echo ========================================
echo 🚀 منصة تواصل الكاملة
echo ========================================
echo 🌐 الموقع + 📱 التطبيق المحمول
echo ========================================
echo.

echo 🔧 التحقق من المتطلبات...

:: التحقق من Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo 💡 يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)
echo ✅ Python مثبت

:: التحقق من Flutter
flutter doctor --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Flutter غير مثبت - سيتم تشغيل الموقع فقط
    set FLUTTER_AVAILABLE=false
) else (
    echo ✅ Flutter مثبت
    set FLUTTER_AVAILABLE=true
)

echo.
echo 📦 تثبيت مكتبات Python...
pip install Flask-CORS PyJWT >nul 2>&1

echo.
echo 🗄️ تنظيف قاعدة البيانات...
if exist "database.db" del "database.db"
if exist "instance\database.db" del "instance\database.db"

echo 📁 إنشاء المجلدات المطلوبة...
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\uploads\profiles" mkdir "static\uploads\profiles"
if not exist "static\uploads\messages" mkdir "static\uploads\messages"

echo.
echo 🚀 تشغيل الخادم...
echo ========================================
echo 🌐 الموقع: http://127.0.0.1:5000
echo 📱 API: http://127.0.0.1:5000/api/
echo ========================================

if "%FLUTTER_AVAILABLE%"=="true" (
    echo.
    echo 📱 سيتم تشغيل التطبيق المحمول بعد 5 ثوان...
    echo 💡 يمكنك إيقاف التطبيق والاكتفاء بالموقع بالضغط على Ctrl+C
    
    start "Flutter App" cmd /k "timeout /t 5 /nobreak >nul && cd /d %~dp0mobile_app && flutter pub get && flutter run"
)

echo.
echo 🎯 بدء تشغيل منصة تواصل...
echo.

python app.py