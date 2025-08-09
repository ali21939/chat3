@echo off
title تشخيص مشاكل منصة تواصل
color 0E

echo.
echo ========================================
echo 🔍 تشخيص مشاكل منصة تواصل
echo ========================================
echo.

echo 📋 تقرير التشخيص:
echo ========================================

echo.
echo 1️⃣ فحص Python:
echo ----------------------------------------
python --version 2>nul
if errorlevel 1 (
    echo ❌ python: غير متاح
    py --version 2>nul
    if errorlevel 1 (
        echo ❌ py: غير متاح
        echo 💡 Python غير مثبت أو غير مُعرف في PATH
    ) else (
        echo ✅ py: متاح
        py --version
    )
) else (
    echo ✅ python: متاح
    python --version
)

echo.
echo 2️⃣ فحص pip:
echo ----------------------------------------
pip --version 2>nul
if errorlevel 1 (
    echo ❌ pip: غير متاح
) else (
    echo ✅ pip: متاح
    pip --version
)

echo.
echo 3️⃣ فحص المكتبات المطلوبة:
echo ----------------------------------------

:: فحص Flask
python -c "import flask; print('✅ Flask:', flask.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Flask: غير مثبت
)

:: فحص SQLAlchemy
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy: مثبت')" 2>nul
if errorlevel 1 (
    echo ❌ Flask-SQLAlchemy: غير مثبت
)

:: فحص CORS
python -c "import flask_cors; print('✅ Flask-CORS: مثبت')" 2>nul
if errorlevel 1 (
    echo ❌ Flask-CORS: غير مثبت
)

:: فحص JWT
python -c "import jwt; print('✅ PyJWT: مثبت')" 2>nul
if errorlevel 1 (
    echo ❌ PyJWT: غير مثبت
)

echo.
echo 4️⃣ فحص الملفات:
echo ----------------------------------------
if exist "app.py" (
    echo ✅ app.py: موجود
) else (
    echo ❌ app.py: غير موجود
)

if exist "templates" (
    echo ✅ مجلد templates: موجود
) else (
    echo ❌ مجلد templates: غير موجود
)

if exist "static" (
    echo ✅ مجلد static: موجود
) else (
    echo ❌ مجلد static: غير موجود
)

echo.
echo 5️⃣ فحص المنافذ:
echo ----------------------------------------
netstat -an | find "5000" >nul
if errorlevel 1 (
    echo ✅ المنفذ 5000: متاح
) else (
    echo ⚠️ المنفذ 5000: مستخدم (قد يكون الخادم يعمل بالفعل)
)

echo.
echo 6️⃣ فحص Flutter (للتطبيق المحمول):
echo ----------------------------------------
flutter --version 2>nul
if errorlevel 1 (
    echo ❌ Flutter: غير مثبت
    echo 💡 مطلوب فقط للتطبيق المحمول
) else (
    echo ✅ Flutter: مثبت
    flutter --version | head -1
)

echo.
echo ========================================
echo 📊 ملخص التشخيص:
echo ========================================

echo.
echo 💡 الحلول المقترحة:
echo.
echo 🔧 إذا كان Python غير مثبت:
echo    - شغل: fix_errors.bat
echo    - أو ثبت Python من: https://python.org
echo.
echo 🔧 إذا كانت المكتبات غير مثبتة:
echo    - شغل: pip install -r requirements.txt
echo    - أو شغل: fix_errors.bat
echo.
echo 🔧 إذا كانت الملفات غير موجودة:
echo    - تأكد من وجودك في المجلد الصحيح
echo    - تحقق من استكمال تحميل المشروع
echo.

echo ========================================
pause