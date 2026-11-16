import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

logging.basicConfig(level=logging.INFO)

# التوكن من متغير بيئة (لا تكتبيه في الكود)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("ضعي التوكن في متغير البيئة BOT_TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


# =========================
# روابط مجلدات المواد
# =========================

SUBJECT_FOLDERS = {
    # Semester 1
    "s1_algebra": "https://drive.google.com/drive/folders/1KM2qHcBnCQbsFr1G7yx7LfHzCjJVkwME",
    "s1_english": "https://drive.google.com/drive/folders/16vhUMgexGmYSgDLU2DB-eJmxuoErlk74",
    "s1_drawing": "https://drive.google.com/drive/folders/1ptdNFv6FGed-5KImJUWXf2Cv2XEaSaHY",
    "s1_physics": "https://drive.google.com/drive/folders/13lBf1afyUSUcCXfV2rvNag76u7XFhJPH",
    "s1_chemistry": "https://drive.google.com/drive/folders/19Zd2CNa2BLr7RnL66aeK7O1MxuLpwzb-",
    "s1_elective": "https://drive.google.com/drive/folders/1tPMf04amCWwelIsmlT4VgsEVn1EnbO60",
    "s1_calculus": "https://drive.google.com/drive/folders/1LyI_tVXDHuAPijtGXUbA1ekX0E5qBSFg",

    # Semester 2
    "s2_biochem": "",
    "s2_calc2": "",
    "s2_mechanics": "",
    "s2_geom": "",
    "s2_comp": "",
    "s2_eng2": "",
    "s2_modern_phys": "",

    # Semester 3
    "s3_devices": "https://drive.google.com/drive/folders/1lkPWPcKRQGm0FFf7mg41FoUOCwnF2xpB",
    "s3_prog": "https://drive.google.com/drive/folders/1i4gNKFs008w7SVL3CNTggt8HPOFpSDAl",
    "s3_anat1": "https://drive.google.com/drive/folders/15UEHMJniZEYfX4WC5kr-shdtB28MUbI3",
    "s3_mech_eng": "https://drive.google.com/drive/folders/1Z9YP1zBMO9DFXMUaOlISi17xtyGVeWQf",
    "s3_matlab": "https://drive.google.com/drive/folders/13JB11yPSEHZ5EJILm0nEcnJc7NQfuuXZ",
    "s3_sudan": "https://drive.google.com/drive/folders/1xk3AZ58nu5QrdUP8Wx1QZRaiEkrSftBn",
    "s3_circuits1": "https://drive.google.com/drive/folders/1iAfZTvHww-Lg86sscmyD4cZCFmEe3gt3",
    "s3_diff": "https://drive.google.com/drive/folders/1zPr96L2Nx-rIzT-Vf_6qeMh4v1ETv0eg",
    "s3_materials": "https://drive.google.com/drive/folders/1vMI9Na30BdXO51nKFsw98huibk09WaZM",

    # Semester 4
    "s4_biomaterials": "https://drive.google.com/drive/folders/1CyI3lpW1RezmIV4RLfD3DRD1fEZrPi9o",
    "s4_data_struct": "https://drive.google.com/drive/folders/1r-nig8PDPOyiLtMwR6gVHvZFcQUDxnvt",
    "s4_circuits2": "https://drive.google.com/drive/folders/1iqLyQn-wOTfh0WfgBDxjsr_7-p9qIyry",
    "s4_analog": "https://drive.google.com/drive/folders/1PEvrDtxoLfgU4KfA57GLI1eRTO9VQMzb",
    "s4_applied_math": "https://drive.google.com/drive/folders/1V8JXFiWH4wST0YRQw0pISgQWeyDjfFhO",
    "s4_complex": "https://drive.google.com/drive/folders/1aWCNSM3v3OWRYGbAgk8CtUfEuJm69gmk",
    "s4_anat2": "",
    "s4_med_phys": "https://drive.google.com/drive/folders/16-Z0oAl8ZK2gG1rin6b7QijyNIDv1G6Q",

    # Semester 5
    "s5_signals": "https://drive.google.com/drive/folders/1Cqo4mwalrHXx_EvC9BGVo-q5L5E9ioG2",
    "s5_analog": "https://drive.google.com/drive/folders/1PEvrDtxoLfgU4KfA57GLI1eRTO9VQMzb",
    "s5_biomech": "https://drive.google.com/drive/folders/15PJ2nND87CpnyZeDqHfd6eENwPHqs5Rp",
    "s5_med_phys": "",
    "s5_digital": "",
    "s5_em": "",
    "s5_numerical": "",
}


