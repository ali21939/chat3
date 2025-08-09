@echo off
title إصلاح أخطاء منصة تواصل
color 0C

echo.
echo ========================================
echo 🔧 إصلاح أخطاء منصة تواصل
echo ========================================
echo.

echo 🔍 فحص المشاكل الشائعة...
echo.

:: التحقق من Python
echo 1️⃣ التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير مُعرف في PATH
    echo.
    echo 💡 حلول مقترحة:
    echo    أ. تثبيت Python من Microsoft Store:
    echo       - اكتب "python" في Start Menu
    echo       - اختر "Python 3.x from Microsoft Store"
    echo.
    echo    ب. تثبيت Python من الموقع الرسمي:
    echo       - اذهب إلى: https://python.org/downloads
    echo       - حمل أحدث إصدار
    echo       - تأكد من تفعيل "Add to PATH"
    echo.
    echo    ج. إذا كان Python مثبت:
    echo       - جرب: py --version
    echo       - أو: python3 --version
    echo.
    
    :: محاولة استخدام py بدلاً من python
    py --version >nul 2>&1
    if not errorlevel 1 (
        echo ✅ تم العثور على Python باستخدام 'py'
        echo 📝 سيتم استخدام 'py' بدلاً من 'python'
        
        echo.
        echo 📦 تثبيت المكتبات المطلوبة...
        py -m pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug
        
        echo.
        echo 🚀 تشغيل الموقع...
        py app.py
        goto :end
    )
    
    pause
    exit /b 1
) else (
    echo ✅ Python مثبت: 
    python --version
)

echo.
echo 2️⃣ التحقق من المكتبات المطلوبة...

:: تثبيت المكتبات
echo 📦 تثبيت/تحديث المكتبات...
pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow

if errorlevel 1 (
    echo ⚠️ خطأ في تثبيت المكتبات بـ pip، جاري المحاولة بـ py -m pip...
    py -m pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow
)

echo.
echo 3️⃣ التحقق من الملفات...

if not exist "app.py" (
    echo ❌ ملف app.py غير موجود!
    echo 💡 تأكد من وجودك في المجلد الصحيح
    pause
    exit /b 1
)

echo ✅ ملف app.py موجود

echo.
echo 4️⃣ إنشاء المجلدات المطلوبة...
if not exist "static" mkdir "static"
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\uploads\profiles" mkdir "static\uploads\profiles"
if not exist "static\uploads\messages" mkdir "static\uploads\messages"
if not exist "templates" mkdir "templates"

echo ✅ تم إنشاء المجلدات

echo.
echo 5️⃣ تنظيف قاعدة البيانات...
if exist "database.db" (
    echo 🗑️ حذف قاعدة البيانات القديمة...
    del "database.db"
)
if exist "instance\database.db" (
    del "instance\database.db"
)

echo.
echo ✅ تم إصلاح جميع المشاكل المحتملة!
echo.
echo 🚀 تشغيل الموقع...
echo ========================================
echo 🌐 الموقع: http://127.0.0.1:5000
echo ========================================

python app.py

:end
echo.
echo 🎉 انتهى الإصلاح!
pause