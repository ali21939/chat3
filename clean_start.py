#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تشغيل نظيف للتطبيق مع حل مشكلة قاعدة البيانات
"""

import os
import shutil
import sys
from datetime import datetime

def clean_database():
    """حذف قاعدة البيانات القديمة وإنشاء واحدة جديدة"""
    
    print("🧹 تنظيف قاعدة البيانات...")
    
    # قائمة بجميع ملفات قاعدة البيانات المحتملة
    db_files = [
        'database.db',
        'instance/database.db',
        'app.db',
        'instance/app.db'
    ]
    
    # حذف جميع ملفات قاعدة البيانات
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                # إنشاء نسخة احتياطية
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"backup_{timestamp}_{os.path.basename(db_file)}"
                shutil.copy2(db_file, backup_name)
                print(f"💾 نسخة احتياطية: {backup_name}")
                
                # حذف الملف القديم
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
    
    # إنشاء المجلدات المطلوبة
    folders = [
        'static/uploads',
        'static/uploads/messages',
        'static/uploads/profiles'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 مجلد جاهز: {folder}")
    
    print("✅ تم تنظيف قاعدة البيانات بنجاح!")

def main():
    """تشغيل التطبيق مع التنظيف"""
    
    print("🚀 تشغيل منصة تواصل - إصدار محسن")
    print("=" * 50)
    
    # تنظيف قاعدة البيانات
    clean_database()
    
    print("\n📱 الميزات الجديدة:")
    print("   🧭 تنقل ذكي للصفحة الرئيسية")
    print("   💬 محادثات مع دعم الوسائط")
    print("   🔄 رد وتعديل وحذف الرسائل")
    print("   🎨 مسافات محسنة في المنشورات")
    print("   ✨ تصميم موحد ومتطور")
    
    # استيراد وتشغيل التطبيق
    try:
        from app import app
        
        print(f"\n🌐 الموقع متاح على:")
        print(f"   http://localhost:5000")
        print(f"   http://127.0.0.1:5000")
        
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