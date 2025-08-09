from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
import jwt
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تفعيل CORS للتطبيق المحمول
CORS(app, origins=['*'])

db = SQLAlchemy(app)

# مفتاح JWT للتطبيق المحمول
JWT_SECRET = 'mobile_app_secret_key_2024'

# تعريف نماذج قاعدة البيانات
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(100), default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    media_path = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    shares = db.Column(db.Integer, default=0)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='comment', lazy=True, cascade='all, delete-orphan')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

# إنشاء قاعدة البيانات مع التحديثات الجديدة
with app.app_context():
    try:
        # محاولة إنشاء الجداول
        db.create_all()
        print("✅ تم إنشاء/تحديث قاعدة البيانات بنجاح!")
        
        # التحقق من وجود الأعمدة الجديدة في جدول message
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('message')]
        
        if 'message_type' not in columns or 'media_path' not in columns:
            print("⚠️ الأعمدة الجديدة غير موجودة - يجب تحديث قاعدة البيانات يدوياً")
            print("📝 قم بحذف ملف database.db وإعادة تشغيل التطبيق")
        else:
            print("✅ جميع الأعمدة موجودة ومحدثة")
            
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        print("💡 حل المشكلة: احذف ملف database.db وأعد تشغيل التطبيق")

@app.route('/')
def home():
    # إذا كان المستخدم مسجل دخول، توجيهه إلى صفحة index
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    # إذا لم يكن مسجل دخول، عرض الصفحة الرئيسية
    return render_template('home.html', user=None)

# الصفحة الرئيسية
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    for post in posts:
        post.likes_count = len(post.likes)
        post.comments_count = len(post.comments)
        post.liked_by_current = any(like.user_id == user.id for like in post.likes)

        for comment in post.comments:
            comment.likes_count = len(comment.likes)
            comment.liked_by_current = any(like.user_id == user.id for like in comment.likes)
            comment.replies_count = len(comment.replies)

    return render_template('index.html', user=user, posts=posts)

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['profile_pic'] = user.profile_pic
            session['full_name'] = user.full_name
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')

    return render_template('login.html')

# صفحة إنشاء حساب
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('كلمة المرور غير متطابقة', 'danger')
            return redirect(url_for('signup'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('اسم المستخدم أو البريد الإلكتروني موجود مسبقاً', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# إنشاء منشور جديد
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    content = request.form['post_text']
    post_type = request.form['post_type']
    media_files = request.files.getlist('post_files')

    # معالجة الملفات المتعددة
    media_paths = []
    if media_files and any(f.filename for f in media_files):
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        for media_file in media_files:
            if media_file.filename:
                # التحقق من حجم الملف (20MB)
                if len(media_file.read()) > 20 * 1024 * 1024:
                    flash(f'الملف {media_file.filename} يتجاوز الحد الأقصى 20 ميجابايت', 'error')
                    return redirect(url_for('index'))

                # إعادة تعيين مؤشر الملف
                media_file.seek(0)

                filename = f"media_{session['user_id']}_{int(time.time())}_{media_file.filename}"
                # تنظيف اسم الملف
                filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.')).rstrip()

                media_path = os.path.join(upload_folder, filename)
                media_file.save(media_path)
                media_paths.append(os.path.join('uploads', filename))

    # حفظ المسارات كسلسلة نصية مفصولة بفواصل
    media_path_for_db = ','.join(media_paths) if media_paths else None

    new_post = Post(
        content=content,
        post_type=post_type,
        media_path=media_path_for_db,
        user_id=session['user_id']
    )

    db.session.add(new_post)
    db.session.commit()

    flash('تم نشر المنشور بنجاح!', 'success')
    return redirect(url_for('index'))

# إضافة إعجاب
@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401

    user_id = session['user_id']
    post_id = request.form.get('post_id')
    comment_id = request.form.get('comment_id')

    if post_id:
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        item = Post.query.get(post_id)
    elif comment_id:
        existing_like = Like.query.filter_by(user_id=user_id, comment_id=comment_id).first()
        item = Comment.query.get(comment_id)
    else:
        return jsonify({'status': 'error', 'message': 'بيانات غير صحيحة'}), 400

    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = Like(
            user_id=user_id,
            post_id=post_id,
            comment_id=comment_id
        )
        db.session.add(new_like)
        liked = True

    db.session.commit()

    likes_count = len(item.likes)

    return jsonify({
        'status': 'success',
        'liked': liked,
        'likes_count': likes_count
    })

# مشاركة المنشور
@app.route('/share_post', methods=['POST'])
def share_post():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401

    post_id = request.form['post_id']

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'status': 'error', 'message': 'المنشور غير موجود'}), 404

    post.shares += 1
    db.session.commit()

    # إنشاء رابط المشاركة
    share_url = url_for('index', _external=True) + f'#post-{post_id}'
    share_text = f"شاهد هذا المنشور: {post.content[:100]}..."
    
    # روابط المشاركة
    whatsapp_url = f"https://wa.me/?text={share_text} {share_url}"
    instagram_url = f"https://www.instagram.com/"
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    twitter_url = f"https://twitter.com/intent/tweet?text={share_text}&url={share_url}"

    return jsonify({
        'status': 'success',
        'shares_count': post.shares,
        'share_url': share_url,
        'whatsapp_url': whatsapp_url,
        'instagram_url': instagram_url,
        'facebook_url': facebook_url,
        'twitter_url': twitter_url
    })

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('home'))  # تغيير إلى الصفحة الرئيسية

