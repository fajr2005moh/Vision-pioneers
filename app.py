from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# قاعدة البيانات (المحفظة)
digital_wallet = {
    "national_id": "1010101010",
    "full_name": "محمد عبدالله",
    "phone_number": "0500000000",
    "birth_notification": {
        "notification_ref": "REF-2025-9988",
        "birth_date": "2025-09-01",
        "gender": "ذكر",
        "hospital": "مدينة الملك فهد الطبية",
        "mother_name": "نورة سعد (1020304050)"
    },
    "vaccines_schedule": [
        {"name": "تطعيم الولادة", "months_offset": 0},
        {"name": "تطعيم شهرين", "months_offset": 2},
        {"name": "تطعيم 4 أشهر", "months_offset": 4},
        {"name": "تطعيم 6 أشهر", "months_offset": 6},
        {"name": "تطعيم 9 أشهر", "months_offset": 9},
        {"name": "تطعيم سنة", "months_offset": 12},
    ]
}

# 1. API رحلة المولود
@app.route("/api/baby_journey", methods=["GET"])
def baby_journey():
    notif = digital_wallet["birth_notification"]
    return jsonify({
        "status": "success",
        "birth_data": {
            "hospital": notif["hospital"],
            "ref": notif["notification_ref"],
            "date": notif["birth_date"],
            "gender": notif["gender"],
            "mother_name": notif["mother_name"]
        },
        "steps": [
            {"title": "إشعار ولادة (مكتمل)", "desc": f"وصل تبليغ من {notif['hospital']}."},
            {"title": "الربط العائلي (مكتمل)", "desc": "تم التحقق من صلة القرابة."},
            {"title": "تسمية المولود (مطلوب)", "desc": "يرجى اعتماد الاسم."},
            {"title": "إصدار الوثائق (معلق)", "desc": "بانتظار الاعتماد."}
        ]
    })

# 2. API التطعيمات
@app.route("/api/baby_vaccines", methods=["GET"])
def baby_vaccines():
    birth_date = datetime.strptime(digital_wallet["birth_notification"]["birth_date"], "%Y-%m-%d")
    schedule = []
    months_ar = ["", "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

    for rule in digital_wallet["vaccines_schedule"]:
        m_index = (birth_date.month + rule["months_offset"])
        year = birth_date.year
        while m_index > 12:
            m_index -= 12
            year += 1
        schedule.append({"name": rule["name"], "due_date": f"{months_ar[m_index]} {year}"})

    return jsonify({"vaccines": schedule})

# 3. API المركز الصحي
@app.route("/api/nearest_center", methods=["GET"])
def nearest_center():
    return jsonify({"center": {"name": "مركز صحي حي النموذج"}})

# 4. API التحقق الخارجي
@app.route("/api/external_verify", methods=["POST"])
def external_verify():
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)