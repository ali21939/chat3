@echo off
title تشغيل سريع للتطبيق المحمول
color 0B

echo 🚀 تشغيل سريع للتطبيق المحمول
echo ===============================================

cd mobile_app

echo 🧹 تنظيف...
flutter clean >nul 2>&1

echo 📦 تحميل المكتبات...
flutter pub get

if errorlevel 1 (
    echo ❌ خطأ في المكتبات!
    pause
    exit /b 1
)

echo 🎯 تشغيل التطبيق...
flutter run

pause