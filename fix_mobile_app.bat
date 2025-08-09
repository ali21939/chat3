@echo off
title إصلاح التطبيق المحمول
color 0B

echo.
echo ========================================
echo 🔧 إصلاح التطبيق المحمول
echo ========================================
echo.

echo 🔍 التحقق من Flutter...
flutter doctor --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Flutter غير مثبت!
    echo 💡 حمل Flutter من: https://flutter.dev
    pause
    exit /b 1
)

echo ✅ Flutter متاح
echo.

echo 📁 إنشاء المجلدات المطلوبة...
cd mobile_app

if not exist "assets" mkdir "assets"
if not exist "assets\images" mkdir "assets\images"
if not exist "assets\icons" mkdir "assets\icons"
if not exist "assets\fonts" mkdir "assets\fonts"

echo ✅ تم إنشاء المجلدات

echo.
echo 🧹 تنظيف التطبيق...
flutter clean

echo.
echo 📦 تحميل المكتبات...
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
echo ✅ إصلاح التطبيق مكتمل!
echo.
echo 🚀 لتشغيل التطبيق:
echo    flutter run
echo.

pause