# إضافة route لعرض المنشور الفردي (للمشاركة)
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)

    # حساب الإحصائيات
    post.likes_count = len(post.likes)
    post.comments_count = len(post.comments)

    # التحقق من الإعجاب للمستخدم الحالي
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        post.liked_by_current = any(like.user_id == user.id for like in post.likes)

        for comment in post.comments:
            comment.likes_count = len(comment.likes)
            comment.liked_by_current = any(like.user_id == user.id for like in comment.likes)
            comment.replies_count = len(comment.replies)

        return render_template('post_detail.html', post=post, user=user)
    else:
        return render_template('post_detail.html', post=post, user=None)

@app.context_processor
def inject_datetime():
    return {'now': datetime.now}

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    post = Post.query.get_or_404(post_id)

    if post.user_id != session['user_id']:
        flash('غير مصرح لك بتعديل هذا المنشور', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        content = request.form['post_text']
        post_type = request.form['post_type']
        media_file = request.files.get('post_file')

        if media_file and media_file.filename:
            if post.media_path:
                old_path = os.path.join('static', post.media_path)
                if os.path.exists(old_path):
                    os.remove(old_path)

            filename = f"media_{session['user_id']}_{int(time.time())}.{media_file.filename.split('.')[-1]}"
            upload_folder = 'static/uploads'
            os.makedirs(upload_folder, exist_ok=True)
            media_path = os.path.join(upload_folder, filename)
            media_file.save(media_path)
            post.media_path = os.path.join('uploads', filename)

        post.content = content
        post.post_type = post_type

        db.session.commit()
        flash('تم تعديل المنشور بنجاح!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    post = Post.query.get_or_404(post_id)

    if post.user_id != session['user_id']:
        flash('غير مصرح لك بحذف هذا المنشور', 'danger')
        return redirect(url_for('index'))

    if post.media_path:
        full_path = os.path.join('static', post.media_path)
        if os.path.exists(full_path):
            os.remove(full_path)

    db.session.delete(post)
    db.session.commit()
    flash('تم حذف المنشور بنجاح', 'success')
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            flash('تم العثور على الحساب. يمكنك الآن إعادة تعيين كلمة المرور.', 'success')
            return redirect(url_for('reset_password', user_id=user.id))
        else:
            flash('لم يتم العثور على حساب بهذا البريد الإلكتروني.', 'danger')

    return render_template('forgot_password.html')

@app.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('كلمتا المرور غير متطابقتين.', 'danger')
            return redirect(url_for('reset_password', user_id=user.id))

        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.commit()

        flash('تم إعادة تعيين كلمة المرور بنجاح. يمكنك تسجيل الدخول الآن.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', user=user)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    current_user = None
    
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])

    users = []
    posts = []

    if query and len(query) >= 2:
        # البحث عن المستخدمين
        users = User.query.filter(
            db.or_(
                User.full_name.ilike(f'%{query}%'),
                User.username.ilike(f'%{query}%')
            )
        ).limit(10).all()

        # البحث في المنشورات
        posts = Post.query.filter(
            Post.content.ilike(f'%{query}%')
        ).order_by(Post.timestamp.desc()).limit(20).all()
        
        # إضافة إحصائيات للمنشورات
        for post in posts:
            post.likes_count = len(post.likes)
            post.comments_count = len(post.comments)
            if current_user:
                post.liked_by_current = any(like.user_id == current_user.id for like in post.likes)
            else:
                post.liked_by_current = False

    return render_template('search_results.html', 
                         user=current_user, 
                         users=users, 
                         posts=posts, 
                         query=query)


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # جلب المحادثات (آخر رسالة مع كل مستخدم)
    conversations = db.session.query(
        Message,
        User
    ).join(
        User, 
        db.or_(
            db.and_(Message.sender_id == User.id, Message.receiver_id == user_id),
            db.and_(Message.receiver_id == User.id, Message.sender_id == user_id)
        )
    ).filter(
        db.or_(Message.sender_id == user_id, Message.receiver_id == user_id)
    ).order_by(Message.timestamp.desc()).all()
    
    # تنظيم المحادثات حسب المستخدم
    chat_users = {}
    for message, user in conversations:
        other_user_id = message.sender_id if message.receiver_id == user_id else message.receiver_id
        if other_user_id not in chat_users:
            other_user = User.query.get(other_user_id)
            chat_users[other_user_id] = {
                'user': other_user,
                'last_message': message,
                'unread_count': Message.query.filter_by(
                    sender_id=other_user_id, 
                    receiver_id=user_id, 
                    is_read=False
                ).count()
            }
    
    return render_template('messages.html', chat_users=chat_users.values())