# =========================
# روابط امتحانات السمسترات
# =========================

SEMESTER_EXAM_FOLDERS = {
    "1": "https://drive.google.com/drive/folders/1E7r5KoRZtOrs2mU51CpaTGCMib40IeOZ",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
}


# =========================
# المواد حسب السمستر
# =========================

SUBJECTS_BY_SEMESTER = {
    "1": [
        ("🔬 General Physics (الفيزياء العامة)", "s1_physics"),
        ("📐 Calculus I (الحسبان 1)", "s1_calculus"),
        ("🧪 General Chemistry (الكيمياء العامة)", "s1_chemistry"),
        ("📖 English I (اللغة الإنجليزية)", "s1_english"),
        ("📐 Engineering Drawing (الرسم الهندسي)", "s1_drawing"),
        ("📊 Linear Algebra (الجبر الخطي)", "s1_algebra"),
        ("📚 مهارات العرض والتواصل", "s1_elective"),
    ],

    "2": [
        ("🧬 Biochemistry (كيمياء حيوية)", "s2_biochem"),
        ("📐 Calculus II (حسبان 2)", "s2_calc2"),
        ("⚙️ Mechanics (ميكانيكا)", "s2_mechanics"),
        ("📉 Analytical Geometry (هندسة تحليلية)", "s2_geom"),
        ("💻 Computer Fundamentals (أساسيات الحاسوب)", "s2_comp"),
        ("📖 English II (لغة إنجليزية 2)", "s2_eng2"),
        ("⚛️ Modern Physics (فيزياء حديثة)", "s2_modern_phys"),
    ],

    "3": [
        ("📈 Differential Equations (معادلات تفاضلية)", "s3_diff"),
        ("⚙️ Mech Engineering Fundamentals (أساسيات الهندسة الميكانيكية)", "s3_mech_eng"),
        ("⚡ Electrical Circuits I (الدوائر الكهربائية 1)", "s3_circuits1"),
        ("🔌 Electronic Devices (النبائط الإلكترونية)", "s3_devices"),
        ("🧠 Anatomy & Physiology I (تشريح ووظائف الأعضاء 1)", "s3_anat1"),
        ("💻 Computer Programming (برمجة الحاسوب)", "s3_prog"),
        ("🇸🇩 Sudanese Studies (دراسات سودانية)", "s3_sudan"),
        ("🖥️ MATLAB (ماتلاب)", "s3_matlab"),
        ("🧱 Materials Science (علم المواد)", "s3_materials"),
    ],

    "4": [
        ("🧠 Anatomy & Physiology II (التشريح ووظائف الأعضاء 2)", "s4_anat2"),
        ("🗂️ Data Structures (بنية البيانات)", "s4_data_struct"),
        ("🩺 Medical Physics (فيزياء طبية)", "s4_med_phys"),
        ("📐 Complex Variables (دوال مركبة)", "s4_complex"),
        ("📊 Applied Mathematics (رياضيات تطبيقية)", "s4_applied_math"),
        ("⚡ Electrical Circuits II (دوائر كهربائية 2)", "s4_circuits2"),
        ("🎛️ Analog Electronics (الالكترونيات التماثلية)", "s4_analog"),
        ("🦴 Biomaterials (مواد حيوية)", "s4_biomaterials"),
    ],

    "5": [
        ("🩺 Medical Physics (فيزياء طبية)", "s5_med_phys"),
        ("🎛️ Analog Electronics (الالكترونيات التماثلية)", "s5_analog"),
        ("📡 Signals & Systems (اشارات ونظم)", "s5_signals"),
        ("💻 Digital Electronics (إلكترونيات رقمية)", "s5_digital"),
        ("🦾 Biomechanics (ميكانيكا حيوية)", "s5_biomech"),
        ("⚡ Electromagnetic Theory (النظرية الكهرومغناطيسية)", "s5_em"),
        ("🔢 Numerical Analysis (تحليل عددي)", "s5_numerical"),
    ],
}


SEMESTER_INFO = {
    "1": {"level": "1", "title": "السمستر الأول"},
    "2": {"level": "1", "title": "السمستر الثاني"},
    "3": {"level": "2", "title": "السمستر الثالث"},
    "4": {"level": "2", "title": "السمستر الرابع"},
    "5": {"level": "3", "title": "السمستر الخامس"},
}


# =========================
# لوحات الأزرار
# =========================

def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎓 المستوى الأول (Level 1)",
            callback_data="level_1_menu",
        )],
        [InlineKeyboardButton(
            text="🎓 المستوى الثاني (Level 2)",
            callback_data="level_2_menu",
        )],
        [InlineKeyboardButton(
            text="🎓 المستوى الثالث (Level 3)",
            callback_data="level_3_menu",
        )],
    ])


