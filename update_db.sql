-- تحديث قاعدة البيانات لدعم الوسائط في المحادثات

-- إضافة عمود نوع الرسالة
ALTER TABLE message ADD COLUMN message_type VARCHAR(20) DEFAULT 'text';

-- إضافة عمود مسار الوسائط
ALTER TABLE message ADD COLUMN media_path VARCHAR(200);

-- تحديث الرسائل الموجودة لتكون من نوع نص
UPDATE message SET message_type = 'text' WHERE message_type IS NULL;

-- عرض هيكل الجدول المحدث
.schema message