@app.route('/chat/<int:user_id>')
def chat(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    other_user = User.query.get_or_404(user_id)
    
    # جلب الرسائل بين المستخدمين
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user_id, Message.receiver_id == user_id),
            db.and_(Message.sender_id == user_id, Message.receiver_id == current_user_id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    # تحديد الرسائل كمقروءة
    Message.query.filter_by(
        sender_id=user_id, 
        receiver_id=current_user_id, 
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    
    return render_template('chat.html', other_user=other_user, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401
    
    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']
    content = request.form.get('content', '').strip()
    message_type = request.form.get('message_type', 'text')
    media_file = request.files.get('media_file')
    
    # التحقق من وجود محتوى أو ملف
    if not content and not media_file:
        return jsonify({'status': 'error', 'message': 'لا يمكن إرسال رسالة فارغة'}), 400
    
    media_path = None
    
    # معالجة الملف المرفق
    if media_file and media_file.filename:
        # التحقق من حجم الملف (10MB للمحادثات)
        if len(media_file.read()) > 10 * 1024 * 1024:
            return jsonify({'status': 'error', 'message': 'الملف يتجاوز الحد الأقصى 10 ميجابايت'}), 400
        
        # إعادة تعيين مؤشر الملف
        media_file.seek(0)
        
        # إنشاء مجلد الرسائل إذا لم يكن موجوداً
        upload_folder = 'static/uploads/messages'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # إنشاء اسم ملف فريد
        filename = f"msg_{sender_id}_{receiver_id}_{int(time.time())}_{media_file.filename}"
        filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.')).rstrip()
        
        media_path_full = os.path.join(upload_folder, filename)
        media_file.save(media_path_full)
        media_path = os.path.join('uploads/messages', filename)
        
        # تحديد نوع الرسالة بناءً على نوع الملف
        if media_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            message_type = 'image'
        elif media_file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.webm')):
            message_type = 'video'
        else:
            message_type = 'file'
    
    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content if content else None,
        message_type=message_type,
        media_path=media_path
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': {
            'id': new_message.id,
            'content': new_message.content,
            'message_type': new_message.message_type,
            'media_path': new_message.media_path,
            'timestamp': new_message.timestamp.strftime('%H:%M')
        }
    })

@app.route('/search_users')
def search_users():
    if 'user_id' not in session:
        return jsonify({'users': []}), 401
    
    query = request.args.get('q', '').strip()
    current_user_id = session['user_id']
    
    if len(query) < 2:
        return jsonify({'users': []})
    
    users = User.query.filter(
        db.and_(
            User.id != current_user_id,
            db.or_(
                User.full_name.ilike(f'%{query}%'),
                User.username.ilike(f'%{query}%')
            )
        )
    ).limit(10).all()
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name
        })
    
    return jsonify({'users': users_data})

