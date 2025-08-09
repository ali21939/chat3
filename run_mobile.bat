@echo off
echo.
echo ========================================
echo 📱 تشغيل تطبيق منصة تواصل المحمول
echo ========================================
echo.

echo 🔧 التحقق من متطلبات Flutter...
flutter doctor --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Flutter غير مثبت!
    echo 💡 يرجى تثبيت Flutter من: https://flutter.dev
    pause
    exit /b 1
)

echo ✅ Flutter مثبت بنجاح
echo.

echo 🚀 بدء تشغيل الخادم...
start "API Server" cmd /k "cd /d %~dp0 && python app.py"

echo ⏳ انتظار تشغيل الخادم...
timeout /t 3 /nobreak >nul

echo.
echo 📱 تشغيل تطبيق Flutter...
cd /d "%~dp0mobile_app"

echo 📦 تحميل المكتبات...
flutter clean
flutter pub get

if errorlevel 1 (
    echo ❌ خطأ في تحميل المكتبات!
    echo 💡 شغل: fix_mobile_app.bat
    pause
    exit /b 1
)

echo 🎯 تشغيل التطبيق...
flutter run

echo.
echo ✅ تم تشغيل التطبيق بنجاح!
pause