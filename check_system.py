#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص شامل للنظام والمتطلبات
"""

import sys
import os
import subprocess

def check_python():
    """فحص Python"""
    print("🐍 فحص Python:")
    print(f"   الإصدار: {sys.version}")
    print(f"   المسار: {sys.executable}")
    return True

def check_modules():
    """فحص المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات:")
    
    required_modules = [
        'flask',
        'flask_sqlalchemy', 
        'flask_cors',
        'jwt',
        'werkzeug',
        'os',
        'time',
        'datetime',
        'functools'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}: متاح")
        except ImportError:
            print(f"   ❌ {module}: غير متاح")
            missing_modules.append(module)
    
    return missing_modules

def check_files():
    """فحص الملفات المطلوبة"""
    print("\n📁 فحص الملفات:")
    
    required_files = [
        'app.py',
        'templates',
        'static'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}: موجود")
        else:
            print(f"   ❌ {file_path}: غير موجود")
            missing_files.append(file_path)
    
    return missing_files

def check_syntax():
    """فحص صحة كود Python"""
    print("\n🔍 فحص صحة الكود:")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'app.py', 'exec')
        print("   ✅ كود app.py: صحيح")
        return True
    except SyntaxError as e:
        print(f"   ❌ خطأ في الكود: {e}")
        return False
    except Exception as e:
        print(f"   ❌ خطأ في قراءة الملف: {e}")
        return False

def install_missing_modules(modules):
    """تثبيت المكتبات المفقودة"""
    if not modules:
        return True
    
    print(f"\n📥 تثبيت المكتبات المفقودة: {', '.join(modules)}")
    
    # تحويل أسماء المكتبات للأسماء الصحيحة لـ pip
    pip_names = {
        'flask_sqlalchemy': 'flask-sqlalchemy',
        'flask_cors': 'flask-cors',
        'jwt': 'PyJWT'
    }
    
    install_list = []
    for module in modules:
        if module in pip_names:
            install_list.append(pip_names[module])
        elif module not in ['os', 'time', 'datetime', 'functools']:  # مكتبات مدمجة
            install_list.append(module)
    
    if install_list:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + install_list)
            print("   ✅ تم تثبيت المكتبات بنجاح")
            return True
        except subprocess.CalledProcessError:
            print("   ❌ فشل في تثبيت المكتبات")
            return False
    
    return True

def create_missing_dirs():
    """إنشاء المجلدات المفقودة"""
    print("\n📁 إنشاء المجلدات المطلوبة:")
    
    dirs = [
        'static',
        'static/uploads',
        'static/uploads/profiles',
        'static/uploads/messages',
        'templates'
    ]
    
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"   ✅ تم إنشاء: {dir_path}")
        else:
            print(f"   ✅ موجود: {dir_path}")

def main():
    print("🔍 فحص شامل لمنصة تواصل")
    print("=" * 40)
    
    # فحص Python
    check_python()
    
    # فحص المكتبات
    missing_modules = check_modules()
    
    # فحص الملفات
    missing_files = check_files()
    
    # فحص صحة الكود
    syntax_ok = check_syntax()
    
    print("\n" + "=" * 40)
    print("📊 ملخص الفحص:")
    
    if missing_modules:
        print(f"❌ مكتبات مفقودة: {len(missing_modules)}")
        install_missing_modules(missing_modules)
    else:
        print("✅ جميع المكتبات متاحة")
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {len(missing_files)}")
        create_missing_dirs()
    else:
        print("✅ جميع الملفات موجودة")
    
    if syntax_ok:
        print("✅ الكود صحيح")
    else:
        print("❌ يوجد أخطاء في الكود")
    
    print("\n" + "=" * 40)
    
    if not missing_modules and not missing_files and syntax_ok:
        print("🎉 النظام جاهز للتشغيل!")
        print("🚀 شغل: python app.py")
    else:
        print("⚠️ يوجد مشاكل تحتاج إصلاح")
        print("🔧 شغل: fix_errors.bat")

if __name__ == '__main__':
    main()