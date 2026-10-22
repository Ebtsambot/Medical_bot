import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# توكن البوت الخاص بكِ من BotFather
TOKEN="8513184138:AAGIfp6PhqrzVgdfjolmA06yjv-KCZitcNA"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- 1. القائمة الرئيسية (عرض المستويات الثلاثة) ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الأول (Level 1)",
                  callback_data="level_1_menu",
              )
          ],
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الثاني (Level 2)",
                  callback_data="level_2_menu",
              )
          ],
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الثالث (Level 3)",
                  callback_data="level_3_menu",
              )
          ],
      ]
  )
  await message.answer(
      "أهلاً بكِ يا باش مهندسة في مكتبة الهندسة الطبية 🩺✨\nاختر المستوى"
      " الدراسي:",
      reply_markup=keyboard,
  )


# --- 2. قوائم المستويات والسمسترات ---


# المستوى الأول (سمستر 1 و 2)
@dp.callback_query(F.data == "level_1_menu")
async def show_level_1(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📚 السمستر الأول (Semester 1)",
                  callback_data="sem_1",
              )
          ],
          [
              InlineKeyboardButton(
                  text="📚 السمستر الثاني (Semester 2)",
                  callback_data="sem_2",
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ رجوع للمستويات", callback_data="go_home"
              )
          ],
      ]
  )
  await callback.message.edit_text(
      "🎓 **المستوى الأول**\nاختر السمستر المطلوب:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )
  await callback.answer()


# المستوى الثاني (سمستر 3 و 4)
@dp.callback_query(F.data == "level_2_menu")
async def show_level_2(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📚 السمستر الثالث (Semester 3)",
                  callback_data="sem_3",
              )
          ],
          [
              InlineKeyboardButton(
                  text="📚 السمستر الرابع (Semester 4)",
                  callback_data="sem_4",
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ رجوع للمستويات", callback_data="go_home"
              )
          ],
      ]
  )
  await callback.message.edit_text(
      "🎓 **المستوى الثاني**\nاختر السمستر المطلوب:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )
  await callback.answer()


# المستوى الثالث (سمستر 5)
@dp.callback_query(F.data == "level_3_menu")
async def show_level_3(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📚 السمستر الخامس (Semester 5)",
                  callback_data="sem_5",
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ رجوع للمستويات", callback_data="go_home"
              )
          ],
      ]
  )
  await callback.message.edit_text(
      "🎓 **المستوى الثالث**\nاختر السمستر المطلوب:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )
  await callback.answer()


# --- 3. دالة موحدة لإنشاء أزرار المادة (درايف + يوتيوب + رجوع للسمستر + رئيسية) ---
def get_material_keyboard(back_callback):
  return InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📂 مجلد الشيتات والمحاضرات (Google Drive)",
                  url="https://drive.google.com/...",
              )
          ],
          [
              InlineKeyboardButton(
                  text="🎥 فيديوهات الشرح (YouTube)",
                  url="https://youtube.com/...",
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ رجوع للسمستر", callback_data=back_callback
              ),
              InlineKeyboardButton(
                  text="🏠 الرئيسية", callback_data="go_home"
              ),
          ],
      ]
  )


# دالة موحدة لأزرار السمستر (تحتوي على زر الامتحانات لكل سمستر + رجوع للمستوى + رئيسية)
def get_semester_menu_keyboard(subjects_list, exam_callback, level_menu):
  keyboard = []
  for sub_name, sub_code in subjects_list:
    keyboard.append(
        [
            InlineKeyboardButton(
                text=sub_name, callback_data=f"sub_{sub_code}"
            )
        ]
    )

  # زر الامتحانات الخاص بالسمستر
  keyboard.append(
      [
          InlineKeyboardButton(
              text="📝 امتحانات السمستر (Exams)", callback_data=exam_callback
          )
      ]
  )
  # أزرار الرجوع والرئيسية
  keyboard.append([
      InlineKeyboardButton(
          text="⬅️ رجوع للمستوى", callback_data=level_menu
      ),
      InlineKeyboardButton(text="🏠 الرئيسية", callback_data="go_home"),
  ])
  return InlineKeyboardMarkup(inline_keyboard=keyboard)


