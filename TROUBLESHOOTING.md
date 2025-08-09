# 🔧 دليل إصلاح الأخطاء - منصة تواصل

## 🚨 المشاكل الشائعة والحلول

### ❌ مشكلة: "Python was not found"

#### 🔍 السبب:
Python غير مثبت أو غير مُعرف في PATH

#### 💡 الحلول:

##### الحل الأول - تثبيت من Microsoft Store:
1. اضغط `Win + R`
2. اكتب `ms-windows-store:`
3. ابحث عن "Python"
4. ثبت "Python 3.x"

##### الحل الثاني - تثبيت من الموقع الرسمي:
1. اذهب إلى: https://python.org/downloads
2. حمل أحدث إصدار
3. **مهم**: فعل "Add Python to PATH" أثناء التثبيت
4. أعد تشغيل الكمبيوتر

##### الحل الثالث - استخدام py بدلاً من python:
```cmd
py app.py
```

---

### ❌ مشكلة: "ModuleNotFoundError: No module named 'flask'"

#### 🔍 السبب:
المكتبات المطلوبة غير مثبتة

#### 💡 الحل:
```cmd
pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow
```

أو:
```cmd
py -m pip install flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow
```

---

### ❌ مشكلة: "Access is denied" أثناء تثبيت المكتبات

#### 🔍 السبب:
عدم وجود صلاحيات كافية

#### 💡 الحلول:

##### الحل الأول - تشغيل كمدير:
1. اضغط بالزر الأيمن على Command Prompt
2. اختر "Run as administrator"
3. شغل الأمر مرة أخرى

##### الحل الثاني - تثبيت للمستخدم الحالي:
```cmd
pip install --user flask flask-sqlalchemy flask-cors PyJWT werkzeug pillow
```

---

### ❌ مشكلة: "Port 5000 is already in use"

#### 🔍 السبب:
المنفذ 5000 مستخدم من برنامج آخر

#### 💡 الحلول:

##### الحل الأول - إيقاف العملية:
```cmd
netstat -ano | findstr :5000
taskkill /PID [رقم العملية] /F
```

##### الحل الثاني - استخدام منفذ آخر:
في ملف `app.py`، غير السطر الأخير إلى:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

---

### ❌ مشكلة: "Template not found"

#### 🔍 السبب:
مجلد templates غير موجود أو فارغ

#### 💡 الحل:
```cmd
mkdir templates
mkdir static
mkdir static\uploads
mkdir static\uploads\profiles
```

---

### ❌ مشكلة: "Database is locked"

#### 🔍 السبب:
قاعدة البيانات مفتوحة في برنامج آخر

#### 💡 الحل:
```cmd
del database.db
rmdir /s instance
```

---

### ❌ مشكلة: التطبيق المحمول لا يتصل بالخادم

#### 🔍 السبب:
الخادم غير مشغل أو مشاكل في الشبكة

#### 💡 الحلول:

##### تأكد من تشغيل الخادم:
```cmd
python app.py
```

##### تحقق من عنوان IP:
في كود Flutter، تأكد من استخدام:
```dart
static const String baseUrl = 'http://10.0.2.2:5000'; // للمحاكي
// أو
static const String baseUrl = 'http://192.168.1.x:5000'; // للجهاز الحقيقي
```

---

## 🛠️ أدوات الإصلاح التلقائي

### 🔧 إصلاح شامل:
```cmd
fix_errors.bat
```

### 🔍 تشخيص المشاكل:
```cmd
diagnose.bat
```

### 🧪 فحص النظام:
```cmd
python check_system.py
```

### 🚀 تشغيل بسيط:
```cmd
run_simple.bat
```

---

## 📱 مشاكل التطبيق المحمول

### ❌ مشكلة: "Flutter not found"

#### 💡 الحل:
1. حمل Flutter من: https://flutter.dev
2. استخرج الملف إلى `C:\flutter`
3. أضف `C:\flutter\bin` إلى PATH
4. شغل `flutter doctor`

### ❌ مشكلة: "No connected devices"

#### 💡 الحلول:
- **للمحاكي**: شغل Android Studio وافتح AVD Manager
- **للجهاز الحقيقي**: فعل USB Debugging

### ❌ مشكلة: "Gradle build failed"

#### 💡 الحل:
```cmd
cd mobile_app
flutter clean
flutter pub get
flutter run
```

---

## 🆘 الحصول على المساعدة

### 📋 معلومات مطلوبة عند طلب المساعدة:

1. **نظام التشغيل**: Windows 10/11
2. **إصدار Python**: `python --version`
3. **رسالة الخطأ**: نسخ كامل للخطأ
4. **الخطوات المتبعة**: ما فعلته قبل ظهور الخطأ

### 🔍 أوامر التشخيص:
```cmd
python --version
pip --version
pip list
flutter doctor
netstat -an | find "5000"
```

---

## ✅ قائمة التحقق السريع

قبل طلب المساعدة، تأكد من:

- [ ] Python مثبت ومُعرف في PATH
- [ ] المكتبات مثبتة: `pip list`
- [ ] الملفات موجودة: `app.py`, `templates/`, `static/`
- [ ] المنفذ 5000 متاح
- [ ] تم تشغيل الأوامر كمدير إذا لزم الأمر
- [ ] إعادة تشغيل الكمبيوتر بعد تثبيت Python

---

## 🎯 نصائح لتجنب المشاكل

1. **ثبت Python من الموقع الرسمي** وفعل "Add to PATH"
2. **استخدم Command Prompt كمدير** عند التثبيت
3. **أعد تشغيل الكمبيوتر** بعد تثبيت Python
4. **تأكد من اتصال الإنترنت** عند تثبيت المكتبات
5. **أغلق برامج مكافحة الفيروسات** مؤقتاً إذا منعت التثبيت

---

**🌟 مع هذا الدليل، ستتمكن من حل معظم المشاكل بسهولة! 🌟**