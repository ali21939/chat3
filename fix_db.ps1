# سكريبت PowerShell لحل مشكلة قاعدة البيانات

Write-Host "🔧 حل مشكلة قاعدة البيانات..." -ForegroundColor Yellow

# التحقق من وجود ملف قاعدة البيانات
$dbFile = "c:\Users\ali\Desktop\pp\database.db"

if (Test-Path $dbFile) {
    Write-Host "📁 ملف قاعدة البيانات موجود - سيتم حذفه..." -ForegroundColor Cyan
    
    # إنشاء نسخة احتياطية
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = "c:\Users\ali\Desktop\pp\database_backup_$timestamp.db"
    
    try {
        Copy-Item $dbFile $backupFile
        Write-Host "💾 تم إنشاء نسخة احتياطية: $backupFile" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ تعذر إنشاء نسخة احتياطية: $_" -ForegroundColor Yellow
    }
    
    # حذف قاعدة البيانات القديمة
    try {
        Remove-Item $dbFile -Force
        Write-Host "🗑️ تم حذف قاعدة البيانات القديمة" -ForegroundColor Green
    } catch {
        Write-Host "❌ تعذر حذف قاعدة البيانات: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ℹ️ ملف قاعدة البيانات غير موجود" -ForegroundColor Blue
}

# إنشاء المجلدات المطلوبة
$folders = @(
    "c:\Users\ali\Desktop\pp\static\uploads",
    "c:\Users\ali\Desktop\pp\static\uploads\messages", 
    "c:\Users\ali\Desktop\pp\static\uploads\profiles"
)

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        try {
            New-Item -ItemType Directory -Path $folder -Force | Out-Null
            Write-Host "📁 تم إنشاء مجلد: $folder" -ForegroundColor Green
        } catch {
            Write-Host "❌ تعذر إنشاء مجلد $folder : $_" -ForegroundColor Red
        }
    } else {
        Write-Host "✅ المجلد موجود: $folder" -ForegroundColor Blue
    }
}

Write-Host ""
Write-Host "🎉 تم الإصلاح بنجاح!" -ForegroundColor Green
Write-Host "الآن يمكنك تشغيل التطبيق باستخدام: python app.py" -ForegroundColor Cyan
Write-Host "ستتم إعادة إنشاء قاعدة البيانات تلقائياً مع جميع الحقول الجديدة" -ForegroundColor Yellow