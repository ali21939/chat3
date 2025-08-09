#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار سريع لـ API التطبيق المحمول
"""

import requests
import json

# إعدادات الاختبار
BASE_URL = 'http://127.0.0.1:5000/api'
TEST_USER = {
    'username': 'test_mobile',
    'password': 'test123',
    'email': 'test@mobile.com',
    'full_name': 'مستخدم تجريبي للموبايل'
}

def test_api():
    print("🧪 اختبار API التطبيق المحمول")
    print("=" * 40)
    
    # 1. اختبار تسجيل دخول
    print("1️⃣ اختبار تسجيل الدخول...")
    
    login_data = {
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                token = result['token']
                user = result['user']
                print(f"   ✅ تسجيل دخول ناجح!")
                print(f"   👤 المستخدم: {user['full_name']}")
                print(f"   🔑 Token: {token[:20]}...")
                
                # 2. اختبار جلب المنشورات
                print("\n2️⃣ اختبار جلب المنشورات...")
                headers = {'Authorization': f'Bearer {token}'}
                
                posts_response = requests.get(f'{BASE_URL}/posts', headers=headers)
                print(f"   📡 Status: {posts_response.status_code}")
                
                if posts_response.status_code == 200:
                    posts_result = posts_response.json()
                    if posts_result.get('success'):
                        posts = posts_result['posts']
                        print(f"   ✅ تم جلب {len(posts)} منشور")
                        
                        if posts:
                            print(f"   📝 أول منشور: {posts[0]['content'][:50]}...")
                    else:
                        print(f"   ❌ خطأ: {posts_result.get('error')}")
                else:
                    print(f"   ❌ خطأ HTTP: {posts_response.status_code}")
                
                # 3. اختبار جلب المحادثات
                print("\n3️⃣ اختبار جلب المحادثات...")
                
                conv_response = requests.get(f'{BASE_URL}/conversations', headers=headers)
                print(f"   📡 Status: {conv_response.status_code}")
                
                if conv_response.status_code == 200:
                    conv_result = conv_response.json()
                    if conv_result.get('success'):
                        conversations = conv_result['conversations']
                        print(f"   ✅ تم جلب {len(conversations)} محادثة")
                    else:
                        print(f"   ❌ خطأ: {conv_result.get('error')}")
                else:
                    print(f"   ❌ خطأ HTTP: {conv_response.status_code}")
                
                print("\n🎉 جميع اختبارات API نجحت!")
                print("📱 التطبيق المحمول جاهز للاتصال!")
                
            else:
                print(f"   ❌ فشل تسجيل الدخول: {result.get('error')}")
        else:
            print(f"   ❌ خطأ HTTP: {response.status_code}")
            print(f"   📄 الاستجابة: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ خطأ في الاتصال!")
        print("   💡 تأكد من تشغيل الخادم أولاً: python app.py")
    except Exception as e:
        print(f"   ❌ خطأ غير متوقع: {e}")

if __name__ == '__main__':
    test_api()