def level_keyboard(level):
    semesters = {
        "1": [
            ("📚 السمستر الأول (Semester 1)", "sem_1"),
            ("📚 السمستر الثاني (Semester 2)", "sem_2"),
        ],
        "2": [
            ("📚 السمستر الثالث (Semester 3)", "sem_3"),
            ("📚 السمستر الرابع (Semester 4)", "sem_4"),
        ],
        "3": [
            ("📚 السمستر الخامس (Semester 5)", "sem_5"),
        ],
    }

    rows = [
        [InlineKeyboardButton(text=label, callback_data=data)]
        for label, data in semesters[level]
    ]

    rows.append([
        InlineKeyboardButton(
            text="⬅️ رجوع للمستويات",
            callback_data="go_home",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def semester_keyboard(semester):
    rows = []

    for name, code in SUBJECTS_BY_SEMESTER[semester]:
        url = SUBJECT_FOLDERS.get(code, "").strip()

        if url:
            # اسم المادة نفسه يفتح Google Drive مباشرة
            button = InlineKeyboardButton(text=name, url=url)
        else:
            # المواد التي لم تتم إضافة روابطها بعد
            button = InlineKeyboardButton(
                text=name,
                callback_data=f"subject:{code}",
            )

        rows.append([button])

    rows.append([
        InlineKeyboardButton(
            text="📝 امتحانات السمستر لكل المواد",
            callback_data=f"semester_exams:{semester}",
        )
    ])

    level = SEMESTER_INFO[semester]["level"]

    rows.append([
        InlineKeyboardButton(
            text="⬅️ رجوع للمستوى",
            callback_data=f"level_{level}_menu",
        ),
        InlineKeyboardButton(
            text="🏠 الرئيسية",
            callback_data="go_home",
        ),
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# =========================
# أدوات مساعدة
# =========================

WELCOME = (
    "مرحباً بك في مكتبة الهندسة الطبية 🩺✨\n\n"
    "💻 <b>تم تصميم هذا البوت بواسطة: Ebtsam Murtada Fawzi</b>\n\n"
    "اختاري المستوى الدراسي:"
)


async def safe_edit(callback: CallbackQuery, text: str, markup):
    """تعديل الرسالة بدون انهيار لو ما تغيرت."""
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


# =========================
# الأوامر والتنقل
# =========================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(WELCOME, reply_markup=main_menu_keyboard())


@dp.callback_query(F.data == "go_home")
async def go_home(callback: CallbackQuery):
    await safe_edit(callback, WELCOME, main_menu_keyboard())
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^level_([123])_menu$").as_("m"))
async def show_level(callback: CallbackQuery, m):
    level = m.group(1)
    await safe_edit(
        callback,
        f"🎓 المستوى {level}\nاختاري السمستر المطلوب:",
        level_keyboard(level),
    )
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^sem_([1-5])$").as_("m"))
async def show_semester(callback: CallbackQuery, m):
    semester = m.group(1)
    await safe_edit(
        callback,
        f"📚 {SEMESTER_INFO[semester]['title']}\n"
        "اختاري المادة لفتح مجلدها مباشرة في Google Drive:",
        semester_keyboard(semester),
    )
    await callback.answer()


# =========================
# المواد التي بلا روابط
# =========================

@dp.callback_query(F.data.startswith("subject:"))
async def subject_without_link(callback: CallbackQuery):
    # لا يصل هنا إلا من الأزرار التي بلا رابط
    await callback.answer(
        "رابط مجلد هذه المادة لم يُضف بعد.",
        show_alert=True,
    )


# =========================
# امتحانات السمستر
# =========================

@dp.callback_query(F.data.startswith("semester_exams:"))
async def open_semester_exams(callback: CallbackQuery):
    semester = callback.data.split(":", 1)[1]

    if semester not in SEMESTER_INFO:
        await callback.answer("السمستر غير موجود.", show_alert=True)
        return

    url = SEMESTER_EXAM_FOLDERS.get(semester, "").strip()

    if not url:
        await callback.answer(
            "رابط مجلد امتحانات هذا السمستر لم يُضف بعد.",
            show_alert=True,
        )
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 فتح امتحانات السمستر في Google Drive",
            url=url,
        )],
    ])

    await callback.message.answer(
        f"📝 امتحانات {SEMESTER_INFO[semester]['title']} — جميع المواد",
        reply_markup=keyboard,
    )
    await callback.answer()


# =========================
# تشغيل البوت
# =========================

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
    
