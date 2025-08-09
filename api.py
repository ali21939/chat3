#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API للتطبيق المحمول - منصة تواصل
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db, User, Post, Comment, Like, Message
import os
import time
from datetime import datetime
import jwt
from functools import wraps

# تفعيل CORS للسماح للتطبيق المحمول بالوصول
CORS(app, origins=['*'])

# مفتاح JWT للمصادقة
JWT_SECRET = 'mobile_app_secret_key_2024'

def token_required(f):
    """decorator للتحقق من صحة token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token مطلوب'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'مستخدم غير صالح'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token منتهي الصلاحية'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token غير صالح'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ===== API Routes =====

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """تسجيل دخول API"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
    
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        # إنشاء JWT token
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow().timestamp() + (24 * 60 * 60)  # صالح لـ 24 ساعة
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'profile_pic': user.profile_pic
            }
        })
    else:
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """إنشاء حساب جديد API"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'full_name', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} مطلوب'}), 400
    
    # التحقق من عدم وجود المستخدم
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'اسم المستخدم أو البريد الإلكتروني موجود مسبقاً'}), 400
    
    # إنشاء المستخدم الجديد
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # إنشاء token للمستخدم الجديد
    token = jwt.encode({
        'user_id': new_user.id,
        'username': new_user.username,
        'exp': datetime.utcnow().timestamp() + (24 * 60 * 60)
    }, JWT_SECRET, algorithm='HS256')
    
    return jsonify({
        'success': True,
        'message': 'تم إنشاء الحساب بنجاح',
        'token': token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'full_name': new_user.full_name,
            'email': new_user.email,
            'profile_pic': new_user.profile_pic
        }
    })

@app.route('/api/posts', methods=['GET'])
@token_required
def api_get_posts(current_user):
    """جلب المنشورات API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    posts_data = []
    for post in posts.items:
        # حساب الإحصائيات
        likes_count = len(post.likes)
        comments_count = len(post.comments)
        liked_by_current = any(like.user_id == current_user.id for like in post.likes)
        
        # معالجة الوسائط
        media_files = []
        if post.media_path:
            media_files = [f"http://127.0.0.1:5000/static/{media}" for media in post.media_path.split(',')]
        
        posts_data.append({
            'id': post.id,
            'content': post.content,
            'post_type': post.post_type,
            'media_files': media_files,
            'timestamp': post.timestamp.isoformat(),
            'likes_count': likes_count,
            'comments_count': comments_count,
            'shares_count': post.shares or 0,
            'liked_by_current': liked_by_current,
            'author': {
                'id': post.author.id,
                'username': post.author.username,
                'full_name': post.author.full_name,
                'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{post.author.profile_pic}" if post.author.profile_pic != 'default.png' else None
            }
        })
    
    return jsonify({
        'success': True,
        'posts': posts_data,
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    })