# --- 4. قوائم مواد السمسترات ---

# أ) السمستر الأول
SEM_1_SUBJECTS = [
    ("🔬 General Physics (الفيزياء العامة)", "s1_physics"),
    ("📐 Calculus I (التفاضل والتكامل 1)", "s1_calculus"),
    ("🧪 General Chemistry (الكيمياء العامة)", "s1_chemistry"),
    ("📖 English I (اللغة الإنجليزية 1)", "s1_english"),
    ("📐 Engineering Drawing (الرسم الهندسي)", "s1_drawing"),
    ("📊 Linear Algebra (الجبر الخطي)", "s1_algebra"),
    ("📚 Elective Course (المادة الاختيارية)", "s1_elective"),
]


@dp.callback_query(F.data == "sem_1")
async def show_sem_1(callback: CallbackQuery):
  await callback.message.edit_text(
      "📚 **السمستر الأول (Semester 1)**\nاختر المادة أو الامتحانات المطلوبة:",
      reply_markup=get_semester_menu_keyboard(
          SEM_1_SUBJECTS, "exams_sem_1", "level_1_menu"
      ),
      parse_mode="Markdown",
  )
  await callback.answer()


# ب) السمستر الثاني
SEM_2_SUBJECTS = [
    ("🧬 Biochemistry (كيمياء حيوية)", "s2_biochem"),
    ("📐 Calculus II (حسبان 2)", "s2_calc2"),
    ("⚙️ Mechanics (ميكانيكا)", "s2_mechanics"),
    ("📉 Analytical Geometry (هندسة تحليلية)", "s2_geom"),
    ("💻 Computer Fundamentals (أساسيات الحاسوب)", "s2_comp"),
    ("📖 English II (لغة إنجليزية 2)", "s2_eng2"),
    ("⚛️ Modern Physics (فيزياء حديثة)", "s2_modern_phys"),
]


@dp.callback_query(F.data == "sem_2")
async def show_sem_2(callback: CallbackQuery):
  await callback.message.edit_text(
      "📚 **السمستر الثاني (Semester 2)**\nاختر المادة أو الامتحانات المطلوبة:",
      reply_markup=get_semester_menu_keyboard(
          SEM_2_SUBJECTS, "exams_sem_2", "level_1_menu"
      ),
      parse_mode="Markdown",
  )
  await callback.answer()


# جـ) السمستر الثالث
SEM_3_SUBJECTS = [
    ("📈 Differential Equations (معادلات تفاضلية)", "s3_diff"),
    (
        "⚙️ Mech Engineering Fundamentals (أساسيات الهندسة الميكانيكية)",
        "s3_mech_eng",
    ),
    ("⚡ Electrical Circuits I (الدوائر الكهربائية 1)", "s3_circuits1"),
    ("🔌 Electronic Devices (النبائط الإلكترونية)", "s3_devices"),
    ("🧠 Anatomy & Physiology I (التشريح ووظائف الأعضاء 1)", "s3_anat1"),
    ("💻 Computer Programming (برمجة الحاسوب)", "s3_prog"),
    ("🇸🇩 Sudanese Studies (دراسات سودانية)", "s3_sudan"),
    ("🖥️ MATLAB (ماتلاب)", "s3_matlab"),
    ("🧱 Materials Science (علم المواد)", "s3_materials"),
]


@dp.callback_query(F.data == "sem_3")
async def show_sem_3(callback: CallbackQuery):
  await callback.message.edit_text(
      "📚 **السمستر الثالث (Semester 3)**\nاختر المادة أو الامتحانات المطلوبة:",
      reply_markup=get_semester_menu_keyboard(
          SEM_3_SUBJECTS, "exams_sem_3", "level_2_menu"
      ),
      parse_mode="Markdown",
  )
  await callback.answer()


# د) السمستر الرابع
SEM_4_SUBJECTS = [
    ("🧠 Anatomy & Physiology II (التشريح ووظائف الأعضاء 2)", "s4_anat2"),
    ("🗂️ Data Structures (بنية البيانات)", "s4_data_struct"),
    ("🩺 Medical Physics (فيزياء طبية)", "s4_med_phys"),
    ("📐 Complex Variables (دوال مركبة)", "s4_complex"),
    ("📊 Applied Mathematics (رياضيات تطبيقية)", "s4_applied_math"),
    ("⚡ Electrical Circuits II (دوائر كهربائية 2)", "s4_circuits2"),
    ("🎛️ Analog Electronics (إلكترونيات تماثلية)", "s4_analog"),
    ("🦴 Biomaterials (مواد حيوية)", "s4_biomaterials"),
]


