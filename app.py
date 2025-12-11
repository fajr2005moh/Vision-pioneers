from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask (__name__)
# نسمح للكل بالاتصال عشان ما يعلق
CORS(app)

# --- قاعدة البيانات (وهمية) ---
digital_wallet = {
    "national_id": "1010101010",
    "full_name": "محمد عبدالله",
    "phone_number": "0500000000",
    
    # تفاصيل المولود (السيناريو الجديد)
    "birth_notification": {
        "ref_number": "",
        "birth_date": "2025-09-01", # تاريخ الولادة (سبتمبر)
        "gender": "ذكر",
        "mother_id": "1020304050",
        "hospital": "مدينة الملك فهد الطبية"
    },
    
    # جدول التطعيمات (قاعدة بيانات)
    "vaccines_rules": [
        {"name": "تطعيم الولادة", "offset": 0},
        {"name": "تطعيم شهرين", "offset": 2},
        {"name": "تطعيم 4 أشهر", "offset": 4},
        {"name": "تطعيم 6 أشهر", "offset": 6},
        {"name": "تطعيم 9 أشهر", "offset": 9},
        {"name": "تطعيم سنة", "offset": 12},
    ]
}

# --- الروابط (APIs) ---

# 1. تفاصيل رحلة الولادة (الخطوات)
@app.route("/api/baby_journey", methods=["GET"])
def baby_journey():
    notif = digital_wallet["birth_notification"]
    return jsonify({
        "status": "success",
        "journey_name": "رحلة قدوم مولود",
        "steps": [
            {
                "title": "إشعار ولادة (مكتمل)",
                "desc": f"وصل تبليغ رقم {notif['ref_number']} من {notif['hospital']} مرتبط بهوية الأم ({notif['mother_id']})."
            },
            {
                "title": "الربط العائلي (مكتمل)",
                "desc": "تم التحقق من صلة القرابة وإشعار الأب."
            },
            {
                "title": "تسمية المولود (مطلوب إجراء)",
                "desc": "الرجاء اختيار الاسم إلكترونياً واعتماده لإصدار الشهادة."
            },
            {
                "title": "إصدار الوثائق (معلق)",
                "desc": "بانتظار التسمية لإصدار شهادة الميلاد وكرت العائلة."
            }
        ]
    })

# 2. حساب جدول التطعيمات (الذكاء هنا)
@app.route("/api/baby_vaccines", methods=["GET"])
def baby_vaccines():
    birth_str = digital_wallet["birth_notification"]["birth_date"]
    birth_date = datetime.strptime(birth_str, "%Y-%m-%d")
    
    schedule = []
    # أسماء الشهور بالعربي
    months_ar = ["", "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

    for rule in digital_wallet["vaccines_rules"]:
        # نضيف عدد الشهور على تاريخ الميلاد
        # معادلة بسيطة: الشهر الجديد = (شهر الميلاد + الإضافة)
        # نحتاج منطق dates دقيق
        
        # طريقة حساب مبسطة للعرض
        future_month_index = (birth_date.month + rule["offset"])
        future_year = birth_date.year
        
        # لو الشهر زاد عن 12، ندخل في السنة الجديدة
        while future_month_index > 12:
            future_month_index -= 12
            future_year += 1
            
        month_name = months_ar[future_month_index]
        
        schedule.append({
            "name": rule["name"],
            "due_date": f"{month_name} {future_year}", # مثال: نوفمبر 2025
            "status": "قادم"
        })

    return jsonify({"vaccines": schedule})

# 3. أقرب مركز صحي
@app.route("/api/nearest_center", methods=["GET"])
def nearest_center():
    # محاكاة: نرجع مركز ثابت
    return jsonify({
        "found": True,
        "center": {
            "name": "مركز صحي حي النموذج",
            "dist": "1.2 كم",
            "work_hours": "08:00 ص - 04:00 م"
        }
    })

# 4. رحلة التجارة (البيانات)
@app.route("/api/business_steps", methods=["GET"])
def business_steps():
    return jsonify({
        "steps": [
            {"id": 1, "title": "التحقق من الأهلية التجارية", "system": "وزارة التجارة"},
            {"id": 2, "title": "حجز الاسم التجاري", "system": "وزارة التجارة"},
            {"id": 3, "title": "إصدار السجل التجاري", "system": "وزارة التجارة"},
            {"id": 4, "title": "التوقيع الإلكتروني (عقد التأسيس)", "system": "مركز التصديق الرقمي"},
            {"id": 5, "title": "الرخصة البلدية وملف الزكاة", "system": "الربط الحكومي الموحد"}
        ]
    })

# 5. التحقق الخارجي
@app.route("/api/external_verify", methods=["POST"])
def external_verify():
    data = request.json
    phone = data.get("phone")
    
    # لازم الرقم يطابق الموجود في digital_wallet
    if phone == digital_wallet["phone_number"]:
        return jsonify({"status": "success", "msg": "تم التحقق (بيانات مطابقة)"})
    else:
        return jsonify({"status": "error", "msg": "الرقم غير مسجل"}), 400

if __name__== "__main__":
    app.run(debug=True, port=5000)