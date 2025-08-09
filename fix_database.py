#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
حل سريع لمشكلة قاعدة البيانات
"""

import os
import shutil
from datetime import datetime

def fix_database():
    """حل مشكلة قاعدة البيانات"""
    
    db_file = 'database.db'
    
    print("🔧 حل مشكلة قاعدة البيانات...")
    
    # إنشاء نسخة احتياطية إذا كان الملف موجوداً
    if os.path.exists(db_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'database_backup_{timestamp}.db'
        
        try:
            shutil.copy2(db_file, backup_file)
            print(f"💾 تم إنشاء نسخة احتياطية: {backup_file}")
        except Exception as e:
            print(f"⚠️ تعذر إنشاء نسخة احتياطية: {e}")
        
        # حذف قاعدة البيانات القديمة
        try:
            os.remove(db_file)
            print(f"🗑️ تم حذف قاعدة البيانات القديمة")
        except Exception as e:
            print(f"❌ تعذر حذف قاعدة البيانات: {e}")
            return False
    
    # إنشاء المجلدات المطلوبة
    folders = [
        'static/uploads',
        'static/uploads/messages',
        'static/uploads/profiles'
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f"📁 تم إنشاء مجلد: {folder}")
            except Exception as e:
                print(f"❌ تعذر إنشاء مجلد {folder}: {e}")
    
    print("✅ تم إعداد البيئة بنجاح!")
    print("🚀 يمكنك الآن تشغيل التطبيق - ستتم إعادة إنشاء قاعدة البيانات تلقائياً")
    
    return True

if __name__ == '__main__':
    print("🛠️ أداة إصلاح قاعدة البيانات")
    print("=" * 40)
    
    if fix_database():
        print("\n🎉 تم الإصلاح بنجاح!")
        print("الآن شغل التطبيق باستخدام: python app.py")
    else:
        print("\n❌ فشل في الإصلاح!")
        print("حاول حذف ملف database.db يدوياً وأعد تشغيل التطبيق")