# الرد على رسالة (إصدار مبسط)
@app.route('/reply_message', methods=['POST'])
def reply_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401
    
    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']
    content = request.form.get('content', '').strip()
    reply_to_id = request.form['reply_to_id']
    
    # التحقق من وجود محتوى
    if not content:
        return jsonify({'status': 'error', 'message': 'لا يمكن إرسال رد فارغ'}), 400
    
    # التحقق من وجود الرسالة الأصلية
    original_message = Message.query.get(reply_to_id)
    if not original_message:
        return jsonify({'status': 'error', 'message': 'الرسالة الأصلية غير موجودة'}), 404
    
    # إضافة مؤشر الرد في بداية النص
    reply_content = f"↩️ رد على: {original_message.content[:30]}...\n\n{content}"
    
    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=reply_content
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': {
            'id': new_message.id,
            'content': new_message.content,
            'timestamp': new_message.timestamp.strftime('%H:%M')
        }
    })

# تعديل رسالة (إصدار مبسط)
@app.route('/edit_message', methods=['POST'])
def edit_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401
    
    message_id = request.form['message_id']
    new_content = request.form['content'].strip()
    
    if not new_content:
        return jsonify({'status': 'error', 'message': 'لا يمكن أن تكون الرسالة فارغة'}), 400
    
    message = Message.query.get(message_id)
    if not message:
        return jsonify({'status': 'error', 'message': 'الرسالة غير موجودة'}), 404
    
    # التحقق من أن المستخدم هو مرسل الرسالة
    if message.sender_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بتعديل هذه الرسالة'}), 403
    
    # تحديث الرسالة مع مؤشر التعديل
    message.content = f"{new_content} ✏️ (تم التعديل)"
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'تم تعديل الرسالة بنجاح',
        'edited_content': message.content
    })

# حذف رسالة (إصدار مبسط)
@app.route('/delete_message', methods=['POST'])
def delete_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401
    
    message_id = request.form['message_id']
    
    message = Message.query.get(message_id)
    if not message:
        return jsonify({'status': 'error', 'message': 'الرسالة غير موجودة'}), 404
    
    # التحقق من أن المستخدم هو مرسل الرسالة
    if message.sender_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بحذف هذه الرسالة'}), 403
    
    # حذف الرسالة
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'تم حذف الرسالة بنجاح'
    })

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        new_name = request.form['new_name']
        new_email = request.form['new_email']
        current_pass = request.form['current_pass']
        new_pass = request.form['new_pass']
        confirm_new_pass = request.form['confirm_new_pass']
        profile_pic = request.files.get('profile_pic')

        # تحديث الاسم والبريد
        user.full_name = new_name
        user.email = new_email

        # تحديث صورة الملف الشخصي
        if profile_pic and profile_pic.filename:
            upload_folder = 'static/uploads/profiles'
            os.makedirs(upload_folder, exist_ok=True)

            # حذف الصورة القديمة إذا لم تكن الصورة الافتراضية
            if user.profile_pic != 'default.png':
                old_pic = os.path.join(upload_folder, user.profile_pic)
                if os.path.exists(old_pic):
                    os.remove(old_pic)

            # حفظ الصورة الجديدة
            filename = f"profile_{user.id}_{int(time.time())}.{profile_pic.filename.split('.')[-1]}"
            profile_pic.save(os.path.join(upload_folder, filename))
            user.profile_pic = filename

        # تحديث كلمة المرور إذا تم إدخالها
        if new_pass:
            if not current_pass or not check_password_hash(user.password, current_pass):
                flash("❌ كلمة المرور الحالية غير صحيحة")
                return redirect(url_for('edit_profile'))

            if new_pass != confirm_new_pass:
                flash("❌ كلمة المرور الجديدة غير متطابقة")
                return redirect(url_for('edit_profile'))

            user.password = generate_password_hash(new_pass)
        elif current_pass and not new_pass:
            # التحقق من كلمة المرور الحالية حتى لو لم يتم تغييرها
            if not check_password_hash(user.password, current_pass):
                flash("❌ كلمة المرور الحالية غير صحيحة")
                return redirect(url_for('edit_profile'))

        db.session.commit()

        # تحديث session بالبيانات الجديدة
        session['profile_pic'] = user.profile_pic
        session['full_name'] = user.full_name
        session['username'] = user.username

        flash("✅ تم تحديث الملف الشخصي بنجاح")
        return redirect(url_for('profile', username=user.username))

    return render_template('edit_profile.html', user=user)


