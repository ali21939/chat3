// 🚀 تحسينات التفاعل والحركة للموقع

document.addEventListener('DOMContentLoaded', function() {
    
    // 🎨 تأثيرات الحركة المتقدمة
    initAdvancedAnimations();
    
    // 📱 تحسين التفاعل مع المنشورات
    enhancePostInteractions();
    
    // 🔍 تحسين البحث
    enhanceSearchFunctionality();
    
    // 💬 تحسين التعليقات
    enhanceCommentSystem();
    
    // 🎯 تحسين الأزرار والتفاعلات
    enhanceButtonInteractions();
    
    // 📊 تحسين الإحصائيات المباشرة
    enhanceLiveStats();
    
    // 🌟 تأثيرات بصرية إضافية
    addVisualEffects();
});

// 🎨 تأثيرات الحركة المتقدمة
function initAdvancedAnimations() {
    // تأثير الظهور التدريجي للمنشورات
    const posts = document.querySelectorAll('.post');
    posts.forEach((post, index) => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            post.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            post.style.opacity = '1';
            post.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // تأثير التمرير الناعم للشريط العلوي
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // التمرير لأسفل - إخفاء الشريط
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // التمرير لأعلى - إظهار الشريط
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
        
        // تأثير الشفافية
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// 📱 تحسين التفاعل مع المنشورات
function enhancePostInteractions() {
    // تأثير الماوس على المنشورات
    document.querySelectorAll('.post').forEach(post => {
        post.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.2)';
        });
        
        post.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
        });
        
        // تتبع حركة الماوس للتأثيرات البصرية
        post.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            this.style.setProperty('--mouse-x', x + '%');
            this.style.setProperty('--mouse-y', y + '%');
        });
    });
    
    // تحسين أزرار الإعجاب
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // تأثير القلب المتحرك
            const heart = this.querySelector('i');
            heart.style.animation = 'heartbeat 0.6s ease-in-out';
            
            // إضافة جسيمات القلوب
            createHeartParticles(e.clientX, e.clientY);
            
            setTimeout(() => {
                heart.style.animation = '';
            }, 600);
        });
    });
}

// 🔍 تحسين البحث
function enhanceSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    
    if (searchInput && searchForm) {
        let searchTimeout;
        
        // البحث المباشر أثناء الكتابة
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performLiveSearch(query);
                }, 300);
            }
        });
        
        // تأثيرات بصرية للبحث
        searchInput.addEventListener('focus', function() {
            searchForm.style.transform = 'scale(1.05)';
            searchForm.style.boxShadow = '0 0 30px rgba(102, 126, 234, 0.3)';
        });
        
        searchInput.addEventListener('blur', function() {
            searchForm.style.transform = 'scale(1)';
            searchForm.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        });
    }
}

// 💬 تحسين التعليقات
function enhanceCommentSystem() {
    // تحسين نماذج التعليقات فقط (تجنب التعارض مع الكود الموجود)
    document.querySelectorAll('.comment-form textarea').forEach(textarea => {
        textarea.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.2)';
        });
        
        textarea.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
            this.parentElement.style.boxShadow = 'none';
        });
    });
}

// 🎯 تحسين الأزرار والتفاعلات
function enhanceButtonInteractions() {
    // تأثير الموجة للأزرار
    document.querySelectorAll('.btn, .action-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // تحسين أزرار المشاركة
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // تأثير دوران الأيقونة
            const icon = this.querySelector('i');
            icon.style.transform = 'rotate(360deg)';
            icon.style.transition = 'transform 0.6s ease-in-out';
            
            setTimeout(() => {
                icon.style.transform = 'rotate(0deg)';
            }, 600);
        });
    });
}