@dp.callback_query(F.data == "sem_4")
async def show_sem_4(callback: CallbackQuery):
  await callback.message.edit_text(
      "📚 **السمستر الرابع (Semester 4)**\nاختر المادة أو الامتحانات المطلوبة:",
      reply_markup=get_semester_menu_keyboard(
          SEM_4_SUBJECTS, "exams_sem_4", "level_2_menu"
      ),
      parse_mode="Markdown",
  )
  await callback.answer()


# هـ) السمستر الخامس
SEM_5_SUBJECTS = [
    ("🩺 Medical Physics (فيزياء طبية)", "s5_med_phys"),
    ("🎛️ Analog Electronics (إلكترونيات تماثلية)", "s5_analog"),
    ("📡 Signals & Systems (إشارات ونظم)", "s5_signals"),
    ("💻 Digital Electronics (إلكترونيات رقمية)", "s5_digital"),
    ("🦾 Biomechanics (ميكانيكا حيوية)", "s5_biomech"),
    ("⚡ Electromagnetic Theory (النظرية الكهرومغناطيسية)", "s5_em"),
    ("🔢 Numerical Analysis (تحليل عددي)", "s5_numerical"),
]


@dp.callback_query(F.data == "sem_5")
async def show_sem_5(callback: CallbackQuery):
  await callback.message.edit_text(
      "📚 **السمستر الخامس (Semester 5)**\nاختر المادة أو الامتحانات المطلوبة:",
      reply_markup=get_semester_menu_keyboard(
          SEM_5_SUBJECTS, "exams_sem_5", "level_3_menu"
      ),
      parse_mode="Markdown",
  )
  await callback.answer()


# --- 5. التعامل مع ضغطات المواد (عرض الدرايف واليوتيوب) ---
# مثال لمادة من السمستر الثاني (الكيمياء الحيوية) وبقية المواد بتسير بنفس النمط
@dp.callback_query(F.data == "sub_s2_biochem")
async def sub_s2_biochem(callback: CallbackQuery):
  await callback.message.edit_text(
      "🧬 **Biochemistry (كيمياء حيوية)**\nاختر ما تحتاجه للمادة:",
      reply_markup=get_material_keyboard("sem_2"),
      parse_mode="Markdown",
  )
  await callback.answer()


# --- 6. أزرار امتحانات السمسترات ---
@dp.callback_query(F.data.startswith("exams_sem_"))
async def show_semester_exams(callback: CallbackQuery):
  sem_num = callback.data.split("_")[-1]
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="📂 مجلد الامتحانات السابقة (Google Drive)",
                  url="https://drive.google.com/...",
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ رجوع للسمستر", callback_data=f"sem_{sem_num}"
              ),
              InlineKeyboardButton(
                  text="🏠 الرئيسية", callback_data="go_home"
              ),
          ],
      ]
  )
  await callback.message.edit_text(
      f"📝 **امتحانات السمستر {sem_num}**\nاضغط للانتقال لمجلد الامتحانات:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )
  await callback.answer()


# --- 7. زر الرجوع للقائمة الرئيسية (المستويات) ---
@dp.callback_query(F.data == "go_home")
async def go_home(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الأول (Level 1)",
                  callback_data="level_1_menu",
              )
          ],
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الثاني (Level 2)",
                  callback_data="level_2_menu",
              )
          ],
          [
              InlineKeyboardButton(
                  text="🎓 المستوى الثالث (Level 3)",
                  callback_data="level_3_menu",
              )
          ],
      ]
  )
  await callback.message.edit_text(
      "أهلاً بكِ مجدداً في القائمة الرئيسية 🩺✨\nاختر المستوى الدراسي:",
      reply_markup=keyboard,
  )
  await callback.answer()


# --- تشغيل البوت ---
async def main():
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())