# إضافة تعليق جديد
@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401

    try:
        post_id = request.form['post_id']
        content = request.form['content'].strip()
        parent_id = request.form.get('parent_id')  # للردود على التعليقات

        if not content:
            return jsonify({'status': 'error', 'message': 'لا يمكن إرسال تعليق فارغ'}), 400

        # التحقق من وجود المنشور
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'status': 'error', 'message': 'المنشور غير موجود'}), 404

        # إنشاء التعليق الجديد
        new_comment = Comment(
            content=content,
            user_id=session['user_id'],
            post_id=post_id,
            parent_id=parent_id if parent_id else None
        )

        db.session.add(new_comment)
        db.session.commit()

        # إرجاع بيانات التعليق الجديد
        user = User.query.get(session['user_id'])

        return jsonify({
            'status': 'success',
            'comment': {
                'id': new_comment.id,
                'content': new_comment.content,
                'user_name': user.full_name,
                'username': user.username,
                'timestamp': new_comment.timestamp.strftime('%Y-%m-%d %H:%M'),
                'parent_id': new_comment.parent_id
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء إضافة التعليق'}), 500



# الحصول على تعليقات منشور
@app.route('/get_comments/<int:post_id>')
def get_comments(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.timestamp.desc()).all()

        comments_data = []
        for comment in comments:
            # الحصول على الردود للتعليق
            replies = Comment.query.filter_by(parent_id=comment.id).order_by(Comment.timestamp.asc()).all()
            replies_data = []

            for reply in replies:
                replies_data.append({
                    'id': reply.id,
                    'content': reply.content,
                    'user_name': reply.author.full_name,
                    'username': reply.author.username,
                    'timestamp': reply.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'user_id': reply.user_id
                })

            comments_data.append({
                'id': comment.id,
                'content': comment.content,
                'user_name': comment.author.full_name,
                'username': comment.author.username,
                'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M'),
                'user_id': comment.user_id,
                'replies': replies_data
            })

        return jsonify({'status': 'success', 'comments': comments_data})

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء جلب التعليقات'}), 500


# تعديل التعليق
@app.route('/edit_comment', methods=['POST'])
def edit_comment():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401

    comment_id = request.form['comment_id']
    new_content = request.form['content']

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'status': 'error', 'message': 'التعليق غير موجود'}), 404

    # التحقق من أن المستخدم هو صاحب التعليق
    if comment.user_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بتعديل هذا التعليق'}), 403

    comment.content = new_content
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'تم تعديل التعليق بنجاح'
    })

# حذف التعليق
@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'يجب تسجيل الدخول أولاً'}), 401

    comment_id = request.form['comment_id']

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'status': 'error', 'message': 'التعليق غير موجود'}), 404

    # التحقق من أن المستخدم هو صاحب التعليق
    if comment.user_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'غير مصرح لك بحذف هذا التعليق'}), 403

    # حذف جميع الردود المرتبطة بهذا التعليق
    replies = Comment.query.filter_by(parent_id=comment.id).all()
    for reply in replies:
        db.session.delete(reply)

    # حذف التعليق الأساسي
    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'تم حذف التعليق بنجاح'
    })


# ===== API Routes للتطبيق المحمول =====

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
                'profile_pic': f"http://127.0.0.1:5000/static/uploads/profiles/{user.profile_pic}" if user.profile_pic != 'default.png' else None
            }
        })
    else:
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401

@app.route('/api/posts', methods=['GET'])
@token_required
def api_get_posts(current_user):
    """جلب المنشورات API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts_query = Post.query.order_by(Post.timestamp.desc())
    posts = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    
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

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@token_required
def api_toggle_like_post(current_user, post_id):
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

@app.route('/api/user/profile', methods=['GET'])
@token_required
def api_get_user_profile(current_user):
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

if __name__ == '__main__':
    # إنشاء مجلدات التحميلات
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/uploads/profiles', exist_ok=True)
    os.makedirs('static/uploads/messages', exist_ok=True)

    # إنشاء ملف افتراضي إذا لم يكن موجودًا
    default_img = 'static/uploads/profiles/default.png'
    if not os.path.exists(default_img):
        open(default_img, 'a').close()

    print("🚀 منصة تواصل - الموقع + API للتطبيق المحمول")
    print("=" * 50)
    print("🌐 الموقع متاح على: http://127.0.0.1:5000")
    print("📱 API متاح على: http://127.0.0.1:5000/api/")
    print("🔗 API Endpoints:")
    print("   POST /api/auth/login")
    print("   GET  /api/posts")
    print("   GET  /api/conversations")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)