// 📊 تحسين الإحصائيات المباشرة
function enhanceLiveStats() {
    // تحديث الإحصائيات بشكل متحرك
    function animateCounter(element, target) {
        const start = parseInt(element.textContent) || 0;
        const increment = (target - start) / 20;
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 50);
    }
    
    // مراقبة تغييرات الإحصائيات
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
                const target = mutation.target;
                if (target.classList && target.classList.contains('likes-count')) {
                    const newValue = parseInt(target.textContent);
                    if (!isNaN(newValue)) {
                        animateCounter(target, newValue);
                    }
                }
            }
        });
    });
    
    document.querySelectorAll('.likes-count, .shares-count').forEach(counter => {
        observer.observe(counter, { childList: true, characterData: true, subtree: true });
    });
}

// 🌟 تأثيرات بصرية إضافية
function addVisualEffects() {
    // إضافة جسيمات متحركة في الخلفية
    createBackgroundParticles();
    
    // تأثير التوهج للعناصر التفاعلية
    document.querySelectorAll('.avatar, .logo').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.filter = 'drop-shadow(0 0 20px rgba(102, 126, 234, 0.5))';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.filter = 'none';
        });
    });
    
    // تأثير الكتابة المتحركة للعناوين
    const titles = document.querySelectorAll('.auth-title, .logo span');
    titles.forEach(title => {
        const text = title.textContent;
        title.textContent = '';
        
        for (let i = 0; i < text.length; i++) {
            setTimeout(() => {
                title.textContent += text[i];
            }, i * 100);
        }
    });
}

// 🎨 إنشاء جسيمات القلوب
function createHeartParticles(x, y) {
    for (let i = 0; i < 6; i++) {
        const heart = document.createElement('div');
        heart.innerHTML = '❤️';
        heart.style.position = 'fixed';
        heart.style.left = x + 'px';
        heart.style.top = y + 'px';
        heart.style.fontSize = '12px';
        heart.style.pointerEvents = 'none';
        heart.style.zIndex = '9999';
        heart.style.animation = `heartFloat 2s ease-out forwards`;
        heart.style.animationDelay = i * 0.1 + 's';
        
        document.body.appendChild(heart);
        
        setTimeout(() => {
            heart.remove();
        }, 2000);
    }
}

// 🌌 إنشاء جسيمات الخلفية
function createBackgroundParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.pointerEvents = 'none';
    particlesContainer.style.zIndex = '-1';
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.background = 'rgba(102, 126, 234, 0.3)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${3 + Math.random() * 4}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 2 + 's';
        
        particlesContainer.appendChild(particle);
    }
    
    document.body.appendChild(particlesContainer);
}

// 🔍 البحث المباشر
function performLiveSearch(query) {
    // هنا يمكن إضافة منطق البحث المباشر
    console.log('البحث عن:', query);
    
    // إظهار مؤشر التحميل
    const searchBtn = document.querySelector('.search-btn');
    const originalContent = searchBtn.innerHTML;
    searchBtn.innerHTML = '<div class="loading"></div>';
    
    // محاكاة استعلام البحث
    setTimeout(() => {
        searchBtn.innerHTML = originalContent;
    }, 1000);
}

// 🎭 تأثيرات CSS إضافية
const additionalStyles = `
    @keyframes heartFloat {
        0% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-100px) scale(0.5);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    .loading {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .navbar {
        transition: transform 0.3s ease-in-out;
    }
    
    .post {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .comments-section {
        transition: all 0.4s ease-out;
    }
`;

// إضافة الأنماط الإضافية
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// 🚀 تحسينات الأداء
// تأخير تحميل الصور
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// تشغيل تحسينات الأداء
lazyLoadImages();

// 📱 تحسينات الهاتف المحمول
if (window.innerWidth <= 768) {
    // تحسينات خاصة بالهاتف المحمول
    document.body.classList.add('mobile-optimized');
    
    // تحسين اللمس
    document.querySelectorAll('.post, .btn').forEach(element => {
        element.style.touchAction = 'manipulation';
    });
}

console.log('🚀 تم تحميل جميع التحسينات بنجاح!');