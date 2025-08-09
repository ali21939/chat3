#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تشغيل منصة تواصل - إصدار محسن ومُصحح
"""

import os
import sys
import shutil
import glob
from datetime import datetime

def clean_all_databases():
    """حذف جميع ملفات قاعدة البيانات"""
    
    print("🧹 تنظيف شامل لقاعدة البيانات...")
    
    # البحث عن جميع ملفات .db
    db_patterns = [
        '*.db',
        'instance/*.db',
        '**/*.db'
    ]
    
    for pattern in db_patterns:
        for db_file in glob.glob(pattern, recursive=True):
            try:
                if os.path.exists(db_file):
                    # إنشاء نسخة احتياطية
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_name = f"backup_{timestamp}_{os.path.basename(db_file)}"
                    shutil.copy2(db_file, backup_name)
                    print(f"💾 نسخة احتياطية: {backup_name}")
                    
                    # حذف الملف
                    os.remove(db_file)
                    print(f"🗑️ تم حذف: {db_file}")
            except Exception as e:
                print(f"⚠️ تعذر حذف {db_file}: {e}")
    
    # حذف مجلد instance بالكامل
    if os.path.exists('instance'):
        try:
            shutil.rmtree('instance')
            print("🗑️ تم حذف مجلد instance")
        except Exception as e:
            print(f"⚠️ تعذر حذف مجلد instance: {e}")
    
    # حذف ملفات cache
    cache_patterns = [
        '__pycache__',
        '*.pyc',
        '**/__pycache__',
        '**/*.pyc'
    ]
    
    for pattern in cache_patterns:
        for cache_item in glob.glob(pattern, recursive=True):
            try:
                if os.path.isdir(cache_item):
                    shutil.rmtree(cache_item)
                else:
                    os.remove(cache_item)
                print(f"🧹 تم حذف cache: {cache_item}")
            except Exception as e:
                pass  # تجاهل أخطاء cache

def setup_directories():
    """إنشاء المجلدات المطلوبة"""
    
    print("📁 إنشاء المجلدات...")
    
    folders = [
        'static/uploads',
        'static/uploads/messages',
        'static/uploads/profiles'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ مجلد جاهز: {folder}")

def main():
    """تشغيل التطبيق مع التنظيف الشامل"""
    
    print("🚀 منصة تواصل - التشغيل المُصحح")
    print("=" * 50)
    
    # تنظيف شامل
    clean_all_databases()
    setup_directories()
    
    print("\n📱 الميزات المحسنة:")
    print("   🧭 تنقل ذكي للصفحة الرئيسية")
    print("   💬 رد وتعديل وحذف الرسائل")
    print("   🔍 بحث محسن للمستخدمين والمنشورات")
    print("   🎨 مسافات محسنة وتصميم موحد")
    print("   🔧 أزرار التحكم تظهر دائماً")
    
    # استيراد وتشغيل التطبيق
    try:
        from app import app
        
        print(f"\n🌐 الموقع متاح على:")
        print(f"   http://localhost:5000")
        print(f"   http://127.0.0.1:5000")
        
        print(f"\n💡 نصائح:")
        print(f"   - أزرار التحكم في الرسائل تظهر عند التمرير")
        print(f"   - البحث يعمل للمستخدمين والمنشورات")
        print(f"   - التنقل محسن حسب حالة تسجيل الدخول")
        
        print(f"\n🔄 لإيقاف التطبيق: اضغط Ctrl+C")
        print("=" * 50)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        print("تأكد من تثبيت المتطلبات: pip install -r requirements.txt")

if __name__ == '__main__':
    main()