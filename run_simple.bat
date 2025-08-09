@echo off
echo 🚀 تشغيل منصة تواصل - الطريقة البسيطة
echo ===============================================

:: محاولة تشغيل بـ python
python app.py 2>nul
if not errorlevel 1 goto :end

:: محاولة تشغيل بـ py
echo جاري المحاولة بـ py...
py app.py 2>nul
if not errorlevel 1 goto :end

:: محاولة تشغيل بـ python3
echo جاري المحاولة بـ python3...
python3 app.py 2>nul
if not errorlevel 1 goto :end

:: فشل في جميع المحاولات
echo ❌ فشل في تشغيل Python!
echo.
echo 💡 الحلول:
echo 1. تثبيت Python من: https://python.org
echo 2. تشغيل: fix_errors.bat
echo 3. إعادة تشغيل الكمبيوتر بعد تثبيت Python
echo.

:end
pause