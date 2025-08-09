#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ملف تشغيل منصة تواصل
تم تحسين التصميم والوظائف
"""

import sys
import os

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    
    if __name__ == '__main__':
        print("🚀 بدء تشغيل منصة تواصل...")
        print("📱 التحسينات الجديدة:")
        print("   ✅ تحسين التنقل للصفحة الرئيسية")
        print("   ✅ إضافة دعم الوسائط في المحادثات")
        print("   ✅ تحسين المسافات في المنشورات")
        print("   ✅ تصميم موحد ومحسن")
        print("   ✅ تفاعلات متقدمة")
        print()
        print("🌐 الموقع متاح على: http://localhost:5000")
        print("🔗 للوصول من الشبكة: http://0.0.0.0:5000")
        print()
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
        
except ImportError as e:
    print(f"❌ خطأ في استيراد التطبيق: {e}")
    print("تأكد من تثبيت جميع المتطلبات:")
    print("pip install flask flask-sqlalchemy werkzeug")
    
except Exception as e:
    print(f"❌ خطأ في تشغيل التطبيق: {e}")