@app.route('/api/posts', methods=['POST'])
@token_required
def api_create_post(current_user):
    """إنشاء منشور جديد API"""
    content = request.form.get('content', '').strip()
    post_type = request.form.get('post_type', 'text')
    
    if not content:
        return jsonify({'error': 'محتوى المنشور مطلوب'}), 400
    
    # معالجة الملفات المرفقة
    media_paths = []
    media_files = request.files.getlist('media_files')
    
    if media_files:
        upload_folder = 'static/uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        for media_file in media_files:
            if media_file.filename:
                # التحقق من حجم الملف (20MB)
                if len(media_file.read()) > 20 * 1024 * 1024:
                    return jsonify({'error': f'الملف {media_file.filename} يتجاوز 20MB'}), 400
                
                media_file.seek(0)
                
                filename = f"mobile_{current_user.id}_{int(time.time())}_{media_file.filename}"
                filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.')).rstrip()
                
                media_path = os.path.join(upload_folder, filename)
                media_file.save(media_path)
                media_paths.append(os.path.join('uploads', filename))
    
    # إنشاء المنشور
    new_post = Post(
        content=content,
        post_type=post_type,
        media_path=','.join(media_paths) if media_paths else None,
        user_id=current_user.id
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'تم نشر المنشور بنجاح',
        'post': {
            'id': new_post.id,
            'content': new_post.content,
            'timestamp': new_post.timestamp.isoformat()
        }
    })

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@token_required
def api_toggle_like(current_user, post_id):
    """إعجاب/إلغاء إعجاب API"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'المنشور غير موجود'}), 404
    
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        liked = True
    
    db.session.commit()
    
    likes_count = len(post.likes)
    
    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    })

@app.route('/api/messages', methods=['GET'])
@token_required
def api_get_messages(current_user):
    """جلب الرسائل API"""
    other_user_id = request.args.get('user_id', type=int)
    
    if not other_user_id:
        return jsonify({'error': 'معرف المستخدم مطلوب'}), 400
    
    # جلب الرسائل بين المستخدمين
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.receiver_id == other_user_id),
            db.and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read,
            'sender': {
                'id': message.sender.id,
                'username': message.sender.username,
                'full_name': message.sender.full_name,
                'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{message.sender.profile_pic}" if message.sender.profile_pic != 'default.png' else None
            }
        })
    
    # تحديد الرسائل كمقروءة
    Message.query.filter(
        Message.sender_id == other_user_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).update({'is_read': True})
    db.session.commit()
    
    return jsonify({
        'success': True,
        'messages': messages_data
    })

@app.route('/api/messages', methods=['POST'])
@token_required
def api_send_message(current_user):
    """إرسال رسالة API"""
    data = request.get_json()
    
    if not data or not data.get('receiver_id') or not data.get('content'):
        return jsonify({'error': 'معرف المستلم والمحتوى مطلوبان'}), 400
    
    receiver_id = data['receiver_id']
    content = data['content'].strip()
    
    # التحقق من وجود المستلم
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'المستلم غير موجود'}), 404
    
    # إنشاء الرسالة
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'تم إرسال الرسالة بنجاح',
        'message_data': {
            'id': new_message.id,
            'content': new_message.content,
            'timestamp': new_message.timestamp.isoformat()
        }
    })

@app.route('/api/users/search', methods=['GET'])
@token_required
def api_search_users(current_user):
    """البحث عن المستخدمين API"""
    query = request.args.get('query', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'error': 'يجب أن يكون البحث أكثر من حرفين'}), 400
    
    users = User.query.filter(
        db.or_(
            User.full_name.ilike(f'%{query}%'),
            User.username.ilike(f'%{query}%')
        ),
        User.id != current_user.id  # استبعاد المستخدم الحالي
    ).limit(20).all()
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{user.profile_pic}" if user.profile_pic != 'default.png' else None
        })
    
    return jsonify({
        'success': True,
        'users': users_data
    })

@app.route('/api/conversations', methods=['GET'])
@token_required
def api_get_conversations(current_user):
    """جلب قائمة المحادثات API"""
    # جلب آخر رسالة مع كل مستخدم
    conversations = db.session.query(
        Message,
        User
    ).join(
        User, 
        db.or_(
            db.and_(Message.sender_id == User.id, Message.receiver_id == current_user.id),
            db.and_(Message.receiver_id == User.id, Message.sender_id == current_user.id)
        )
    ).filter(
        db.or_(Message.sender_id == current_user.id, Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()
    
    # تنظيم المحادثات حسب المستخدم
    chat_users = {}
    for message, user in conversations:
        other_user_id = message.sender_id if message.receiver_id == current_user.id else message.receiver_id
        if other_user_id not in chat_users:
            other_user = User.query.get(other_user_id)
            
            # حساب الرسائل غير المقروءة
            unread_count = Message.query.filter(
                Message.sender_id == other_user_id,
                Message.receiver_id == current_user.id,
                Message.is_read == False
            ).count()
            
            chat_users[other_user_id] = {
                'user': {
                    'id': other_user.id,
                    'username': other_user.username,
                    'full_name': other_user.full_name,
                    'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{other_user.profile_pic}" if other_user.profile_pic != 'default.png' else None
                },
                'last_message': {
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'sender_id': message.sender_id
                },
                'unread_count': unread_count
            }
    
    conversations_list = list(chat_users.values())
    
    return jsonify({
        'success': True,
        'conversations': conversations_list
    })

@app.route('/api/user/profile', methods=['GET'])
@token_required
def api_get_profile(current_user):
    """جلب الملف الشخصي API"""
    return jsonify({
        'success': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'full_name': current_user.full_name,
            'email': current_user.email,
            'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{current_user.profile_pic}" if current_user.profile_pic != 'default.png' else None
        }
    })

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
@token_required
def api_get_comments(current_user, post_id):
    """جلب تعليقات المنشور API"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'المنشور غير موجود'}), 404
    
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.timestamp.asc()).all()
    
    comments_data = []
    for comment in comments:
        likes_count = len(comment.likes)
        liked_by_current = any(like.user_id == current_user.id for like in comment.likes)
        
        # جلب الردود
        replies_data = []
        for reply in comment.replies:
            reply_likes_count = len(reply.likes)
            reply_liked_by_current = any(like.user_id == current_user.id for like in reply.likes)
            
            replies_data.append({
                'id': reply.id,
                'content': reply.content,
                'timestamp': reply.timestamp.isoformat(),
                'likes_count': reply_likes_count,
                'liked_by_current': reply_liked_by_current,
                'author': {
                    'id': reply.author.id,
                    'username': reply.author.username,
                    'full_name': reply.author.full_name,
                    'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{reply.author.profile_pic}" if reply.author.profile_pic != 'default.png' else None
                }
            })
        
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'timestamp': comment.timestamp.isoformat(),
            'likes_count': likes_count,
            'liked_by_current': liked_by_current,
            'replies_count': len(comment.replies),
            'replies': replies_data,
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'full_name': comment.author.full_name,
                'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{comment.author.profile_pic}" if comment.author.profile_pic != 'default.png' else None
            }
        })
    
    return jsonify({
        'success': True,
        'comments': comments_data
    })

if __name__ == '__main__':
    print("🚀 API Server للتطبيق المحمول")
    print("=" * 40)
    print("📱 API متاح على: http://127.0.0.1:5000/api/")
    print("🔗 endpoints المتاحة:")
    print("   POST /api/auth/login")
    print("   POST /api/auth/register") 
    print("   GET  /api/posts")
    print("   POST /api/posts")
    print("   GET  /api/messages")
    print("   POST /api/messages")
    print("   GET  /api/conversations")
    print("   GET  /api/users/search")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=True)