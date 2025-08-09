#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت تحديث قاعدة البيانات
إضافة الأعمدة الجديدة لدعم الوسائط في المحادثات
"""

import sqlite3
import os
from datetime import datetime

def update_database():
    """تحديث قاعدة البيانات لإضافة الأعمدة الجديدة"""
    
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ ملف قاعدة البيانات غير موجود!")
        return False
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 بدء تحديث قاعدة البيانات...")
        
        # التحقق من وجود الأعمدة الجديدة
        cursor.execute("PRAGMA table_info(message)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 الأعمدة الحالية في جدول message: {columns}")
        
        # إضافة العمود message_type إذا لم يكن موجوداً
        if 'message_type' not in columns:
            print("➕ إضافة عمود message_type...")
            cursor.execute("ALTER TABLE message ADD COLUMN message_type VARCHAR(20) DEFAULT 'text'")
            print("✅ تم إضافة عمود message_type")
        else:
            print("ℹ️ عمود message_type موجود مسبقاً")
        
        # إضافة العمود media_path إذا لم يكن موجوداً
        if 'media_path' not in columns:
            print("➕ إضافة عمود media_path...")
            cursor.execute("ALTER TABLE message ADD COLUMN media_path VARCHAR(200)")
            print("✅ تم إضافة عمود media_path")
        else:
            print("ℹ️ عمود media_path موجود مسبقاً")
        
        # تحديث الرسائل الموجودة لتكون من نوع 'text'
        cursor.execute("UPDATE message SET message_type = 'text' WHERE message_type IS NULL")
        
        # حفظ التغييرات
        conn.commit()
        
        # التحقق من النتيجة
        cursor.execute("PRAGMA table_info(message)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 الأعمدة بعد التحديث: {updated_columns}")
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        
        # إنشاء مجلدات الرفع إذا لم تكن موجودة
        upload_folders = [
            'static/uploads',
            'static/uploads/messages',
            'static/uploads/profiles'
        ]
        
        for folder in upload_folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"📁 تم إنشاء مجلد: {folder}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ ملف قاعدة البيانات غير موجود!")
        return False
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'database_backup_{timestamp}.db'
        
        # نسخ الملف
        import shutil
        shutil.copy2(db_path, backup_path)
        
        print(f"💾 تم إنشاء نسخة احتياطية: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return False

if __name__ == '__main__':
    print("🚀 سكريبت تحديث قاعدة البيانات")
    print("=" * 50)
    
    # إنشاء نسخة احتياطية أولاً
    print("1️⃣ إنشاء نسخة احتياطية...")
    if backup_database():
        print("✅ تم إنشاء النسخة الاحتياطية")
    else:
        print("⚠️ فشل في إنشاء النسخة الاحتياطية، لكن سنتابع...")
    
    print("\n2️⃣ تحديث قاعدة البيانات...")
    if update_database():
        print("\n🎉 تم تحديث قاعدة البيانات بنجاح!")
        print("يمكنك الآن تشغيل التطبيق بأمان.")
    else:
        print("\n❌ فشل في تحديث قاعدة البيانات!")
        print("تحقق من الأخطاء أعلاه وحاول مرة أخرى.")