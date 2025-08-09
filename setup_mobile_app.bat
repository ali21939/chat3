@echo off
title إعداد تطبيق منصة تواصل المحمول
color 0B

echo.
echo ========================================
echo 📱 إعداد تطبيق منصة تواصل المحمول
echo ========================================
echo.

echo 🔧 التحقق من Flutter...
flutter doctor --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Flutter غير مثبت!
    echo.
    echo 💡 لتثبيت Flutter:
    echo    1. اذهب إلى: https://flutter.dev/docs/get-started/install/windows
    echo    2. حمل Flutter SDK
    echo    3. أضف Flutter إلى PATH
    echo    4. شغل flutter doctor للتحقق
    echo.
    pause
    exit /b 1
)

echo ✅ Flutter مثبت بنجاح
echo.

echo 📁 إنشاء مجلدات التطبيق...
if not exist "mobile_app\android\app\src\main" mkdir "mobile_app\android\app\src\main"
if not exist "mobile_app\assets\images" mkdir "mobile_app\assets\images"
if not exist "mobile_app\assets\fonts" mkdir "mobile_app\assets\fonts"

echo.
echo 📦 تحميل مكتبات Flutter...
cd mobile_app
flutter pub get

if errorlevel 1 (
    echo ❌ خطأ في تحميل المكتبات!
    echo 💡 تحقق من ملف pubspec.yaml
    pause
    exit /b 1
)

echo ✅ تم تحميل المكتبات بنجاح
echo.

echo 🔧 التحقق من إعدادات Android...
flutter doctor

echo.
echo ✅ إعداد التطبيق مكتمل!
echo.
echo 🚀 لتشغيل التطبيق:
echo    1. تأكد من تشغيل الخادم: python app.py
echo    2. شغل التطبيق: flutter run
echo.
echo 📱 أو استخدم: run_mobile.bat
echo.

pause