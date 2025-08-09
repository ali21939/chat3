#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ملف تشغيل منصة تواصل - إصدار محسن
"""

import os
import sys

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """تشغيل التطبيق مع التحقق من المتطلبات"""
    
    print("🚀 بدء تشغيل منصة تواصل...")
    print("=" * 50)
    
    # التحقق من وجود المجلدات المطلوبة
    folders = [
        'static/uploads',
        'static/uploads/messages',
        'static/uploads/profiles'
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 تم إنشاء مجلد: {folder}")
    
    # استيراد وتشغيل التطبيق
    try:
        from app import app
        
        print("\n✅ التحسينات المطبقة:")
        print("   🧭 تحسين التنقل للصفحة الرئيسية")
        print("   💬 دعم الوسائط في المحادثات")
        print("   🎨 مسافات محسنة في المنشورات")
        print("   🌟 تصميم موحد ومتطور")
        
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
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("تأكد من تثبيت المتطلبات: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")

if __name__ == '__main__':
    main()