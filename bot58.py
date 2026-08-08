#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# به نام خدا - ربات جنگ جهانی

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters
)
import sqlite3
import json
import uuid
from datetime import datetime, time, timedelta
import random
import re
import pytz
import copy

TOKEN = "8689255863:AAG_20MSCY2_7aGSMoV3VVS58aO0m-Pgrbc"
OWNER_ID = 7812916669
STATEMENT_CHANNEL = "@PerzuraGame"
WAR_CHANNEL = "@PerzuraWar"
ROLE_CHANNEL = "@TesteBoyt"
REPORTS_CHANNEL = -1003939522875
REPORTS_CHANNEL_RAW = 3939522875  # گزارش‌های لشکرکشی، محاصره و نظامی (اصلی: 3939522875)  # گزارش‌های لشکرکشی، محاصره و نظامی
DATABASE_NAME = "world_war_game3.db"
BOT_NAME = "جنگ‌جهانی"

INTERNET_INCOME_RATES = {
    2: 10000000,
    3: 20000000,
    4: 30000000,
    5: 40000000,
    6: 50000000,
    7: 60000000
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

(
    MAIN_MENU,
    ADMIN_MENU,
    ADD_COUNTRY,
    DELETE_COUNTRY_MENU,
    SELECT_COUNTRY_TO_VIEW_ASSETS,
    ATTACK_TARGET,
    GET_ATTACK_TROOPS_DETAILS,
    GET_ATTACK_SCENARIO_INPUT,
    CONFIRM_ATTACK_SCENARIO,
    RELIGION_MENU,
    ADD_ADMIN,
    REMOVE_ADMIN,
    MANAGE_GLOBAL_BUTTONS,
    GET_PROPOSAL_TEXT,
    SHOP_MENU,
    SHOP_CATEGORY,
    GET_SHOP_ITEM_QUANTITY,
    GET_STATEMENT_CONTENT,
    EDIT_MAIN_PROPS,
    SELECT_MAIN_PROP,
    GET_MAIN_PROP_VALUE,
    EDIT_ASSETS_MENU,
    SELECT_ASSET_CATEGORY,
    SELECT_ASSET_ITEM,
    GET_ASSET_EDIT_VALUE,
    COUNTRY_MANAGEMENT,
    INTERNET_CONTROL,
    DRONE_ATTACK_SELECT_TARGET,
    DRONE_ATTACK_SELECT_DRONE,
    DRONE_ATTACK_GET_QUANTITY,
    DRONE_ATTACK_SELECT_ZONE,
    DRONE_ATTACK_CONFIRM,
    TRADE_MENU,
    TRADE_TYPE,
    TRADE_SELECT_TARGET,
    TRADE_DOMAIN_SELECTION,
    TRADE_ADD_ITEMS,
    TRADE_SEND_ITEM_CATEGORY,
    TRADE_SEND_ITEM_SELECT,
    TRADE_GET_SEND_AMOUNT,
    TRADE_RECEIVE_ITEM_CATEGORY,
    TRADE_RECEIVE_ITEM_SELECT,
    TRADE_GET_RECEIVE_AMOUNT,
    TRADE_CONFIRMATION,
    ADMIN_TRADE_SETTINGS,
    SET_MAX_TRADES,
    SET_TRADE_CHANNEL,
    SELECT_USER_TO_MESSAGE,
    GET_MESSAGE_TEXT,
    MANAGE_NOTIFICATION_IMAGES,
    GET_NOTIFICATION_IMAGE,
    RANDOM_PRIZE_MENU,
    SELECT_PRIZE_CATEGORY,
    SELECT_PRIZE_ITEM,
    GET_PRIZE_QUANTITY,
    CONFIRM_RANDOM_PRIZE,
    EXECUTE_RANDOM_PRIZE,
    MILITARY_EXERCISE_TYPE,
    GET_EXERCISE_CODE,
    MISSILE_ATTACK_MENU,
    MISSILE_ATTACK_SELECT_TARGET,
    MISSILE_ATTACK_SELECT_MISSILE,
    MISSILE_ATTACK_GET_QUANTITY,
    MISSILE_ATTACK_CONFIRM,
    REFINERY_MENU,
    REFINERY_UPGRADE,
    CONSTRUCTION_CATEGORY,
    CONSTRUCTION_SELECT_PROJECT,
    CONSTRUCTION_CONFIRM,
    ANNOUNCE_TOP_OIL,
    ANNOUNCE_TOP_SATISFACTION,
    MISSILE_ATTACK_RESULT,
    EQUIP_MANAGE_MENU,
    EQUIP_DELETE_INPUT,
    EQUIP_ADD_GET_NAME,
    EQUIP_ADD_GET_PRICE,
    EQUIP_ADD_GET_CATEGORY,
    EQUIP_NEW_CATEGORY_NAME,
    EQUIP_PRESET_MENU,
    EQUIP_PRESET_SAVE_NAME,
    EQUIP_PRESET_LOAD_CONFIRM,
    CAMPAIGN_SELECT_TARGET,
    CAMPAIGN_SELECT_TYPES,
    CAMPAIGN_GET_EQUIPMENT,
    CAMPAIGN_GET_SCENARIO,
    CAMPAIGN_CONFIRM,
    MISSILE_ATTACK_SELECT_ZONE,
    ROLE_SENA_MENU,
    ROLE_SENA_GET_CONTENT,
    ROLE_SENA_LIMITS_MENU,
    ROLE_SENA_GET_LIMIT_VALUE,
    ADD_FORCE_NAME,
    ADD_FORCE_PRICE,
    ADD_FORCE_GRAIN,
    SIEGE_SELECT_TARGET,
    SIEGE_CONFIRM,
    CASTLE_MENU,
    FORT_MENU,
    WORKSHOP_MENU,
    WORKSHOP_CFG_MENU,
    WORKSHOP_CFG_SOLDIER,
    WORKSHOP_CFG_AMOUNT,
    WORKSHOP_CFG_COST,
    DARAYI_MENU,
    DARAYI_VIEW,
    DARAYI_EDIT_SELECT,
    DARAYI_EDIT_VALUE,
    DARAYI_CREATE_NAME,
    DARAYI_CREATE_DATA,
    DELETE_FORCE_MENU,
    DELETE_ALL_CONFIRM,
    DELETE_SINGLE_SELECT,
    DISASTER_MENU,
    DISASTER_TARGET,
    DISASTER_CONFIRM
) = range(115)

ASSET_NAMES = {
    # --- نیروهای قرون وسطی (جایگزین تفنگدار) ---
    'spearman_1': "نیزه‌دار سطح ۱ 🪓",
    'spearman_2': "نیزه‌دار سطح ۲ 🪓",
    'spearman_3': "نیزه‌دار سطح ۳ 🪓",
    'swordsman_1': "شمشیرزن سطح ۱ ⚔️",
    'swordsman_2': "شمشیرزن سطح ۲ ⚔️",
    'swordsman_3': "شمشیرزن سطح ۳ ⚔️",
    'archer_1': "کماندار سطح ۱ 🏹",
    'archer_2': "کماندار سطح ۲ 🏹",
    'archer_3': "کماندار سطح ۳ 🏹",
    'cavalry_light': "سواره‌نظام سبک 🐎",
    'cavalry_heavy': "سواره‌نظام سنگین 🐎‍🛡️",
    'catapult': "منجنیق 🏰",
    'trebuchet': "منجنیق سنگین 🏰",
    'grains': "غلات 🌾",
    'farm_level': "مزرعه 🌾",
    # --- منابع پایه (بدون تغییر) ---
    'satisfaction': "رضایت 😊",
    'security': "امنیت 🛡️",
    'daily_income': "سود روزانه 💹",
    'population': "جمعیت 👫",
    'capital': "سرمایه 💰",
    'trade_land': "کاروان تجاری 🐫",
    'attack': "حمله نظامی ⚔️"
}

DEFAULT_ASSETS = {
    'population': 15000000,
    'capital': 100000000,
    'grains': 5000,
    'satisfaction': 50,
    'daily_income': 0,
    'custom_income': 0,
    'loan_amount': 0,
    'loan_date': None,
    'religion': "islam",
    'security': 50,
    'farm_level': 0,
    # --- ارتش قرون وسطی ---
    'land_troops': {
        'spearman_1': 0,
        'spearman_2': 0,
        'spearman_3': 0,
        'swordsman_1': 0,
        'swordsman_2': 0,
        'swordsman_3': 0,
        'archer_1': 0,
        'archer_2': 0,
        'archer_3': 0,
        'cavalry_light': 0,
        'cavalry_heavy': 0,
        'catapult': 0,
        'trebuchet': 0
    },
    'disabled_buttons': []
}

ASSET_PRICES = {
    # --- قرون وسطی: نیزه‌دار ---
    'spearman_1': 3000,
    'spearman_2': 6000,
    'spearman_3': 12000,
    # شمشیرزن
    'swordsman_1': 8000,
    'swordsman_2': 15000,
    'swordsman_3': 28000,
    # کماندار
    'archer_1': 5000,
    'archer_2': 10000,
    'archer_3': 20000,
    # سواره‌نظام و محاصره
    'cavalry_light': 25000,
    'cavalry_heavy': 50000,
    'catapult': 40000,
    'trebuchet': 80000,
    'satisfaction': 0,
    'security': 0,
    'daily_income': 0,
    'population': 0,
    'capital': 0,
    'trade_land': 0,
    'attack': 0
}

ASSET_CATEGORIES_FOR_DISPLAY = [
    ('land_troops', 'سپاه پیاده ⚔️'),
]

BOT_MAIN_MENU_BUTTONS = [
    {"text": "📊 لیست دارایی", "callback_data": "show_assets"},
    {"text": "⚔️ لشکر‌کشی", "callback_data": "campaign_menu"},
    {"text": "🏰 محاصره", "callback_data": "siege_menu"},
    {"text": "📜 ارسال رول و سنا", "callback_data": "role_sena_menu"},
    {"text": "🏗️ ساخت و ساز قرون وسطی", "callback_data": "construction_proposal_start"},
    {"text": "🛒 درخواست خرید", "callback_data": "shop_menu_start"},
    {"text": "☪️ تنظیم دین", "callback_data": "religion_menu"},
    {"text": "📣 ارسال بیانیه", "callback_data": "statement_proposal_start"},
    {"text": "🏛️ مدیریت کشور", "callback_data": "country_management"}
]

ADMIN_PANEL_BUTTONS = [
    {"text": "📋 لیست کشورها", "callback_data": "list_countries"},
    {"text": "⚙️ ویرایش ویژگی‌های اصلی", "callback_data": "edit_main_props"},
    {"text": "⚔️ ویرایش نیروها و دارایی‌ها", "callback_data": "edit_assets_menu"},
    {"text": "\u0622\u067e \u062f\u0627\u0631\u0627\u06cc\u06cc", "callback_data": "admin_update_assets"},
    {"text": "📦 ویرایش ظرفیت انبار", "callback_data": "edit_storage_capacity"},
    {"text": "📊 مشاهده دارایی کشورها", "callback_data": "select_country_view_assets"},
    {"text": "➕ افزودن نیرو", "callback_data": "add_force"},
    {"text": "👑 افزودن ادمین", "callback_data": "add_admin"},
    {"text": "🗑 حذف ادمین", "callback_data": "remove_admin"},
    {"text": "🔌 خاموش/روشن ربات", "callback_data": "toggle_bot"},
    {"text": "⚙️ مدیریت دکمه‌های عمومی", "callback_data": "manage_global_buttons"},
    {"text": "🚦 تعیین محدودیت", "callback_data": "role_sena_limits_menu"},
    {"text": "🤝 مدیریت تجارت", "callback_data": "trade_settings"},
    {"text": "🖼️ مدیریت عکس اطلاعیه‌ها", "callback_data": "manage_notification_images"},
    {"text": "🎁 جایزه رندوم", "callback_data": "random_prize_menu"},
    {"text": "😊 اعلام برترین رضایت", "callback_data": "announce_top_satisfaction"}
]

RELIGIONS = [
    ("islam", "اسلام ☪️"),
    ("christianity", "مسیحیت ✝️"),
    ("judaism", "یهودیت ✡️"),
    ("buddhism", "بودیسم ☸️"),
    ("hinduism", "هندوئیسم 🕉️"),
    ("atheism", "الحاد ⚛️"),
]

PROPOSAL_TYPES = {
    "defense": "دفاعی",
    "construction": "ساخت و ساز",
    "economic": "اقتصادی",
    "attack": "حمله",
    "campaign": "لشکر‌کشی",
    "tax_rate": "تغییر خراج"
}

TRADE_DOMAINS = [
    ("land", "تجارت زمینی 🌍"),
    ("air", "تجارت هوایی ✈️"),
    ("sea", "تجارت دریایی ⚓")
]

CONSTRUCTION_PROJECTS = {
    "castle": {
        "small_keep": {"name": "برجک دیده‌بانی", "cost": 40000, "daily_income": 2000, "description": "برجک چوبی برای دیده‌بانی مرز"},
        "stone_wall": {"name": "دیوار سنگی", "cost": 80000, "daily_income": 5000, "description": "دیوار سنگی دور روستا"},
        "great_castle": {"name": "قلعه بزرگ", "cost": 150000, "daily_income": 12000, "description": "قلعه سنگی با خندق"},
        "citadel": {"name": "ارگ سلطنتی", "cost": 300000, "daily_income": 25000, "description": "ارگ باشکوه پایتخت"},
    },
    "bazaar": {
        "caravanserai": {"name": "کاروانسرا", "cost": 30000, "daily_income": 3000, "description": "استراحتگاه کاروان‌ها، + تجارت"},
        "grand_bazaar": {"name": "بازار بزرگ", "cost": 70000, "daily_income": 7000, "description": "بازار شلوغ شهر"},
        "silk_road": {"name": "تیمچه ابریشم", "cost": 130000, "daily_income": 15000, "description": "مرکز تجارت ابریشم"},
    },
    "temple": {
        "shrine": {"name": "زیارتگاه", "cost": 20000, "daily_income": 1500, "description": "زیارتگاه کوچک، + رضایت"},
        "mosque": {"name": "مسجد جامع", "cost": 60000, "daily_income": 6000, "description": "مسجد بزرگ شهر"},
        "cathedral": {"name": "کلیسای جامع", "cost": 120000, "daily_income": 10000, "description": "کلیسای سنگی باشکوه"},
    }
}

DEFENSE_INTERCEPT_RATES = {
    'patriots': 0.3,
    's300': 0.4,
    'iron_dome': 0.7,
    's400': 0.6,
    'thaad': 0.8
}

# ==================== DRONE ATTACK CONFIG ====================
DRONE_DAMAGE_RATES = {
    'spy_drone':        {'population': 0.0003, 'capital': 30000, 'satisfaction': 1, 'security': 0},
    'kamikaze_drone':   {'population': 0.0008, 'capital': 45000, 'satisfaction': 2, 'security': 1},
    'cruise_drone':     {'population': 0.0006, 'capital': 55000, 'satisfaction': 1, 'security': 0},
    'hermes_drone':     {'population': 0.0010, 'capital': 70000, 'satisfaction': 2, 'security': 1},
}

DRONE_INTERCEPT_RATES = {
    'patriots': 0.25,
    's300': 0.35,
    'iron_dome': 0.60,
    's400': 0.50,
    'thaad': 0.70
}




def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            population INTEGER,
            capital INTEGER,
            daily_income INTEGER,
            religion TEXT,
            oil_barrels INTEGER,
            satisfaction INTEGER,
            grains INTEGER DEFAULT 5000,
            assets TEXT,
            custom_income INTEGER DEFAULT 0,
            loan_amount INTEGER DEFAULT 0,
            loan_date TEXT,
            crypto INTEGER DEFAULT 0,
            security INTEGER DEFAULT 70,
            farm_level INTEGER DEFAULT 0,
            fort_level INTEGER DEFAULT 0,
            workshop_level INTEGER DEFAULT 0,
            internet_nationalized INTEGER DEFAULT 0,
            internet_level INTEGER DEFAULT 2,
            refinery_level INTEGER DEFAULT 0,
            storage_capacity INTEGER DEFAULT 100
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            type TEXT,
            status TEXT,
            text_content TEXT,
            photo_ids TEXT,
            submitted_at TEXT,
            admin_message_id INTEGER DEFAULT NULL,
            user_message_id INTEGER DEFAULT NULL,
            target_user_id INTEGER DEFAULT NULL,
            target_country_name TEXT DEFAULT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id TEXT PRIMARY KEY,
            sender_id INTEGER,
            receiver_id INTEGER,
            domain TEXT,
            send_resource TEXT,
            send_amount INTEGER,
            receive_resource TEXT,
            receive_amount INTEGER,
            trade_type TEXT,
            status TEXT,
            created_at TEXT,
            delivery_time TEXT,
            completed INTEGER DEFAULT 0,
            secret_code TEXT DEFAULT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS trade_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notification_images (
            event_type TEXT PRIMARY KEY,
            photo_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS attack_deliveries (
            proposal_id TEXT PRIMARY KEY,
            delivery_time TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS random_prizes (
            id TEXT PRIMARY KEY,
            category TEXT,
            item TEXT,
            quantity INTEGER,
            created_at TEXT
        )
    ''')
    # جدول رول/سنا: ردیابی استفاده روزانه هر کاربر در هر دسته
    c.execute('''
        CREATE TABLE IF NOT EXISTS role_sena_usage (
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            day_key TEXT NOT NULL,
            used_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, category, day_key)
        )
    ''')
    # جدول گپ‌های اکتویت‌شده برای پلیرها
    c.execute('''
        CREATE TABLE IF NOT EXISTS active_chats (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            activated_by INTEGER,
            activated_at TEXT
        )
    ''')
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('bot_active', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('global_disabled_buttons', '[]'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('country_management_active', '1'))
    # مقادیر دیفالت رول/سنا
    # محدودیت تجمعی برای سه بخش رول (امنیتی/اقتصادی/خرابکاری) به‌صورت تعداد پیام در روز
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_security_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_economic_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_sabotage_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_total_daily_limit', '10'))
    # سنا
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('sena_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('sena_daily_limit', '3'))
    # حداکثر کاراکتر برای هر پیام رول/سنا (پیش‌فرض: ۵ صفحه × 4096)
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_sena_max_chars', str(5 * 4096)))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('trade_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('max_trades', '5'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('trade_channel', STATEMENT_CHANNEL))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('discreet_trade_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('discreet_trade_channel', STATEMENT_CHANNEL))
    c.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (OWNER_ID,))

    # جداول مربوط به مدیریت پویای تجهیزات
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_key TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment_categories (
            cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cat_key TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sieges (
            siege_id TEXT PRIMARY KEY,
            besieger_id INTEGER,
            besieger_name TEXT,
            target_id INTEGER,
            target_name TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS siege_participants (
            siege_id TEXT,
            user_id INTEGER,
            joined_at TEXT,
            PRIMARY KEY (siege_id, user_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS darayi_presets (
            preset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment_presets (
            preset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            preset_name TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

    # سید کردن اولیه از داده‌های پیش‌فرض اگر خالی باشد
    _seed_equipment_from_defaults_if_empty()

    # مایگریشن برای DBهای قدیمی (grains, farm_level)
    try:
        conn2 = __import__('sqlite3').connect(DATABASE_NAME)
        c2 = conn2.cursor()
        try:
            c2.execute("SELECT grains FROM countries LIMIT 1")
        except __import__('sqlite3').OperationalError:
            c2.execute("ALTER TABLE countries ADD COLUMN grains INTEGER DEFAULT 5000")
        try:
            c2.execute("SELECT farm_level FROM countries LIMIT 1")
        except __import__('sqlite3').OperationalError:
            c2.execute("ALTER TABLE countries ADD COLUMN farm_level INTEGER DEFAULT 0")
        try:
            c2.execute("SELECT fort_level FROM countries LIMIT 1")
        except __import__('sqlite3').OperationalError:
            c2.execute("ALTER TABLE countries ADD COLUMN fort_level INTEGER DEFAULT 0")
        try:
            c2.execute("SELECT workshop_level FROM countries LIMIT 1")
        except __import__('sqlite3').OperationalError:
            c2.execute("ALTER TABLE countries ADD COLUMN workshop_level INTEGER DEFAULT 0")
        conn2.commit()
        conn2.close()
    except Exception:
        pass


STORAGE_LEVELS = {
    1: {'capacity': 100, 'cost': 0},
    2: {'capacity': 200, 'cost': 30000},
    3: {'capacity': 350, 'cost': 70000},
    4: {'capacity': 500, 'cost': 120000},
    5: {'capacity': 800, 'cost': 200000},
}
def get_storage_level(capacity):
    for lvl in sorted(STORAGE_LEVELS.keys(), reverse=True):
        if capacity >= STORAGE_LEVELS[lvl]['capacity']:
            return lvl
    return 1
def get_next_storage_upgrade(capacity):
    lvl = get_storage_level(capacity)
    nxt = lvl + 1
    if nxt in STORAGE_LEVELS:
        return nxt, STORAGE_LEVELS[nxt]
    return None, None

# --- مزرعه: تولید غلات ---
FARM_LEVELS = {
    1: {'cost': 25000, 'production': 200, 'name': 'مزرعه کوچک'},
    2: {'cost': 50000, 'production': 500, 'name': 'مزرعه متوسط'},
    3: {'cost': 75000, 'production': 900, 'name': 'مزرعه بزرگ'},
    4: {'cost': 120000, 'production': 1500, 'name': 'مزرعه وسیع'},
    5: {'cost': 180000, 'production': 2500, 'name': 'مزرعه پیشرفته'},
    6: {'cost': 250000, 'production': 4000, 'name': 'مزرعه امپراتوری'},
    7: {'cost': 350000, 'production': 6000, 'name': 'مزرعه افسانه‌ای'},
}

def get_farm_production(level):
    return FARM_LEVELS.get(level, {}).get('production', 0)

# --- استحکامات قلعه ---
FORT_LEVELS = {
    1: {'cost': 20000, 'name': 'دیوار چوبی', 'security': 5, 'desc': 'حصار چوبی ساده، +5 امنیت'},
    2: {'cost': 50000, 'name': 'دیوار سنگی', 'security': 10, 'desc': 'دیوار سنگی مستحکم، +10 امنیت'},
    3: {'cost': 100000, 'name': 'دیوار با خندق', 'security': 15, 'desc': 'خندق پر از آب، دشمن را کند می‌کند'},
    4: {'cost': 180000, 'name': 'برج دیده‌بانی', 'security': 20, 'desc': 'برج بلند، محاصره را زودتر هشدار می‌دهد'},
    5: {'cost': 300000, 'name': 'منجنیق روی دیوار', 'security': 25, 'desc': 'منجنیق‌های غول‌پیکر روی بارو، دفاع خودکار'},
}

def get_fort_security(level):
    return FORT_LEVELS.get(level, {}).get('security', 0)

# --- کارگاه اسلحه‌سازی (پیش‌فرض) ---
WORKSHOP_LEVELS = {
    1: {'cost': 30000, 'name': 'آهنگری ساده', 'soldier': 'spearman_1', 'amount': 3},
    2: {'cost': 70000, 'name': 'کوره ذوب', 'soldier': 'swordsman_1', 'amount': 5},
    3: {'cost': 120000, 'name': 'کارگاه کمان‌سازی', 'soldier': 'archer_1', 'amount': 5},
    4: {'cost': 200000, 'name': 'زرادخانه سلطنتی', 'soldier': 'cavalry_light', 'amount': 3},
    5: {'cost': 350000, 'name': 'اسلحه‌خانه افسانه‌ای', 'soldier': 'swordsman_3', 'amount': 5},
}

def get_workshop_config():
    import json as _j, sqlite3 as _s
    try:
        conn = _s.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key='workshop_config'")
        row = c.fetchone()
        conn.close()
        if row and row[0]:
            return _j.loads(row[0])
    except: pass
    return {}

def save_workshop_config(cfg):
    import json as _j, sqlite3 as _s
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('workshop_config', ?)", (_j.dumps(cfg, ensure_ascii=False),))
    conn.commit()
    conn.close()

def get_workshop_level_config(level):
    cfg = get_workshop_config()
    if str(level) in cfg:
        return cfg[str(level)]
    return WORKSHOP_LEVELS.get(level, {})

def save_darayi_preset(name, data):
    import json as _j, sqlite3 as _s
    from datetime import datetime as _dt
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO darayi_presets (name, data, created_at) VALUES (?,?,?)", (name, _j.dumps(data, ensure_ascii=False), _dt.now().isoformat()))
        conn.commit()
        pid = c.lastrowid
        conn.close()
        return pid
    except _s.IntegrityError:
        conn.close()
        return None

def get_all_darayi():
    import sqlite3 as _s, json as _j
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT preset_id, name, created_at FROM darayi_presets ORDER BY preset_id")
    rows = c.fetchall()
    conn.close()
    return [{"preset_id": r[0], "name": r[1], "created_at": r[2]} for r in rows]

def get_darayi(preset_id):
    import sqlite3 as _s, json as _j
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT preset_id, name, data, created_at FROM darayi_presets WHERE preset_id=?", (preset_id,))
    r = c.fetchone()
    conn.close()
    if r:
        return {"preset_id": r[0], "name": r[1], "data": _j.loads(r[2]), "created_at": r[3]}
    return None

def get_darayi_by_name(name):
    import sqlite3 as _s, json as _j
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT preset_id, name, data FROM darayi_presets WHERE name=?", (name,))
    r = c.fetchone()
    conn.close()
    if r:
        return {"preset_id": r[0], "name": r[1], "data": _j.loads(r[2])}
    return None

def delete_darayi(preset_id):
    import sqlite3 as _s
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM darayi_presets WHERE preset_id=?", (preset_id,))
    conn.commit()
    d = c.rowcount>0
    conn.close()
    return d

def update_darayi_data(preset_id, new_data):
    import json as _j, sqlite3 as _s
    conn = _s.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE darayi_presets SET data=? WHERE preset_id=?", (_j.dumps(new_data, ensure_ascii=False), preset_id))
    conn.commit()
    conn.close()

def get_daily_workshop_production(level):
    cfg = get_workshop_level_config(level)
    soldier = cfg.get('soldier') or cfg.get('unit')
    amount = cfg.get('amount', 0)
    if soldier and amount:
        return soldier, int(amount)
    return None, 0

# --- سیستم غلات و مصرف سربازان ---
GRAIN_CONSUMPTION_RATES = {
    'spearman_1': 1,
    'spearman_2': 2,
    'spearman_3': 3,
    'swordsman_1': 2,
    'swordsman_2': 3,
    'swordsman_3': 4,
    'archer_1': 2,
    'archer_2': 3,
    'archer_3': 4,
    'cavalry_light': 5,
    'cavalry_heavy': 7,
    'catapult': 3,
    'trebuchet': 5,
}
def get_custom_grain_rates():
    import json as _json, sqlite3 as _sql
    try:
        conn = _sql.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key='custom_grain_rates'")
        row = c.fetchone()
        conn.close()
        if row and row[0]:
            return _json.loads(row[0])
    except Exception:
        pass
    return {}

def set_custom_grain_rate(item_key, rate):
    import json as _json, sqlite3 as _sql
    rates = get_custom_grain_rates()
    rates[item_key] = int(rate)
    conn = _sql.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('custom_grain_rates', ?)", (_json.dumps(rates),))
    conn.commit()
    conn.close()
    # also update in-memory
    GRAIN_CONSUMPTION_RATES[item_key] = int(rate)

# ادغام نرخ‌های سفارشی در حافظه
try:
    GRAIN_CONSUMPTION_RATES.update(get_custom_grain_rates())
except: pass

def calculate_daily_grain_consumption(country):
    total = 0
    troops = country.get('land_troops', {}) or {}
    for unit, cnt in troops.items():
        rate = GRAIN_CONSUMPTION_RATES.get(unit, 1)
        total += int(cnt) * rate
    return total

def apply_grain_starvation(country):
    grains = int(country.get('grains', 0) or 0)
    consumption = calculate_daily_grain_consumption(country)
    if consumption == 0:
        return consumption, 0, {}, grains
    if grains >= consumption:
        return consumption, 0, {}, grains - consumption
    deficit = consumption - grains
    death_order = ['spearman_1','spearman_2','spearman_3','archer_1','archer_2','archer_3','swordsman_1','swordsman_2','swordsman_3','cavalry_light','catapult','cavalry_heavy','trebuchet']
    troops = dict(country.get('land_troops', {}) or {})
    deaths = {}
    remaining = deficit
    for unit in death_order:
        if remaining <= 0:
            break
        cnt = int(troops.get(unit, 0) or 0)
        if cnt <= 0:
            continue
        rate = GRAIN_CONSUMPTION_RATES.get(unit, 1)
        need = (remaining + rate - 1)// rate
        die = min(cnt, need)
        troops[unit] = cnt - die
        deaths[unit] = die
        remaining -= die * rate
    dead_total = sum(deaths.values())
    return consumption, dead_total, deaths, 0

DRONE_KEYS = {'spy_drone', 'kamikaze_drone', 'cruise_drone', 'hermes_drone'}

def calculate_storage_used(country):
    """محاسبه فضای استفاده‌شده انبار
       موشک = ۲ واحد، پهپاد = ۱ واحد (فقط پهپادهای واقعی)
    """
    try:
        rockets = country.get('rockets', {}) or {}
        air_troops = country.get('air_troops', {}) or {}
        
        missile_units = sum(int(v) for v in rockets.values()) * 2
        drone_units = sum(int(air_troops.get(k, 0)) for k in DRONE_KEYS) * 1
        
        return missile_units + drone_units
    except Exception:
        return 0
def _seed_equipment_from_defaults_if_empty():
    """اگر جدول تجهیزات خالی است، از DEFAULT_ASSETS و ASSET_NAMES سید می‌کنیم."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM equipment_items")
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return

    now = datetime.now().isoformat()
    # افزودن دسته‌بندی‌ها
    for cat_key, cat_disp in ASSET_CATEGORIES_FOR_DISPLAY:
        try:
            c.execute(
                "INSERT OR IGNORE INTO equipment_categories (cat_key, display_name, created_at) VALUES (?, ?, ?)",
                (cat_key, cat_disp, now)
            )
        except Exception as e:
            logger.error(f"خطا در سید دسته‌بندی {cat_key}: {e}")

    # افزودن آیتم‌ها بر اساس DEFAULT_ASSETS
    for cat_key, cat_disp in ASSET_CATEGORIES_FOR_DISPLAY:
        items_dict = DEFAULT_ASSETS.get(cat_key, {})
        if isinstance(items_dict, dict):
            for item_key in items_dict.keys():
                display_name = ASSET_NAMES.get(item_key, item_key.replace('_', ' ').title())
                price = ASSET_PRICES.get(item_key, 0)
                try:
                    c.execute(
                        "INSERT OR IGNORE INTO equipment_items (item_key, display_name, category, price, created_at) VALUES (?, ?, ?, ?, ?)",
                        (item_key, display_name, cat_key, price, now)
                    )
                except Exception as e:
                    logger.error(f"خطا در سید آیتم {item_key}: {e}")

    conn.commit()
    conn.close()
    logger.info("داده‌های تجهیزات از مقادیر پیش‌فرض سید شدند.")


# ========== توابع مدیریت پویای تجهیزات ==========

def get_all_equipment_categories():
    """لیست همه دسته‌بندی‌ها از DB: [(cat_key, display_name), ...]"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT cat_key, display_name FROM equipment_categories ORDER BY cat_id")
    rows = c.fetchall()
    conn.close()
    return [(r[0], r[1]) for r in rows]


def get_all_equipment_items():
    """لیست همه آیتم‌ها: [{item_id, item_key, display_name, category, price}, ...]"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT item_id, item_key, display_name, category, price FROM equipment_items ORDER BY category, item_id")
    rows = c.fetchall()
    conn.close()
    return [
        {"item_id": r[0], "item_key": r[1], "display_name": r[2], "category": r[3], "price": r[4]}
        for r in rows
    ]


def get_equipment_item_by_id(item_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT item_id, item_key, display_name, category, price FROM equipment_items WHERE item_id = ?", (item_id,))
    r = c.fetchone()
    conn.close()
    if r:
        return {"item_id": r[0], "item_key": r[1], "display_name": r[2], "category": r[3], "price": r[4]}
    return None


def add_equipment_item(item_key, display_name, category, price):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO equipment_items (item_key, display_name, category, price, created_at) VALUES (?, ?, ?, ?, ?)",
            (item_key, display_name, category, price, datetime.now().isoformat())
        )
        conn.commit()
        new_id = c.lastrowid
        return new_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def delete_equipment_item(item_id):
    # Also get item_key to clean grain rates and country assets
    item = get_equipment_item_by_id(item_id)
    item_key = item['item_key'] if item else None
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM equipment_items WHERE item_id = ?", (item_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    if deleted and item_key:
        # حذف از نرخ غلات سفارشی
        try:
            import json as _j, sqlite3 as _s
            conn = _s.connect(DATABASE_NAME)
            cc = conn.cursor()
            cc.execute("SELECT value FROM settings WHERE key='custom_grain_rates'")
            row = cc.fetchone()
            if row and row[0]:
                rates = _j.loads(row[0])
                if item_key in rates:
                    del rates[item_key]
                    cc.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('custom_grain_rates', ?)", (_j.dumps(rates),))
                    conn.commit()
            # حذف از GRAIN dict حافظه
            if item_key in GRAIN_CONSUMPTION_RATES:
                del GRAIN_CONSUMPTION_RATES[item_key]
            conn.close()
        except: pass
        # حذف از دارایی همه کشورها
        try:
            conn = _s.connect(DATABASE_NAME) if '_s' in locals() else __import__('sqlite3').connect(DATABASE_NAME)
            cc = conn.cursor()
            cc.execute("SELECT user_id, assets FROM countries")
            for uid, assets_json in cc.fetchall():
                try:
                    assets = _j.loads(assets_json) if assets_json else {}
                except: assets = {}
                changed = False
                for cat in list(assets.keys()):
                    if item_key in assets.get(cat, {}):
                        del assets[cat][item_key]
                        changed = True
                if changed:
                    cc.execute("UPDATE countries SET assets=? WHERE user_id=?", (_j.dumps(assets, ensure_ascii=False), uid))
            conn.commit()
            conn.close()
        except: pass
    return deleted


def add_equipment_category(cat_key, display_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO equipment_categories (cat_key, display_name, created_at) VALUES (?, ?, ?)",
            (cat_key, display_name, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_equipment_category(cat_key):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # حذف آیتم‌های متعلق به این دسته
    c.execute("DELETE FROM equipment_items WHERE category = ?", (cat_key,))
    c.execute("DELETE FROM equipment_categories WHERE cat_key = ?", (cat_key,))
    conn.commit()
    conn.close()


def get_dynamic_asset_categories_for_display():
    """جایگزین پویای ASSET_CATEGORIES_FOR_DISPLAY"""
    cats = get_all_equipment_categories()
    if not cats:
        return ASSET_CATEGORIES_FOR_DISPLAY
    return cats


def get_dynamic_asset_names():
    """جایگزین پویای ASSET_NAMES (با fallback)"""
    items = get_all_equipment_items()
    result = dict(ASSET_NAMES)  # کپی از پیش‌فرض
    for it in items:
        result[it['item_key']] = it['display_name']
    return result


def get_dynamic_asset_prices():
    """جایگزین پویای ASSET_PRICES (با fallback)"""
    items = get_all_equipment_items()
    result = dict(ASSET_PRICES)  # کپی از پیش‌فرض
    for it in items:
        result[it['item_key']] = it['price']
    return result


def get_dynamic_default_assets():
    """جایگزین پویای DEFAULT_ASSETS (برای ساختار دسته‌ها و آیتم‌ها)"""
    base = copy.deepcopy(DEFAULT_ASSETS)
    items = get_all_equipment_items()
    cats = get_all_equipment_categories()

    if not items and not cats:
        return base

    # حذف دسته‌های پویا که در DB نیستند ولی در base هستند (به جز کلیدهای ثابت)
    fixed_top_keys = {
        'population', 'capital', 'oil_barrels', 'satisfaction', 'daily_income',
        'custom_income', 'loan_amount', 'loan_date',  'religion',
        'security', 'internet_nationalized', 'internet_level', 'refinery_level',
        'disabled_buttons'
    }

    db_cat_keys = {c[0] for c in cats}
    for key in list(base.keys()):
        if key in fixed_top_keys:
            continue
        if isinstance(base[key], dict) and key not in db_cat_keys:
            # دسته‌ای که در DB حذف شده
            del base[key]

    # اضافه کردن دسته‌های موجود در DB
    for cat_key, _ in cats:
        if cat_key not in base or not isinstance(base[cat_key], dict):
            base[cat_key] = {}

    # ساخت آیتم‌های هر دسته از DB
    for cat_key, _ in cats:
        base[cat_key] = {}
    for it in items:
        cat = it['category']
        if cat not in base:
            base[cat] = {}
        base[cat][it['item_key']] = 0

    return base


def save_equipment_preset(preset_name):
    """ذخیره وضعیت فعلی تجهیزات و دسته‌ها به صورت یک پریست."""
    cats = get_all_equipment_categories()
    items = get_all_equipment_items()
    data = {
        "categories": [{"cat_key": c[0], "display_name": c[1]} for c in cats],
        "items": [
            {"item_key": it['item_key'], "display_name": it['display_name'],
             "category": it['category'], "price": it['price']}
            for it in items
        ]
    }
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO equipment_presets (preset_name, data, created_at) VALUES (?, ?, ?)",
            (preset_name, json.dumps(data, ensure_ascii=False), datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # اگر قبلا با همین اسم بوده، آپدیت کن
        try:
            c.execute(
                "UPDATE equipment_presets SET data = ?, created_at = ? WHERE preset_name = ?",
                (json.dumps(data, ensure_ascii=False), datetime.now().isoformat(), preset_name)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"خطا در ذخیره پریست: {e}")
            return False
    finally:
        conn.close()


def get_all_equipment_presets():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT preset_id, preset_name, created_at FROM equipment_presets ORDER BY preset_id")
    rows = c.fetchall()
    conn.close()
    return [{"preset_id": r[0], "preset_name": r[1], "created_at": r[2]} for r in rows]


def get_equipment_preset(preset_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT preset_id, preset_name, data, created_at FROM equipment_presets WHERE preset_id = ?", (preset_id,))
    r = c.fetchone()
    conn.close()
    if r:
        return {"preset_id": r[0], "preset_name": r[1], "data": json.loads(r[2]), "created_at": r[3]}
    return None


def delete_equipment_preset(preset_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM equipment_presets WHERE preset_id = ?", (preset_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted


def load_equipment_preset(preset_id, reset_countries_inventory=False):
    """بارگذاری یک پریست: جایگزینی کامل دسته‌ها و آیتم‌ها."""
    preset = get_equipment_preset(preset_id)
    if not preset:
        return False
    data = preset['data']

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # پاک کردن همه چیز
    c.execute("DELETE FROM equipment_items")
    c.execute("DELETE FROM equipment_categories")

    now = datetime.now().isoformat()
    # افزودن دسته‌ها
    for cat in data.get('categories', []):
        try:
            c.execute(
                "INSERT INTO equipment_categories (cat_key, display_name, created_at) VALUES (?, ?, ?)",
                (cat['cat_key'], cat['display_name'], now)
            )
        except Exception as e:
            logger.error(f"خطا در بارگذاری دسته {cat}: {e}")

    # افزودن آیتم‌ها
    for it in data.get('items', []):
        try:
            c.execute(
                "INSERT INTO equipment_items (item_key, display_name, category, price, created_at) VALUES (?, ?, ?, ?, ?)",
                (it['item_key'], it['display_name'], it['category'], it.get('price', 0), now)
            )
        except Exception as e:
            logger.error(f"خطا در بارگذاری آیتم {it}: {e}")

    conn.commit()
    conn.close()

    if reset_countries_inventory:
        _reset_countries_inventory_to_new_schema()

    return True


def _reset_countries_inventory_to_new_schema():
    """موجودی تجهیزات تمام کشورها را به ساختار جدید با مقدار صفر بازنشانی می‌کند."""
    new_schema = get_dynamic_default_assets()
    new_assets_template = {}
    for k, v in new_schema.items():
        if isinstance(v, dict):
            new_assets_template[k] = {ik: 0 for ik in v.keys()}

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id FROM countries")
    user_ids = [r[0] for r in c.fetchall()]
    for uid in user_ids:
        c.execute(
            "UPDATE countries SET assets = ? WHERE user_id = ?",
            (json.dumps(new_assets_template, ensure_ascii=False), uid)
        )
    conn.commit()
    conn.close()
    logger.info(f"موجودی تجهیزات {len(user_ids)} کشور بازنشانی شد.")


# ===================== توابع رول/سنا =====================

# حداکثر طول یک پیام تلگرام
TELEGRAM_MSG_LIMIT = 4096


def _split_message(text, chunk_size=TELEGRAM_MSG_LIMIT):
    """تقسیم متن به قطعاتی که در یک پیام تلگرام جا می‌شوند.
    سعی می‌کند روی خط جدید یا فاصله بشکند تا کلمات نصف نشوند.
    """
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    remaining = text
    while len(remaining) > chunk_size:
        cut = remaining.rfind('\n', 0, chunk_size)
        if cut < int(chunk_size * 0.6):
            cut = remaining.rfind(' ', 0, chunk_size)
        if cut < int(chunk_size * 0.6):
            cut = chunk_size
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


async def _send_long_message(bot_instance, chat_id, header, body, parse_mode=None):
    """ارسال یک متن بلند به چت با تقسیم خودکار به چند پیام تلگرام.
    header فقط در پیام اول قرار می‌گیرد.
    اگر هدر+بدنه در یک پیام جا شود، یک پیام می‌فرستد.
    در صورت چندتایی، شماره صفحه (مثل «📄 1/3») به ابتدای هر پیام افزوده می‌شود.
    """
    header = header or ""
    body = body or ""
    single = f"{header}{body}"
    if len(single) <= TELEGRAM_MSG_LIMIT:
        try:
            await bot_instance.send_message(chat_id=chat_id, text=single, parse_mode=parse_mode)
        except Exception as e:
            logger.warning(f"ارسال با parse_mode={parse_mode} ناموفق ({e})، بدون parse_mode تلاش می‌کنم")
            await bot_instance.send_message(chat_id=chat_id, text=single)
        return 1

    # اگه هدر خودش بزرگ‌تر از حد بود، جدا بفرست
    if len(header) > TELEGRAM_MSG_LIMIT - 16:
        for h_chunk in _split_message(header):
            try:
                await bot_instance.send_message(chat_id=chat_id, text=h_chunk, parse_mode=parse_mode)
            except Exception:
                await bot_instance.send_message(chat_id=chat_id, text=h_chunk)
        header = ""

    # بدنه را تقسیم می‌کنیم
    available_for_first = TELEGRAM_MSG_LIMIT - len(header) - 16  # 16 برای پیش‌بند صفحه
    available_for_rest = TELEGRAM_MSG_LIMIT - 16

    # اول بخش اول رو با اندازه‌ای می‌بریم که با هدر در یک پیام جا بشه
    first_chunk = body[:available_for_first]
    # سعی کن روی خط جدید/فاصله بشکنی
    cut = first_chunk.rfind('\n')
    if cut < int(available_for_first * 0.6):
        cut = first_chunk.rfind(' ')
    if cut > int(available_for_first * 0.6):
        first_chunk = body[:cut].rstrip()
        rest_start = cut
    else:
        rest_start = available_for_first

    rest = body[rest_start:].lstrip()
    rest_chunks = _split_message(rest, available_for_rest) if rest else []
    all_chunks = [first_chunk] + rest_chunks
    total = len(all_chunks)

    sent = 0
    for idx, chunk in enumerate(all_chunks, start=1):
        prefix = f"📄 {idx}/{total}\n" if total > 1 else ""
        if idx == 1 and header:
            text = f"{header}{prefix}{chunk}"
        else:
            text = f"{prefix}{chunk}"
        if len(text) > TELEGRAM_MSG_LIMIT:
            # امنیت: اگه به هر دلیلی هنوز بزرگ بود، بدون هدر/prefix بفرست
            text = chunk[:TELEGRAM_MSG_LIMIT]
        try:
            await bot_instance.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
            sent += 1
        except Exception as e:
            logger.warning(f"ارسال قطعه {idx}/{total} با parse_mode ناموفق: {e}؛ بدون parse_mode تلاش می‌کنم")
            try:
                await bot_instance.send_message(chat_id=chat_id, text=text)
                sent += 1
            except Exception as e2:
                logger.error(f"خطا در ارسال قطعه {idx}/{total} به {chat_id}: {e2}")
    return sent


ROLE_SENA_CATEGORIES = {
    'security': {'label': '🛡️ امنیتی', 'group': 'role'},
    'economic': {'label': '💹 اقتصادی', 'group': 'role'},
    'sabotage': {'label': '💣 خرابکاری', 'group': 'role'},
    'sena':     {'label': '📜 سنا',     'group': 'sena'},
}


def _today_key_tehran():
    """کلید روز فعلی به وقت تهران؛ روز جدید ساعت 12 ظهر تهران شروع می‌شود."""
    try:
        tz = pytz.timezone('Asia/Tehran')
        now = datetime.now(tz)
    except Exception:
        now = datetime.now()
    # روز جدید بعد از ساعت 12 ظهر تهران شروع می‌شه
    if now.hour < 12:
        base = now - timedelta(days=1)
    else:
        base = now
    return base.strftime('%Y-%m-%d')


def role_sena_is_category_enabled(category):
    """بررسی فعال بودن یک دسته."""
    if category not in ROLE_SENA_CATEGORIES:
        return False
    key = f"role_{category}_enabled" if ROLE_SENA_CATEGORIES[category]['group'] == 'role' else 'sena_enabled'
    val = get_setting(key)
    return val == '1'


def role_sena_set_category_enabled(category, enabled):
    if category not in ROLE_SENA_CATEGORIES:
        return False
    key = f"role_{category}_enabled" if ROLE_SENA_CATEGORIES[category]['group'] == 'role' else 'sena_enabled'
    set_setting(key, '1' if enabled else '0')
    return True


def role_sena_get_limit(group):
    """group: 'role' یا 'sena'"""
    if group == 'role':
        val = get_setting('role_total_daily_limit')
    else:
        val = get_setting('sena_daily_limit')
    try:
        return int(val) if val is not None else 0
    except ValueError:
        return 0


def role_sena_set_limit(group, value):
    if group == 'role':
        set_setting('role_total_daily_limit', str(int(value)))
    else:
        set_setting('sena_daily_limit', str(int(value)))


def role_sena_get_max_chars():
    val = get_setting('role_sena_max_chars')
    try:
        return int(val) if val is not None else 5 * 4096
    except ValueError:
        return 5 * 4096


def role_sena_get_user_used(user_id, category):
    """تعداد استفاده‌شده‌ی کاربر امروز."""
    if category not in ROLE_SENA_CATEGORIES:
        return 0
    day = _today_key_tehran()
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT used_count FROM role_sena_usage WHERE user_id = ? AND category = ? AND day_key = ?",
        (user_id, category, day)
    )
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0


def role_sena_get_group_used(user_id, group):
    """مجموع استفاده‌شده‌ی کاربر در یک گروه (role یا sena) امروز."""
    day = _today_key_tehran()
    cats = [c for c, info in ROLE_SENA_CATEGORIES.items() if info['group'] == group]
    if not cats:
        return 0
    placeholders = ','.join(['?'] * len(cats))
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        f"SELECT COALESCE(SUM(used_count), 0) FROM role_sena_usage "
        f"WHERE user_id = ? AND day_key = ? AND category IN ({placeholders})",
        [user_id, day] + cats
    )
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0


def role_sena_increment_usage(user_id, category):
    """یک واحد به استفاده‌ی کاربر در یک دسته امروز اضافه کن."""
    day = _today_key_tehran()
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT used_count FROM role_sena_usage WHERE user_id = ? AND category = ? AND day_key = ?",
        (user_id, category, day)
    )
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE role_sena_usage SET used_count = used_count + 1 WHERE user_id = ? AND category = ? AND day_key = ?",
            (user_id, category, day)
        )
    else:
        c.execute(
            "INSERT INTO role_sena_usage (user_id, category, day_key, used_count) VALUES (?, ?, ?, 1)",
            (user_id, category, day)
        )
    conn.commit()
    conn.close()


def role_sena_can_send(user_id, category):
    """بررسی اینکه کاربر می‌تواند پیام جدید در این دسته بفرستد یا نه.
    خروجی: (ok: bool, reason: str)
    """
    if category not in ROLE_SENA_CATEGORIES:
        return False, "دسته نامعتبر است."
    if not role_sena_is_category_enabled(category):
        return False, f"بخش «{ROLE_SENA_CATEGORIES[category]['label']}» توسط مدیریت غیرفعال شده است."
    group = ROLE_SENA_CATEGORIES[category]['group']
    limit = role_sena_get_limit(group)
    if limit <= 0:
        # محدودیت صفر = غیرفعال شدن کامل
        return False, "محدودیت ارسال برای این بخش به صفر تنظیم شده است."
    used = role_sena_get_group_used(user_id, group)
    if used >= limit:
        if group == 'role':
            return False, f"سهمیه روزانه شما برای رول‌ها به پایان رسیده ({used}/{limit}). فردا ساعت ۱۲ ظهر تهران ریست می‌شود."
        else:
            return False, f"سهمیه روزانه شما برای سنا به پایان رسیده ({used}/{limit}). فردا ساعت ۱۲ ظهر تهران ریست می‌شود."
    return True, ""


# ===================== توابع گپ‌های فعال =====================

def is_chat_active(chat_id):
    """بررسی اینکه آیا یک گپ برای پلیرها فعال (اکتویت‌شده) است یا نه."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM active_chats WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    return row is not None


def activate_chat(chat_id, title, activated_by):
    """گپ را به لیست گپ‌های فعال اضافه می‌کند."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO active_chats (chat_id, title, activated_by, activated_at) VALUES (?, ?, ?, ?)",
        (chat_id, title, activated_by, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def deactivate_chat(chat_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM active_chats WHERE chat_id = ?", (chat_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted


def get_all_active_chats():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT chat_id, title, activated_by, activated_at FROM active_chats")
    rows = c.fetchall()
    conn.close()
    return [{"chat_id": r[0], "title": r[1], "activated_by": r[2], "activated_at": r[3]} for r in rows]


def get_setting(key):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_setting(key, value):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_trade_setting(key):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM trade_settings WHERE key = ?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_trade_setting(key, value):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO trade_settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_notification_image(event_type):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT photo_id FROM notification_images WHERE event_type = ?", (event_type,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_notification_image(event_type, photo_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO notification_images (event_type, photo_id) VALUES (?, ?)", (event_type, photo_id))
    conn.commit()
    conn.close()


def get_bot_active_status():
    status = get_setting('bot_active')
    return status == '1'


def set_bot_active_status(active: bool):
    set_setting('bot_active', '1' if active else '0')


def get_global_disabled_buttons():
    disabled_buttons_json = get_setting('global_disabled_buttons')
    return json.loads(disabled_buttons_json) if disabled_buttons_json else []


def set_global_disabled_buttons(disabled_buttons: list):
    set_setting('global_disabled_buttons', json.dumps(disabled_buttons))


def get_country(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, name, population, capital, daily_income, religion, oil_barrels, grains, satisfaction, assets, custom_income, loan_amount, loan_date, crypto, security, farm_level, fort_level, workshop_level, internet_nationalized, internet_level, refinery_level, storage_capacity FROM countries WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        country_data = {
            "user_id": row[0],
            "name": row[1],
            "population": row[2],
            "capital": row[3],
            "daily_income": row[4],
            "religion": row[5],
            "oil_barrels": row[6],
            "grains": row[7],
            "satisfaction": row[8],
            "assets": json.loads(row[9]) if row[9] else {},
            "custom_income": row[10],
            "loan_amount": row[11],
            "loan_date": row[12],
            "crypto": row[13],
            "security": row[14],
            "farm_level": row[15],
            "fort_level": row[16],
            "workshop_level": row[17],
            "internet_nationalized": bool(row[18]),
            "internet_level": row[19],
            "refinery_level": row[20],
            "storage_capacity": row[21] if len(row) > 21 and row[18] is not None else 100
        }

        merged_data = get_dynamic_default_assets()
        merged_data.update(country_data)

        if 'assets' in country_data:
            for category, items in country_data['assets'].items():
                if category in merged_data and isinstance(merged_data[category], dict):
                    merged_data[category].update(items)

        return merged_data
    return None


def create_country(user_id, name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    initial_data = get_dynamic_default_assets()
    initial_data['name'] = name

    assets_json = {}
    for key, value in initial_data.items():
        if isinstance(value, dict):
            assets_json[key] = value

    loan_date = initial_data['loan_date'] or None

    c.execute("""
        INSERT INTO countries (
            user_id, name, population, capital, daily_income, religion, oil_barrels,
            satisfaction, assets, custom_income, loan_amount, loan_date, crypto,
            security, farm_level, fort_level, workshop_level, internet_nationalized, internet_level, refinery_level, storage_capacity, grains
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        initial_data['population'],
        initial_data['capital'],
        initial_data['daily_income'],
        initial_data['religion'],
        initial_data.get('oil_barrels', 0),
        initial_data.get('satisfaction', 50),
        json.dumps(assets_json, ensure_ascii=False),
        initial_data.get('custom_income', 0),
        initial_data.get('loan_amount', 0),
        loan_date,
        initial_data.get('crypto', 0),
        initial_data.get('security', 50),
        int(initial_data.get('internet_nationalized', False)),
        initial_data.get('internet_level', 2),
        initial_data.get('refinery_level', 0),
        initial_data.get('storage_capacity', 100),
        initial_data.get('grains', 5000),
        initial_data.get('farm_level', 0),
        initial_data.get('fort_level', 0),
        initial_data.get('workshop_level', 0)
    ))
    conn.commit()
    conn.close()


def update_country(user_id, data):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT assets FROM countries WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        logger.error(f"Attempted to update non-existent country: {user_id}")
        conn.close()
        return

    current_assets = json.loads(row[0]) if row[0] else {}

    top_level_updates = {}
    asset_updates = {}
    dynamic_defaults_for_check = get_dynamic_default_assets()
    for key, value in data.items():
        if key in dynamic_defaults_for_check and isinstance(dynamic_defaults_for_check[key], dict):
            asset_updates[key] = value
        else:
            top_level_updates[key] = value

    for category, items in asset_updates.items():
        if category not in current_assets:
            current_assets[category] = {}
        for item, amount in items.items():
            current_assets[category][item] = amount

    # --- FIX: whitelist برای جلوگیری از SQL injection ---
    ALLOWED_TOP_LEVEL_COLS = {'name','population','capital','daily_income','religion','satisfaction','custom_income','loan_amount','loan_date','security','storage_capacity','farm_level','fort_level','workshop_level','grains'}
    set_clauses = []
    values = []
    for key, value in top_level_updates.items():
        if key not in ALLOWED_TOP_LEVEL_COLS:
            logger.warning(f"Ignoring disallowed column in update_country: {key}")
            continue
        set_clauses.append(f"{key} = ?")
        values.append(value)
    if not set_clauses and not asset_updates:
        logger.warning(f"update_country called with no valid fields for user {user_id}")
        conn.close()
        return

    set_clauses.append("assets = ?")
    values.append(json.dumps(current_assets, ensure_ascii=False))

    values.append(user_id)

    query = f"UPDATE countries SET {', '.join(set_clauses)} WHERE user_id = ?"
    try:
        c.execute(query, values)
        conn.commit()
    except Exception as e:
        logger.error(f"Error updating country {user_id}: {e}")
        raise
    finally:
        conn.close()


def delete_country(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM countries WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_all_countries():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, name FROM countries")
    countries = c.fetchall()
    conn.close()
    return countries


def is_admin(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None


def get_all_admins():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id FROM admins")
    admins = [row[0] for row in c.fetchall()]
    conn.close()
    return admins


def add_admin_to_db(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_admin_from_db(user_id):
    if user_id == OWNER_ID:
        return False
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
    conn.commit()
    rowcount = c.rowcount
    conn.close()
    return rowcount > 0


def save_proposal(user_id, proposal_type, text_content, photo_ids, user_message_id, target_user_id=None, target_country_name=None):
    proposal_id = str(uuid.uuid4())
    submitted_at = datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO proposals (id, user_id, type, status, text_content, photo_ids, submitted_at, user_message_id, target_user_id, target_country_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (proposal_id, user_id, proposal_type, "pending", text_content, json.dumps(photo_ids), submitted_at, user_message_id, target_user_id, target_country_name))
    conn.commit()
    conn.close()
    return proposal_id


def get_proposal(proposal_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT id, user_id, type, status, text_content, photo_ids, submitted_at, admin_message_id, user_message_id, target_user_id, target_country_name FROM proposals WHERE id = ?", (proposal_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "type": row[2],
            "status": row[3],
            "text_content": row[4],
            "photo_ids": json.loads(row[5]) if row[5] else [],
            "submitted_at": row[6],
            "admin_message_id": row[7],
            "user_message_id": row[8],
            "target_user_id": row[9],
            "target_country_name": row[10]
        }
    return None


def update_proposal_status(proposal_id, status, admin_message_id=None):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    if admin_message_id:
        c.execute("UPDATE proposals SET status = ?, admin_message_id = ? WHERE id = ?", (status, admin_message_id, proposal_id))
    else:
        c.execute("UPDATE proposals SET status = ? WHERE id = ?", (status, proposal_id))
    conn.commit()
    conn.close()


def create_trade(sender_id, receiver_id, domain, send_items, receive_items, trade_type):
    trade_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    delivery_minutes = random.randint(5, 17)
    delivery_time = (datetime.now() + timedelta(minutes=delivery_minutes)).isoformat()
    secret_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (
            id, sender_id, receiver_id, domain, send_resource, send_amount,
            receive_resource, receive_amount, trade_type, status, created_at, delivery_time, secret_code
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        trade_id,
        sender_id,
        receiver_id,
        domain,
        json.dumps(send_items),
        0,
        json.dumps(receive_items),
        0,
        trade_type,
        'pending',
        created_at,
        delivery_time,
        secret_code
    ))
    conn.commit()
    conn.close()
    return trade_id, delivery_minutes, secret_code


def get_trade(trade_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "sender_id": row[1],
            "receiver_id": row[2],
            "domain": row[3],
            "send_resource": json.loads(row[4]) if row[4] else [],
            "send_amount": row[5],
            "receive_resource": json.loads(row[6]) if row[6] else [],
            "receive_amount": row[7],
            "trade_type": row[8],
            "status": row[9],
            "created_at": row[10],
            "delivery_time": row[11],
            "completed": bool(row[12]),
            "secret_code": row[13]
        }
    return None


def update_trade_status(trade_id, status):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE trades SET status = ? WHERE id = ?", (status, trade_id))
    conn.commit()
    conn.close()


def complete_trade(trade_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE trades SET completed = 1 WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()


def get_trades_for_delivery():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("SELECT * FROM trades WHERE delivery_time <= ? AND completed = 0 AND status = 'accepted'", (now,))
    trades = []
    for row in c.fetchall():
        trades.append({
            "id": row[0],
            "sender_id": row[1],
            "receiver_id": row[2],
            "domain": row[3],
            "send_resource": json.loads(row[4]) if row[4] else [],
            "send_amount": row[5],
            "receive_resource": json.loads(row[6]) if row[6] else [],
            "receive_amount": row[7],
            "trade_type": row[8],
            "status": row[9],
            "created_at": row[10],
            "delivery_time": row[11],
            "completed": bool(row[12]),
            "secret_code": row[13]
        })
    conn.close()
    return trades


def save_random_prize(category, item, quantity):
    prize_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO random_prizes (id, category, item, quantity, created_at) VALUES (?, ?, ?, ?, ?)",
              (prize_id, category, item, quantity, created_at))
    conn.commit()
    conn.close()
    return prize_id


def get_random_prize(prize_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM random_prizes WHERE id = ?", (prize_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "category": row[1],
            "item": row[2],
            "quantity": row[3],
            "created_at": row[4]
        }
    return None


def calculate_daily_income(country):
    base_income = country.get('daily_income', 0)
    custom_income = country.get('custom_income', 0)
    # قبل 1600: فقط مالیات و عوارض کاروان
    return base_income + custom_income


async def daily_production_job(context: CallbackContext):
    logger.info("شروع توزیع خودکار سود و تولید روزانه...")
    countries = get_all_countries()

    if not countries:
        logger.info("هیچ کشوری برای توزیع سود وجود ندارد")
        return

    logger.info(f"توزیع سود و تولید به {len(countries)} کشور")

    for user_id, name in countries:
        country = get_country(user_id)
        if not country:
            continue

        # --- تولید مزرعه ---
        farm_prod = get_farm_production(int(country.get('farm_level', 0) or 0))
        # اول تولید را اضافه کن
        country['grains'] = int(country.get('grains', 0) or 0) + farm_prod

        # --- مصرف روزانه غلات و مرگ بر اثر گرسنگی ---
        consumption, dead_total, deaths, new_grains = apply_grain_starvation(country)
        grain_updates = {'grains': new_grains}
        if dead_total > 0:
            troops = dict(country.get('land_troops', {}) or {})
            for unit, die in deaths.items():
                if unit in troops:
                    troops[unit] = max(0, int(troops.get(unit,0)) - die)
            grain_updates['land_troops'] = troops
            pop_loss = dead_total * 10
            grain_updates['population'] = max(0, int(country.get('population',0)) - pop_loss)

        total_income = calculate_daily_income(country)
        new_capital = country['capital'] + total_income

        updates = {'capital': new_capital}
        # کارگاه: تولید روزانه بر اساس تنظیم ادمین
        workshop_lvl = int(country.get('workshop_level',0) or 0)
        soldier, amount = get_daily_workshop_production(workshop_lvl) if workshop_lvl>0 else (None, 0)
        if soldier and amount:
            # اگر قحطی troops را عوض کرده، از grain_updates بگیر
            base_troops = grain_updates.get('land_troops', country.get('land_troops', {}) or {}) if 'land_troops' in grain_updates else country.get('land_troops', {}) or {}
            base_troops = dict(base_troops)
            base_troops[soldier] = int(base_troops.get(soldier,0)) + int(amount)
            grain_updates['land_troops'] = base_troops
        updates.update(grain_updates)
        update_country(user_id, updates)

        logger.info(f"برای کشور {name} (ID: {user_id}): سود و تولید انجام شد.")

        try:
            message = (
                f"🌅 به روز جدید خوش آمدید!\n"
                f"✅ سود روزانه شما به مبلغ {total_income:,} به سرمایه اضافه شد\n"
                f"💰 سرمایه جدید: {new_capital:,}"
            )


            if farm_prod > 0:
                message += f"\n🌾 مزرعه: +{farm_prod} غلات"
            message += f"\n🌾 غلات: مصرف {consumption} - باقی {new_grains:,}"
            if dead_total > 0:
                death_detail = ", ".join([f"{get_asset_display_name(k)}:{v}" for k,v in deaths.items()])
                message += f"\n💀 مرگ بر اثر گرسنگی: {dead_total} نفر ({death_detail})"

            await context.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"خطا در ارسال پیام به کاربر {user_id}: {e}")

    logger.info("توزیع سود و تولید روزانه با موفقیت انجام شد")


async def run_daily_production_manually(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return

    await daily_production_job(context)
    await update.message.reply_text("✅ توزیع سود و تولید روزانه به صورت دستی انجام شد")


def get_asset_display_name(asset_key):
    """Get display name for asset key with fallback (dynamic from DB)"""
    try:
        dynamic_names = get_dynamic_asset_names()
        return dynamic_names.get(asset_key, asset_key.replace('_', ' ').title())
    except Exception:
        return ASSET_NAMES.get(asset_key, asset_key.replace('_', ' ').title())


async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_id = user.id
    chat = update.effective_chat
    chat_type = chat.type if chat else None
    try:
        # بررسی وضعیت کلی ربات (مالک همیشه دسترسی داره)
        if not get_bot_active_status() and user_id != OWNER_ID:
            if update.message:
                await update.message.reply_text("🤖 ربات موقتاً غیرفعال است!")
            elif update.callback_query:
                await update.callback_query.answer("🤖 ربات موقتاً غیرفعال است!", show_alert=True)
            return ConversationHandler.END

        # ===== حالت پی‌وی =====
        if chat_type == "private":
            # ادمین در پی‌وی: دسترسی کامل
            if is_admin(user_id):
                country_data = get_country(user_id)
                if not country_data:
                    return await admin_panel(update, context)
                return await show_main_menu(update, context)

            # پلیر در پی‌وی: فقط پاسخ یکباره به /start
            if update.message:
                await update.message.reply_text(
                    "👋 سلام!\n\n"
                    "🗨️ گپ خود را از ادمین تحویل بگیرید.\n"
                    "ربات در پی‌وی به پیام‌های شما پاسخ نمی‌دهد."
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    "گپ خود را از ادمین تحویل بگیرید.", show_alert=True
                )
            return ConversationHandler.END

        # ===== حالت گپ =====
        # ادمین در گپ: پنل ادمین در هر گپی فعال است
        if is_admin(user_id):
            country_data = get_country(user_id)
            if not country_data:
                return await admin_panel(update, context)
            return await show_main_menu(update, context)

        # پلیر در گپ: فقط در گپ‌های فعال‌شده دسترسی دارد
        chat_id = chat.id if chat else None
        if chat_id and is_chat_active(chat_id):
            country_data = get_country(user_id)
            if not country_data:
                msg = "⚠️ شما هنوز کشور خود را ثبت نکرده‌اید!\nلطفاً آیدی عددی خود را به مالک ربات ارسال کنید."
                if update.message:
                    await update.message.reply_text(msg)
                elif update.callback_query:
                    await update.callback_query.answer(msg, show_alert=True)
                return ConversationHandler.END
            return await show_main_menu(update, context)
        else:
            # گپ فعال نیست؛ به پلیر هیچ پاسخی ندیم تا اسپم نشه
            return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in start: {e}", exc_info=True)
        try:
            if update.message:
                await update.message.reply_text("متاسفانه خطایی رخ داد. لطفاً /start را دوباره ارسال کنید.")
        except Exception:
            pass
        return ConversationHandler.END


async def show_main_menu(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        if not get_bot_active_status() and user_id != OWNER_ID:
            if update.callback_query:
                await update.callback_query.answer("🤖 ربات موقتاً غیرفعال است!", show_alert=True)
            return MAIN_MENU
        country = get_country(user_id)
        if not country:
            error_msg = "❌ کشور شما یافت نشد. لطفاً با مالک ربات تماس بگیرید."
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
                await update.callback_query.edit_message_text(error_msg)
            else:
                await update.message.reply_text(error_msg)
            return ConversationHandler.END
        keyboard = [
            [InlineKeyboardButton("📊 اطلاعات کشور", callback_data='cat_player_info')],
            [InlineKeyboardButton("⚔️ نظامی", callback_data='cat_player_military')],
            [InlineKeyboardButton("💰 اقتصاد", callback_data='cat_player_economy')],
            [InlineKeyboardButton("📜 سیاسی", callback_data='cat_player_political')],
            [InlineKeyboardButton("🏰 مدیریت قلعه", callback_data='castle_menu')],
        ]
        if is_admin(user_id):
            keyboard.append([InlineKeyboardButton("👑 پنل مدیریت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = f"سلام رهبر {country['name']}!\nبه ربات {BOT_NAME} خوش آمدید.\nلطفا یک دسته را انتخاب کنید:"
        if update.message:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        elif update.callback_query:
            try:
                await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
            except:
                await update.callback_query.message.reply_text(message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error showing main menu: {e}", exc_info=True)
        if update.effective_chat:
            await update.effective_chat.send_message("متاسفانه خطایی رخ داد. لطفاً /start را دوباره ارسال کنید.")
    return MAIN_MENU

async def player_cat_info(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    kb = [
        [InlineKeyboardButton("📊 لیست دارایی", callback_data='show_assets')],
        [InlineKeyboardButton("🏛️ مدیریت کشور", callback_data='country_management')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')],
    ]
    await query.edit_message_text("📊 اطلاعات کشور:", reply_markup=InlineKeyboardMarkup(kb))
    return MAIN_MENU

async def player_cat_military(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    disabled = get_global_disabled_buttons()
    kb = []
    if 'campaign_menu' not in disabled:
        kb.append([InlineKeyboardButton("⚔️ لشکر‌کشی", callback_data='campaign_menu')])
    if 'siege_menu' not in disabled:
        kb.append([InlineKeyboardButton("🏰 محاصره", callback_data='siege_menu')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
    await query.edit_message_text("⚔️ عملیات نظامی:", reply_markup=InlineKeyboardMarkup(kb))
    return MAIN_MENU

async def player_cat_economy(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    kb = [
        [InlineKeyboardButton("🛒 درخواست خرید", callback_data='shop_menu_start')],
        [InlineKeyboardButton("🏗️ ارسال ساخت و ساز", callback_data='construction_proposal_start')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')],
    ]
    await query.edit_message_text("💰 اقتصاد:", reply_markup=InlineKeyboardMarkup(kb))
    return MAIN_MENU

async def player_cat_political(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    kb = [
        [InlineKeyboardButton("📜 ارسال رول و سنا", callback_data='role_sena_menu')],
        [InlineKeyboardButton("📣 ارسال بیانیه", callback_data='statement_proposal_start')],
        [InlineKeyboardButton("☪️ تنظیم دین", callback_data='religion_menu')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')],
    ]
    await query.edit_message_text("📜 سیاسی:", reply_markup=InlineKeyboardMarkup(kb))
    return MAIN_MENU


async def show_assets(update: Update, context: CallbackContext, target_user_id: int = None):
    query = update.callback_query
    if query:
        await query.answer()
    try:
        user_id = target_user_id if target_user_id else (query.from_user.id if query else update.effective_user.id)
        country = get_country(user_id)
        if not country:
            message = "❌ کشور مورد نظر یافت نشد."
            if query:
                await query.edit_message_text(message)
            else:
                await update.message.reply_text(message)
            return ConversationHandler.END
        total_income = calculate_daily_income(country)

        message = f"🏛️ *وضعیت کشور {country.get('name', 'نامعلوم')}*\n\n"
        message += f"👫 جمعیت: {country.get('population', 0):,}\n"
        message += f"💰 سرمایه: {country.get('capital', 0):,}\n"
        message += f"💹 سود روزانه: {total_income:,}\n\n"

        message += f"😊 رضایت: {country.get('satisfaction', 0)}%\n"
        message += f"🛡️ امنیت: {country.get('security', 0)}%\n"
        religion_display_name = next((disp for code, disp in RELIGIONS if code == country.get('religion', '')), 'نامعلوم')
        message += f"☪️ دین: {religion_display_name}\n"
        message += f"🌾 غلات: {country.get('grains', 0):,}\n"
        message += f"🌾 مزرعه: سطح {country.get('farm_level', 0)} (تولید +{get_farm_production(int(country.get('farm_level',0) or 0))}/روز)\n"
        message += f"🏰 استحکامات: سطح {country.get('fort_level', 0)} ({FORT_LEVELS.get(int(country.get('fort_level',0) or 0),{}).get('name','بی‌دفاع')})\n"
        message += f"⚒️ کارگاه: سطح {country.get('workshop_level', 0)} ({WORKSHOP_LEVELS.get(int(country.get('workshop_level',0) or 0),{}).get('name','ویرانه')})\n"
        message += "\n"
        used = calculate_storage_used(country)
        capacity = country.get("storage_capacity", 100)
        message += f"📦 انبار: {used} / {capacity} واحد\n\n"

        for category_key, category_display_name in get_dynamic_asset_categories_for_display():
            assets_dict = country.get(category_key, {})
            if isinstance(assets_dict, dict):
                message += f"*{category_display_name}:*\n"
                for item_key, count in assets_dict.items():
                    display_name = get_asset_display_name(item_key)
                    message += f"• {display_name}: {count:,}\n"
                message += "\n"

        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')]]
        if target_user_id and is_admin(update.effective_user.id):
            keyboard = [[InlineKeyboardButton("🔙 بازگشت به پنل مدیریت", callback_data='admin_panel')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query:
            await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_assets: {e}", exc_info=True)
        if query:
            await query.answer("خطا در نمایش دارایی‌ها.", show_alert=True)
        else:
            await update.message.reply_text("خطا در نمایش دارایی‌ها.")

    if target_user_id and is_admin(update.effective_user.id):
        return ADMIN_MENU
    return MAIN_MENU


async def admin_panel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        if update.message:
            await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        else:
            await update.callback_query.answer("⛔️ فقط ادمین‌ها دسترسی دارند!", show_alert=True)
        return MAIN_MENU
    try:
        keyboard = [
            [InlineKeyboardButton("👥 کشورها", callback_data='cat_admin_countries')],
            [InlineKeyboardButton("⚙️ تنظیمات ربات", callback_data='cat_admin_settings')],
            [InlineKeyboardButton("👑 ادمین‌ها", callback_data='cat_admin_admins')],
            [InlineKeyboardButton("🎁 جوایز و اعلام", callback_data='cat_admin_rewards')],
            [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data='back_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = "👑 پنل مدیریت کشورها - یک دسته را انتخاب کنید:"
        if update.message:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        elif update.callback_query:
            try:
                await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
            except:
                await update.callback_query.message.reply_text(message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error showing admin panel: {e}", exc_info=True)
        if update.effective_chat:
            await update.effective_chat.send_message("متاسفانه خطایی در پنل مدیریت رخ داد. لطفاً /start را دوباره ارسال کنید.")
    return ADMIN_MENU

async def admin_cat_countries(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    kb = [
        [InlineKeyboardButton("📊 مشاهده دارایی کشورها", callback_data='select_country_view_assets')],
        [InlineKeyboardButton("⚙️ ویرایش ویژگی‌های اصلی", callback_data='edit_main_props')],
        [InlineKeyboardButton("⚔️ ویرایش نیروها و دارایی‌ها", callback_data='edit_assets_menu')],
        [InlineKeyboardButton("➕ افزودن نیرو", callback_data='add_force')],
        [InlineKeyboardButton("🗑️ حذف نیرو", callback_data='delete_force_menu')],
        [InlineKeyboardButton("📦 ویرایش ظرفیت انبار", callback_data='edit_storage_capacity')],
        [InlineKeyboardButton("⚒️ تنظیم کارگاه (تولید روزانه)", callback_data='workshop_cfg_menu')],
        [InlineKeyboardButton("💎 مدیریت دارایی‌ها", callback_data='darayi_menu')],
        [InlineKeyboardButton("🗑️ حذف تکی کشور", callback_data='delete_single_menu')],
        [InlineKeyboardButton("💥 حذف همه کشورها", callback_data='delete_all_menu')],
        [InlineKeyboardButton("🌪️ بلایای طبیعی", callback_data='disaster_menu')],
        [InlineKeyboardButton("📋 لیست کشورها", callback_data='list_countries')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')],
    ]
    await q.edit_message_text("👥 مدیریت کشورها:", reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU

async def admin_cat_settings(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    kb = [
        [InlineKeyboardButton("🔌 خاموش/روشن ربات", callback_data='toggle_bot')],
        [InlineKeyboardButton("⚙️ مدیریت دکمه‌های عمومی", callback_data='manage_global_buttons')],
        [InlineKeyboardButton("🚦 تعیین محدودیت", callback_data='role_sena_limits_menu')],
        [InlineKeyboardButton("🤝 مدیریت تجارت", callback_data='trade_settings')],
        [InlineKeyboardButton("🖼️ مدیریت عکس اطلاعیه‌ها", callback_data='manage_notification_images')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')],
    ]
    await q.edit_message_text("⚙️ تنظیمات ربات:", reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU

async def admin_cat_admins(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    kb = [
        [InlineKeyboardButton("👑 افزودن ادمین", callback_data='add_admin')],
        [InlineKeyboardButton("🗑 حذف ادمین", callback_data='remove_admin')],
        [InlineKeyboardButton("آپ دارایی", callback_data='admin_update_assets')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')],
    ]
    await q.edit_message_text("👑 مدیریت ادمین‌ها:", reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU

async def admin_cat_rewards(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    kb = [
        [InlineKeyboardButton("🎁 جایزه رندوم", callback_data='random_prize_menu')],
        [InlineKeyboardButton("😊 اعلام برترین رضایت", callback_data='announce_top_satisfaction')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')],
    ]
    await q.edit_message_text("🎁 جوایز و اعلام:", reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU


async def select_country_view_assets(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("هیچ کشوری برای نمایش وجود ندارد.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"view_assets_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("لطفاً کشوری را برای مشاهده دارایی‌هایش انتخاب کنید:", reply_markup=reply_markup)
        return SELECT_COUNTRY_TO_VIEW_ASSETS
    except Exception as e:
        logger.error(f"Error in select_country_view_assets: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return ADMIN_MENU


async def handle_view_selected_country_assets(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("view_assets_", ""))
        return await show_assets(update, context, target_user_id=target_user_id)
    except Exception as e:
        logger.error(f"Error in handle_view_selected_country_assets: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش دارایی کشور")
        return ADMIN_MENU


async def edit_main_props(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("هیچ کشوری برای ویرایش وجود ندارد.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"edit_main_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("لطفاً کشوری را برای ویرایش ویژگی‌های اصلی انتخاب کنید:", reply_markup=reply_markup)
        return EDIT_MAIN_PROPS
    except Exception as e:
        logger.error(f"Error in edit_main_props: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return ADMIN_MENU


async def select_main_prop_to_edit(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_edit = int(query.data.replace("edit_main_country_", ""))
        context.user_data['user_id_to_edit'] = user_id_to_edit
        country = get_country(user_id_to_edit)
        if not country:
            await query.edit_message_text("❌ کشور مورد نظر یافت نشد.")
            return ADMIN_MENU

        main_properties = [
            ('daily_income', "خراج روزانه 💰"),
            ('capital', "خزانه 💰"),
            ('population', "جمعیت 👫"),
            ('satisfaction', "رضایت 😊"),
            ('security', "امنیت کشور 🛡️"),
            ('grains', "غلات 🌾"),
            ('farm_level', "سطح مزرعه 🌾"),
            ('fort_level', "سطح استحکامات 🏰"),
            ('workshop_level', "سطح کارگاه ⚒️"),
        ]

        keyboard = []
        for prop_key, prop_name in main_properties:
            current_value = country.get(prop_key, 0)
            keyboard.append([InlineKeyboardButton(f"{prop_name} (فعلی: {current_value:,})", callback_data=f"set_main_prop_{prop_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='edit_main_props')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"ویرایش ویژگی‌های اصلی برای {country['name']}:\nلطفاً ویژگی مورد نظر را انتخاب کنید:", reply_markup=reply_markup)
        return SELECT_MAIN_PROP
    except Exception as e:
        logger.error(f"Error in select_main_prop_to_edit: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت اطلاعات کشور")
        return ADMIN_MENU


async def get_main_prop_value(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        prop_key = query.data.replace("set_main_prop_", "")
        context.user_data['edit_main_prop_key'] = prop_key
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        country = get_country(user_id_to_edit)
        prop_display_name = get_asset_display_name(prop_key)
        current_value = country.get(prop_key, 0)
        await query.edit_message_text(f"ویرایش {prop_display_name} برای {country['name']}:\n"
                                      f"مقدار فعلی: {current_value:,}\n"
                                      "لطفاً مقدار جدید (عدد صحیح) را وارد کنید (برای کاهش از علامت - استفاده کنید):")
        return GET_MAIN_PROP_VALUE
    except Exception as e:
        logger.error(f"Error in get_main_prop_value: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت اطلاعات ویژگی")
        return ADMIN_MENU


async def save_main_prop_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        prop_key = context.user_data.get('edit_main_prop_key')
        if not user_id_to_edit or not prop_key:
            await update.message.reply_text("خطا در پردازش درخواست. لطفاً دوباره تلاش کنید.")
            return await admin_panel(update, context)

        value_str = update.message.text.strip()
        if value_str.startswith('+') or value_str.startswith('-'):
            is_relative = True
            value = int(value_str)
        else:
            is_relative = False
            value = int(value_str)

        if prop_key in ['satisfaction', 'security'] and not (0 <= value <= 100):
            await update.message.reply_text(f"برای {get_asset_display_name(prop_key)}، مقدار باید بین 0 تا 100 باشد. لطفاً مجدداً وارد کنید.")
            return GET_MAIN_PROP_VALUE
    except ValueError:
        await update.message.reply_text("مقدار وارد شده نامعتبر است. لطفاً یک عدد صحیح وارد کنید.")
        return GET_MAIN_PROP_VALUE
    try:
        country = get_country(user_id_to_edit)
        if not country:
            await update.message.reply_text("خطا: اطلاعات کشور یافت نشد.")
            return await admin_panel(update, context)

        if is_relative:
            new_value = country.get(prop_key, 0) + value
            if prop_key in ['satisfaction', 'security']:
                new_value = max(0, min(100, new_value))
        else:
            new_value = value

        update_country(user_id_to_edit, {prop_key: new_value})

        prop_display_name = get_asset_display_name(prop_key)
        await update.message.reply_text(f"✅ {prop_display_name} برای {country['name']} به {new_value:,} تغییر یافت.")
        context.user_data.pop('user_id_to_edit', None)
        context.user_data.pop('edit_main_prop_key', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_main_prop_value: {e}", exc_info=True)
        await update.message.reply_text("خطا در ذخیره‌سازی تغییرات")
        return await admin_panel(update, context)


async def edit_assets_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("هیچ کشوری برای ویرایش وجود ندارد.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"edit_assets_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("لطفاً کشوری را برای ویرایش نیروها و دارایی‌ها انتخاب کنید:", reply_markup=reply_markup)
        return EDIT_ASSETS_MENU
    except Exception as e:
        logger.error(f"Error in edit_assets_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return ADMIN_MENU



async def edit_storage_capacity(update: Update, context: CallbackContext) -> int:
    """نمایش لیست کشورها برای ویرایش ظرفیت انبار (با نمایش لول)"""
    query = update.callback_query
    await query.answer()
    try:
        countries = get_all_countries()
        if not countries:
            await query.edit_message_text("هیچ کشوری وجود ندارد.")
            return ADMIN_MENU
        keyboard = []
        for user_id, name in countries:
            c = get_country(user_id)
            cap = c.get('storage_capacity', 100) if c else 100
            lvl = get_storage_level(cap)
            keyboard.append([InlineKeyboardButton(f"{name} — لول {lvl} ({cap})", callback_data=f"storage_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📦 کشوری را برای ویرایش سطح انبار انتخاب کنید:", reply_markup=reply_markup)
        return ADMIN_MENU
        
    except Exception as e:
        logger.error(f"Error in edit_storage_capacity: {e}")
        await query.edit_message_text("خطا در بارگذاری لیست کشورها.")
        return ADMIN_MENU


async def select_country_for_storage(update: Update, context: CallbackContext) -> int:
    """انتخاب کشور و نمایش لول + دکمه‌های ارتقا"""
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("storage_country_", ""))
        context.user_data['storage_edit_user_id'] = target_user_id
        country = get_country(target_user_id)
        if not country:
            await query.edit_message_text("کشور یافت نشد.")
            return ADMIN_MENU
        current_capacity = country.get('storage_capacity', 100)
        used = calculate_storage_used(country)
        lvl = get_storage_level(current_capacity)
        nxt_lvl, nxt_data = get_next_storage_upgrade(current_capacity)
        keyboard = []
        for l in sorted(STORAGE_LEVELS.keys()):
            cap = STORAGE_LEVELS[l]['capacity']
            cost = STORAGE_LEVELS[l]['cost']
            mark = "✅" if l == lvl else "🔓" if l < lvl else "🔒"
            keyboard.append([InlineKeyboardButton(f"{mark} لول {l} — {cap} واحد (هزینه {cost:,})", callback_data=f"storage_set_level_{l}")])
        keyboard.append([InlineKeyboardButton("✏️ وارد کردن عدد دستی", callback_data="storage_custom_input")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="edit_storage_capacity")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            f"📦 کشور: {country['name']}\n"
            f"سطح فعلی: لول {lvl} ({current_capacity} واحد)\n"
            f"استفاده شده: {used} واحد\n"
        )
        if nxt_lvl:
            text += f"⬆️ لول بعدی: {nxt_lvl} ({nxt_data['capacity']} واحد) هزینه {nxt_data['cost']:,}\n"
        else:
            text += "🏆 حداکثر لول!\n"
        text += "\nیک لول را انتخاب کنید یا عدد دستی وارد کنید:"
        await query.edit_message_text(text, reply_markup=reply_markup)
        return ADMIN_MENU
        
    except Exception as e:
        logger.error(f"Error in select_country_for_storage: {e}")
        await query.edit_message_text("خطا در انتخاب کشور.")
        return ADMIN_MENU



async def set_storage_level(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        lvl = int(query.data.replace("storage_set_level_", ""))
        target_user_id = context.user_data.get('storage_edit_user_id')
        if not target_user_id:
            await query.edit_message_text("خطا: کشور انتخاب نشده.")
            return ADMIN_MENU
        if lvl not in STORAGE_LEVELS:
            await query.answer("لول نامعتبر!", show_alert=True)
            return ADMIN_MENU
        new_cap = STORAGE_LEVELS[lvl]['capacity']
        conn = __import__('sqlite3').connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("UPDATE countries SET storage_capacity = ? WHERE user_id = ?", (new_cap, target_user_id))
        conn.commit()
        conn.close()
        country = get_country(target_user_id)
        await query.edit_message_text(f"✅ انبار کشور {country['name']} به لول {lvl} ({new_cap} واحد) ارتقا یافت.")
        if 'storage_edit_user_id' in context.user_data:
            del context.user_data['storage_edit_user_id']
        return ADMIN_MENU
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error set_storage_level: {e}")
        await query.edit_message_text("خطا در تنظیم لول انبار.")
        return ADMIN_MENU


async def storage_custom_input_prompt(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✏️ ظرفیت جدید را به صورت عدد (۵۰ تا ۱۰۰۰) وارد کنید:")
    return ADMIN_MENU


async def get_new_storage_capacity(update: Update, context: CallbackContext) -> int:
    """دریافت مقدار جدید و به‌روزرسانی"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("فقط ادمین‌ها دسترسی دارند.")
        return MAIN_MENU
    
    target_user_id = context.user_data.get('storage_edit_user_id')
    if not target_user_id:
        await update.message.reply_text("خطا: کشور انتخاب نشده است.")
        return MAIN_MENU
    
    try:
        new_capacity = int(update.message.text)
        if new_capacity < 50 or new_capacity > 1000:
            await update.message.reply_text("ظرفیت باید بین ۵۰ تا ۱۰۰۰ باشد.")
            return ADMIN_MENU
        
        # به‌روزرسانی ظرفیت
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("UPDATE countries SET storage_capacity = ? WHERE user_id = ?", (new_capacity, target_user_id))
        conn.commit()
        conn.close()
        
        country = get_country(target_user_id)
        await update.message.reply_text(
            f"✅ ظرفیت انبار کشور {country['name']} با موفقیت به {new_capacity} واحد تغییر یافت."
        )
        
        # پاک کردن داده‌های موقت
        if 'storage_edit_user_id' in context.user_data:
            del context.user_data['storage_edit_user_id']
        
        return ADMIN_MENU
        
    except ValueError:
        await update.message.reply_text("لطفاً فقط عدد وارد کنید.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in get_new_storage_capacity: {e}")
        await update.message.reply_text("خطا در به‌روزرسانی ظرفیت.")
        return ADMIN_MENU
async def select_asset_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_edit = int(query.data.replace("edit_assets_country_", ""))
        context.user_data['user_id_to_edit'] = user_id_to_edit
        country = get_country(user_id_to_edit)
        if not country:
            await query.edit_message_text("❌ کشور مورد نظر یافت نشد.")
            return ADMIN_MENU
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"select_asset_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='edit_assets_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"ویرایش نیروها و دارایی‌ها برای {country['name']}:\nلطفاً دسته‌بندی مورد نظر را انتخاب کنید:", reply_markup=reply_markup)
        return SELECT_ASSET_CATEGORY
    except Exception as e:
        logger.error(f"Error in select_asset_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت اطلاعات کشور")
        return ADMIN_MENU


async def select_asset_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        category_key = query.data.replace("select_asset_category_", "")
        context.user_data['asset_category'] = category_key
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        country = get_country(user_id_to_edit)

        if category_key not in country or not isinstance(country[category_key], dict):
            await query.edit_message_text("❌ دسته‌بندی مورد نظر یافت نشد.")
            return await select_asset_category(update, context)
        keyboard = []
        for item_key in country[category_key].keys():
            current_count = country[category_key].get(item_key, 0)
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(f"{display_name} (فعلی: {current_count:,})", callback_data=f"set_asset_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"edit_assets_country_{user_id_to_edit}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(f"ویرایش آیتم‌های {category_display_name} برای {country['name']}:\nلطفاً آیتم مورد نظر را انتخاب کنید:", reply_markup=reply_markup)
        return SELECT_ASSET_ITEM
    except Exception as e:
        logger.error(f"Error in select_asset_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت آیتم‌ها")
        return SELECT_ASSET_CATEGORY


async def get_asset_edit_value(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("set_asset_item_", "")
        context.user_data['asset_item'] = item_key
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        category_key = context.user_data.get('asset_category')
        country = get_country(user_id_to_edit)

        current_count = country.get(category_key, {}).get(item_key, 0)
        item_display_name = get_asset_display_name(item_key)

        await query.edit_message_text(f"ویرایش {item_display_name} برای {country['name']}:\n"
                                      f"تعداد فعلی: {current_count:,}\n"
                                      "لطفاً مقدار جدید را وارد کنید (برای کاهش از علامت - استفاده کنید):")
        return GET_ASSET_EDIT_VALUE
    except Exception as e:
        logger.error(f"Error in get_asset_edit_value: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت اطلاعات آیتم")
        return SELECT_ASSET_ITEM


async def save_asset_edit_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        category_key = context.user_data.get('asset_category')
        item_key = context.user_data.get('asset_item')
        if not user_id_to_edit or not category_key or not item_key:
            await update.message.reply_text("خطا در پردازش درخواست. لطفاً دوباره تلاش کنید.")
            return await admin_panel(update, context)

        value_str = update.message.text.strip()
        if value_str.startswith('+') or value_str.startswith('-'):
            is_relative = True
            value = int(value_str)
        else:
            is_relative = False
            value = int(value_str)
    except ValueError:
        await update.message.reply_text("مقدار وارد شده نامعتبر است. لطفاً یک عدد صحیح وارد کنید.")
        return GET_ASSET_EDIT_VALUE
    try:
        country = get_country(user_id_to_edit)
        if not country:
            await update.message.reply_text("خطا: اطلاعات کشور یافت نشد.")
            return await admin_panel(update, context)

        current_count = country.get(category_key, {}).get(item_key, 0)
        if is_relative:
            new_count = current_count + value
            if new_count < 0:
                new_count = 0
        else:
            new_count = value if value >= 0 else 0

        update_data = {
            category_key: {
                item_key: new_count
            }
        }
        update_country(user_id_to_edit, update_data)

        item_display_name = get_asset_display_name(item_key)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)

        await update.message.reply_text(f"✅ {item_display_name} در {category_display_name} برای {country['name']} به {new_count:,} تغییر یافت.")
        context.user_data.pop('user_id_to_edit', None)
        context.user_data.pop('asset_category', None)
        context.user_data.pop('asset_item', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_asset_edit_value: {e}", exc_info=True)
        await update.message.reply_text("خطا در ذخیره‌سازی تغییرات")
        return await admin_panel(update, context)


# ========================== لشکر‌کشی (Campaign) ==========================

CAMPAIGN_TYPE_LABELS = {
    'air': '✈️ هوایی',
    'land': '🪖 زمینی',
    'sea': '🚢 دریایی'
}


async def campaign_menu(update: Update, context: CallbackContext) -> int:
    """مرحله ۱: انتخاب کشور هدف برای لشکر‌کشی."""
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ شما هنوز کشوری ثبت نکرده‌اید.")
            return MAIN_MENU
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != user_id]
        if not other_countries:
            await query.edit_message_text("در حال حاضر هیچ کشور دیگری برای لشکر‌کشی وجود ندارد.")
            return MAIN_MENU

        # ریست داده‌های موقت
        context.user_data.pop('campaign', None)
        context.user_data['campaign'] = {
            'types': set(),  # 'air', 'land', 'sea'
        }

        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"campaign_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "⚔️ *لشکر‌کشی*\n\n"
            "🎯 لطفاً کشور هدف را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return CAMPAIGN_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in campaign_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی لشکر‌کشی")
        return MAIN_MENU


async def campaign_select_target(update: Update, context: CallbackContext) -> int:
    """مرحله ۲: نمایش انتخاب نوع نیروها (هوایی/زمینی/دریایی)."""
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("campaign_target_", ""))
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("❌ کشور هدف یافت نشد.")
            return await campaign_menu(update, context)
        context.user_data.setdefault('campaign', {})
        context.user_data['campaign']['target_id'] = target_user_id
        context.user_data['campaign']['target_name'] = target_country['name']
        context.user_data['campaign']['types'] = set()
        return await _show_campaign_types_menu(update, context)
    except Exception as e:
        logger.error(f"Error in campaign_select_target: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کشور هدف")
        return CAMPAIGN_SELECT_TARGET


async def _show_campaign_types_menu(update: Update, context: CallbackContext) -> int:
    """نمایش منوی انتخاب نوع نیروها با تیک."""
    campaign = context.user_data.get('campaign', {})
    selected = campaign.get('types', set())
    target_name = campaign.get('target_name', '')

    def btn(label_key, label_text):
        check = "✅ " if label_key in selected else "▫️ "
        return InlineKeyboardButton(check + label_text, callback_data=f"campaign_toggle_{label_key}")

    keyboard = [
        [btn('air', 'هوایی ✈️')],
        [btn('land', 'زمینی 🪖')],
        [btn('sea', 'دریایی 🚢')],
        [InlineKeyboardButton("⚔️ لشکر‌کشی", callback_data='campaign_start_input')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='campaign_back_targets')]
    ]
    text = (
        f"⚔️ *لشکر‌کشی به {target_name}*\n\n"
        "🎖️ نوع نیروهای اعزامی را انتخاب کنید (می‌توانید چند نوع را همزمان انتخاب کنید):\n\n"
        "سپس روی «⚔️ لشکر‌کشی» بزنید تا تجهیزات و سناریو را وارد کنید."
    )
    query = update.callback_query
    try:
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Edit failed in campaign types menu: {e}")
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return CAMPAIGN_SELECT_TYPES


async def campaign_toggle_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    type_key = query.data.replace("campaign_toggle_", "")
    if type_key not in ('air', 'land', 'sea'):
        return CAMPAIGN_SELECT_TYPES
    campaign = context.user_data.setdefault('campaign', {})
    selected = set(campaign.get('types', set()))
    if type_key in selected:
        selected.remove(type_key)
    else:
        selected.add(type_key)
    campaign['types'] = selected
    return await _show_campaign_types_menu(update, context)


async def campaign_back_targets(update: Update, context: CallbackContext) -> int:
    """برگشت به انتخاب کشور هدف."""
    return await campaign_menu(update, context)


async def campaign_start_input(update: Update, context: CallbackContext) -> int:
    """مرحله ۳: درخواست وارد کردن لیست تجهیزات."""
    query = update.callback_query
    await query.answer()
    campaign = context.user_data.get('campaign', {})
    selected = campaign.get('types', set())
    if not selected:
        await query.answer("❌ حداقل یک نوع نیرو را انتخاب کنید!", show_alert=True)
        return CAMPAIGN_SELECT_TYPES

    target_name = campaign.get('target_name', '')
    types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in ['air', 'land', 'sea'] if t in selected)
    await query.edit_message_text(
        f"⚔️ *لشکر‌کشی به {target_name}*\n"
        f"🎖️ نوع نیروها: {types_str}\n\n"
        "📋 لطفاً *لیست تجهیزات اعزامی* را در یک پیام بنویسید\n"
        "(مثال: «۵۰۰۰ سرباز، ۱۰۰ تانک، ۲۰ جنگنده»)",
        parse_mode="Markdown"
    )
    return CAMPAIGN_GET_EQUIPMENT


async def campaign_get_equipment(update: Update, context: CallbackContext) -> int:
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("❌ پیام خالی است. لطفاً لیست تجهیزات را وارد کنید:")
        return CAMPAIGN_GET_EQUIPMENT
    context.user_data.setdefault('campaign', {})['equipment'] = text
    await update.message.reply_text(
        "✅ لیست تجهیزات ثبت شد.\n\n"
        "📝 حالا *سناریوی اولیه* لشکر‌کشی را در یک پیام بنویسید (حداکثر *۱۰۰۰ کاراکتر*).\n\n"
        "پس از ارسال متن، دکمه «✅ ارسال نهایی» نمایش داده می‌شود.",
        parse_mode="Markdown"
    )
    return CAMPAIGN_GET_SCENARIO


async def campaign_get_scenario(update: Update, context: CallbackContext) -> int:
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("❌ سناریو خالی است. لطفاً متن سناریو را ارسال کنید:")
        return CAMPAIGN_GET_SCENARIO
    if len(text) > 1000:
        extra = len(text) - 1000
        await update.message.reply_text(
            f"⚠️ محدودیت ۱۰۰۰ کاراکتر است؛ متن شما {extra} کاراکتر بیشتر است.\n"
            "لطفاً متن کوتاه‌تری ارسال کنید."
        )
        return CAMPAIGN_GET_SCENARIO

    context.user_data.setdefault('campaign', {})['scenario'] = text

    campaign = context.user_data['campaign']
    target_name = campaign.get('target_name', '')
    types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in ['air', 'land', 'sea'] if t in campaign.get('types', set()))

    preview = (
        f"⚔️ *پیش‌نمایش لشکر‌کشی*\n\n"
        f"🎯 کشور هدف: {target_name}\n"
        f"🎖️ نوع نیروها: {types_str}\n\n"
        f"📋 *تجهیزات:*\n{campaign.get('equipment','-')}\n\n"
        f"📝 *سناریو:*\n{campaign.get('scenario','-')}"
    )
    keyboard = [
        [InlineKeyboardButton("✅ ارسال نهایی", callback_data='campaign_final_send')],
        [InlineKeyboardButton("❌ لغو", callback_data='campaign_cancel')]
    ]
    await update.message.reply_text(preview, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return CAMPAIGN_CONFIRM


async def campaign_cancel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.pop('campaign', None)
    try:
        await query.edit_message_text("❌ لشکر‌کشی لغو شد.")
    except Exception:
        pass
    return await show_main_menu(update, context)


async def campaign_final_send(update: Update, context: CallbackContext) -> int:
    """ارسال درخواست لشکر‌کشی به ادمین برای تأیید."""
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ کشور شما یافت نشد.")
            return MAIN_MENU
        campaign = context.user_data.get('campaign', {})
        target_id = campaign.get('target_id')
        target_name = campaign.get('target_name')
        types_set = campaign.get('types', set())
        equipment = campaign.get('equipment', '-')
        scenario = campaign.get('scenario', '-')

        if not target_id or not types_set:
            await query.edit_message_text("❌ اطلاعات ناقص است. دوباره از منوی لشکر‌کشی شروع کنید.")
            return MAIN_MENU

        types_list = [t for t in ['air', 'land', 'sea'] if t in types_set]
        types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in types_list)

        # متن ارسال شده به ادمین (ساده، شامل همه جزئیات)
        admin_text = (
            f"⚔️ درخواست لشکر‌کشی جدید\n\n"
            f"از کشور: {country['name']} (ID: {user_id})\n"
            f"به کشور: {target_name} (ID: {target_id})\n"
            f"نوع نیروها: {types_str}\n\n"
            f"تجهیزات:\n{equipment}\n\n"
            f"سناریوی اولیه:\n{scenario}"
        )

        # ذخیره proposal با type جدید 'campaign'
        # داده‌های اضافه را در text_content JSON-مانند می‌گذاریم تا حین تأیید بازیابی شود
        extra_payload = {
            "types": types_list,
            "equipment": equipment,
            "scenario": scenario,
            "target_id": target_id,
            "target_name": target_name,
            "attacker_name": country['name'],
            "attacker_id": user_id,
        }
        # text_content = admin_text + payload markers
        full_text_content = admin_text + "\n\n[CAMPAIGN_DATA]\n" + json.dumps(extra_payload, ensure_ascii=False)

        proposal_id = save_proposal(
            user_id,
            "campaign",
            full_text_content,
            [],
            None,
            target_user_id=target_id,
            target_country_name=target_name
        )

        admin_action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ تایید", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("❌ رد", callback_data=f"reject_{proposal_id}")]
        ])

        admins = get_all_admins()
        for admin_id in admins:
            try:
                sent_msg = await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    reply_markup=admin_action_keyboard
                )
                if sent_msg:
                    update_proposal_status(proposal_id, "pending", admin_message_id=sent_msg.message_id)
            except Exception as e:
                logger.error(f"خطا در ارسال به ادمین {admin_id}: {e}")

        await query.edit_message_text(
            "✅ درخواست لشکر‌کشی برای بررسی ادمین ارسال شد.\n"
            "پس از تأیید، خبر آن در کانال جنگ منتشر خواهد شد."
        )

        context.user_data.pop('campaign', None)
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in campaign_final_send: {e}", exc_info=True)
        await query.edit_message_text("❌ خطا در ارسال درخواست لشکر‌کشی.")
        return MAIN_MENU


# ============================== پایان لشکر‌کشی ==============================


# ============================== رول و سنا (پلیر) ==============================

async def role_sena_menu(update: Update, context: CallbackContext) -> int:
    """منوی اصلی رول و سنا برای پلیر: ۴ دکمه."""
    query = update.callback_query
    if query:
        await query.answer()
    try:
        user_id = (query.from_user.id if query else update.effective_user.id)
        country = get_country(user_id)
        if not country:
            text = "❌ شما هنوز کشوری ثبت نکرده‌اید."
            if query:
                await query.edit_message_text(text)
            else:
                await update.message.reply_text(text)
            return MAIN_MENU

        # ساخت دکمه‌ها با نمایش وضعیت
        def cat_btn(cat_key):
            info = ROLE_SENA_CATEGORIES[cat_key]
            enabled = role_sena_is_category_enabled(cat_key)
            group = info['group']
            limit = role_sena_get_limit(group)
            used = role_sena_get_group_used(user_id, group)
            if not enabled:
                txt = f"{info['label']} (❌ غیرفعال)"
            else:
                remaining = max(0, limit - used)
                txt = f"{info['label']}  •  باقیمانده: {remaining}/{limit}"
            return InlineKeyboardButton(txt, callback_data=f"role_sena_cat_{cat_key}")

        keyboard = [
            [cat_btn('security')],
            [cat_btn('economic')],
            [cat_btn('sabotage')],
            [cat_btn('sena')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "📜 *ارسال رول و سنا*\n\n"
            "از بین گزینه‌های زیر یکی را انتخاب کنید:\n"
            "• امنیتی، اقتصادی و خرابکاری در سهمیه رول‌ها مشترک هستند.\n"
            "• سنا سهمیه جداگانه دارد.\n"
            "🔁 سهمیه‌ها هر روز ساعت ۱۲ ظهر تهران ریست می‌شوند."
        )
        if query:
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        return ROLE_SENA_MENU
    except Exception as e:
        logger.error(f"Error in role_sena_menu: {e}", exc_info=True)
        if query:
            try:
                await query.edit_message_text("خطا در نمایش منوی رول و سنا.")
            except Exception:
                pass
        return MAIN_MENU


async def role_sena_pick_category(update: Update, context: CallbackContext) -> int:
    """کاربر یکی از دسته‌ها رو انتخاب کرده."""
    query = update.callback_query
    await query.answer()
    try:
        cat_key = query.data.replace("role_sena_cat_", "")
        if cat_key not in ROLE_SENA_CATEGORIES:
            await query.answer("دسته نامعتبر است", show_alert=True)
            return ROLE_SENA_MENU

        user_id = query.from_user.id
        ok, reason = role_sena_can_send(user_id, cat_key)
        if not ok:
            await query.answer(reason, show_alert=True)
            return ROLE_SENA_MENU

        context.user_data['role_sena_category'] = cat_key
        info = ROLE_SENA_CATEGORIES[cat_key]
        group = info['group']
        limit = role_sena_get_limit(group)
        used = role_sena_get_group_used(user_id, group)
        remaining = max(0, limit - used)
        max_chars = role_sena_get_max_chars()
        # محدودیت واقعی ورودی = min(max_chars, 4096) چون تلگرام بیشتر از ۴۰۹۶ نمی‌فرستد
        effective_input_limit = min(max_chars, TELEGRAM_MSG_LIMIT)

        if cat_key == 'sena':
            header = (
                f"📜 *ارسال سنا*\n"
                f"📊 سهمیه باقیمانده امروز: {remaining}/{limit}\n"
                f"📏 حداکثر طول این پیام: {effective_input_limit:,} کاراکتر\n"
                f"   (هر صفحه = ۴۰۹۶ کاراکتر؛ سقف کلی توسط ادمین: {max_chars:,})\n\n"
                "متن سنای خود را در یک پیام بنویسید و ارسال کنید."
            )
        else:
            header = (
                f"{info['label']}\n"
                f"📊 سهمیه باقیمانده امروز (رول): {remaining}/{limit}\n"
                f"📏 حداکثر طول این پیام: {effective_input_limit:,} کاراکتر\n"
                f"   (هر صفحه = ۴۰۹۶ کاراکتر؛ سقف کلی توسط ادمین: {max_chars:,})\n\n"
                "متن رول خود را در یک پیام بنویسید و ارسال کنید."
            )

        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='role_sena_back')]]
        await query.edit_message_text(header, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return ROLE_SENA_GET_CONTENT
    except Exception as e:
        logger.error(f"Error in role_sena_pick_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب دسته")
        return ROLE_SENA_MENU


async def role_sena_back(update: Update, context: CallbackContext) -> int:
    """برگشت به منوی رول/سنا."""
    context.user_data.pop('role_sena_category', None)
    return await role_sena_menu(update, context)


async def role_sena_get_content(update: Update, context: CallbackContext) -> int:
    """دریافت متن رول/سنا و ارسال به مقصد."""
    user_id = update.effective_user.id
    cat_key = context.user_data.get('role_sena_category')
    if not cat_key or cat_key not in ROLE_SENA_CATEGORIES:
        await update.message.reply_text("❌ دسته انتخاب نشده. لطفاً دوباره از منوی رول/سنا شروع کنید.")
        return MAIN_MENU

    # بررسی مجدد سهمیه (ممکنه بین انتخاب و ارسال، ادمین تغییر داده باشه)
    ok, reason = role_sena_can_send(user_id, cat_key)
    if not ok:
        await update.message.reply_text(f"❌ {reason}")
        return await role_sena_menu(update, context)

    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("❌ متن خالی است. لطفاً متن خود را ارسال کنید:")
        return ROLE_SENA_GET_CONTENT

    max_chars = role_sena_get_max_chars()
    effective_input_limit = min(max_chars, TELEGRAM_MSG_LIMIT)
    if len(text) > effective_input_limit:
        extra = len(text) - effective_input_limit
        await update.message.reply_text(
            f"⚠️ متن شما از حداکثر مجاز ({effective_input_limit:,} کاراکتر) بیشتر است.\n"
            f"تعداد اضافی: {extra:,} کاراکتر.\n"
            f"(هر صفحه = ۴۰۹۶ کاراکتر، که سقف خود تلگرام برای یک پیام است.)\n"
            "لطفاً متن کوتاه‌تری ارسال کنید."
        )
        return ROLE_SENA_GET_CONTENT

    country = get_country(user_id)
    country_name = country.get('name', 'نامشخص') if country else 'نامشخص'
    info = ROLE_SENA_CATEGORIES[cat_key]

    try:
        if cat_key == 'sena':
            # ارسال به همه ادمین‌ها در پی‌وی (با تقسیم چندپیامی در صورت طولانی بودن)
            header = (
                f"📜 سنای جدید\n"
                f"از کشور: {country_name} (ID: {user_id})\n"
                f"━━━━━━━━━━━━━━━\n\n"
            )
            admins = get_all_admins()
            sent_any = False
            for admin_id in admins:
                try:
                    sent_count = await _send_long_message(
                        context.bot, admin_id, header, text, parse_mode=None
                    )
                    if sent_count > 0:
                        sent_any = True
                except Exception as e:
                    logger.error(f"خطا در ارسال سنا به ادمین {admin_id}: {e}")
            if not sent_any:
                await update.message.reply_text("❌ ارسال موفق نبود. لطفاً بعداً تلاش کنید.")
                return ROLE_SENA_MENU
            # ثبت استفاده
            role_sena_increment_usage(user_id, cat_key)
            limit = role_sena_get_limit('sena')
            used = role_sena_get_group_used(user_id, 'sena')
            remaining = max(0, limit - used)
            await update.message.reply_text(
                f"✅ سنای شما ارسال شد.\n"
                f"📊 سهمیه باقیمانده سنا: {remaining}/{limit}"
            )
        else:
            # ارسال رول به کانال با نام کشور (با تقسیم چندپیامی در صورت طولانی بودن)
            header_md = (
                f"{info['label']} — *{country_name}*\n"
                f"━━━━━━━━━━━━━━━\n\n"
            )
            sent_count = 0
            try:
                sent_count = await _send_long_message(
                    context.bot, ROLE_CHANNEL, header_md, text, parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"خطا در ارسال رول به کانال (Markdown): {e}", exc_info=True)
                # تلاش دوباره بدون Markdown
                header_plain = (
                    f"{info['label']} — {country_name}\n"
                    f"━━━━━━━━━━━━━━━\n\n"
                )
                try:
                    sent_count = await _send_long_message(
                        context.bot, ROLE_CHANNEL, header_plain, text, parse_mode=None
                    )
                except Exception as e2:
                    logger.error(f"خطا در تلاش دوم ارسال رول: {e2}")
                    # اگر کانال رول یافت نشد، سعی کن به WAR_CHANNEL بفرستی تا پیام گم نشود
                    if "Chat not found" in str(e2):
                        try:
                            sent_count = await _send_long_message(
                                context.bot, REPORTS_CHANNEL, header_plain + text, "", parse_mode=None
                            )
                            if sent_count > 0:
                                # به پلیر چیزی نگو، فقط به ادمین اطلاع بده
                                try:
                                    for aid in get_all_admins():
                                        try:
                                            await context.bot.send_message(chat_id=aid, text=f"⚠️ کانال رول {ROLE_CHANNEL} یافت نشد، پیام به {REPORTS_CHANNEL} ارسال شد. فرستنده {country_name}")
                                        except: pass
                                except: pass
                        except Exception:
                            pass
            if sent_count <= 0:
                # به پلیر چیزی نشان نده، فقط به ادمین پیوی بفرست
                try:
                    admins = get_all_admins()
                    err_text = (
                        f"⚠️ ارسال رول ناموفق: کانال رول یافت نشد\n"
                        f"کانال: {ROLE_CHANNEL}\n"
                        f"فرستنده: {country_name} (ID:{user_id}) دسته {cat_key}\n"
                        f"متن: {text[:500]}"
                    )
                    for aid in admins:
                        try:
                            await context.bot.send_message(chat_id=aid, text=err_text)
                        except: pass
                except: pass
                await update.message.reply_text("✅ پیام شما ثبت شد و برای بررسی به مدیریت ارسال شد.")
                return ROLE_SENA_MENU
            role_sena_increment_usage(user_id, cat_key)
            limit = role_sena_get_limit('role')
            used = role_sena_get_group_used(user_id, 'role')
            remaining = max(0, limit - used)
            extra_info = f"\n📄 تقسیم شد به {sent_count} پیام" if sent_count > 1 else ""
            await update.message.reply_text(
                f"✅ {info['label']} شما ارسال شد.{extra_info}\n"
                f"📊 سهمیه باقیمانده رول‌ها: {remaining}/{limit}"
            )
    except Exception as e:
        logger.error(f"Error sending role/sena: {e}", exc_info=True)
        await update.message.reply_text("❌ خطا در ارسال. لطفاً دوباره تلاش کنید.")
        return ROLE_SENA_MENU

    context.user_data.pop('role_sena_category', None)
    return await role_sena_menu(update, context)


# --------- مدیریت محدودیت‌ها (پنل ادمین) ---------

async def role_sena_limits_menu(update: Update, context: CallbackContext) -> int:
    """منوی مدیریت محدودیت‌ها: ۵ دکمه (۴ دسته + سقف ها)."""
    query = update.callback_query
    if query:
        await query.answer()
    user_id = (query.from_user.id if query else update.effective_user.id)
    if not is_admin(user_id):
        if query:
            await query.answer("⛔️ فقط ادمین‌ها دسترسی دارند!", show_alert=True)
        return ADMIN_MENU

    role_limit = role_sena_get_limit('role')
    sena_limit = role_sena_get_limit('sena')
    max_chars = role_sena_get_max_chars()

    def cat_btn_admin(cat_key):
        info = ROLE_SENA_CATEGORIES[cat_key]
        en = role_sena_is_category_enabled(cat_key)
        mark = "✅" if en else "❌"
        return InlineKeyboardButton(
            f"{mark} {info['label']}",
            callback_data=f"role_sena_toggle_{cat_key}"
        )

    keyboard = [
        [cat_btn_admin('security')],
        [cat_btn_admin('economic')],
        [cat_btn_admin('sabotage')],
        [cat_btn_admin('sena')],
        [InlineKeyboardButton(f"🔢 محدودیت روزانه رول‌ها: {role_limit}", callback_data='role_sena_set_limit_role')],
        [InlineKeyboardButton(f"🔢 محدودیت روزانه سنا: {sena_limit}", callback_data='role_sena_set_limit_sena')],
        [InlineKeyboardButton(f"📏 حداکثر کاراکتر هر پیام: {max_chars:,}", callback_data='role_sena_set_max_chars')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]
    ]
    text = (
        "🚦 *تعیین محدودیت — رول و سنا*\n\n"
        "روی هر بخش بزن تا فعال/غیرفعال شود.\n"
        "روی محدودیت‌ها بزن تا تعداد را تغییر دهی.\n\n"
        f"• رول‌ها (امنیتی + اقتصادی + خرابکاری): {role_limit} پیام در روز\n"
        f"• سنا: {sena_limit} پیام در روز\n"
        f"• حداکثر کاراکتر هر پیام: {max_chars:,}\n"
        "🔁 ریست خودکار ساعت ۱۲ ظهر تهران."
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    return ROLE_SENA_LIMITS_MENU


async def role_sena_toggle_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if not is_admin(user_id):
        await query.answer("⛔️ فقط ادمین‌ها دسترسی دارند!", show_alert=True)
        return ROLE_SENA_LIMITS_MENU
    cat_key = query.data.replace("role_sena_toggle_", "")
    if cat_key not in ROLE_SENA_CATEGORIES:
        return ROLE_SENA_LIMITS_MENU
    current = role_sena_is_category_enabled(cat_key)
    role_sena_set_category_enabled(cat_key, not current)
    return await role_sena_limits_menu(update, context)


async def role_sena_set_limit_start(update: Update, context: CallbackContext) -> int:
    """شروع وارد کردن مقدار جدید محدودیت یا حداکثر کاراکتر."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'role_sena_set_limit_role':
        context.user_data['role_sena_setting_target'] = 'role_limit'
        await query.edit_message_text(
            f"🔢 مقدار جدید محدودیت روزانه رول‌ها (مجموع امنیتی/اقتصادی/خرابکاری) را ارسال کنید.\n"
            f"مقدار فعلی: {role_sena_get_limit('role')}\n\n"
            "یک عدد صحیح غیرمنفی وارد کنید (۰ یعنی غیرفعال):"
        )
    elif data == 'role_sena_set_limit_sena':
        context.user_data['role_sena_setting_target'] = 'sena_limit'
        await query.edit_message_text(
            f"🔢 مقدار جدید محدودیت روزانه سنا را ارسال کنید.\n"
            f"مقدار فعلی: {role_sena_get_limit('sena')}\n\n"
            "یک عدد صحیح غیرمنفی وارد کنید (۰ یعنی غیرفعال):"
        )
    elif data == 'role_sena_set_max_chars':
        context.user_data['role_sena_setting_target'] = 'max_chars'
        await query.edit_message_text(
            f"📏 سقف کاراکتر برای هر ارسال رول/سنا را وارد کنید.\n"
            f"مقدار فعلی: {role_sena_get_max_chars():,}\n"
            f"(دیفالت پیشنهادی: {5 * 4096:,} = ۵ صفحه × ۴۰۹۶)\n\n"
            f"ℹ️ توجه: چون تلگرام برای *هر پیام* فقط {TELEGRAM_MSG_LIMIT:,} کاراکتر اجازه می‌دهد،\n"
            f"حداکثر طول پیام ورودی پلیر در عمل = min(این عدد, {TELEGRAM_MSG_LIMIT:,}) خواهد بود.\n\n"
            "یک عدد صحیح بزرگتر از صفر وارد کنید:"
        )
    else:
        return ROLE_SENA_LIMITS_MENU
    return ROLE_SENA_GET_LIMIT_VALUE


async def role_sena_save_limit_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    target = context.user_data.get('role_sena_setting_target')
    if not target:
        await update.message.reply_text("خطا در شناسایی تنظیم. دوباره از منو شروع کنید.")
        return await role_sena_limits_menu(update, context)
    text = (update.message.text or "").strip().replace(',', '')
    try:
        value = int(text)
        if value < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text("❌ مقدار نامعتبر. یک عدد صحیح غیرمنفی وارد کنید:")
        return ROLE_SENA_GET_LIMIT_VALUE

    if target == 'role_limit':
        role_sena_set_limit('role', value)
        await update.message.reply_text(f"✅ محدودیت روزانه رول‌ها به {value} تنظیم شد.")
    elif target == 'sena_limit':
        role_sena_set_limit('sena', value)
        await update.message.reply_text(f"✅ محدودیت روزانه سنا به {value} تنظیم شد.")
    elif target == 'max_chars':
        if value <= 0:
            await update.message.reply_text("❌ حداکثر کاراکتر باید بزرگتر از صفر باشد:")
            return ROLE_SENA_GET_LIMIT_VALUE
        set_setting('role_sena_max_chars', str(value))
        await update.message.reply_text(f"✅ حداکثر کاراکتر هر پیام به {value:,} تنظیم شد.")
    context.user_data.pop('role_sena_setting_target', None)
    return await role_sena_limits_menu(update, context)


# ============================ پایان رول و سنا ============================


async def attack_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ شما هنوز کشوری ثبت نکرده‌اید.")
            return MAIN_MENU
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != user_id]
        if not other_countries:
            await query.edit_message_text("در حال حاضر هیچ کشور دیگری برای حمله وجود ندارد.")
            return MAIN_MENU
        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"attack_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("⚔️ لطفا کشوری را برای حمله انتخاب کنید:", reply_markup=reply_markup)
        return ATTACK_TARGET
    except Exception as e:
        logger.error(f"Error in attack_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return MAIN_MENU


async def select_attack_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("attack_target_", ""))
        context.user_data['attack_target_id'] = target_user_id
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("❌ کشور مورد نظر برای حمله یافت نشد.")
            return await attack_menu(update, context)
        context.user_data['attack_target_name'] = target_country['name']
        await query.edit_message_text(f"شما کشور {target_country['name']} را برای حمله انتخاب کردید.\n"
                                      "لطفا لیست نیروهای استفاده شده در حمله را بنویسید (مثال: '5000 سرباز، 100 تانک'):")
        return GET_ATTACK_TROOPS_DETAILS
    except Exception as e:
        logger.error(f"Error in select_attack_target: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کشور هدف")
        return ATTACK_TARGET


async def get_attack_troops_details(update: Update, context: CallbackContext) -> int:
    try:
        attack_target_name = context.user_data.get('attack_target_name')
        if not attack_target_name:
            await update.message.reply_text("خطا در انتخاب هدف حمله. لطفاً دوباره از منوی حمله شروع کنید.")
            return MAIN_MENU
        troops_details = update.message.text
        context.user_data['attack_troops_details'] = troops_details
        await update.message.reply_text(f"لیست نیروها ثبت شد.\n"
                                        "اکنون، لطفاً سناریوی حمله خود را بنویسید.\n"
                                        "می‌توانید متن را در چند پیام ارسال کنید و یا عکس‌های مرتبط ارسال کنید.\n"
                                        "بعد از اتمام، دکمه 'تایید و ارسال' را بزنید.")
        context.user_data['attack_scenario_text'] = []
        context.user_data['attack_scenario_photos'] = []
        keyboard = [[InlineKeyboardButton("✅ تایید و ارسال سناریو", callback_data='confirm_attack_scenario')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await update.message.reply_text("برای ارسال نهایی سناریو پس از وارد کردن تمامی اطلاعات، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
        context.user_data['user_proposal_message_id'] = sent_message.message_id
        return GET_ATTACK_SCENARIO_INPUT
    except Exception as e:
        logger.error(f"Error in get_attack_troops_details: {e}", exc_info=True)
        await update.message.reply_text("خطا در ثبت اطلاعات نیروها")
        return MAIN_MENU


async def get_attack_scenario_input(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    try:
        if update.message.text:
            context.user_data['attack_scenario_text'].append(update.message.text)
            await context.bot.send_message(chat_id, "متن سناریو اضافه شد. می‌توانید ادامه دهید یا دکمه 'تایید و ارسال سناریو' را بزنید.")
        elif update.message.photo:
            photo_id = update.message.photo[-1].file_id
            context.user_data['attack_scenario_photos'].append(photo_id)
            await context.bot.send_message(chat_id, "عکس سناریو اضافه شد. می‌توانید ادامه دهید یا دکمه 'تایید و ارسال سناریو' را بزنید.")
        else:
            await context.bot.send_message(chat_id, "لطفاً متن یا عکس معتبر برای سناریو ارسال کنید.")
    except Exception as e:
        logger.error(f"Error in get_attack_scenario_input: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "خطا در پردازش سناریو. لطفاً دوباره تلاش کنید.")

    keyboard = [[InlineKeyboardButton("✅ تایید و ارسال سناریو", callback_data='confirm_attack_scenario')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_proposal_message_id = context.user_data.get('user_proposal_message_id')
    if user_proposal_message_id:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=user_proposal_message_id,
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.warning(f"Could not edit reply markup: {e}")
            try:
                sent_message = await context.bot.send_message(chat_id, "برای ارسال نهایی سناریو پس از وارد کردن تمامی اطلاعات، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
                context.user_data['user_proposal_message_id'] = sent_message.message_id
            except Exception as e2:
                logger.error(f"Failed to send new message: {e2}")
    else:
        try:
            sent_message = await context.bot.send_message(chat_id, "برای ارسال نهایی سناریو پس از وارد کردن تمامی اطلاعات، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
            context.user_data['user_proposal_message_id'] = sent_message.message_id
        except Exception as e:
            logger.error(f"Failed to send initial message: {e}")
    return GET_ATTACK_SCENARIO_INPUT


async def confirm_attack_scenario(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    try:
        if query.message:
            await query.edit_message_text("در حال پردازش درخواست...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "در حال پردازش درخواست...")

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await context.bot.send_message(chat_id, "❌ کشور شما یافت نشد.")
            return MAIN_MENU
        attack_target_id = context.user_data.get('attack_target_id')
        attack_target_name = context.user_data.get('attack_target_name')
        troops_details = context.user_data.get('attack_troops_details', 'بدون جزئیات نیرو.')
        scenario_text_parts = context.user_data.get('attack_scenario_text', [])
        scenario_photos = context.user_data.get('attack_scenario_photos', [])
        user_proposal_message_id = context.user_data.get('user_proposal_message_id')
        full_scenario_text = "\n\n".join(scenario_text_parts) if scenario_text_parts else "بدون سناریو."
        if not attack_target_id:
            await context.bot.send_message(chat_id, "خطا در اطلاعات حمله. لطفاً دوباره تلاش کنید.")
            return MAIN_MENU
        target_country = get_country(attack_target_id)
        admin_message = (
            f"⚔️ *درخواست حمله جدید*\n\n"
            f"👤 آغازکننده: {country['name']} (ID: {user_id})\n"
            f"🎯 هدف حمله: {target_country['name']} (ID: {attack_target_id})\n\n"
            f"*نیروهای استفاده شده:*\n{troops_details}\n\n"
            f"*سناریوی حمله:*\n{full_scenario_text}"
        )
        proposal_id = save_proposal(
            user_id,
            "attack",
            admin_message,
            scenario_photos,
            user_proposal_message_id,
            target_user_id=attack_target_id,
            target_country_name=attack_target_name
        )
        admin_action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ تایید حمله", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("❌ رد حمله", callback_data=f"reject_{proposal_id}")]
        ])

        admins = get_all_admins()
        for admin_id in admins:
            sent_message = None
            if scenario_photos:
                media = [InputMediaPhoto(media=photo_id) for photo_id in scenario_photos]
                if len(media) > 1:
                    await context.bot.send_media_group(chat_id=admin_id, media=media)
                    sent_message = await context.bot.send_message(chat_id=admin_id, text=admin_message,
                                                                  reply_markup=admin_action_keyboard, parse_mode="Markdown")
                else:
                    sent_message = await context.bot.send_photo(chat_id=admin_id, photo=scenario_photos[0],
                                                                caption=admin_message, reply_markup=admin_action_keyboard,
                                                                parse_mode="Markdown")
            else:
                sent_message = await context.bot.send_message(chat_id=admin_id, text=admin_message,
                                                              reply_markup=admin_action_keyboard, parse_mode="Markdown")
            if sent_message:
                admin_msg_id = sent_message.message_id if not isinstance(sent_message, list) else sent_message[0].message_id
                update_proposal_status(proposal_id, "pending", admin_message_id=admin_msg_id)
        await context.bot.send_message(chat_id, "✅ درخواست حمله شما به ادمین ارسال شد و در حال بررسی است. منتظر پاسخ بمانید.")

        keys_to_remove = [
            'attack_target_id', 'attack_target_name', 'attack_troops_details',
            'attack_scenario_text', 'attack_scenario_photos', 'user_proposal_message_id'
        ]
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in confirm_attack_scenario: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "خطا در ارسال درخواست حمله")
        return MAIN_MENU


async def send_proposal_start(update: Update, context: CallbackContext, proposal_type: str) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ شما هنوز کشوری ثبت نکرده‌اید.")
            return MAIN_MENU
        context.user_data['current_proposal_type'] = proposal_type
        context.user_data['proposal_text_parts'] = []
        context.user_data['proposal_photo_ids'] = []
        proposal_display_name = PROPOSAL_TYPES.get(proposal_type, "درخواست")
        await query.edit_message_text(f"📝 لطفاً جزئیات درخواست {proposal_display_name} خود را بنویسید.\n"
                                      "می‌توانید متن را در چند پیام و همچنین عکس‌های مرتبط ارسال کنید.\n"
                                      "پس از اتمام، دکمه 'ارسال نهایی' را بزنید.")
        keyboard = [[InlineKeyboardButton("✅ ارسال نهایی", callback_data='final_send_proposal')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await query.message.reply_text("برای ارسال نهایی درخواست خود، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
        context.user_data['user_proposal_message_id'] = sent_message.message_id
        return GET_PROPOSAL_TEXT
    except Exception as e:
        logger.error(f"Error in send_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("خطا در شروع درخواست")
        return MAIN_MENU


async def get_proposal_content(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    try:
        if update.message.text:
            context.user_data['proposal_text_parts'].append(update.message.text)
            await context.bot.send_message(chat_id, "متن درخواست اضافه شد. می‌توانید ادامه دهید یا دکمه 'ارسال نهایی' را بزنید.")
        elif update.message.photo:
            photo_id = update.message.photo[-1].file_id
            context.user_data['proposal_photo_ids'].append(photo_id)
            await context.bot.send_message(chat_id, "عکس درخواست اضافه شد. می‌توانید ادامه دهید یا دکمه 'ارسال نهایی' را بزنید.")
        else:
            await context.bot.send_message(chat_id, "لطفاً متن یا عکس معتبر برای درخواست ارسال کنید.")
    except Exception as e:
        logger.error(f"Error in get_proposal_content: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "خطا در پردازش درخواست. لطفاً دوباره تلاش کنید.")

    keyboard = [[InlineKeyboardButton("✅ ارسال نهایی", callback_data='final_send_proposal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_proposal_message_id = context.user_data.get('user_proposal_message_id')
    if user_proposal_message_id:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=user_proposal_message_id,
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.warning(f"Could not edit reply markup: {e}")
            try:
                sent_message = await context.bot.send_message(chat_id, "برای ارسال نهایی درخواست خود، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
                context.user_data['user_proposal_message_id'] = sent_message.message_id
            except Exception as e2:
                logger.error(f"Failed to send new message: {e2}")
    else:
        try:
            sent_message = await context.bot.send_message(chat_id, "برای ارسال نهایی درخواست خود، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
            context.user_data['user_proposal_message_id'] = sent_message.message_id
        except Exception as e:
            logger.error(f"Failed to send initial message: {e}")
    return GET_PROPOSAL_TEXT


async def final_send_proposal(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    try:
        if query.message:
            await query.edit_message_text("در حال پردازش درخواست...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "در حال پردازش درخواست...")

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await context.bot.send_message(chat_id, "❌ کشور شما یافت نشد.")
            return MAIN_MENU
        proposal_type = context.user_data.get('current_proposal_type')
        proposal_text_parts = context.user_data.get('proposal_text_parts', [])
        proposal_photo_ids = context.user_data.get('proposal_photo_ids', [])
        user_proposal_message_id = context.user_data.get('user_proposal_message_id')
        full_proposal_text = "\n\n".join(proposal_text_parts) if proposal_text_parts else "بدون جزئیات."
        proposal_display_name = PROPOSAL_TYPES.get(proposal_type, "درخواست")
        if not proposal_type:
            await context.bot.send_message(chat_id, "خطا در نوع درخواست. لطفاً دوباره تلاش کنید.")
            return MAIN_MENU
        admin_message = (
            f"📝 *درخواست جدید - {proposal_display_name}*\n\n"
            f"👤 از: {country['name']} (ID: {user_id})\n\n"
            f"*جزئیات درخواست:*\n{full_proposal_text}"
        )
        proposal_id = save_proposal(user_id, proposal_type, admin_message, proposal_photo_ids, user_proposal_message_id)
        admin_action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ تایید", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("❌ رد", callback_data=f"reject_{proposal_id}")]
        ])

        admins = get_all_admins()
        for admin_id in admins:
            sent_message = None
            if proposal_photo_ids:
                media = [InputMediaPhoto(media=photo_id) for photo_id in proposal_photo_ids]
                if len(media) > 1:
                    await context.bot.send_media_group(chat_id=admin_id, media=media)
                    sent_message = await context.bot.send_message(chat_id=admin_id, text=admin_message,
                                                                  reply_markup=admin_action_keyboard, parse_mode="Markdown")
                else:
                    sent_message = await context.bot.send_photo(chat_id=admin_id, photo=proposal_photo_ids[0],
                                                                caption=admin_message, reply_markup=admin_action_keyboard,
                                                                parse_mode="Markdown")
            else:
                sent_message = await context.bot.send_message(chat_id=admin_id, text=admin_message,
                                                              reply_markup=admin_action_keyboard, parse_mode="Markdown")

            if sent_message:
                admin_msg_id = sent_message.message_id if not isinstance(sent_message, list) else sent_message[0].message_id
                update_proposal_status(proposal_id, "pending", admin_message_id=admin_msg_id)
        await context.bot.send_message(chat_id, f"✅ درخواست {proposal_display_name} شما به ادمین ارسال شد و در حال بررسی است. منتظر پاسخ بمانید.")

        keys_to_remove = [
            'current_proposal_type', 'proposal_text_parts', 'proposal_photo_ids', 'user_proposal_message_id'
        ]
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in final_send_proposal: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "خطا در ارسال درخواست")
        return MAIN_MENU


async def handle_proposal_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        await query.answer("⛔️ فقط ادمین‌ها می‌توانند این عمل را انجام دهند!", show_alert=True)
        return ADMIN_MENU
    try:
        action, proposal_id = query.data.split('_', 1)
        proposal = get_proposal(proposal_id)
        if not proposal:
            await query.edit_message_text("❌ درخواست یافت نشد یا قبلاً رسیدگی شده است.")
            return ADMIN_MENU
        user_id = proposal['user_id']
        country = get_country(user_id)
        proposal_display_name = PROPOSAL_TYPES.get(proposal['type'], "درخواست")
        status_text = "تایید" if action == "approve" else "رد"
        update_proposal_status(proposal_id, action)
        try:
            if query.message.caption:
                await query.edit_message_caption(caption=f"{query.message.caption}\n\n*وضعیت: {status_text} شده توسط ادمین {query.from_user.first_name}*",
                                                 reply_markup=None,
                                                 parse_mode="Markdown")
            else:
                await query.edit_message_text(text=f"{query.message.text}\n\n*وضعیت: {status_text} شده توسط ادمین {query.from_user.first_name}*",
                                              reply_markup=None,
                                              parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error editing admin message for proposal {proposal_id}: {e}")
            if proposal['admin_message_id']:
                try:
                    await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                        message_id=proposal['admin_message_id'],
                                                        text=f"{proposal['text_content']}\n\n*وضعیت: {status_text} شده توسط ادمین {query.from_user.first_name}*",
                                                        parse_mode="Markdown",
                                                        reply_markup=None)
                except Exception as e:
                    logger.error(f"Error editing admin message via ID {proposal['admin_message_id']} for proposal {proposal_id}: {e}")
                    await query.message.reply_text(f"درخواست {proposal_id} با موفقیت {status_text} شد. (خطا در ویرایش پیام اصلی ادمین)")
            else:
                await query.message.reply_text(f"درخواست {proposal_id} با موفقیت {status_text} شد. (پیام اصلی ادمین یافت نشد.)")
        user_notification_text = (
            f"✅ درخواست {proposal_display_name} شما توسط ادمین *{query.from_user.first_name}* {status_text} شد.\n"
        )
        # برای campaign از نمایش جزئیات JSON در پیام کاربر صرف نظر می‌کنیم
        if proposal['type'] != "campaign" and len(proposal['text_content']) < 1000:
            user_notification_text += f"🔗 جزئیات: {proposal['text_content']}"
        if proposal['type'] == "campaign" and action == "reject":
            user_notification_text = (
                f"❌ لشکر‌کشی شما توسط ادمین *{query.from_user.first_name}* رد شد."
            )

        # ===== لشکر‌کشی تأیید شد: ارسال خبر به کانال WAR_CHANNEL =====
        if action == "approve" and proposal['type'] == "campaign":
            try:
                payload = {}
                marker = "[CAMPAIGN_DATA]"
                if marker in proposal['text_content']:
                    json_part = proposal['text_content'].split(marker, 1)[1].strip()
                    try:
                        payload = json.loads(json_part)
                    except Exception as e:
                        logger.error(f"خطا در پارس CAMPAIGN_DATA: {e}")
                attacker_name = payload.get('attacker_name') or (get_country(proposal['user_id']) or {}).get('name', 'نامعلوم')
                target_name = payload.get('target_name') or proposal.get('target_country_name') or 'نامعلوم'
                types_list = payload.get('types', [])

                types_str = " + ".join(CAMPAIGN_TYPE_LABELS.get(t, t) for t in types_list) if types_list else "نامشخص"

                channel_text = (
                    "⚔️ *لشکر‌کشی جدید آغاز شد!*\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🗺️ *کشور مهاجم:* {attacker_name}\n"
                    f"🎯 *کشور هدف:* {target_name}\n"
                    f"🎖️ *نوع نیروها:* {types_str}\n"
                    "━━━━━━━━━━━━━━━\n"
                    "\n🕊️ به امید پیروزی..."
                )

                campaign_photo_id = get_notification_image('campaign') or get_notification_image('attack')
                if campaign_photo_id:
                    await context.bot.send_photo(
                        chat_id=REPORTS_CHANNEL,
                        photo=campaign_photo_id,
                        caption=channel_text,
                        parse_mode="Markdown"
                    )
                else:
                    await context.bot.send_message(
                        chat_id=REPORTS_CHANNEL,
                        text=channel_text,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"خطا در ارسال لشکر‌کشی به کانال: {e}", exc_info=True)

            # بازنویسی پیام کاربر برای حالت لشکر‌کشی
            user_notification_text = (
                f"✅ لشکر‌کشی شما توسط ادمین *{query.from_user.first_name}* تأیید شد.\n"
                f"📢 خبر در کانال جنگ منتشر شد."
            )

        if action == "approve" and proposal['type'] == "attack":
            delivery_minutes = random.randint(30, 60)
            delivery_time = (datetime.now() + timedelta(minutes=delivery_minutes)).isoformat()

            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO attack_deliveries (proposal_id, delivery_time) VALUES (?, ?)",
                      (proposal_id, delivery_time))
            conn.commit()
            conn.close()

            attacker = get_country(proposal['user_id'])
            target = get_country(proposal['target_user_id'])

            attack_message = (
                f"⚔️ حمله جدید تایید شد!\n\n"
                f"🗺️ از: {attacker['name']}\n"
                f"🎯 به: {target['name']}\n"
                f"⏱️ زمان رسیدن نیروها: {delivery_minutes} دقیقه دیگر"
            )

            attack_photo_id = get_notification_image('attack')
            if attack_photo_id:
                await context.bot.send_photo(
                    chat_id=STATEMENT_CHANNEL,
                    photo=attack_photo_id,
                    caption=attack_message
                )
            else:
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=attack_message
                )
        if proposal['user_message_id'] and user_id:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=user_notification_text,
                    reply_to_message_id=proposal['user_message_id'],
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Error replying to user's proposal message {proposal['user_message_id']}: {e}")
                await context.bot.send_message(chat_id=user_id, text=user_notification_text, parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id=user_id, text=user_notification_text, parse_mode="Markdown")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in handle_proposal_callback: {e}", exc_info=True)
        await query.answer("خطا در پردازش درخواست", show_alert=True)
        return ADMIN_MENU


async def shop_menu_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"shop_category_{category_key}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🛒 به بخش خرید خوش آمدید! لطفا دسته‌بندی مورد نظر خود را انتخاب کنید:", reply_markup=reply_markup)
        return SHOP_MENU
    except Exception as e:
        logger.error(f"Error in shop_menu_start: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی خرید")
        return MAIN_MENU


async def select_shop_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        category_key = query.data.replace("shop_category_", "")
        context.user_data['current_shop_category'] = category_key
        keyboard = []

        _check_defaults = get_dynamic_default_assets()
        if category_key not in _check_defaults or not isinstance(_check_defaults[category_key], dict):
            await query.edit_message_text("❌ دسته‌بندی مورد نظر یافت نشد.")
            return await shop_menu_start(update, context)

        items_added = False
        dynamic_defaults = get_dynamic_default_assets()
        dynamic_prices = get_dynamic_asset_prices()
        for item_key in dynamic_defaults.get(category_key, {}).keys():
            try:
                price = dynamic_prices.get(item_key)
                if price is None:
                    continue

                item_display_name = get_asset_display_name(item_key)
                formatted_price = f"{price:,}"
                button_text = f"{item_display_name} (قیمت: {formatted_price})"

                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"shop_item_{item_key}")])
                items_added = True
            except Exception as e:
                logger.error(f"خطا در پردازش آیتم {item_key}: {e}")
        if not items_added:
            await query.answer("⚠️ هیچ آیتمی در این دسته‌بندی موجود نیست!", show_alert=True)
            return await shop_menu_start(update, context)
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='shop_menu_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        category_display_name = next(
            (disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key),
            category_key
        )

        await query.edit_message_text(
            f"🛍️ آیتم‌های موجود در دسته‌بندی '{category_display_name}':",
            reply_markup=reply_markup
        )
        return SHOP_CATEGORY

    except Exception as e:
        logger.error(f"Error in select_shop_category: {e}", exc_info=True)
        await query.edit_message_text("⚠️ خطا در نمایش دسته‌بندی. لطفاً بعداً تلاش کنید.")
        return SHOP_MENU


async def select_shop_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        item_key = query.data.replace("shop_item_", "")
        current_shop_category = context.user_data.get('current_shop_category')
        if not current_shop_category:
            await query.edit_message_text("خطا در انتخاب دسته‌بندی. لطفاً دوباره تلاش کنید.")
            return await shop_menu_start(update, context)
        dynamic_prices = get_dynamic_asset_prices()
        price = dynamic_prices.get(item_key)
        if price is None:
            await query.edit_message_text("❌ قیمت این آیتم نامشخص است.")
            return await select_shop_category(update, context)
        context.user_data['selected_shop_item_key'] = item_key
        context.user_data['selected_shop_item_price'] = price
        item_display_name = get_asset_display_name(item_key)
        await query.edit_message_text(f"شما '{item_display_name}' را انتخاب کردید.\n"
                                      f"قیمت هر واحد: {price:,} سرمایه.\n"
                                      "لطفاً تعداد مورد نظر برای خرید را وارد کنید:")
        return GET_SHOP_ITEM_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_shop_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب آیتم")
        return SHOP_CATEGORY


async def get_shop_item_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("❌ کشور شما یافت نشد. لطفاً با مالک ربات تماس بگیرید.")
        return MAIN_MENU
    item_key = context.user_data.get('selected_shop_item_key')
    price = context.user_data.get('selected_shop_item_price')
    category_key = context.user_data.get('current_shop_category')
    if not item_key or price is None or not category_key:
        await update.message.reply_text("خطا در پردازش خرید. لطفاً دوباره از منوی خرید شروع کنید.")
        return await shop_menu_start(update, context)
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("لطفاً تعداد صحیح و مثبت وارد کنید.")
            return GET_SHOP_ITEM_QUANTITY
    except ValueError:
        await update.message.reply_text("تعداد وارد شده نامعتبر است. لطفاً یک عدد صحیح وارد کنید.")
        return GET_SHOP_ITEM_QUANTITY
    total_cost = quantity * price
    if country['capital'] < total_cost:
        await update.message.reply_text(f"سرمایه شما ({country['capital']:,}) برای خرید {quantity:,} واحد از {get_asset_display_name(item_key)} به قیمت {total_cost:,} کافی نیست.")
        return GET_SHOP_ITEM_QUANTITY
    try:
        new_capital = country['capital'] - total_cost

        update_data = {
            'capital': new_capital,
            category_key: {
                item_key: country.get(category_key, {}).get(item_key, 0) + quantity
            }
        }

        update_country(user_id, update_data)

        item_display_name = get_asset_display_name(item_key)
        await update.message.reply_text(f"✅ خرید شما با موفقیت انجام شد!\n"
                                        f"{quantity:,} واحد از '{item_display_name}' به دارایی شما اضافه شد.\n"
                                        f"سرمایه باقی‌مانده: {new_capital:,}")
        context.user_data.pop('selected_shop_item_key', None)
        context.user_data.pop('selected_shop_item_price', None)
        context.user_data.pop('current_shop_category', None)
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_shop_item_quantity: {e}", exc_info=True)
        await update.message.reply_text("خطا در انجام خرید")
        return MAIN_MENU


async def statement_proposal_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ شما هنوز کشوری ثبت نکرده‌اید.")
            return MAIN_MENU
        context.user_data['statement_text_parts'] = []
        context.user_data['statement_photo_ids'] = []
        await query.edit_message_text("📣 لطفاً بیانیه خود را ارسال کنید.\n"
                                      "می‌توانید متن و/یا عکس را در یک پیام یا چند پیام متوالی ارسال کنید. "
                                      "بیانیه شما بلافاصله پس از ارسال به کانال عمومی فرستاده خواهد شد.")
        return GET_STATEMENT_CONTENT
    except Exception as e:
        logger.error(f"Error in statement_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("خطا در شروع ارسال بیانیه")
        return MAIN_MENU


async def get_statement_content(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.effective_message.reply_text("❌ کشور شما یافت نشد.")
        return MAIN_MENU
    try:
        # هندل عکس، ویدیو، انیمیشن، داکیومنت
        statement_text = ""
        statement_photo_id = None
        statement_video_id = None
        statement_animation_id = None
        statement_document_id = None
        media_type = None
        if update.effective_message.photo:
            statement_text = update.effective_message.caption or ""
            statement_photo_id = update.effective_message.photo[-1].file_id
            media_type = "photo"
        elif update.effective_message.video:
            statement_text = update.effective_message.caption or ""
            statement_video_id = update.effective_message.video.file_id
            media_type = "video"
        elif update.effective_message.animation:
            statement_text = update.effective_message.caption or ""
            statement_animation_id = update.effective_message.animation.file_id
            media_type = "animation"
        elif update.effective_message.document:
            statement_text = update.effective_message.caption or ""
            statement_document_id = update.effective_message.document.file_id
            media_type = "document"
        else:
            statement_text = update.effective_message.text or ""
            media_type = "text"
        # فرمت جدید: بیانیه ی <نام> + نقل قول تلگرامی + فرستنده لینک‌دار
        import html as _html
        safe_name = _html.escape(country['name'])
        safe_text = _html.escape(statement_text)
        # لینک به صاحب کشور
        owner_id = user_id
        header = f"بیانیه ی {safe_name}"
        # برای تلگرام: blockquote
        quoted = f"<blockquote>{safe_text}</blockquote>" if safe_text.strip() else "<blockquote> </blockquote>"
        footer = f'فرستنده: <a href="tg://user?id={owner_id}">{safe_name}</a>'
        if statement_photo_id:
            caption = f"{header}\n\n{quoted}\n\n{footer}"
            await context.bot.send_photo(chat_id=STATEMENT_CHANNEL, photo=statement_photo_id,
                                         caption=caption, parse_mode="HTML")
        elif statement_video_id:
            caption = f"{header}\n\n{quoted}\n\n{footer}"
            await context.bot.send_video(chat_id=STATEMENT_CHANNEL, video=statement_video_id,
                                         caption=caption, parse_mode="HTML")
        elif statement_animation_id:
            caption = f"{header}\n\n{quoted}\n\n{footer}"
            await context.bot.send_animation(chat_id=STATEMENT_CHANNEL, animation=statement_animation_id,
                                             caption=caption, parse_mode="HTML")
        elif statement_document_id:
            caption = f"{header}\n\n{quoted}\n\n{footer}"
            await context.bot.send_document(chat_id=STATEMENT_CHANNEL, document=statement_document_id,
                                            caption=caption, parse_mode="HTML")
        else:
            channel_message = f"{header}\n\n{quoted}\n\n{footer}"
            await context.bot.send_message(chat_id=STATEMENT_CHANNEL, text=channel_message,
                                           parse_mode="HTML")
        await update.effective_message.reply_text("✅ بیانیه شما با موفقیت به کانال عمومی ارسال شد!")

        if 'statement_text_parts' in context.user_data:
            del context.user_data['statement_text_parts']
        if 'statement_photo_ids' in context.user_data:
            del context.user_data['statement_photo_ids']

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_statement_content: {e}", exc_info=True)
        await update.effective_message.reply_text("❌ متاسفانه خطایی در ارسال بیانیه رخ داد.")
        return GET_STATEMENT_CONTENT


async def list_countries(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        if not countries:
            await query.edit_message_text("هیچ کشوری ثبت نشده است.")
            return ADMIN_MENU
        message = "لیست کشورها:\n\n"
        for user_id, name in countries:
            message += f"نام: {name}, ID: {user_id}\n"
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in list_countries: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return ADMIN_MENU


async def add_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("لطفا آیدی عددی کاربر و نام کشور را به این فرمت وارد کنید:\n`ID, نام کشور`\n\nمثال: `12345, ایران`")
    return ADD_COUNTRY


async def create_new_country(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        text = update.message.text
        try:
            target_user_id_str, country_name = text.split(',', 1)
            target_user_id = int(target_user_id_str.strip())
            country_name = country_name.strip()
        except ValueError:
            await update.message.reply_text("فرمت وارد شده صحیح نیست. لطفاً مجدداً وارد کنید.")
            return ADD_COUNTRY
        if get_country(target_user_id):
            await update.message.reply_text(f"کشوری با این آیدی ({target_user_id}) از قبل موجود است.")
            return ADD_COUNTRY
        create_country(target_user_id, country_name)
        await update.message.reply_text(f"✅ کشور '{country_name}' با موفقیت برای کاربر با آیدی {target_user_id} ثبت شد.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in create_new_country: {e}", exc_info=True)
        await update.message.reply_text(f"خطا در ایجاد کشور جدید: {str(e)}")
        return ADD_COUNTRY


async def delete_country_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("هیچ کشوری برای حذف وجود ندارد.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"delete_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("لطفاً کشوری را برای حذف انتخاب کنید:", reply_markup=reply_markup)
        return DELETE_COUNTRY_MENU
    except Exception as e:
        logger.error(f"Error in delete_country_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return ADMIN_MENU


async def confirm_delete_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_delete = int(query.data.replace("delete_country_", ""))

        country_data = get_country(user_id_to_delete)
        if not country_data:
            await query.edit_message_text("کشور مورد نظر برای حذف یافت نشد.")
            return ADMIN_MENU
        keyboard = [
            [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f"execute_delete_country_{user_id_to_delete}")],
            [InlineKeyboardButton("❌ خیر، انصراف", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"⚠️ آیا مطمئنید که می‌خواهید کشور '{country_data['name']}' با آیدی {user_id_to_delete} را حذف کنید؟ این عمل غیرقابل برگشت است.", reply_markup=reply_markup)
        return DELETE_COUNTRY_MENU
    except Exception as e:
        logger.error(f"Error in confirm_delete_country: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت اطلاعات کشور")
        return ADMIN_MENU


async def execute_delete_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_delete = int(query.data.replace("execute_delete_country_", ""))

        country_data = get_country(user_id_to_delete)
        if not country_data:
            await query.edit_message_text("کشور مورد نظر برای حذف یافت نشد.")
            return ADMIN_MENU
        delete_country(user_id_to_delete)
        await query.edit_message_text(f"✅ کشور '{country_data['name']}' با موفقیت حذف شد.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in execute_delete_country: {e}", exc_info=True)
        await query.edit_message_text("خطا در حذف کشور")
        return ADMIN_MENU


async def set_religion_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ شما هنوز کشوری ثبت نکرده‌اید.")
            return MAIN_MENU
        keyboard = []
        for code, display_name in RELIGIONS:
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"set_religion_{code}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"🌍 دین فعلی کشور شما: {next((disp for code, disp in RELIGIONS if code == country['religion']), 'نامعلوم')}\n"
                                      "لطفاً دین جدید را انتخاب کنید:", reply_markup=reply_markup)
        return RELIGION_MENU
    except Exception as e:
        logger.error(f"Error in set_religion_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی دین")
        return MAIN_MENU


async def set_country_religion(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        new_religion = query.data.replace("set_religion_", "")
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ کشور شما یافت نشد.")
            return MAIN_MENU

        religion_display_name = next((disp for code, disp in RELIGIONS if code == new_religion), new_religion)
        update_country(user_id, {'religion': new_religion})

        try:
            photo_id = get_notification_image("religion")
            message = f"🌍 کشور {country['name']} دین خود را به {religion_display_name} تغییر داد"

            if photo_id:
                await context.bot.send_photo(
                    chat_id=STATEMENT_CHANNEL,
                    photo=photo_id,
                    caption=message
                )
            else:
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=message
                )
        except Exception as e:
            logger.error(f"خطا در ارسال اطلاع دین به کانال: {e}")

        await query.edit_message_text(f"✅ دین کشور شما با موفقیت به '{religion_display_name}' تغییر یافت.")
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in set_country_religion: {e}", exc_info=True)
        await query.edit_message_text("خطا در تغییر دین")
        return RELIGION_MENU


async def add_admin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("لطفاً آیدی عددی کاربری که می‌خواهید ادمین کنید را وارد کنید:")
    return ADD_ADMIN


async def process_add_admin(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        user_id_to_add = update.message.text
        try:
            user_id_to_add = int(user_id_to_add)
        except ValueError:
            await update.message.reply_text("آیدی نامعتبر است. لطفاً یک عدد صحیح وارد کنید.")
            return ADD_ADMIN
        if add_admin_to_db(user_id_to_add):
            await update.message.reply_text(f"✅ کاربر با آیدی {user_id_to_add} با موفقیت به عنوان ادمین اضافه شد.")
        else:
            await update.message.reply_text(f"کاربر با آیدی {user_id_to_add} از قبل ادمین است.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_add_admin: {e}", exc_info=True)
        await update.message.reply_text("خطا در افزودن ادمین")
        return ADD_ADMIN


async def remove_admin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_admins = get_all_admins()
        keyboard = []
        for admin_id in current_admins:
            if admin_id != OWNER_ID:
                keyboard.append([InlineKeyboardButton(f"ID: {admin_id}", callback_data=f"remove_admin_{admin_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if not keyboard or len(keyboard) == 1:
            await query.edit_message_text("هیچ ادمین دیگری برای حذف وجود ندارد.")
            return ADMIN_MENU
        await query.edit_message_text("لطفاً ادمینی را برای حذف انتخاب کنید:", reply_markup=reply_markup)
        return REMOVE_ADMIN
    except Exception as e:
        logger.error(f"Error in remove_admin: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست ادمین‌ها")
        return ADMIN_MENU


async def process_remove_admin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_remove = int(query.data.replace("remove_admin_", ""))
        if remove_admin_from_db(user_id_to_remove):
            await query.edit_message_text(f"✅ ادمین با آیدی {user_id_to_remove} با موفقیت حذف شد.")
        else:
            await query.edit_message_text(f"❌ کاربر با آیدی {user_id_to_remove} ادمین نیست یا نمی‌توان آن را حذف کرد (شاید مالک باشد).")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_remove_admin: {e}", exc_info=True)
        await query.edit_message_text("خطا در حذف ادمین")
        return ADMIN_MENU


async def toggle_bot_active_status(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_bot_active_status()
        set_bot_active_status(not current_status)
        new_status_text = "فعال" if not current_status else "غیرفعال"
        await query.edit_message_text(f"✅ وضعیت ربات با موفقیت به '{new_status_text}' تغییر یافت.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in toggle_bot_active_status: {e}", exc_info=True)
        await query.edit_message_text("خطا در تغییر وضعیت ربات")
        return ADMIN_MENU


async def manage_global_buttons(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        disabled_buttons = get_global_disabled_buttons()
        keyboard = []
        for btn in BOT_MAIN_MENU_BUTTONS:
            status = "❌ غیرفعال" if btn['callback_data'] in disabled_buttons else "✅ فعال"
            keyboard.append([InlineKeyboardButton(f"{btn['text']} {status}", callback_data=f"toggle_global_button_{btn['callback_data']}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("مدیریت دکمه‌های عمومی:\n"
                                      "برای تغییر وضعیت دکمه‌ها روی آنها کلیک کنید.", reply_markup=reply_markup)
        return MANAGE_GLOBAL_BUTTONS
    except Exception as e:
        logger.error(f"Error in manage_global_buttons: {e}", exc_info=True)
        await query.edit_message_text("خطا در مدیریت دکمه‌ها")
        return ADMIN_MENU


async def toggle_global_button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        button_callback_data = query.data.replace("toggle_global_button_", "")
        disabled_buttons = get_global_disabled_buttons()
        if button_callback_data in disabled_buttons:
            disabled_buttons.remove(button_callback_data)
        else:
            disabled_buttons.append(button_callback_data)
        set_global_disabled_buttons(disabled_buttons)
        await manage_global_buttons(update, context)
        return MANAGE_GLOBAL_BUTTONS
    except Exception as e:
        logger.error(f"Error in toggle_global_button: {e}", exc_info=True)
        await query.answer("خطا در تغییر وضعیت دکمه", show_alert=True)
        return MANAGE_GLOBAL_BUTTONS


async def back_to_main_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query:
        await query.answer()

    keys_to_remove = [
        'current_proposal_type', 'proposal_text_parts', 'proposal_photo_ids',
        'user_proposal_message_id', 'attack_target_id', 'attack_target_name',
        'attack_troops_details', 'attack_scenario_text', 'attack_scenario_photos',
        'selected_shop_item_key', 'selected_shop_item_price', 'current_shop_category',
        'user_id_to_edit', 'edit_main_prop_key', 'asset_category', 'asset_item',
        'statement_text_parts', 'statement_photo_ids'
    ]

    for key in keys_to_remove:
        if key in context.user_data:
            del context.user_data[key]

    return await show_main_menu(update, context)


async def back_to_admin_panel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query:
        await query.answer()
    context.user_data.pop('user_id_to_edit', None)
    context.user_data.pop('edit_main_prop_key', None)
    context.user_data.pop('asset_category', None)
    context.user_data.pop('asset_item', None)
    return await admin_panel(update, context)


async def send_message_to_user(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("هیچ کشوری برای ارسال پیام وجود ندارد.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"select_user_{user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("لطفاً کاربر مورد نظر را برای ارسال پیام انتخاب کنید:", reply_markup=reply_markup)
        return SELECT_USER_TO_MESSAGE
    except Exception as e:
        logger.error(f"Error in send_message_to_user: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کاربران")
        return ADMIN_MENU


async def select_user_for_message(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = int(query.data.replace("select_user_", ""))
        context.user_data['message_target_id'] = user_id

        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ کاربر مورد نظر یافت نشد.")
            return ADMIN_MENU

        await query.edit_message_text(f"ارسال پیام به کاربر: {country['name']}\nلطفاً پیام خود را وارد کنید:")
        return GET_MESSAGE_TEXT
    except Exception as e:
        logger.error(f"Error in select_user_for_message: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کاربر")
        return SELECT_USER_TO_MESSAGE


async def send_user_message(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        target_id = context.user_data.get('message_target_id')
        message_text = update.message.text

        if not target_id:
            await update.message.reply_text("خطا در انتخاب کاربر. لطفاً دوباره تلاش کنید.")
            return await admin_panel(update, context)

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=f"📮 پیامی از مدیریت:\n\n{message_text}"
            )
            await update.message.reply_text(f"✅ پیام با موفقیت به کاربر ارسال شد.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در ارسال پیام: {str(e)}")

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in send_user_message: {e}", exc_info=True)
        await update.message.reply_text("خطا در ارسال پیام")
        return ADMIN_MENU


async def country_management(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if not get_setting('country_management_active') == '1':
        await query.answer("⛔ بخش مدیریت کشور موقتاً غیرفعال است!", show_alert=True)
        return MAIN_MENU

    try:
        keyboard = [
            [InlineKeyboardButton("💂‍♂️ رزمایش نظامی", callback_data='military_exercise')],
            [InlineKeyboardButton("📩 ارسال پیام", callback_data='send_message_to_country')],
            [InlineKeyboardButton("🤝 تجارت", callback_data='trade_menu')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🏛️ منوی مدیریت کشور:",
            reply_markup=reply_markup
        )
        return COUNTRY_MANAGEMENT
    except Exception as e:
        logger.error(f"Error in country_management: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی مدیریت کشور")
        return MAIN_MENU


    query = update.callback_query
    await query.answer()

    try:
        country = get_country(query.from_user.id)
        status = "✅ ملی" if country['internet_nationalized'] else "❌ غیرملی"
        current_income = INTERNET_INCOME_RATES.get(country.get('internet_level', 2), 0)

        keyboard = [
            [InlineKeyboardButton(f"وضعیت: {status}", callback_data='nationalize_internet')],
            [InlineKeyboardButton(f"ارتقاء ({country['internet_level']}G)", callback_data='upgrade_internet')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🌐 کنترل اینترنت:\nوضعیت: {status}\nسطح فعلی: {country['internet_level']}G\nدرآمد روزانه: {current_income:,}",
            reply_markup=reply_markup
        )
        return INTERNET_CONTROL
    except Exception as e:
        await query.edit_message_text("خطا در نمایش کنترل اینترنت")
        return COUNTRY_MANAGEMENT


async def nationalize_internet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        new_status = not country['internet_nationalized']

        update_country(user_id, {'internet_nationalized': new_status})
        status = "✅ ملی" if new_status else "❌ غیرملی"

        try:
            event_type = "internet_on" if new_status else "internet_off"
            photo_id = get_notification_image(event_type)
            message = f"🌐 کشور {country['name']} اینترنت خود را {'ملی کرد' if new_status else 'از حالت ملی خارج کرد'}"

            if photo_id:
                await context.bot.send_photo(
                    chat_id=STATEMENT_CHANNEL,
                    photo=photo_id,
                    caption=message
                )
            else:
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=message
                )
        except Exception as e:
            logger.error(f"خطا در ارسال وضعیت اینترنت به کانال: {e}")

        await query.answer(f"اینترنت {status} شد")
    except Exception as e:
        logger.error(f"Error in nationalize_internet: {e}", exc_info=True)
        await query.answer("خطا در تغییر وضعیت اینترنت", show_alert=True)
        return INTERNET_CONTROL


async def upgrade_internet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country['internet_level']

        if current_level >= 7:
            await query.answer("اینترنت شما در بالاترین سطح (7G) است!", show_alert=True)
            return INTERNET_CONTROL
        keyboard = []
        for level in range(current_level + 1, 8):
            price = ASSET_PRICES[f'internet_upgrade_{level}g']
            income = INTERNET_INCOME_RATES.get(level, 0)
            keyboard.append([InlineKeyboardButton(
                f"ارتقاء به {level}G - هزینه: {price:,} - درآمد: +{income:,}/روز",
                callback_data=f"upgrade_to_{level}"
            )])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🔼 لطفاً سطح مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return INTERNET_CONTROL
    except Exception as e:
        logger.error(f"Error in upgrade_internet: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش سطوح اینترنت")
        return INTERNET_CONTROL


async def process_internet_upgrade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_level = int(query.data.replace("upgrade_to_", ""))
        user_id = query.from_user.id
        country = get_country(user_id)
        price = ASSET_PRICES[f'internet_upgrade_{target_level}g']

        if country['capital'] < price:
            await query.answer(f"سرمایه شما کافی نیست! قیمت ارتقاء: {price:,}", show_alert=True)

        new_capital = country['capital'] - price
        update_country(user_id, {
            'capital': new_capital,
            'internet_level': target_level
        })
        income = INTERNET_INCOME_RATES.get(target_level, 0)
        await query.answer(f"✅ اینترنت شما به {target_level}G ارتقاء یافت! درآمد روزانه: +{income:,}", show_alert=True)
    except Exception as e:
        logger.error(f"Error in process_internet_upgrade: {e}", exc_info=True)
        await query.answer("خطا در ارتقاء اینترنت", show_alert=True)
        return INTERNET_CONTROL


async def trade_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if get_trade_setting('trade_enabled') != '1':
        await query.answer("⛔ سیستم تجارت موقتاً غیرفعال است!", show_alert=True)
        return COUNTRY_MANAGEMENT

    try:
        keyboard = [
            [InlineKeyboardButton("تجارت عادی", callback_data='normal_trade')]
        ]

        if get_trade_setting('discreet_trade_enabled') == '1':
            keyboard.append([InlineKeyboardButton("تجارت نامحسوس", callback_data='discreet_trade')])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='country_management')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🤝 منوی تجارت:\n"
            "- تجارت عادی: عمومی و با اطلاع کامل به کانال\n"
            "- تجارت نامحسوس: خصوصی و بدون افشای جزئیات در کانال",
            reply_markup=reply_markup
        )
        return TRADE_MENU
    except Exception as e:
        logger.error(f"Error in trade_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی تجارت")
        return COUNTRY_MANAGEMENT


async def normal_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['trade_type'] = 'normal'

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]

        if not other_countries:
            await query.edit_message_text("هیچ کشوری برای تجارت وجود ندارد.")
            return TRADE_MENU
        keyboard = []
        for uid, name in other_countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"trade_target_{uid}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "لطفاً کشور مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return TRADE_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in normal_trade: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش کشورها")
        return TRADE_MENU


async def discreet_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['trade_type'] = 'discreet'

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]

        if not other_countries:
            await query.edit_message_text("هیچ کشوری برای تجارت وجود ندارد.")
            return TRADE_MENU
        keyboard = []
        for uid, name in other_countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"trade_target_{uid}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "لطفاً کشور مورد نظر را انتخاب کنید (تجارت محرمانه):",
            reply_markup=reply_markup
        )
        return TRADE_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in discreet_trade: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش کشورها")
        return TRADE_MENU


async def select_trade_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_id = int(query.data.replace("trade_target_", ""))
        context.user_data['trade_target_id'] = target_id

        target_country = get_country(target_id)
        if not target_country:
            await query.edit_message_text("کشور مورد نظر یافت نشد!")
            return TRADE_MENU

        context.user_data['trade_target_name'] = target_country['name']

        keyboard = []
        for domain_key, domain_name in TRADE_DOMAINS:
            keyboard.append([InlineKeyboardButton(domain_name, callback_data=f"trade_domain_{domain_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"تجارت با {target_country['name']}\nلطفاً دامنه تجارت را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return TRADE_DOMAIN_SELECTION
    except Exception as e:
        logger.error(f"Error in select_trade_target: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کشور هدف")
        return TRADE_MENU


async def select_trade_domain(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        domain_key = query.data.replace("trade_domain_", "")
        context.user_data['trade_domain'] = domain_key

        domain_display_name = next((name for key, name in TRADE_DOMAINS if key == domain_key), domain_key)

        await query.edit_message_text(
            f"دامنه تجارت: {domain_display_name}\n"
            "لطفاً آیتم‌هایی که می‌خواهید ارسال کنید را انتخاب کنید (تا 3 آیتم):"
        )

        context.user_data['trade_items'] = {'send': [], 'receive': []}

        keyboard = [
            [InlineKeyboardButton("➕ افزودن آیتم ارسالی", callback_data='add_send_item')],
            [InlineKeyboardButton("➕ افزودن آیتم دریافتی", callback_data='add_receive_item')],
            [InlineKeyboardButton("✅ تأیید و ارسال درخواست تجارت", callback_data='confirm_trade')],
            [InlineKeyboardButton("❌ لغو", callback_data='trade_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "لطفاً آیتم‌های ارسالی و دریافتی خود را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return TRADE_ADD_ITEMS
    except Exception as e:
        logger.error(f"Error in select_trade_domain: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب دامنه تجارت")
        return TRADE_SELECT_TARGET


async def add_send_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"trade_send_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("💰 سرمایه", callback_data="trade_send_capital")])
        keyboard.append([InlineKeyboardButton("🛢️ نفت", callback_data="trade_send_oil_barrels")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"trade_domain_{context.user_data['trade_domain']}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "انتخاب منبع ارسالی:",
            reply_markup=reply_markup
        )
        return TRADE_SEND_ITEM_CATEGORY
    except Exception as e:
        logger.error(f"Error in add_send_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در افزودن آیتم ارسالی")
        return TRADE_ADD_ITEMS


async def add_receive_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"trade_receive_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("💰 سرمایه", callback_data="trade_receive_capital")])
        keyboard.append([InlineKeyboardButton("🛢️ نفت", callback_data="trade_receive_oil_barrels")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='add_receive_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "انتخاب منبع دریافتی:",
            reply_markup=reply_markup
        )
        return TRADE_RECEIVE_ITEM_CATEGORY
    except Exception as e:
        logger.error(f"Error in add_receive_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در افزودن آیتم دریافتی")
        return TRADE_ADD_ITEMS


async def select_send_item_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'trade_send_capital':
            context.user_data['current_trade_item'] = {'type': 'send', 'resource': 'capital'}
            await query.edit_message_text("💰 لطفاً مقدار سرمایه‌ای که می‌خواهید ارسال کنید را وارد کنید:")
            return TRADE_GET_SEND_AMOUNT

        if query.data == 'trade_send_oil_barrels':
            context.user_data['current_trade_item'] = {'type': 'send', 'resource': 'oil_barrels'}
            await query.edit_message_text("🛢️ لطفاً مقدار نفتی که می‌خواهید ارسال کنید را وارد کنید:")
            return TRADE_GET_SEND_AMOUNT

        category_key = query.data.replace("trade_send_category_", "")
        context.user_data['current_trade_item'] = {'type': 'send', 'category': category_key}

        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ کشور شما یافت نشد.")
            return MAIN_MENU

        assets = country.get(category_key, {})
        keyboard = []
        for item_key, count in assets.items():
            if count > 0:
                display_name = get_asset_display_name(item_key)
                keyboard.append([InlineKeyboardButton(f"{display_name} (موجود: {count})", callback_data=f"trade_send_item_{item_key}")])

        if not keyboard:
            await query.answer("هیچ آیتمی در این دسته‌بندی موجود نیست!", show_alert=True)
            return TRADE_ADD_ITEMS

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='add_send_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"انتخاب آیتم ارسالی از دسته‌بندی {category_display_name}:",
            reply_markup=reply_markup
        )
        return TRADE_SEND_ITEM_SELECT
    except Exception as e:
        logger.error(f"Error in select_send_item_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب دسته‌بندی")
        return TRADE_SEND_ITEM_CATEGORY


async def select_send_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("trade_send_item_", "")
        trade_item = context.user_data.get('current_trade_item', {})
        trade_item['resource'] = item_key
        context.user_data['current_trade_item'] = trade_item

        await query.edit_message_text(f"لطفاً مقدار {get_asset_display_name(item_key)} که می‌خواهید ارسال کنید را وارد کنید:")
        return TRADE_GET_SEND_AMOUNT
    except Exception as e:
        logger.error(f"Error in select_send_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب آیتم ارسالی")
        return TRADE_SEND_ITEM_SELECT


async def get_send_amount(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("❌ کشور شما یافت نشد.")
        return MAIN_MENU
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("مقدار باید بزرگتر از صفر باشد.")
            return TRADE_GET_SEND_AMOUNT
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
        return TRADE_GET_SEND_AMOUNT
    trade_item = context.user_data.get('current_trade_item', {})
    if not trade_item:
        await update.message.reply_text("خطا در پردازش آیتم. لطفاً دوباره تلاش کنید.")
        return TRADE_ADD_ITEMS

    if trade_item.get('resource') == 'capital':
        if country['capital'] < amount:
            await update.message.reply_text(f"سرمایه شما کافی نیست! سرمایه فعلی: {country['capital']:,}")
            return TRADE_GET_SEND_AMOUNT
    elif trade_item.get('resource') == 'oil_barrels':
        if country['oil_barrels'] < amount:
            await update.message.reply_text(f"نفت شما کافی نیست! نفت فعلی: {country['oil_barrels']:,}")
            return TRADE_GET_SEND_AMOUNT
    else:
        category = trade_item.get('category')
        resource = trade_item.get('resource')
        current_amount = country.get(category, {}).get(resource, 0)
        if current_amount < amount:
            display_name = get_asset_display_name(resource)
            await update.message.reply_text(f"موجودی {display_name} شما کافی نیست! موجودی فعلی: {current_amount:,}")
            return TRADE_GET_SEND_AMOUNT

    trade_items = context.user_data.get('trade_items', {'send': [], 'receive': []})
    trade_item['amount'] = amount
    trade_items['send'].append(trade_item)
    context.user_data['trade_items'] = trade_items
    context.user_data.pop('current_trade_item', None)

    return await show_trade_items(update, context)


async def select_receive_item_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'trade_receive_capital':
            context.user_data['current_trade_item'] = {'type': 'receive', 'resource': 'capital'}
            await query.edit_message_text("💰 لطفاً مقدار سرمایه‌ای که می‌خواهید دریافت کنید را وارد کنید:")
            return TRADE_GET_RECEIVE_AMOUNT

        if query.data == 'trade_receive_oil_barrels':
            context.user_data['current_trade_item'] = {'type': 'receive', 'resource': 'oil_barrels'}
            await query.edit_message_text("🛢️ لطفاً مقدار نفتی که می‌خواهید دریافت کنید را وارد کنید:")
            return TRADE_GET_RECEIVE_AMOUNT

        category_key = query.data.replace("trade_receive_category_", "")
        context.user_data['current_trade_item'] = {'type': 'receive', 'category': category_key}

        keyboard = []
        for item_key in get_dynamic_default_assets().get(category_key, {}).keys():
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"trade_receive_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='add_receive_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"انتخاب آیتم دریافتی از دسته‌بندی {category_display_name}:",
            reply_markup=reply_markup
        )
        return TRADE_RECEIVE_ITEM_SELECT
    except Exception as e:
        logger.error(f"Error in select_receive_item_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب دسته‌بندی")
        return TRADE_RECEIVE_ITEM_CATEGORY


async def select_receive_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("trade_receive_item_", "")
        trade_item = context.user_data.get('current_trade_item', {})
        trade_item['resource'] = item_key
        context.user_data['current_trade_item'] = trade_item

        await query.edit_message_text(f"لطفاً مقدار {get_asset_display_name(item_key)} که می‌خواهید دریافت کنید را وارد کنید:")
        return TRADE_GET_RECEIVE_AMOUNT
    except Exception as e:
        logger.error(f"Error in select_receive_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب آیتم دریافتی")
        return TRADE_RECEIVE_ITEM_SELECT


async def get_receive_amount(update: Update, context: CallbackContext) -> int:
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("مقدار باید بزرگتر از صفر باشد.")
            return TRADE_GET_RECEIVE_AMOUNT
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
        return TRADE_GET_RECEIVE_AMOUNT
    trade_item = context.user_data.get('current_trade_item', {})
    if not trade_item:
        await update.message.reply_text("خطا در پردازش آیتم. لطفاً دوباره تلاش کنید.")
        return TRADE_ADD_ITEMS

    trade_items = context.user_data.get('trade_items', {'send': [], 'receive': []})
    trade_item['amount'] = amount
    trade_items['receive'].append(trade_item)
    context.user_data['trade_items'] = trade_items
    context.user_data.pop('current_trade_item', None)

    return await show_trade_items(update, context)


async def show_trade_items(update: Update, context: CallbackContext) -> int:
    try:
        trade_items = context.user_data.get('trade_items', {'send': [], 'receive': []})
        target_name = context.user_data.get('trade_target_name', '')

        message = "📦 آیتم‌های انتخاب شده برای تجارت:\n\n"
        message += "📤 *ارسال به کشور مقابل:*\n"
        for item in trade_items['send']:
            if item.get('resource') == 'capital':
                message += f"• 💰 سرمایه: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"• 🛢️ نفت: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"• {display_name}: {item['amount']:,}\n"

        message += "\n📥 *دریافت از کشور مقابل:*\n"
        for item in trade_items['receive']:
            if item.get('resource') == 'capital':
                message += f"• 💰 سرمایه: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"• 🛢️ نفت: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"• {display_name}: {item['amount']:,}\n"

        keyboard = [
            [InlineKeyboardButton("➕ افزودن آیتم ارسالی", callback_data='add_send_item')],
            [InlineKeyboardButton("➕ افزودن آیتم دریافتی", callback_data='add_receive_item')],
            [InlineKeyboardButton("✅ تأیید و ارسال درخواست تجارت", callback_data='confirm_trade')],
            [InlineKeyboardButton("❌ لغو", callback_data='trade_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

        return TRADE_ADD_ITEMS
    except Exception as e:
        logger.error(f"Error in show_trade_items: {e}", exc_info=True)
        if update.callback_query:
            await update.callback_query.answer("خطا در نمایش آیتم‌ها", show_alert=True)
        else:
            await update.message.reply_text("خطا در نمایش آیتم‌ها")
        return TRADE_ADD_ITEMS


async def confirm_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    try:
        if query.message:
            await query.edit_message_text("در حال پردازش درخواست...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "در حال پردازش درخواست...")

    try:
        user_id = query.from_user.id
        target_user_id = context.user_data['trade_target_id']
        trade_type = context.user_data.get('trade_type', 'normal')
        domain = context.user_data['trade_domain']
        trade_items = context.user_data.get('trade_items', {'send': [], 'receive': []})

        country = get_country(user_id)
        for item in trade_items['send']:
            resource = item.get('resource')
            amount = item.get('amount', 0)

            if resource == 'capital':
                if country['capital'] < amount:
                    await query.answer(f"سرمایه شما کافی نیست! سرمایه فعلی: {country['capital']:,}", show_alert=True)
                    return TRADE_ADD_ITEMS
            elif resource == 'oil_barrels':
                if country['oil_barrels'] < amount:
                    await query.answer(f"نفت شما کافی نیست! نفت فعلی: {country['oil_barrels']:,}", show_alert=True)
                    return TRADE_ADD_ITEMS
            else:
                category = item.get('category')
                if resource in country.get(category, {}):
                    if country[category][resource] < amount:
                        display_name = get_asset_display_name(resource)
                        await query.answer(f"موجودی {display_name} کافی نیست! موجودی فعلی: {country[category][resource]}", show_alert=True)
                        return TRADE_ADD_ITEMS
                else:
                    display_name = get_asset_display_name(resource)
                    await query.answer(f"شما {display_name} ندارید!", show_alert=True)
                    return TRADE_ADD_ITEMS

        trade_id, delivery_minutes, secret_code = create_trade(
            user_id, target_user_id, domain,
            trade_items['send'],
            trade_items['receive'],
            trade_type
        )

        target_country = get_country(target_user_id)
        trade_display_name = "عادی" if trade_type == "normal" else "محرمانه"
        domain_display_name = next((name for key, name in TRADE_DOMAINS if key == domain), domain)

        sender_country = get_country(user_id)

        message = (
            f"📬 درخواست تجارت جدید!\n\n"
            f"👤 از: {sender_country['name']}\n"
            f"🌐 دامنه: {domain_display_name}\n"
            f"📤 ارسال به شما:\n"
        )
        for item in trade_items['send']:
            if item.get('resource') == 'capital':
                message += f"• 💰 سرمایه: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"• 🛢️ نفت: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"• {display_name}: {item['amount']:,}\n"

        message += f"\n📥 دریافت از شما:\n"
        for item in trade_items['receive']:
            if item.get('resource') == 'capital':
                message += f"• 💰 سرمایه: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"• 🛢️ نفت: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"• {display_name}: {item['amount']:,}\n"

        message += f"\n⏳ زمان تحویل: {delivery_minutes} دقیقه\n"
        message += f"🔒 نوع تجارت: {trade_display_name}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ قبول درخواست", callback_data=f"accept_trade_{trade_id}"),
             InlineKeyboardButton("❌ رد درخواست", callback_data=f"reject_trade_{trade_id}")]
        ])

        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=message,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"خطا در ارسال درخواست تجارت به کشور هدف: {e}", exc_info=True)
            await query.edit_message_text("❌ خطا در ارسال درخواست تجارت به کشور هدف. لطفاً اطمینان حاصل کنید که ربات برای آن کاربر فعال است.")
            return TRADE_ADD_ITEMS

        await query.edit_message_text(f"✅ درخواست تجارت شما به {target_country['name']} ارسال شد. منتظر تأیید آنها باشید.")

        if trade_type == 'discreet':
            discreet_channel = get_trade_setting('discreet_trade_channel') or STATEMENT_CHANNEL
            admin_message = (
                f"🔒 درخواست تجارت نامحسوس جدید!\n\n"
                f"👤 فرستنده: {sender_country['name']} (ID: {user_id})\n"
                f"🎯 گیرنده: {target_country['name']} (ID: {target_user_id})\n"
                f"🌐 دامنه: {domain_display_name}\n"
                f"🔐 کد تجارت: {secret_code}\n\n"
                f"برای لغو تجارت از کد بالا استفاده کنید."
            )

            admin_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ لغو تجارت", callback_data=f"cancel_trade_{trade_id}")]
            ])

            try:
                await context.bot.send_message(
                    chat_id=discreet_channel,
                    text=admin_message,
                    reply_markup=admin_keyboard
                )
            except Exception as e:
                logger.error(f"خطا در ارسال به کانال تجارت نامحسوس: {e}")

        keys_to_remove = [
            'trade_type', 'trade_target_id', 'trade_target_name', 'trade_domain',
            'trade_items', 'current_trade_item'
        ]
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in confirm_trade: {e}", exc_info=True)
        await query.edit_message_text("❌ خطا در ثبت تجارت. لطفاً دوباره تلاش کنید.")
        return TRADE_ADD_ITEMS


async def handle_trade_response(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        parts = query.data.split('_', 2)
        if len(parts) < 3:
            await query.answer("داده‌های فراخوان نامعتبر است", show_alert=True)
            return MAIN_MENU

        action = parts[0]
        trade_id = parts[2]

        trade = get_trade(trade_id)
        if not trade:
            await query.edit_message_text("❌ تجارت مورد نظر یافت نشد یا قبلاً پردازش شده است.")
            return MAIN_MENU

        if action == "accept":
            receiver_country = get_country(trade['receiver_id'])
            if not receiver_country:
                await query.edit_message_text("❌ کشور شما یافت نشد.")
                return MAIN_MENU

            for item in trade['receive_resource']:
                resource = item.get('resource')
                amount = item.get('amount', 0)
                if resource == 'capital':
                    if receiver_country['capital'] < amount:
                        await query.answer(f"سرمایه شما کافی نیست! سرمایه فعلی: {receiver_country['capital']:,}", show_alert=True)
                        return MAIN_MENU
                elif resource == 'oil_barrels':
                    if receiver_country['oil_barrels'] < amount:
                        await query.answer(f"نفت شما کافی نیست! نفت فعلی: {receiver_country['oil_barrels']:,}", show_alert=True)
                        return MAIN_MENU
                else:
                    category = item.get('category')
                    current_amount = receiver_country.get(category, {}).get(resource, 0)
                    if current_amount < amount:
                        display_name = get_asset_display_name(resource)
                        await query.answer(f"موجودی {display_name} شما کافی نیست! موجودی فعلی: {current_amount}", show_alert=True)
                        return MAIN_MENU

            update_trade_status(trade_id, "accepted")

            delivery_time = datetime.fromisoformat(trade['delivery_time'])
            now = datetime.now()
            remaining_minutes = max(0, int((delivery_time - now).total_seconds() / 60))

            await query.edit_message_text("✅ شما این تجارت را قبول کردید. منابع پس از زمان مشخص شده منتقل خواهند شد.")

            sender_country = get_country(trade['sender_id'])
            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"✅ کشور {receiver_country['name']} درخواست تجارت شما را پذیرفت. منابع پس از {remaining_minutes} دقیقه منتقل خواهند شد."
                )
            except Exception as e:
                logger.error(f"خطا در اطلاع به فرستنده: {e}")

            if trade['trade_type'] == 'normal':
                trade_channel = get_trade_setting('trade_channel') or STATEMENT_CHANNEL
                try:
                    domain_display_name = next((name for key, name in TRADE_DOMAINS if key == trade['domain']), trade['domain'])
                    channel_message = (
                        f"📊 تجارت جدید تأیید شد!\n\n"
                        f"🌐 دامنه: {domain_display_name}\n"
                        f"🔄 کشورها: {sender_country['name']} ↔️ {receiver_country['name']}\n"
                        f"⏳ زمان تحویل: {remaining_minutes} دقیقه"
                    )

                    trade_photo_id = get_notification_image(f"trade_{trade['domain']}")
                    if trade_photo_id:
                        await context.bot.send_photo(
                            chat_id=trade_channel,
                            photo=trade_photo_id,
                            caption=channel_message
                        )
                    else:
                        await context.bot.send_message(
                            chat_id=trade_channel,
                            text=channel_message
                        )
                except Exception as e:
                    logger.error(f"خطا در ارسال تجارت به کانال: {e}")

        elif action == "reject":
            update_trade_status(trade_id, "rejected")
            await query.edit_message_text("❌ شما این تجارت را رد کردید.")

            receiver_country = get_country(trade['receiver_id'])
            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"❌ کشور {receiver_country['name']} درخواست تجارت شما را رد کرد."
                )
            except Exception as e:
                logger.error(f"خطا در اطلاع به فرستنده: {e}")
        elif action == "cancel":
            if not is_admin(query.from_user.id):
                await query.answer("⛔️ فقط ادمین‌ها می‌توانند تجارت را لغو کنند!", show_alert=True)
                return ADMIN_MENU

            update_trade_status(trade_id, "cancelled")
            await query.edit_message_text("✅ تجارت لغو شد.")

            sender_country = get_country(trade['sender_id'])
            receiver_country = get_country(trade['receiver_id'])

            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"❌ تجارت شما با کشور {receiver_country['name']} توسط مدیریت لغو شد."
                )
                await context.bot.send_message(
                    chat_id=trade['receiver_id'],
                    text=f"❌ تجارت شما با کشور {sender_country['name']} توسط مدیریت لغو شد."
                )
            except Exception as e:
                logger.error(f"خطا در اطلاع به طرفین تجارت: {e}")

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in handle_trade_response: {e}", exc_info=True)
        await query.edit_message_text("خطا در پردازش درخواست تجارت")
        return MAIN_MENU


async def deliver_trades_job(context: CallbackContext):
    logger.info("بررسی تحویل تجارت‌ها...")
    try:
        trades = get_trades_for_delivery()
        if not trades:
            logger.info("هیچ تجارتی برای تحویل وجود ندارد.")
            return

        logger.info(f"تحویل {len(trades)} تجارت")

        for trade in trades:
            try:
                sender_id = trade['sender_id']
                receiver_id = trade['receiver_id']

                sender_country = get_country(sender_id)
                receiver_country = get_country(receiver_id)

                if not sender_country or not receiver_country:
                    logger.warning(f"کشور فرستنده یا گیرنده برای تجارت {trade['id']} یافت نشد.")
                    continue

                for item in trade['send_resource']:
                    resource = item.get('resource')
                    amount = item.get('amount', 0)
                    category = item.get('category')

                    if resource == 'capital':
                        sender_updates = {'capital': sender_country['capital'] - amount}
                        receiver_updates = {'capital': receiver_country['capital'] + amount}

                        update_country(sender_id, sender_updates)
                        update_country(receiver_id, receiver_updates)
                    elif resource == 'oil_barrels':
                        sender_updates = {'oil_barrels': sender_country['oil_barrels'] - amount}
                        receiver_updates = {'oil_barrels': receiver_country['oil_barrels'] + amount}

                        update_country(sender_id, sender_updates)
                        update_country(receiver_id, receiver_updates)
                    else:
                        sender_assets = sender_country.get(category, {})
                        current_amount = sender_assets.get(resource, 0)
                        new_amount = current_amount - amount

                        update_country(sender_id, {
                            category: {resource: new_amount}
                        })

                        receiver_assets = receiver_country.get(category, {})
                        current_amount = receiver_assets.get(resource, 0)
                        new_amount = current_amount + amount

                        update_country(receiver_id, {
                            category: {resource: new_amount}
                        })

                for item in trade['receive_resource']:
                    resource = item.get('resource')
                    amount = item.get('amount', 0)
                    category = item.get('category')

                    if resource == 'capital':
                        receiver_updates = {'capital': receiver_country['capital'] - amount}
                        sender_updates = {'capital': sender_country['capital'] + amount}

                        update_country(receiver_id, receiver_updates)
                        update_country(sender_id, sender_updates)
                    elif resource == 'oil_barrels':
                        receiver_updates = {'oil_barrels': receiver_country['oil_barrels'] - amount}
                        sender_updates = {'oil_barrels': sender_country['oil_barrels'] + amount}

                        update_country(receiver_id, receiver_updates)
                        update_country(sender_id, sender_updates)
                    else:
                        receiver_assets = receiver_country.get(category, {})
                        current_amount = receiver_assets.get(resource, 0)
                        new_amount = current_amount - amount

                        update_country(receiver_id, {
                            category: {resource: new_amount}
                        })

                        sender_assets = sender_country.get(category, {})
                        current_amount = sender_assets.get(resource, 0)
                        new_amount = current_amount + amount

                        update_country(sender_id, {
                            category: {resource: new_amount}
                        })

                complete_trade(trade['id'])

                try:
                    await context.bot.send_message(
                        sender_id,
                        f"✅ تجارت شما با کشور {receiver_country['name']} با موفقیت تحویل داده شد!"
                    )
                    await context.bot.send_message(
                        receiver_id,
                        f"✅ تجارت شما با کشور {sender_country['name']} با موفقیت تحویل داده شد!"
                    )
                except Exception as e:
                    logger.error(f"خطا در ارسال پیام به کاربران: {e}")

                logger.info(f"تجارت {trade['id']} با موفقیت تحویل داده شد.")

            except Exception as e:
                logger.error(f"خطا در پردازش تجارت {trade['id']}: {e}")

        logger.info("تحویل تجارت‌ها با موفقیت انجام شد.")
    except Exception as e:
        logger.error(f"خطا در تحویل تجارت‌ها: {e}")


async def deliver_attacks_job(context: CallbackContext):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("SELECT * FROM attack_deliveries WHERE delivery_time <= ?", (now,))
    attacks = c.fetchall()
    conn.close()

    for attack in attacks:
        proposal_id = attack[0]
        proposal = get_proposal(proposal_id)
        if proposal:
            try:
                attacker = get_country(proposal['user_id'])
                target = get_country(proposal['target_user_id'])
                if not attacker or not target:
                    continue
                delivery_message = (
                    f"💥 حمله به مقصد رسید!\n\n"
                    f"⚔️ حمله از کشور {attacker['name']}\n"
                    f"🎯 به کشور {target['name']}\n"
                    f"با موفقیت تحویل داده شد!"
                )
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=delivery_message
                )
            except Exception as e:
                logger.error(f"خطا در ارسال پیام تحویل حمله: {e}")

            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM attack_deliveries WHERE proposal_id = ?", (proposal_id,))
            conn.commit()
            conn.close()


async def trade_settings(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        trade_enabled = get_trade_setting('trade_enabled') == '1'
        max_trades = get_trade_setting('max_trades') or '5'
        trade_channel = get_trade_setting('trade_channel') or STATEMENT_CHANNEL
        discreet_enabled = get_trade_setting('discreet_trade_enabled') == '1'
        discreet_channel = get_trade_setting('discreet_trade_channel') or STATEMENT_CHANNEL

        keyboard = [
            [InlineKeyboardButton(f"فعال‌سازی تجارت: {'✅ روشن' if trade_enabled else '❌ خاموش'}", callback_data='toggle_trade_enabled')],
            [InlineKeyboardButton(f"تجارت نامحسوس: {'✅ روشن' if discreet_enabled else '❌ خاموش'}", callback_data='toggle_discreet_trade')],
            [InlineKeyboardButton(f"حداکثر تجارت روزانه: {max_trades}", callback_data='set_max_trades')],
            [InlineKeyboardButton(f"کانال اطلاع‌رسانی: {trade_channel}", callback_data='set_trade_channel')],
            [InlineKeyboardButton(f"کانال تجارت نامحسوس: {discreet_channel}", callback_data='set_discreet_trade_channel')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "⚙️ تنظیمات سیستم تجارت:\n"
            "در این بخش می‌توانید تنظیمات مربوط به سیستم تجارت را مدیریت کنید.",
            reply_markup=reply_markup
        )
        return ADMIN_TRADE_SETTINGS
    except Exception as e:
        logger.error(f"Error in trade_settings: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش تنظیمات تجارت")
        return ADMIN_MENU


async def toggle_trade_enabled(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_trade_setting('trade_enabled')
        new_status = '0' if current_status == '1' else '1'
        set_trade_setting('trade_enabled', new_status)

        status_text = "فعال" if new_status == '1' else "غیرفعال"
        await query.answer(f"وضعیت تجارت: {status_text}")
        return await trade_settings(update, context)
    except Exception as e:
        logger.error(f"Error in toggle_trade_enabled: {e}", exc_info=True)
        await query.answer("خطا در تغییر وضعیت تجارت", show_alert=True)
        return ADMIN_TRADE_SETTINGS


async def toggle_discreet_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_trade_setting('discreet_trade_enabled')
        new_status = '0' if current_status == '1' else '1'
        set_trade_setting('discreet_trade_enabled', new_status)

        status_text = "فعال" if new_status == '1' else "غیرفعال"
        await query.answer(f"تجارت نامحسوس {status_text} شد")
        return await trade_settings(update, context)
    except Exception as e:
        logger.error(f"Error in toggle_discreet_trade: {e}", exc_info=True)
        await query.answer("خطا در تغییر وضعیت تجارت نامحسوس", show_alert=True)
        return ADMIN_TRADE_SETTINGS


async def set_max_trades(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔢 لطفاً حداکثر تعداد تجارت مجاز روزانه برای هر کاربر را وارد کنید:"
    )
    return SET_MAX_TRADES


async def process_max_trades(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        max_trades = int(update.message.text)
        if max_trades <= 0:
            await update.message.reply_text("عدد باید بزرگتر از صفر باشد.")
            return SET_MAX_TRADES

        set_trade_setting('max_trades', str(max_trades))
        await update.message.reply_text(f"✅ حداکثر تجارت روزانه با موفقیت به {max_trades} تنظیم شد.")
        return await admin_panel(update, context)
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
        return SET_MAX_TRADES
    except Exception as e:
        logger.error(f"Error in process_max_trades: {e}", exc_info=True)
        await update.message.reply_text("خطا در ذخیره‌سازی تنظیمات")
        return SET_MAX_TRADES


async def set_trade_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['setting_channel_type'] = 'normal'

    await query.edit_message_text(
        "📣 لطفاً آیدی کانال را برای اطلاع‌رسانی تجارت‌ها وارد کنید (مثال: @channel_username):"
    )
    return SET_TRADE_CHANNEL


async def set_discreet_trade_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['setting_channel_type'] = 'discreet'

    await query.edit_message_text(
        "🔒 لطفاً آیدی کانال را برای تجارت‌های نامحسوس وارد کنید (مثال: @channel_username):"
    )
    return SET_TRADE_CHANNEL


async def process_trade_channel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        channel_id = update.message.text.strip()
        channel_type = context.user_data.get('setting_channel_type', 'normal')
        if channel_type == 'discreet':
            set_trade_setting('discreet_trade_channel', channel_id)
            await update.message.reply_text(f"✅ کانال تجارت نامحسوس با موفقیت به {channel_id} تنظیم شد.")
        else:
            set_trade_setting('trade_channel', channel_id)
            await update.message.reply_text(f"✅ کانال اطلاع‌رسانی تجارت با موفقیت به {channel_id} تنظیم شد.")
        context.user_data.pop('setting_channel_type', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_trade_channel: {e}", exc_info=True)
        await update.message.reply_text("خطا در ذخیره‌سازی تنظیمات")
        return SET_TRADE_CHANNEL


async def manage_notification_images(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = [
            [InlineKeyboardButton("تغییر دین", callback_data="set_religion_image")],
            [InlineKeyboardButton("ملی کردن اینترنت", callback_data="set_internet_on_image")],
            [InlineKeyboardButton("لغو ملی کردن اینترنت", callback_data="set_internet_off_image")],
            [InlineKeyboardButton("تجارت زمینی", callback_data="set_trade_land_image")],
            [InlineKeyboardButton("تجارت هوایی", callback_data="set_trade_air_image")],
            [InlineKeyboardButton("تجارت دریایی", callback_data="set_trade_sea_image")],
            [InlineKeyboardButton("حمله نظامی", callback_data="set_attack_image")],
            [InlineKeyboardButton("رزمایش زمینی", callback_data="set_exercise_land_image")],
            [InlineKeyboardButton("رزمایش دریایی", callback_data="set_exercise_sea_image")],
            [InlineKeyboardButton("رزمایش هوایی", callback_data="set_exercise_air_image")],
            [InlineKeyboardButton("حمله موشکی", callback_data="set_missile_attack_image")],
            [InlineKeyboardButton("ساخت فیلم", callback_data="set_film_image")],
            [InlineKeyboardButton("ساخت بازی", callback_data="set_game_image")],
            [InlineKeyboardButton("ساخت موسیقی", callback_data="set_music_image")],
            [InlineKeyboardButton("برترین نفت", callback_data="set_top_oil_image")],
            [InlineKeyboardButton("برترین رضایت", callback_data="set_top_satisfaction_image")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("انتخاب نوع اطلاعیه برای تنظیم عکس:", reply_markup=reply_markup)
        return MANAGE_NOTIFICATION_IMAGES
    except Exception as e:
        logger.error(f"Error in manage_notification_images: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی عکس اطلاعیه‌ها")
        return ADMIN_MENU


async def set_notification_image_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        event_type = query.data.replace("set_", "").replace("_image", "")
        context.user_data["notification_event_type"] = event_type

        await query.edit_message_text("لطفاً عکس جدید را برای این اطلاعیه ارسال کنید:")
        return GET_NOTIFICATION_IMAGE
    except Exception as e:
        logger.error(f"Error in set_notification_image_handler: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب نوع اطلاعیه")
        return MANAGE_NOTIFICATION_IMAGES


async def save_notification_image(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        if not update.message.photo:
            await update.message.reply_text("لطفاً یک عکس ارسال کنید.")
            return GET_NOTIFICATION_IMAGE

        event_type = context.user_data["notification_event_type"]
        photo_id = update.message.photo[-1].file_id

        set_notification_image(event_type, photo_id)
        await update.message.reply_text(f"✅ عکس برای اطلاعیه {event_type} با موفقیت ذخیره شد!")

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_notification_image: {e}", exc_info=True)
        await update.message.reply_text("خطا در ذخیره عکس")
        return GET_NOTIFICATION_IMAGE


async def random_prize_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"prize_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("💰 سرمایه", callback_data="prize_capital")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎁 منوی جایزه رندوم:\nلطفاً دسته‌بندی جایزه را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return RANDOM_PRIZE_MENU
    except Exception as e:
        logger.error(f"Error in random_prize_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی جایزه رندوم")
        return ADMIN_MENU


async def select_prize_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'prize_capital':
            context.user_data['prize_category'] = 'capital'
            await query.edit_message_text("💰 لطفاً مقدار سرمایه جایزه را وارد کنید:")
            return GET_PRIZE_QUANTITY

        category_key = query.data.replace("prize_category_", "")
        context.user_data['prize_category'] = category_key

        keyboard = []
        for item_key in get_dynamic_default_assets().get(category_key, {}).keys():
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"prize_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='random_prize_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"انتخاب آیتم جایزه از دسته‌بندی {category_display_name}:",
            reply_markup=reply_markup
        )
        return SELECT_PRIZE_CATEGORY
    except Exception as e:
        logger.error(f"Error in select_prize_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب دسته‌بندی")
        return RANDOM_PRIZE_MENU


async def select_prize_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("prize_item_", "")
        context.user_data['prize_item'] = item_key

        await query.edit_message_text(f"لطفاً مقدار {get_asset_display_name(item_key)} برای جایزه را وارد کنید:")
        return GET_PRIZE_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_prize_item: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب آیتم جایزه")
        return SELECT_PRIZE_CATEGORY


async def get_prize_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("مقدار باید بزرگتر از صفر باشد.")
            return GET_PRIZE_QUANTITY
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
        return GET_PRIZE_QUANTITY
    category = context.user_data.get('prize_category')
    item = context.user_data.get('prize_item', None)

    if category == 'capital':
        context.user_data['prize_item'] = 'capital'
        context.user_data['prize_quantity'] = quantity
    else:
        context.user_data['prize_quantity'] = quantity

    verification_code = ''.join(random.choices('0123456789', k=6))
    context.user_data['verification_code'] = verification_code

    prize_description = f"💰 سرمایه: {quantity:,}" if category == 'capital' else f"{get_asset_display_name(item)}: {quantity:,}"

    await update.message.reply_text(
        f"✅ جایزه تنظیم شد!\n"
        f"🔢 جزئیات جایزه: {prize_description}\n"
        f"🔐 کد تأیید: `{verification_code}`\n\n"
        "برای اجرای جایزه رندوم، کد تأیید را ارسال کنید.",
        parse_mode="Markdown"
    )

    return CONFIRM_RANDOM_PRIZE


async def confirm_random_prize(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    try:
        entered_code = update.message.text.strip()
        saved_code = context.user_data.get('verification_code')

        if entered_code != saved_code:
            await update.message.reply_text("❌ کد تأیید نامعتبر است. لطفاً دوباره تلاش کنید.")
            return CONFIRM_RANDOM_PRIZE

        category = context.user_data.get('prize_category')
        item = context.user_data.get('prize_item')
        quantity = context.user_data.get('prize_quantity')

        countries = get_all_countries()
        if not countries:
            await update.message.reply_text("❌ هیچ کشوری برای اهدای جایزه وجود ندارد.")
            return await admin_panel(update, context)

        winner_id, winner_name = random.choice(countries)
        winner_country = get_country(winner_id)

        if category == 'capital':
            new_capital = winner_country['capital'] + quantity
            update_country(winner_id, {'capital': new_capital})
            prize_description = f"💰 سرمایه: {quantity:,}"
        else:
            update_data = {
                category: {
                    item: winner_country.get(category, {}).get(item, 0) + quantity
                }
            }
            update_country(winner_id, update_data)
            prize_description = f"{get_asset_display_name(item)}: {quantity:,}"

        try:
            await context.bot.send_message(
                chat_id=winner_id,
                text=f"🎉 تبریک! شما برنده جایزه رندوم شدید!\n"
                     f"🎁 جایزه شما: {prize_description}\n"
                     f"از طرف مدیریت ربات جنگ جهانی"
            )
        except Exception as e:
            logger.error(f"خطا در ارسال پیام به برنده: {e}")

        try:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=f"🎉 اعلام برنده جایزه رندوم!\n\n"
                     f"🏆 برنده: {winner_name}\n"
                     f"🎁 جایزه: {prize_description}\n"
                     f"با آرزوی موفقیت برای همه کشورها!"
            )
        except Exception as e:
            logger.error(f"خطا در ارسال اطلاعیه به کانال: {e}")

        await update.message.reply_text(
            f"✅ جایزه با موفقیت به کشور {winner_name} اهدا شد!\n"
            f"🎁 جزئیات جایزه: {prize_description}"
        )

        keys_to_remove = ['prize_category', 'prize_item', 'prize_quantity', 'verification_code']
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in confirm_random_prize: {e}", exc_info=True)
        await update.message.reply_text("خطا در اجرای جایزه رندوم")
        return ADMIN_MENU


async def military_exercise(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    disabled_buttons = get_global_disabled_buttons()
    if 'military_exercise' in disabled_buttons:
        await query.answer("⛔ رزمایش نظامی موقتاً غیرفعال است!", show_alert=True)
        return COUNTRY_MANAGEMENT

    try:
        keyboard = [
            [InlineKeyboardButton("زمینی", callback_data='exercise_land')],
            [InlineKeyboardButton("دریایی", callback_data='exercise_sea')],
            [InlineKeyboardButton("هوایی", callback_data='exercise_air')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "نوع رزمایش را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return MILITARY_EXERCISE_TYPE
    except Exception as e:
        logger.error(f"Error in military_exercise: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی رزمایش")
        return COUNTRY_MANAGEMENT


async def select_exercise_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        exercise_type = query.data.replace('exercise_', '')
        context.user_data['exercise_type'] = exercise_type

        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("❌ کشور شما یافت نشد.")
            return MAIN_MENU

        category_map = {
            'land': 'land_troops',
            'sea': 'naval_troops',
            'air': 'air_troops'
        }
        category = category_map.get(exercise_type)
        if not category:
            await query.edit_message_text("❌ نوع رزمایش نامعتبر است.")
            return MILITARY_EXERCISE_TYPE

        forces = country.get(category, {})
        total_forces = sum(forces.values())
        if total_forces == 0:
            await query.edit_message_text(f"❌ شما نیروی {exercise_type}ی ندارید!")
            return COUNTRY_MANAGEMENT

        await query.edit_message_text("لطفاً کد 4 رقمی رزمایش را وارد کنید:")
        return GET_EXERCISE_CODE
    except Exception as e:
        logger.error(f"Error in select_exercise_type: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب نوع رزمایش")
        return MILITARY_EXERCISE_TYPE


async def get_exercise_code(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("❌ کشور شما یافت نشد.")
        return MAIN_MENU
    try:
        code = update.message.text
        if not code.isdigit() or len(code) != 4:
            await update.message.reply_text("کد باید 4 رقم باشد. لطفاً دوباره وارد کنید.")
            return GET_EXERCISE_CODE

        context.user_data['exercise_code'] = code

        exercise_type = context.user_data['exercise_type']
        category_map = {
            'land': 'land_troops',
            'sea': 'naval_troops',
            'air': 'air_troops'
        }
        category = category_map.get(exercise_type)
        forces = country.get(category, {})
        total_forces = sum(forces.values())

        success_rate = min(100, max(70, total_forces // 1000))
        success = random.randint(success_rate - 10, success_rate + 10)
        success = max(70, min(100, success))

        report = (
            f"رزمایش {exercise_type}ی توسط کشور {country['name']} با کد {code} انجام شد.\n\n"
            f"نیروهای شرکت کننده: {total_forces:,}\n"
            f"درصد موفقیت: {success}%\n\n"
        )

        if success >= 85:
            report += "✅ رزمایش با موفقیت عالی انجام شد. نیروها به خوبی آموزش دیدند و آمادگی نظامی افزایش یافت."
        elif success >= 75:
            report += "🟢 رزمایش با موفقیت انجام شد. نقاط قوت و ضعف شناسایی شدند."
        else:
            report += "🔴 رزمایش با موفقیت متوسطی انجام شد. نیاز به آموزش بیشتر نیروها احساس می‌شود."

        event_type = f"military_exercise_{exercise_type}"
        photo_id = get_notification_image(event_type)
        if photo_id:
            await context.bot.send_photo(
                chat_id=STATEMENT_CHANNEL,
                photo=photo_id,
                caption=report
            )
        else:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=report
            )

        await update.message.reply_text("✅ گزارش رزمایش در کانال منتشر شد.")

        keys_to_remove = ['exercise_type', 'exercise_code']
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_exercise_code: {e}", exc_info=True)
        await update.message.reply_text("خطا در پردازش رزمایش")
        return GET_EXERCISE_CODE


async def missile_attack_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    disabled_buttons = get_global_disabled_buttons()
    if 'missile_attack_menu' in disabled_buttons:
        await query.answer("⛔ حمله موشکی موقتاً غیرفعال است!", show_alert=True)
        return MAIN_MENU

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]
        if not other_countries:
            await query.edit_message_text("در حال حاضر هیچ کشور دیگری برای حمله وجود ندارد.")
            return MAIN_MENU
        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"missile_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🚀 لطفا کشوری را برای حمله موشکی انتخاب کنید:", reply_markup=reply_markup)
        return MISSILE_ATTACK_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in missile_attack_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return MAIN_MENU


async def select_missile_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_user_id = int(query.data.replace("missile_target_", ""))
        context.user_data['missile_target_id'] = target_user_id
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("❌ کشور مورد نظر برای حمله یافت نشد.")
            return await missile_attack_menu(update, context)
        context.user_data['missile_target_name'] = target_country['name']

        user_id = query.from_user.id
        country = get_country(user_id)
        rockets = dict(country.get('rockets', {}) or {})

        # افزودن آیتم‌هایی که در DB در دسته rockets هستند ولی به هر دلیل در country نیستند
        try:
            db_items = get_all_equipment_items()
            for it in db_items:
                if it['category'] == 'rockets' and it['item_key'] not in rockets:
                    rockets[it['item_key']] = country.get('rockets', {}).get(it['item_key'], 0)
        except Exception as e:
            logger.warning(f"خطا در همگام‌سازی موشک‌ها با DB: {e}")

        keyboard = []
        for rocket, count in rockets.items():
            if count and count > 0:
                display_name = get_asset_display_name(rocket)
                keyboard.append([InlineKeyboardButton(f"{display_name} (موجود: {count})", callback_data=f"select_missile_{rocket}")])

        if not keyboard:
            await query.edit_message_text(
                "❌ شما موشکی برای حمله ندارید!\n\n"
                "ℹ️ موشک‌ها باید در دسته‌بندی «موشک‌ها 🚀» (با کلید rockets) قرار داشته باشند.\n"
                "اگر ادمین موشک جدیدی اضافه کرده، مطمئن شوید آن را در دسته «موشک‌ها» ساخته است.\n"
                "سپس آن را از منوی «🛒 درخواست خرید» تهیه کنید."
            )
            return MAIN_MENU

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='missile_attack_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎯 هدف: *{target_country['name']}*\n\n"
            "🚀 لطفاً نوع موشک را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_SELECT_MISSILE
    except Exception as e:
        logger.error(f"Error in select_missile_target: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کشور هدف")
        return MISSILE_ATTACK_SELECT_TARGET


async def select_missile_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        missile_type = query.data.replace("select_missile_", "")
        context.user_data['missile_type'] = missile_type

        user_id = query.from_user.id
        country = get_country(user_id)
        missile_count = country.get('rockets', {}).get(missile_type, 0)

        await query.edit_message_text(
            f"شما {get_asset_display_name(missile_type)} را انتخاب کردید.\n"
            f"موجودی: {missile_count}\n"
            "لطفاً تعداد موشک‌های مورد نظر برای شلیک را وارد کنید:"
        )
        return MISSILE_ATTACK_GET_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_missile_type: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب نوع موشک")
        return MISSILE_ATTACK_SELECT_MISSILE


async def get_missile_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("❌ کشور شما یافت نشد.")
        return MAIN_MENU
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("تعداد باید بزرگتر از صفر باشد.")
            return MISSILE_ATTACK_GET_QUANTITY

        missile_type = context.user_data.get('missile_type')
        if not missile_type:
            await update.message.reply_text("خطا در نوع موشک. لطفاً دوباره تلاش کنید.")
            return MAIN_MENU

        available = country.get('rockets', {}).get(missile_type, 0)
        if available < quantity:
            await update.message.reply_text(f"تعداد موشک‌های شما کافی نیست! موجودی: {available}")
            return MISSILE_ATTACK_GET_QUANTITY

        context.user_data['missile_quantity'] = quantity

        target_name = context.user_data.get('missile_target_name')
        missile_name = get_asset_display_name(missile_type)

        # مرحله جدید: انتخاب منطقه هدف
        keyboard = [
            [InlineKeyboardButton("🏘️ منطقه مسکونی", callback_data='missile_zone_residential')],
            [InlineKeyboardButton("🪖 منطقه نظامی", callback_data='missile_zone_military')],
            [InlineKeyboardButton("🏭 منطقه اقتصادی", callback_data='missile_zone_economic')],
            [InlineKeyboardButton("❌ لغو", callback_data='missile_attack_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"🚀 *{quantity} موشک {missile_name}* به سمت *{target_name}*\n\n"
            "🎯 لطفاً *نوع منطقه هدف* را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_SELECT_ZONE
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید.")
        return MISSILE_ATTACK_GET_QUANTITY
    except Exception as e:
        logger.error(f"Error in get_missile_quantity: {e}", exc_info=True)
        await update.message.reply_text("خطا در پردازش تعداد موشک")
        return MISSILE_ATTACK_GET_QUANTITY


# --------- ثابت‌های منطقه ---------
MISSILE_ZONE_LABELS = {
    'residential': '🏘️ منطقه مسکونی',
    'military': '🪖 منطقه نظامی',
    'economic': '🏭 منطقه اقتصادی'
}


async def select_missile_zone(update: Update, context: CallbackContext) -> int:
    """انتخاب منطقه هدف موشک و نمایش پیش‌نمایش تأیید نهایی."""
    query = update.callback_query
    await query.answer()
    try:
        zone_key = query.data.replace("missile_zone_", "")
        if zone_key not in MISSILE_ZONE_LABELS:
            await query.answer("منطقه نامعتبر است", show_alert=True)
            return MISSILE_ATTACK_SELECT_ZONE
        context.user_data['missile_zone'] = zone_key

        target_name = context.user_data.get('missile_target_name', '')
        missile_type = context.user_data.get('missile_type')
        missile_name = get_asset_display_name(missile_type) if missile_type else ''
        quantity = context.user_data.get('missile_quantity', 0)
        zone_label = MISSILE_ZONE_LABELS[zone_key]

        keyboard = [
            [InlineKeyboardButton("✅ تأیید و شلیک", callback_data='confirm_missile_attack')],
            [InlineKeyboardButton("🔙 تغییر منطقه", callback_data='missile_change_zone')],
            [InlineKeyboardButton("❌ لغو", callback_data='missile_attack_menu')]
        ]
        await query.edit_message_text(
            f"🚀 *پیش‌نمایش حمله موشکی*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🎯 کشور هدف: *{target_name}*\n"
            f"💣 نوع موشک: *{missile_name}*\n"
            f"🔢 تعداد: *{quantity}*\n"
            f"🗺️ منطقه هدف: *{zone_label}*\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"آیا مطمئنید؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_CONFIRM
    except Exception as e:
        logger.error(f"Error in select_missile_zone: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب منطقه هدف.")
        return MAIN_MENU


# ==================== DRONE ATTACK FUNCTIONS ====================

async def drone_attack_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    disabled_buttons = get_global_disabled_buttons()
    if 'drone_attack_menu' in disabled_buttons:
        await query.answer("🛸 حمله پهپادی موقتاً غیرفعال است!", show_alert=True)
        return MAIN_MENU

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]

        if not other_countries:
            await query.edit_message_text("در حال حاضر هیچ کشوری برای حمله وجود ندارد.")
            return MAIN_MENU

        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"drone_target_{target_user_id}")])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("🛸 لطفاً کشوری را برای حمله پهپادی انتخاب کنید:", reply_markup=reply_markup)
        return DRONE_ATTACK_SELECT_TARGET

    except Exception as e:
        logger.error(f"Error in drone_attack_menu: {e}", exc_info=True)
        await query.edit_message_text("خطا در دریافت لیست کشورها")
        return MAIN_MENU


async def select_drone_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_user_id = int(query.data.replace("drone_target_", ""))
        context.user_data['drone_target_id'] = target_user_id

        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("❌ کشور یافت نشد.")
            return await drone_attack_menu(update, context)

        context.user_data['drone_target_name'] = target_country['name']
        user_id = query.from_user.id
        country = get_country(user_id)

        air_troops = dict(country.get('air_troops', {}) or {})

        keyboard = []
        for drone, count in air_troops.items():
            if count and count > 0:
                display_name = get_asset_display_name(drone)
                keyboard.append([InlineKeyboardButton(f"{display_name} (موجود: {count})", callback_data=f"select_drone_{drone}")])

        if not keyboard:
            await query.edit_message_text("شما هیچ پهپادی در اختیار ندارید.")
            return MAIN_MENU

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='drone_attack_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎯 هدف: *{target_country['name']}*\n\n"
            "🛸 لطفاً نوع پهپاد را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return DRONE_ATTACK_SELECT_DRONE

    except Exception as e:
        logger.error(f"Error in select_drone_target: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب کشور هدف")
        return DRONE_ATTACK_SELECT_TARGET


async def select_drone_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        drone_type = query.data.replace("select_drone_", "")
        context.user_data['drone_type'] = drone_type

        user_id = query.from_user.id
        country = get_country(user_id)
        drone_count = country.get('air_troops', {}).get(drone_type, 0)

        await query.edit_message_text(
            f"شما {get_asset_display_name(drone_type)} را انتخاب کردید.\n"
            f"موجودی: {drone_count}\n"
            "لطفاً تعداد پهپادهای مورد نظر برای شلیک را وارد کنید:"
        )
        return DRONE_ATTACK_GET_QUANTITY

    except Exception as e:
        logger.error(f"Error in select_drone_type: {e}", exc_info=True)
        return DRONE_ATTACK_SELECT_DRONE


async def get_drone_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)

    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("تعداد باید بزرگتر از صفر باشد.")
            return DRONE_ATTACK_GET_QUANTITY

        drone_type = context.user_data.get('drone_type')
        available = country.get('air_troops', {}).get(drone_type, 0)

        if available < quantity:
            await update.message.reply_text(f"تعداد پهپادهای شما کافی نیست! موجودی: {available}")
            return DRONE_ATTACK_GET_QUANTITY

        context.user_data['drone_quantity'] = quantity

        keyboard = [
            [InlineKeyboardButton("🏠 مسکونی", callback_data='drone_zone_residential')],
            [InlineKeyboardButton("⚔️ نظامی", callback_data='drone_zone_military')],
            [InlineKeyboardButton("💰 اقتصادی", callback_data='drone_zone_economic')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='drone_attack_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("لطفاً منطقه هدف را انتخاب کنید:", reply_markup=reply_markup)
        return DRONE_ATTACK_SELECT_ZONE

    except ValueError:
        await update.message.reply_text("لطفاً فقط عدد وارد کنید.")
        return DRONE_ATTACK_GET_QUANTITY


async def select_drone_zone(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        zone_key = query.data.replace("drone_zone_", "")
        context.user_data['drone_zone'] = zone_key

        target_name = context.user_data.get('drone_target_name', '')
        drone_type = context.user_data.get('drone_type')
        quantity = context.user_data.get('drone_quantity', 0)
        drone_name = get_asset_display_name(drone_type)

        keyboard = [
            [InlineKeyboardButton("✅ تأیید و شلیک", callback_data='confirm_drone_attack')],
            [InlineKeyboardButton("🔙 تغییر منطقه", callback_data='drone_attack_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🛸 *{quantity} {drone_name}* به سمت *{target_name}*\n"
            f"منطقه: {zone_key}\n\n"
            "آیا مطمئن هستید؟",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return DRONE_ATTACK_CONFIRM

    except Exception as e:
        logger.error(f"Error in select_drone_zone: {e}", exc_info=True)
        return MAIN_MENU


async def confirm_drone_attack(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        target_id = context.user_data.get('drone_target_id')
        target_country = get_country(target_id)
        drone_type = context.user_data.get('drone_type')
        quantity = context.user_data.get('drone_quantity')
        zone_key = context.user_data.get('drone_zone')

        if not all([country, target_country, drone_type, quantity, zone_key]):
            await query.edit_message_text("❌ اطلاعات ناقص است.")
            return MAIN_MENU

        used = calculate_storage_used(country)
        capacity = country.get('storage_capacity', 100)
        needed = quantity * 1

        if used + needed > capacity:
            await query.edit_message_text(f"ظرفیت انبار کافی نیست! ({used}/{capacity})")
            return MAIN_MENU

        current_count = country.get('air_troops', {}).get(drone_type, 0)
        if current_count < quantity:
            await query.edit_message_text("موجودی کافی نیست.")
            return MAIN_MENU

        new_air = dict(country.get('air_troops', {}))
        new_air[drone_type] = current_count - quantity
        update_country(user_id, {'air_troops': new_air})

        defenses = target_country.get('defenses', {})
        intercept_rate = 0
        for defense, count in defenses.items():
            rate = DRONE_INTERCEPT_RATES.get(defense, 0)
            intercept_rate += rate * count / 100
        intercept_rate = min(0.75, intercept_rate)

        intercepted = int(quantity * intercept_rate)
        effective = quantity - intercepted

        zone_effects = {
            'residential': {'population_mult': 1.0, 'financial_mult': 0.6, 'satisfaction_drop': 2},
            'military':    {'population_mult': 0.3, 'financial_mult': 0.8, 'security_drop': 3},
            'economic':    {'population_mult': 0.5, 'financial_mult': 1.5, 'satisfaction_drop': 1},
        }

        eff = zone_effects.get(zone_key, zone_effects['residential'])
        damage = DRONE_DAMAGE_RATES.get(drone_type, DRONE_DAMAGE_RATES['kamikaze_drone'])

        population_loss = int(target_country['population'] * effective * damage['population'] * eff['population_mult'])
        financial_damage = int(effective * damage['capital'] * eff['financial_mult'])

        new_population = max(0, target_country['population'] - population_loss)
        new_capital = max(0, target_country['capital'] - financial_damage)

        updates = {
            'population': new_population,
            'capital': new_capital
        }

        side_effects_text = ""
        if 'satisfaction_drop' in eff and effective > 0:
            current_sat = target_country.get('satisfaction', 0)
            new_sat = max(0, current_sat - eff['satisfaction_drop'])
            updates['satisfaction'] = new_sat
            side_effects_text += f"\n😡 افت رضایت: -{eff['satisfaction_drop']}%"

        if 'security_drop' in eff and effective > 0:
            current_sec = target_country.get('security', 0)
            new_sec = max(0, current_sec - eff['security_drop'])
            updates['security'] = new_sec
            side_effects_text += f"\n🛡️ افت امنیت: -{eff['security_drop']}%"

        update_country(target_id, updates)

        report = (
            f"🛸 *نتیجه حمله پهپادی به {target_country['name']}*\n"
            f"────────────────────\n"
            f"🛸 نوع پهپاد: {get_asset_display_name(drone_type)}\n"
            f"🔢 تعداد: {quantity}\n"
            f"🛡️ رهگیری شده: {intercepted}\n"
            f"🎯 مؤثر: {effective}\n"
            f"────────────────────\n"
            f"💀 تلفات جمعیتی: {population_loss:,}\n"
            f"💰 خسارت مالی: {financial_damage:,}"
            f"{side_effects_text}\n"
            f"────────────────────\n"
            f"جمعیت جدید: {new_population:,}\n"
            f"سرمایه جدید: {new_capital:,}"
        )

        await context.bot.send_message(chat_id=STATEMENT_CHANNEL, text=report, parse_mode="Markdown")
        await query.edit_message_text("✅ حمله پهپادی با موفقیت انجام شد!")

        for key in ['drone_target_id', 'drone_target_name', 'drone_type', 'drone_quantity', 'drone_zone']:
            context.user_data.pop(key, None)

        return MAIN_MENU

    except Exception as e:
        logger.error(f"Error in confirm_drone_attack: {e}", exc_info=True)
        await query.edit_message_text("خطا در انجام حمله.")
        return MAIN_MENU


async def missile_change_zone(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    target_name = context.user_data.get('missile_target_name', '')
    missile_type = context.user_data.get('missile_type')
    missile_name = get_asset_display_name(missile_type) if missile_type else ''
    quantity = context.user_data.get('missile_quantity', 0)

    keyboard = [
        [InlineKeyboardButton("🏠 منطقه مسکونی", callback_data='missile_zone_residential')],
        [InlineKeyboardButton("🪖 منطقه نظامی", callback_data='missile_zone_military')],
        [InlineKeyboardButton("🏭 منطقه اقتصادی", callback_data='missile_zone_economic')],
        [InlineKeyboardButton("❌ لغو", callback_data='missile_attack_menu')]
    ]

    await query.edit_message_text(
        f"🚀 *{quantity} موشک {missile_name}* به سمت *{target_name}*\n\n"
        "🎯 لطفاً *نوع منطقه هدف* را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return MISSILE_ATTACK_SELECT_ZONE


async def confirm_missile_attack(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        target_id = context.user_data.get('missile_target_id')
        target_country = get_country(target_id)
        missile_type = context.user_data.get('missile_type')
        quantity = context.user_data.get('missile_quantity')
        zone_key = context.user_data.get('missile_zone')

        if not country or not target_country or not missile_type or not quantity:
            await query.edit_message_text("❌ خطا در اطلاعات حمله. لطفاً دوباره تلاش کنید.")
            return MAIN_MENU

        if not zone_key or zone_key not in MISSILE_ZONE_LABELS:
            await query.edit_message_text("❌ ابتدا منطقه هدف را انتخاب کنید.")
            return MAIN_MENU

        current_count = country.get('rockets', {}).get(missile_type, 0)
        if current_count < quantity:
            await query.edit_message_text(f"❌ موجودی موشک کافی نیست!\nموجودی: {current_count} / درخواست: {quantity}")
            return MAIN_MENU

        new_rocket_count = current_count - quantity
        update_country(user_id, {'rockets': {missile_type: new_rocket_count}})

        delivery_minutes = random.randint(10, 30)
        delivery_time = (datetime.now() + timedelta(minutes=delivery_minutes)).isoformat()

        attack_id = str(uuid.uuid4())
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO attack_deliveries (proposal_id, delivery_time) VALUES (?, ?)", (attack_id, delivery_time))
        conn.commit()
        conn.close()

        context.user_data['missile_attack_id'] = attack_id

        missile_name = get_asset_display_name(missile_type)
        zone_label = MISSILE_ZONE_LABELS[zone_key]

        attack_message = (
            f"⚠️ *هشدار حمله موشکی!*\n"
            f"────────────────────\n"
            f"🚀 *از:* {country['name']}\n"
            f"🎯 *به:* {target_country['name']}\n"
            f"💣 *نوع موشک:* {missile_name}\n"
            f"🔢 *تعداد:* {quantity}\n"
            f"🗺️ *منطقه هدف:* {zone_label}\n"
            f"⏱ *زمان رسیدن:* {delivery_minutes} دقیقه دیگر"
        )

        missile_photo_id = get_notification_image('missile_attack')
        try:
            if missile_photo_id:
                await context.bot.send_photo(
                    chat_id=STATEMENT_CHANNEL,
                    photo=missile_photo_id,
                    caption=attack_message,
                    parse_mode="Markdown"
                )
            else:
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=attack_message,
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"Error sending missile attack message: {e}")

        await query.edit_message_text("✅ حمله موشکی با موفقیت ثبت شد!")

        for key in ['missile_target_id', 'missile_target_name', 'missile_type', 'missile_quantity', 'missile_zone']:
            context.user_data.pop(key, None)

        return MAIN_MENU

    except Exception as e:
        logger.error(f"Error in confirm_missile_attack: {e}", exc_info=True)
        await query.edit_message_text("خطا در انجام حمله.")
        return MAIN_MENU
    


async def castle_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    kb = [
        [InlineKeyboardButton("🌾 مزرعه", callback_data='farm_menu')],
        [InlineKeyboardButton("🏰 استحکامات قلعه", callback_data='fort_menu')],
        [InlineKeyboardButton("⚒️ کارگاه اسلحه‌سازی", callback_data='workshop_menu')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')],
    ]
    await q.edit_message_text(
        "🏰 مدیریت قلعه\n\n"
        "قلعه قلب کشوره! اینجا می‌تونی:\n"
        "🌾 مزرعه - تولید غلات برای سربازا\n"
        "🏰 استحکامات - دیوار و منجنیق برای دفاع\n"
        "⚒️ کارگاه - شمشیر و کمان برای ارتش",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return CASTLE_MENU

async def fort_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    c = get_country(uid)
    lvl = int(c.get('fort_level',0) or 0) if c else 0
    cur = FORT_LEVELS.get(lvl, {'name':'بی‌دفاع','security':0})
    kb = []
    nxt = lvl + 1
    if nxt in FORT_LEVELS:
        nxt_data = FORT_LEVELS[nxt]
        kb.append([InlineKeyboardButton(f"⬆️ ارتقا به {nxt_data['name']} - {nxt_data['cost']:,} 💰", callback_data='upgrade_fort')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='castle_menu')])
    text = f"🏰 استحکامات قلعه\n\nسطح فعلی: {lvl} - {cur.get('name','بی‌دفاع')}\nامنیت: +{cur.get('security',0)}\n{cur.get('desc','')}\n"
    if nxt in FORT_LEVELS:
        nxt_data = FORT_LEVELS[nxt]
        text += f"\nبعدی: {nxt} - {nxt_data['name']}\n{nxt_data['desc']}\nهزینه: {nxt_data['cost']:,}"
    else:
        text += "\n🏆 حداکثر استحکامات!"
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    return FORT_MENU

async def upgrade_fort(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    c = get_country(uid)
    lvl = int(c.get('fort_level',0) or 0)
    nxt = lvl + 1
    if nxt not in FORT_LEVELS:
        await q.answer("حداکثر!", show_alert=True)
        return await fort_menu(update, context)
    cost = FORT_LEVELS[nxt]['cost']
    if c['capital'] < cost:
        await q.answer(f"پول کافی نیست! {cost:,}", show_alert=True)
        return await fort_menu(update, context)
    new_cap = c['capital'] - cost
    new_sec = c.get('security',50) + FORT_LEVELS[nxt]['security'] - FORT_LEVELS.get(lvl,{}).get('security',0)
    update_country(uid, {'capital': new_cap, 'fort_level': nxt, 'security': min(100, new_sec)})
    await q.answer(f"✅ استحکامات به {FORT_LEVELS[nxt]['name']} ارتقا یافت!", show_alert=True)
    return await fort_menu(update, context)

async def workshop_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    c = get_country(uid)
    lvl = int(c.get('workshop_level',0) or 0)
    cur = get_workshop_level_config(lvl)
    cur_name = cur.get('name', 'ویرانه') if lvl>0 else 'ویرانه'
    soldier, amount = get_daily_workshop_production(lvl)
    soldier_name = get_asset_display_name(soldier) if soldier else "هیچ"
    kb = []
    nxt = lvl + 1
    if nxt in WORKSHOP_LEVELS or str(nxt) in get_workshop_config():
        nxt_cfg = get_workshop_level_config(nxt)
        nxt_soldier, nxt_amount = get_daily_workshop_production(nxt)
        nxt_soldier_name = get_asset_display_name(nxt_soldier) if nxt_soldier else "نامشخص"
        kb.append([InlineKeyboardButton(f"⬆️ ارتقا به لول {nxt} - {nxt_cfg.get('cost',0):,} 💰", callback_data='upgrade_workshop')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='castle_menu')])
    text = f"⚒️ کارگاه اسلحه‌سازی\n\nسطح فعلی: {lvl} - {cur_name}\n"
    if soldier and amount:
        text += f"تولید روزانه: {amount} × {soldier_name}\n"
    else:
        text += "تولید روزانه: هیچ\n"
    if nxt in WORKSHOP_LEVELS or str(nxt) in get_workshop_config():
        nxt_cfg = get_workshop_level_config(nxt)
        nxt_soldier, nxt_amount = get_daily_workshop_production(nxt)
        nxt_soldier_name = get_asset_display_name(nxt_soldier) if nxt_soldier else "نامشخص"
        text += f"\nبعدی: لول {nxt} - {nxt_cfg.get('name','')}\nتولید: {nxt_amount} × {nxt_soldier_name}\nهزینه: {nxt_cfg.get('cost',0):,}"
    else:
        text += "\n🏆 حداکثر سطح!"
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    return WORKSHOP_MENU

async def upgrade_workshop(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    c = get_country(uid)
    lvl = int(c.get('workshop_level',0) or 0)
    nxt = lvl + 1
    if nxt not in WORKSHOP_LEVELS:
        await q.answer("حداکثر!", show_alert=True)
        return await workshop_menu(update, context)
    cost = WORKSHOP_LEVELS[nxt]['cost']
    if c['capital'] < cost:
        await q.answer(f"پول کافی نیست! {cost:,}", show_alert=True)
        return await workshop_menu(update, context)
    new_cap = c['capital'] - cost
    update_country(uid, {'capital': new_cap, 'workshop_level': nxt})
    await q.answer(f"✅ کارگاه به {WORKSHOP_LEVELS[nxt]['name']} ارتقا یافت!", show_alert=True)
    return await workshop_menu(update, context)

async def farm_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        lvl = int(country.get('farm_level', 0) or 0)
        prod = get_farm_production(lvl)
        nxt = lvl + 1
        keyboard = []
        if nxt in FARM_LEVELS:
            cost = FARM_LEVELS[nxt]['cost']
            keyboard.append([InlineKeyboardButton(f"⬆️ ارتقا به لول {nxt} ({FARM_LEVELS[nxt]['name']}) - {cost:,} 💰", callback_data='upgrade_farm')])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='country_management')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"🌾 مزرعه - سطح فعلی: {lvl} ({FARM_LEVELS.get(lvl, {}).get('name','بدون مزرعه')})\nتولید روزانه: +{prod} غلات\n"
        if nxt in FARM_LEVELS:
            text += f"لول بعدی: {nxt} تولید +{FARM_LEVELS[nxt]['production']} هزینه {FARM_LEVELS[nxt]['cost']:,}"
        else:
            text += "🏆 حداکثر سطح!"
        await query.edit_message_text(text, reply_markup=reply_markup)
        return COUNTRY_MANAGEMENT
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"farm_menu: {e}")
        await query.edit_message_text("خطا در نمایش مزرعه")
        return COUNTRY_MANAGEMENT

async def upgrade_farm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        lvl = int(country.get('farm_level', 0) or 0)
        nxt = lvl + 1
        if nxt not in FARM_LEVELS:
            await query.answer("حداکثر سطح!", show_alert=True)
            return await farm_menu(update, context)
        cost = FARM_LEVELS[nxt]['cost']
        if country['capital'] < cost:
            await query.answer(f"سرمایه کافی نیست! {cost:,}", show_alert=True)
            return await farm_menu(update, context)
        new_cap = country['capital'] - cost
        update_country(user_id, {'capital': new_cap, 'farm_level': nxt})
        await query.answer(f"✅ مزرعه به لول {nxt} ارتقا یافت!", show_alert=True)
        return await farm_menu(update, context)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"upgrade_farm: {e}")
        await query.answer("خطا در ارتقا", show_alert=True)
        return COUNTRY_MANAGEMENT
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country.get('refinery_level', 0)
        daily_income = current_level * 25

        keyboard = [
            [InlineKeyboardButton("🌾 مزرعه", callback_data='farm_menu')],
            [InlineKeyboardButton(f"ارتقاء پالایشگاه (سطح فعلی: {current_level})", callback_data='upgrade_refinery')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🛢️ پالایشگاه نفت:\nسطح فعلی: {current_level}\nدرآمد روزانه: +{daily_income}\n\n"
            "هر سطح پالایشگاه 25 واحد به درآمد روزانه اضافه می‌کند.",
            reply_markup=reply_markup
        )
        return REFINERY_MENU
    except Exception as e:
        await query.edit_message_text("خطا در نمایش منوی پالایشگاه")
        return COUNTRY_MANAGEMENT


async def upgrade_refinery(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country.get('refinery_level', 0)

        if current_level >= 7:
            await query.answer("پالایشگاه شما در بالاترین سطح (7) است!", show_alert=True)
            return REFINERY_MENU

        next_level = current_level + 1
        price = ASSET_PRICES[f'refinery_upgrade_level{next_level}']

        if country['capital'] < price:
            await query.answer(f"سرمایه شما کافی نیست! قیمت ارتقاء: {price:,}", show_alert=True)
            return REFINERY_MENU

        new_capital = country['capital'] - price
        update_country(user_id, {
            'capital': new_capital,
            'refinery_level': next_level
        })

        upgrade_message = (
            f"🛢️ کشور {country['name']} پالایشگاه نفت خود را به سطح {next_level} ارتقاء داد!\n\n"
            f"💰 هزینه ارتقاء: {price:,}\n"
            f"💹 درآمد روزانه جدید: +{next_level * 25}"
        )

        refinery_photo_id = get_notification_image('refinery_upgrade')
        if refinery_photo_id:
            await context.bot.send_photo(
                chat_id=STATEMENT_CHANNEL,
                photo=refinery_photo_id,
                caption=upgrade_message
            )
        else:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=upgrade_message
            )

        await query.answer(f"✅ پالایشگاه به سطح {next_level} ارتقاء یافت!", show_alert=True)
    except Exception as e:
        logger.error(f"Error in upgrade_refinery: {e}", exc_info=True)
        await query.answer("خطا در ارتقاء پالایشگاه", show_alert=True)
        return REFINERY_MENU


async def construction_proposal_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = [
            [InlineKeyboardButton("🏰 قلعه", callback_data='construction_castle')],
            [InlineKeyboardButton("🛖 بازار", callback_data='construction_bazaar')],
            [InlineKeyboardButton("🕌 معبد", callback_data='construction_temple')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🏗️ لطفاً نوع پروژه ساخت و ساز را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_CATEGORY
    except Exception as e:
        logger.error(f"Error in construction_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش منوی ساخت و ساز")
        return MAIN_MENU


async def select_construction_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        category = query.data.replace('construction_', '')
        context.user_data['construction_category'] = category

        projects = CONSTRUCTION_PROJECTS.get(category, {})
        if not projects:
            await query.edit_message_text("❌ پروژه‌ای در این دسته‌بندی یافت نشد.")
            return CONSTRUCTION_CATEGORY

        keyboard = []
        for project_id, project in projects.items():
            keyboard.append([InlineKeyboardButton(
                f"{project['name']} - هزینه: {project['cost']:,}",
                callback_data=f"select_project_{project_id}"
            )])

        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='construction_proposal_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"پروژه‌های {category}:\nلطفاً پروژه مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_SELECT_PROJECT
    except Exception as e:
        logger.error(f"Error in select_construction_category: {e}", exc_info=True)
        await query.edit_message_text("خطا در نمایش پروژه‌ها")
        return CONSTRUCTION_CATEGORY


async def select_construction_project(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        project_id = query.data.replace("select_project_", "")
        category = context.user_data.get('construction_category')
        projects = CONSTRUCTION_PROJECTS.get(category, {})
        project = projects.get(project_id)

        if not project:
            await query.edit_message_text("❌ پروژه مورد نظر یافت نشد.")
            return CONSTRUCTION_SELECT_PROJECT

        context.user_data['construction_project'] = project

        keyboard = [
            [InlineKeyboardButton("✅ تأیید و ساخت", callback_data='confirm_construction')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f'construction_{category}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🏗️ پروژه: {project['name']}\n"
            f"📝 توضیحات: {project['description']}\n"
            f"💰 هزینه: {project['cost']:,}\n"
            f"💹 سود روزانه: {project['daily_income']:,}\n\n"
            "آیا مایل به ساخت این پروژه هستید؟",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_CONFIRM
    except Exception as e:
        logger.error(f"Error in select_construction_project: {e}", exc_info=True)
        await query.edit_message_text("خطا در انتخاب پروژه")
        return CONSTRUCTION_SELECT_PROJECT


async def confirm_construction(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        project = context.user_data.get('construction_project')
        category = context.user_data.get('construction_category')

        if not country or not project:
            await query.edit_message_text("❌ خطا در اطلاعات پروژه. لطفاً دوباره تلاش کنید.")
            return MAIN_MENU

        if country['capital'] < project['cost']:
            await query.answer(f"سرمایه شما کافی نیست! سرمایه مورد نیاز: {project['cost']:,}", show_alert=True)
            return CONSTRUCTION_CONFIRM

        new_capital = country['capital'] - project['cost']
        new_daily_income = country['daily_income'] + project['daily_income']

        update_country(user_id, {
            'capital': new_capital,
            'daily_income': new_daily_income
        })

        message_templates = {
            'castle': (
                f"🏰 قلعه‌ای جدید توسط کشور {country['name']} ساخته شد!\n\n"
                f"🏟 بنا: {project['name']}\n"
                f"📝 توضیحات: {project['description']}\n\n"
                f"💰 بودجه: {project['cost']:,}\n"
                f"💹 خراج روزانه: {project['daily_income']:,}"
            ),
            'bazaar': (
                f"🛖 بازاری جدید توسط کشور {country['name']} ساخته شد!\n\n"
                f"🏪 بنا: {project['name']}\n"
                f"📝 توضیحات: {project['description']}\n\n"
                f"💰 بودجه: {project['cost']:,}\n"
                f"💹 خراج روزانه: {project['daily_income']:,}"
            ),
            'temple': (
                f"🕌 معبدی جدید توسط کشور {country['name']} ساخته شد!\n\n"
                f"⛩ بنا: {project['name']}\n"
                f"📝 توضیحات: {project['description']}\n\n"
                f"💰 بودجه: {project['cost']:,}\n"
                f"💹 خراج روزانه: {project['daily_income']:,}"
            )
        }

        announcement = message_templates.get(category, "")
        if not announcement:
            announcement = (
                f"🏗️ یک پروژه جدید توسط کشور {country['name']} ساخته شد!\n\n"
                f"📌 نام: {project['name']}\n"
                f"📝 توضیحات: {project['description']}\n\n"
                f"💰 بودجه: {project['cost']:,}\n"
                f"💹 سود روزانه: {project['daily_income']:,}"
            )

        event_type = f"{category}_construction"
        photo_id = get_notification_image(event_type)
        if photo_id:
            await context.bot.send_photo(
                chat_id=STATEMENT_CHANNEL,
                photo=photo_id,
                caption=announcement
            )
        else:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=announcement
            )

        await query.edit_message_text(f"✅ پروژه {project['name']} با موفقیت ساخته شد!")
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in confirm_construction: {e}", exc_info=True)
        await query.edit_message_text("❌ خطا در ساخت پروژه")
        return CONSTRUCTION_CONFIRM


async def announce_top_oil(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer("⛔ نفت برای قبل 1600 حذف شده", show_alert=True)
    return ADMIN_MENU
    query = update.callback_query
    await query.answer()

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT name, oil_barrels FROM countries ORDER BY oil_barrels DESC LIMIT 5")
        top_countries = c.fetchall()
        conn.close()

        if not top_countries:
            await query.edit_message_text("هیچ کشوری برای نمایش وجود ندارد.")
            return ADMIN_MENU

        import html as _html
        header = "<b>🛢️ کشورهای برتر از نظر ذخایر نفتی:</b>\n"
        body = ""
        for i, (name, oil) in enumerate(top_countries, 1):
            safe_name = _html.escape(name)
            body += f"<blockquote>{i}. {safe_name}: {oil:,} بشکه</blockquote>\n"
        message = header + "\n" + body
        photo_id = get_notification_image('top_oil')
        if photo_id:
            await context.bot.send_photo(
                chat_id=STATEMENT_CHANNEL,
                photo=photo_id,
                caption=message,
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=message,
                parse_mode="HTML"
            )

        await query.edit_message_text("✅ لیست برترین‌های نفت در کانال اعلام شد.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in announce_top_oil: {e}", exc_info=True)
        await query.edit_message_text("خطا در اعلام برترین‌های نفت")
        return ADMIN_MENU


async def announce_top_satisfaction(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT name, satisfaction FROM countries ORDER BY satisfaction DESC LIMIT 5")
        top_countries = c.fetchall()
        conn.close()

        if not top_countries:
            await query.edit_message_text("هیچ کشوری برای نمایش وجود ندارد.")
            return ADMIN_MENU

        # خوشگل: تیتر بولد + خط خالی + هر کشور در نقل‌قول جدا
        import html as _html
        header = "<b>😊 کشورهای برتر از نظر رضایت مردمی:</b>\n"
        body = ""
        for i, (name, satisfaction) in enumerate(top_countries, 1):
            safe_name = _html.escape(name)
            body += f"<blockquote>{i}. {safe_name}: {satisfaction}%</blockquote>\n"
        message = header + "\n" + body
        photo_id = get_notification_image('top_satisfaction')
        if photo_id:
            await context.bot.send_photo(
                chat_id=STATEMENT_CHANNEL,
                photo=photo_id,
                caption=message,
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=message,
                parse_mode="HTML"
            )

        await query.edit_message_text("✅ لیست برترین‌های رضایت در کانال اعلام شد.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in announce_top_satisfaction: {e}", exc_info=True)
        await query.edit_message_text("خطا در اعلام برترین‌های رضایت")
        return ADMIN_MENU


# ========================== مدیریت پویای تجهیزات (UI) ==========================

async def equip_manage_entry(update: Update, context: CallbackContext) -> int:
    """ورودی پیامی: 'مدیریت تجهیزات' در پی‌وی."""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها/مالک دسترسی دارند!")
        return ConversationHandler.END
    return await show_equipment_manage_menu(update, context)


async def show_equipment_manage_menu(update: Update, context: CallbackContext) -> int:
    """نمایش لیست همه تجهیزات با آیدی + دکمه‌های افزودن/سیو/لیست‌ها."""
    items = get_all_equipment_items()
    cats = get_all_equipment_categories()
    cat_map = {c[0]: c[1] for c in cats}

    text_lines = ["🛠️ *مدیریت تجهیزات*\n"]
    if not items:
        text_lines.append("هیچ تجهیزی ثبت نشده است.")
    else:
        # گروه‌بندی بر اساس دسته
        by_cat = {}
        for it in items:
            by_cat.setdefault(it['category'], []).append(it)
        for cat_key, _disp in cats:
            if cat_key not in by_cat:
                continue
            cat_disp = cat_map.get(cat_key, cat_key)
            text_lines.append(f"\n*{cat_disp}*")
            for it in by_cat[cat_key]:
                text_lines.append(
                    f"`{it['item_id']}` • {it['display_name']} — قیمت: {it['price']:,}"
                )
        # آیتم‌هایی که دسته‌شون در جدول دسته‌ها نیست
        orphan_cats = [c for c in by_cat.keys() if c not in cat_map]
        for cat_key in orphan_cats:
            text_lines.append(f"\n*دسته نامشخص ({cat_key})*")
            for it in by_cat[cat_key]:
                text_lines.append(
                    f"`{it['item_id']}` • {it['display_name']} — قیمت: {it['price']:,}"
                )

    text_lines.append("\n\nبرای حذف، آیدی عددی تجهیز را ارسال کنید.")
    message_text = "\n".join(text_lines)

    keyboard = [
        [InlineKeyboardButton("➕ افزودن تجهیز", callback_data='equip_add_start')],
        [InlineKeyboardButton("💾 ذخیره (سیو) لیست", callback_data='equip_preset_save_start')],
        [InlineKeyboardButton("📂 لیست‌های ذخیره‌شده", callback_data='equip_preset_menu')],
        [InlineKeyboardButton("🆕 ساخت لیست جدید (پاکسازی)", callback_data='equip_new_list_start')],
        [InlineKeyboardButton("🗂️ مدیریت دسته‌بندی‌ها", callback_data='equip_category_menu')],
        [InlineKeyboardButton("❌ بستن", callback_data='equip_close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message_text, reply_markup=reply_markup, parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                message_text, reply_markup=reply_markup, parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Error in show_equipment_manage_menu: {e}", exc_info=True)
        # احتمال خطای طول پیام: ساده‌تر بفرست
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "🛠️ مدیریت تجهیزات\n\n(لیست خیلی طولانیه؛ از دکمه‌ها استفاده کنید)",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "🛠️ مدیریت تجهیزات\n\n(لیست خیلی طولانیه؛ از دکمه‌ها استفاده کنید)",
                reply_markup=reply_markup
            )
    return EQUIP_MANAGE_MENU


async def equip_delete_by_text(update: Update, context: CallbackContext) -> int:
    """حذف تجهیز با آیدی عددی (پیام متنی در حالت مدیریت)."""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔️ فقط ادمین‌ها دسترسی دارند!")
        return ConversationHandler.END
    text = (update.message.text or "").strip()
    if not text.isdigit():
        await update.message.reply_text(
            "❌ لطفاً فقط یک عدد (آیدی تجهیز) ارسال کنید. برای خروج از منو دکمه ❌ بستن را بزنید."
        )
        return EQUIP_MANAGE_MENU
    item_id = int(text)
    item = get_equipment_item_by_id(item_id)
    if not item:
        await update.message.reply_text(f"❌ تجهیزی با آیدی {item_id} یافت نشد.")
        return EQUIP_MANAGE_MENU
    ok = delete_equipment_item(item_id)
    if ok:
        await update.message.reply_text(
            f"✅ تجهیز «{item['display_name']}» (آیدی {item_id}) حذف شد."
        )
    else:
        await update.message.reply_text("❌ حذف انجام نشد.")
    return await show_equipment_manage_menu(update, context)


# ---- افزودن تجهیز ----

async def equip_add_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['equip_new'] = {}
    await query.edit_message_text(
        "➕ افزودن تجهیز جدید\n\n"
        "لطفاً *نام نمایشی* تجهیز را ارسال کنید (مثلاً: «تانک T-14»):",
        parse_mode="Markdown"
    )
    return EQUIP_ADD_GET_NAME


async def equip_add_get_name(update: Update, context: CallbackContext) -> int:
    name = (update.message.text or "").strip()
    if not name:
        await update.message.reply_text("❌ نام نمی‌تواند خالی باشد. دوباره ارسال کنید:")
        return EQUIP_ADD_GET_NAME
    context.user_data.setdefault('equip_new', {})['display_name'] = name
    await update.message.reply_text(
        f"✅ نام ثبت شد: {name}\n\n"
        "حالا *قیمت* (عدد صحیح، مثلاً 50000) را ارسال کنید:",
        parse_mode="Markdown"
    )
    return EQUIP_ADD_GET_PRICE


async def equip_add_get_price(update: Update, context: CallbackContext) -> int:
    text = (update.message.text or "").strip().replace(',', '')
    try:
        price = int(text)
        if price < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text("❌ قیمت باید یک عدد صحیح غیرمنفی باشد. دوباره ارسال کنید:")
        return EQUIP_ADD_GET_PRICE
    context.user_data.setdefault('equip_new', {})['price'] = price

    # نمایش دسته‌ها
    cats = get_all_equipment_categories()
    keyboard = []
    for cat_key, cat_disp in cats:
        keyboard.append([InlineKeyboardButton(cat_disp, callback_data=f"equip_pick_cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("➕ دسته‌بندی جدید", callback_data='equip_new_cat')])
    keyboard.append([InlineKeyboardButton("❌ لغو", callback_data='equip_back_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"✅ قیمت ثبت شد: {price:,}\n\n"
        "لطفاً *دسته‌بندی* تجهیز را انتخاب کنید:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return EQUIP_ADD_GET_CATEGORY


async def equip_pick_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    cat_key = query.data.replace("equip_pick_cat_", "")
    new_data = context.user_data.get('equip_new', {})
    display_name = new_data.get('display_name')
    price = new_data.get('price', 0)
    if not display_name:
        await query.edit_message_text("❌ خطا در داده‌ها. دوباره از منو شروع کنید.")
        return await show_equipment_manage_menu(update, context)

    # ساخت item_key یکتا از روی نام
    item_key = _make_unique_item_key(display_name)
    new_id = add_equipment_item(item_key, display_name, cat_key, price)
    if not new_id:
        await query.edit_message_text(
            f"❌ افزودن انجام نشد (احتمالاً کلید تکراری است: {item_key})."
        )
    else:
        await query.edit_message_text(
            f"✅ تجهیز جدید اضافه شد:\n"
            f"• آیدی: `{new_id}`\n"
            f"• نام: {display_name}\n"
            f"• کلید داخلی: `{item_key}`\n"
            f"• دسته: {cat_key}\n"
            f"• قیمت: {price:,}",
            parse_mode="Markdown"
        )
    context.user_data.pop('equip_new', None)
    return await show_equipment_manage_menu(update, context)


def _make_unique_item_key(display_name):
    """ساخت کلید یکتا از روی نام نمایشی (انگلیسی-سازی ساده + شمارنده)."""
    # برداشتن کاراکترهای غیرلاتین/غیر عددی
    base = re.sub(r'[^a-zA-Z0-9]+', '_', display_name).strip('_').lower()
    if not base:
        base = "item"
    candidate = base
    counter = 1
    existing = {it['item_key'] for it in get_all_equipment_items()}
    # همینطور باید با کلیدهای ثابت پیش‌فرض هم تداخل نداشته باشه
    existing |= set(ASSET_NAMES.keys())
    while candidate in existing:
        counter += 1
        candidate = f"{base}_{counter}"
    return candidate


async def equip_new_category_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "➕ افزودن دسته‌بندی جدید\n\n"
        "نام نمایشی دسته را ارسال کنید (مثلاً: «نیروهای فضایی 🚀»):"
    )
    return EQUIP_NEW_CATEGORY_NAME


async def equip_new_category_save(update: Update, context: CallbackContext) -> int:
    display_name = (update.message.text or "").strip()
    if not display_name:
        await update.message.reply_text("❌ نام خالی است. دوباره بفرستید:")
        return EQUIP_NEW_CATEGORY_NAME
    # ساخت cat_key یکتا
    base = re.sub(r'[^a-zA-Z0-9]+', '_', display_name).strip('_').lower()
    if not base:
        base = "cat"
    candidate = base
    counter = 1
    existing = {c[0] for c in get_all_equipment_categories()}
    while candidate in existing:
        counter += 1
        candidate = f"{base}_{counter}"
    ok = add_equipment_category(candidate, display_name)
    if ok:
        await update.message.reply_text(
            f"✅ دسته «{display_name}» اضافه شد (کلید: `{candidate}`)",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ افزودن دسته انجام نشد.")
    # برگشت به افزودن تجهیز یا منو
    if context.user_data.get('equip_new'):
        # کاربر در میانه افزودن تجهیز بود
        cats = get_all_equipment_categories()
        keyboard = []
        for cat_key, cat_disp in cats:
            keyboard.append([InlineKeyboardButton(cat_disp, callback_data=f"equip_pick_cat_{cat_key}")])
        keyboard.append([InlineKeyboardButton("➕ دسته‌بندی جدید", callback_data='equip_new_cat')])
        keyboard.append([InlineKeyboardButton("❌ لغو", callback_data='equip_back_menu')])
        await update.message.reply_text(
            "اکنون دسته تجهیز را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return EQUIP_ADD_GET_CATEGORY
    return await show_equipment_manage_menu(update, context)


# ---- منوی دسته‌بندی‌ها (مدیریت) ----

async def equip_category_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    cats = get_all_equipment_categories()
    text = "🗂️ *مدیریت دسته‌بندی‌ها*\n\nبرای حذف یک دسته، روی آن کلیک کنید (تمام تجهیزات آن دسته نیز حذف می‌شوند):"
    keyboard = []
    for cat_key, cat_disp in cats:
        keyboard.append([InlineKeyboardButton(f"🗑️ {cat_disp}", callback_data=f"equip_del_cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("➕ افزودن دسته‌بندی جدید", callback_data='equip_new_cat')])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='equip_back_menu')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_delete_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    cat_key = query.data.replace("equip_del_cat_", "")
    delete_equipment_category(cat_key)
    await query.answer(f"دسته «{cat_key}» حذف شد", show_alert=True)
    return await show_equipment_manage_menu(update, context)


# ---- پریست‌ها ----

async def equip_preset_save_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💾 *ذخیره لیست تجهیزات*\n\n"
        "یک نام برای این لیست انتخاب کنید (مثلاً: «جنگ جهانی 2»):",
        parse_mode="Markdown"
    )
    return EQUIP_PRESET_SAVE_NAME


async def equip_preset_save(update: Update, context: CallbackContext) -> int:
    name = (update.message.text or "").strip()
    if not name:
        await update.message.reply_text("❌ نام خالی است. دوباره بفرستید:")
        return EQUIP_PRESET_SAVE_NAME
    ok = save_equipment_preset(name)
    if ok:
        await update.message.reply_text(f"✅ لیست با نام «{name}» ذخیره شد.")
    else:
        await update.message.reply_text("❌ ذخیره‌سازی انجام نشد.")
    return await show_equipment_manage_menu(update, context)


async def equip_preset_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    presets = get_all_equipment_presets()
    text = "📂 *لیست‌های ذخیره‌شده تجهیزات*\n\n"
    if not presets:
        text += "هیچ لیست ذخیره‌شده‌ای ندارید."
    else:
        for p in presets:
            text += f"• `{p['preset_id']}` — {p['preset_name']}\n"
        text += "\nبرای بارگذاری یا حذف، روی نام کلیک کنید."
    keyboard = []
    for p in presets:
        keyboard.append([
            InlineKeyboardButton(f"📥 {p['preset_name']}", callback_data=f"equip_preset_load_{p['preset_id']}"),
            InlineKeyboardButton("🗑️", callback_data=f"equip_preset_del_{p['preset_id']}")
        ])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='equip_back_menu')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_preset_delete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = int(query.data.replace("equip_preset_del_", ""))
    delete_equipment_preset(preset_id)
    await query.answer("لیست حذف شد", show_alert=True)
    return await equip_preset_menu(update, context)


async def equip_preset_load_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = int(query.data.replace("equip_preset_load_", ""))
    preset = get_equipment_preset(preset_id)
    if not preset:
        await query.edit_message_text("❌ لیست یافت نشد.")
        return await show_equipment_manage_menu(update, context)
    context.user_data['preset_to_load'] = preset_id
    text = (
        f"📥 بارگذاری لیست: *{preset['preset_name']}*\n\n"
        f"تعداد دسته‌ها: {len(preset['data'].get('categories', []))}\n"
        f"تعداد تجهیزات: {len(preset['data'].get('items', []))}\n\n"
        "موجودی تجهیزات کشورهای موجود چه شود؟"
    )
    keyboard = [
        [InlineKeyboardButton("✅ موجودی فعلی حفظ شود", callback_data='equip_preset_load_keep')],
        [InlineKeyboardButton("🔄 موجودی همه کشورها صفر شود", callback_data='equip_preset_load_reset')],
        [InlineKeyboardButton("❌ لغو", callback_data='equip_preset_menu')]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_PRESET_LOAD_CONFIRM


async def equip_preset_load_apply(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = context.user_data.get('preset_to_load')
    if not preset_id:
        await query.edit_message_text("❌ خطا: لیستی برای بارگذاری انتخاب نشده است.")
        return await show_equipment_manage_menu(update, context)
    reset = query.data == 'equip_preset_load_reset'
    ok = load_equipment_preset(preset_id, reset_countries_inventory=reset)
    context.user_data.pop('preset_to_load', None)
    if ok:
        msg = "✅ لیست با موفقیت بارگذاری شد."
        if reset:
            msg += "\n🔄 موجودی تجهیزات همه کشورها صفر شد."
        else:
            msg += "\n💾 موجودی فعلی کشورها حفظ شد."
        await query.edit_message_text(msg)
    else:
        await query.edit_message_text("❌ بارگذاری انجام نشد.")
    return await show_equipment_manage_menu(update, context)


# ---- ساخت لیست جدید (پاکسازی) ----

async def equip_new_list_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = (
        "🆕 *ساخت لیست جدید*\n\n"
        "این عمل تمام تجهیزات و دسته‌بندی‌های فعلی را حذف می‌کند.\n"
        "موجودی تجهیزات کشورها چه شود؟"
    )
    keyboard = [
        [InlineKeyboardButton("✅ موجودی فعلی حفظ شود", callback_data='equip_new_list_keep')],
        [InlineKeyboardButton("🔄 موجودی همه کشورها صفر شود", callback_data='equip_new_list_reset')],
        [InlineKeyboardButton("❌ لغو", callback_data='equip_back_menu')]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_new_list_apply(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    reset = query.data == 'equip_new_list_reset'

    # پاک کردن همه دسته‌ها و آیتم‌ها
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM equipment_items")
    c.execute("DELETE FROM equipment_categories")
    conn.commit()
    conn.close()

    if reset:
        _reset_countries_inventory_to_new_schema()

    msg = "✅ لیست جدید ایجاد شد (همه تجهیزات و دسته‌ها پاک شدند)."
    if reset:
        msg += "\n🔄 موجودی تجهیزات همه کشورها صفر شد."
    else:
        msg += "\n💾 موجودی فعلی کشورها حفظ شد."
    await query.edit_message_text(msg)
    return await show_equipment_manage_menu(update, context)


# ---- بستن منو ----

async def equip_close(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text("✅ منوی مدیریت تجهیزات بسته شد.")
    except Exception:
        pass
    # پاکسازی state موقت
    context.user_data.pop('equip_new', None)
    context.user_data.pop('preset_to_load', None)
    return ConversationHandler.END


async def equip_back_menu(update: Update, context: CallbackContext) -> int:
    return await show_equipment_manage_menu(update, context)


# ============================== مدیریت گپ‌های فعال ==============================

async def activate_chat_handler(update: Update, context: CallbackContext) -> int:
    """با تایپ «اکتویت» توسط ادمین در گپ، آن گپ را به لیست گپ‌های فعال اضافه می‌کند."""
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id
    if not is_admin(user_id):
        # کاربر عادی نمی‌تونه اکتویت کنه
        return ConversationHandler.END
    if is_chat_active(chat.id):
        await update.message.reply_text(
            f"ℹ️ این گپ قبلاً فعال شده است.\n"
            f"🆔 شناسه گپ: `{chat.id}`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    activate_chat(chat.id, chat.title or "بدون عنوان", user_id)
    await update.message.reply_text(
        f"✅ این گپ با موفقیت برای پلیرها فعال شد.\n"
        f"🆔 شناسه گپ: `{chat.id}`\n\n"
        "از این به بعد، پلیرها می‌توانند با /start یا «منو» در همین گپ به ربات دسترسی داشته باشند.\n"
        "برای غیرفعال‌سازی، کلمه «دیاکتویت» را ارسال کنید.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def deactivate_chat_handler(update: Update, context: CallbackContext) -> int:
    """با تایپ «دیاکتویت» توسط ادمین در گپ، آن گپ از لیست خارج می‌شود."""
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return ConversationHandler.END
    if not is_chat_active(chat.id):
        await update.message.reply_text("ℹ️ این گپ از قبل فعال نبوده است.")
        return ConversationHandler.END
    deactivate_chat(chat.id)
    await update.message.reply_text("✅ این گپ از حالت فعال خارج شد. پلیرها دیگر در این گپ به ربات دسترسی ندارند.")
    return ConversationHandler.END


async def menu_in_group_handler(update: Update, context: CallbackContext) -> int:
    """با تایپ «منو» در گپ:
       - اگر ادمین: پنل ادمین در همان گپ
       - اگر پلیر و گپ فعال: منوی اصلی پلیر
       - در غیر این صورت سکوت
    """
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id
    if is_admin(user_id):
        country_data = get_country(user_id)
        if not country_data:
            return await admin_panel(update, context)
        return await show_main_menu(update, context)
    if not is_chat_active(chat.id):
        # گپ فعال نیست، پاسخ ندیم
        return ConversationHandler.END
    country_data = get_country(user_id)
    if not country_data:
        await update.message.reply_text(
            "⚠️ شما هنوز کشور خود را ثبت نکرده‌اید!\nلطفاً آیدی عددی خود را به مالک ربات ارسال کنید."
        )
        return ConversationHandler.END
    return await show_main_menu(update, context)


async def set_country_by_chat(update: Update, context: CallbackContext) -> int:
    """(?:تنظیم|افزودن) کشور آمریکا -> این گپ بشه آمریکا (user_id = chat_id)"""
    try:
        logger.info(f"set_country_by_chat triggered: text={update.message.text if update.message else None} chat={update.effective_chat.id if update.effective_chat else None} user={update.effective_user.id if update.effective_user else None}")
    except: pass
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        try: logger.info(f"not group type={chat.type}")
        except: pass
        return ConversationHandler.END
    user_id = update.effective_user.id if update.effective_user else None
    _is_admin = is_admin(user_id)
    try: logger.info(f"is_admin check {user_id} -> {_is_admin}")
    except: pass
    if not _is_admin:
        try:
            await update.message.reply_text("⛔ فقط ادمین می‌تواند کشور را تنظیم کند.")
        except: pass
        return ConversationHandler.END
    import re
    m = re.match(r"^\s*(?:تنظیم|افزودن) کشور\s+(.+?)\s*$", update.message.text or "")
    if not m:
        return ConversationHandler.END
    country_name = m.group(1).strip()
    if not country_name or len(country_name) > 30:
        await update.message.reply_text("❌ اسم کشور نامعتبر است (۱ تا ۳۰ کاراکتر).")
        return ConversationHandler.END
    chat_id = chat.id
    existing = get_country(chat_id)
    try:
        if existing:
            # آپدیت اسم
            update_country(chat_id, {"name": country_name})
            await update.message.reply_text(f"✅ اسم کشور این گپ به «{country_name}» تغییر کرد.\n🆔 {chat_id}")
        else:
            create_country(chat_id, country_name)
            await update.message.reply_text(f"✅ این گپ به کشور «{country_name}» تبدیل شد!\n🆔 {chat_id}")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"set_country_by_chat: {e}", exc_info=True)
        await update.message.reply_text("❌ خطا در (?:تنظیم|افزودن) کشور.")
    return ConversationHandler.END

async def delete_country_by_chat(update: Update, context: CallbackContext) -> int:
    """حذف کشور -> گپ پاک شه"""
    try:
        logger.info(f"delete_country_by_chat triggered: {update.message.text if update.message else None} chat={update.effective_chat.id if update.effective_chat else None}")
    except: pass
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id if update.effective_user else None
    if not is_admin(user_id):
        try:
            await update.message.reply_text("⛔ فقط ادمین می‌تواند حذف کند.")
        except: pass
        return ConversationHandler.END
    chat_id = chat.id
    country = get_country(chat_id)
    if not country:
        await update.message.reply_text("ℹ️ این گپ کشوری ندارد.")
        return ConversationHandler.END
    try:
        delete_country(chat_id)
        await update.message.reply_text(f"🗑 کشور «{country['name']}» حذف شد. این گپ دیگر کشوری ندارد.")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"delete_country_by_chat: {e}", exc_info=True)
        await update.message.reply_text("❌ خطا در حذف.")
    return ConversationHandler.END


async def add_force_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        await query.answer("دسترسی ندارید", show_alert=True)
        return ADMIN_MENU
    await query.edit_message_text("➕ افزودن نیروی جدید\n\nنام نیرو را وارد کنید (مثلاً: نیزه‌دار زره‌پوش):")
    return ADD_FORCE_NAME

async def add_force_get_name(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ فقط ادمین")
        return ADMIN_MENU
    name = (update.message.text or "").strip()
    if not name or len(name) > 30:
        await update.message.reply_text("❌ اسم نامعتبر (۱-۳۰ کاراکتر)، دوباره:")
        return ADD_FORCE_NAME
    context.user_data['new_force_name'] = name
    await update.message.reply_text(f"✅ نام: {name}\n\nقیمت را وارد کنید (عدد، مثلاً 15000):")
    return ADD_FORCE_PRICE

async def add_force_get_price(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    try:
        price = int((update.message.text or "").strip().replace(",", ""))
        if price < 0:
            raise ValueError
    except:
        await update.message.reply_text("❌ قیمت باید عدد مثبت باشد، دوباره:")
        return ADD_FORCE_PRICE
    context.user_data['new_force_price'] = price
    await update.message.reply_text(f"✅ قیمت: {price:,}\n\nمصرف روزانه غلات را وارد کنید (مثلاً 2):")
    return ADD_FORCE_GRAIN

async def add_force_get_grain(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    try:
        grain = int((update.message.text or "").strip())
        if grain < 0 or grain > 100:
            raise ValueError
    except:
        await update.message.reply_text("❌ مصرف باید 0 تا 100 باشد، دوباره:")
        return ADD_FORCE_GRAIN
    name = context.user_data.get('new_force_name')
    price = context.user_data.get('new_force_price')
    if not name or price is None:
        await update.message.reply_text("❌ خطا، دوباره از پنل شروع کنید.")
        return ADMIN_MENU
    # ساخت کلید یکتا
    import re as _re
    base = _re.sub(r'[^a-zA-Z0-9]+', '_', name).strip('_').lower()
    if not base:
        base = "force"
    candidate = base
    counter = 1
    existing = {it['item_key'] for it in get_all_equipment_items()}
    existing |= set(ASSET_NAMES.keys())
    existing |= set(GRAIN_CONSUMPTION_RATES.keys())
    while candidate in existing:
        counter += 1
        candidate = f"{base}_{counter}"
    # افزودن به تجهیزات (دسته land_troops)
    new_id = add_equipment_item(candidate, name, 'land_troops', price)
    if not new_id:
        await update.message.reply_text(f"❌ افزودن انجام نشد (کلید تکراری {candidate})")
        return ADMIN_MENU
    set_custom_grain_rate(candidate, grain)
    # همچنین به DEFAULT_ASSETS اضافه می‌شود خودکار via DB
    await update.message.reply_text(
        f"✅ نیروی جدید اضافه شد:\n"
        f"• آیدی: {new_id}\n"
        f"• نام: {name}\n"
        f"• کلید: {candidate}\n"
        f"• قیمت: {price:,}\n"
        f"• مصرف غلات: {grain}/روز\n"
        f"• دسته: land_troops"
    )
    for k in ['new_force_name','new_force_price']:
        context.user_data.pop(k, None)
    return ADMIN_MENU


async def siege_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    country = get_country(user_id)
    if not country:
        await query.edit_message_text("❌ کشور شما یافت نشد.")
        return MAIN_MENU
    countries = get_all_countries()
    others = [(uid,name) for uid,name in countries if uid != user_id]
    if not others:
        await query.edit_message_text("هیچ کشوری برای محاصره وجود ندارد.")
        return MAIN_MENU
    keyboard = []
    for tid, tname in others:
        keyboard.append([InlineKeyboardButton(tname, callback_data=f"siege_target_{tid}")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')])
    await query.edit_message_text("🏰 چه کسی را محاصره می‌کنی؟", reply_markup=InlineKeyboardMarkup(keyboard))
    return SIEGE_SELECT_TARGET

async def siege_select_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_id = int(query.data.replace("siege_target_", ""))
        target = get_country(target_id)
        if not target:
            await query.edit_message_text("❌ کشور هدف یافت نشد.")
            return MAIN_MENU
        attacker = get_country(query.from_user.id)
        keyboard = [
            [InlineKeyboardButton("✅ تایید محاصره", callback_data=f"siege_confirm_{target_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='siege_menu')]
        ]
        await query.edit_message_text(
            f"🏰 محاصره «{target['name']}» توسط «{attacker['name']}»\n\nآیا مطمئنی؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SIEGE_CONFIRM
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"siege_select: {e}")
        await query.edit_message_text("خطا")
        return MAIN_MENU

async def siege_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_id = int(query.data.replace("siege_confirm_", ""))
        attacker_id = query.from_user.id
        attacker = get_country(attacker_id)
        target = get_country(target_id)
        if not attacker or not target:
            await query.edit_message_text("❌ اطلاعات ناقص")
            return MAIN_MENU
        import uuid as _uuid, sqlite3 as _sql
        from datetime import datetime as _dt
        siege_id = str(_uuid.uuid4())[:8]
        conn = _sql.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO sieges (siege_id, besieger_id, besieger_name, target_id, target_name, status, created_at) VALUES (?,?,?,?,?,?,?)",
                  (siege_id, attacker_id, attacker['name'], target_id, target['name'], 'active', _dt.now().isoformat()))
        c.execute("INSERT INTO siege_participants (siege_id, user_id, joined_at) VALUES (?,?,?)",
                  (siege_id, attacker_id, _dt.now().isoformat()))
        conn.commit()
        conn.close()
        # پیام به چنل جنگ
        keyboard = [
            [InlineKeyboardButton("🏳️ بازگشت به مبدا", callback_data=f"siege_return_{siege_id}")],
            [InlineKeyboardButton("🏰 محاصره", callback_data=f"siege_join_{siege_id}")]
        ]
        text = f"🏰 محاصره!\n\n⚔️ «{attacker['name']}» کشور «{target['name']}» را محاصره کرد!\n🆔 محاصره: {siege_id}"
        sent = False
        for cid in [REPORTS_CHANNEL, REPORTS_CHANNEL_RAW if 'REPORTS_CHANNEL_RAW' in globals() else None, STATEMENT_CHANNEL, WAR_CHANNEL]:
            if not cid:
                continue
            try:
                await context.bot.send_message(chat_id=cid, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
                sent = True
                break
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"send siege to {cid} failed: {e}")
                continue
        if not sent:
            try:
                for aid in get_all_admins():
                    await context.bot.send_message(chat_id=aid, text=f"⚠️ محاصره ثبت شد ولی چنل گزارش یافت نشد:\n{text}")
            except: pass
        await query.edit_message_text(f"✅ محاصره «{target['name']}» آغاز شد! خبر به چنل رفت.")
        return MAIN_MENU
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"siege_confirm: {e}", exc_info=True)
        await query.edit_message_text("❌ خطا در محاصره")
        return MAIN_MENU

async def siege_callback_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        data = query.data
        user_id = query.from_user.id
        import sqlite3 as _sql
        from datetime import datetime as _dt
        if data.startswith("siege_return_"):
            siege_id = data.replace("siege_return_", "")
            conn = _sql.connect(DATABASE_NAME)
            c = conn.cursor()
            c.execute("SELECT besieger_id, besieger_name, target_name, status FROM sieges WHERE siege_id=?", (siege_id,))
            row = c.fetchone()
            if not row:
                await query.answer("محاصره یافت نشد", show_alert=True)
                conn.close()
                return MAIN_MENU
            besieger_id, besieger_name, target_name, status = row
            if status != 'active':
                await query.answer("این محاصره قبلا تمام شده", show_alert=True)
                conn.close()
                return MAIN_MENU
            if user_id != besieger_id:
                await query.answer("⛔ فقط محاصره‌کننده می‌تواند بازگشت بزند!", show_alert=True)
                conn.close()
                return MAIN_MENU
            c.execute("UPDATE sieges SET status='returned' WHERE siege_id=?", (siege_id,))
            conn.commit()
            conn.close()
            try:
                await query.edit_message_text(f"🏳️ «{besieger_name}» محاصره «{target_name}» را شکست و به مبدا بازگشت!\n🆔 {siege_id}")
            except: 
                await context.bot.send_message(chat_id=query.message.chat_id, text=f"🏳️ بازگشت به مبدا انجام شد - {siege_id}")
            return MAIN_MENU
        elif data.startswith("siege_join_"):
            siege_id = data.replace("siege_join_", "")
            conn = _sql.connect(DATABASE_NAME)
            c = conn.cursor()
            c.execute("SELECT besieger_id, target_name, status FROM sieges WHERE siege_id=?", (siege_id,))
            row = c.fetchone()
            if not row:
                await query.answer("محاصره یافت نشد", show_alert=True)
                conn.close()
                return MAIN_MENU
            besieger_id, target_name, status = row
            if status != 'active':
                await query.answer("محاصره تمام شده", show_alert=True)
                conn.close()
                return MAIN_MENU
            if user_id == besieger_id:
                await query.answer("تو خودت محاصره‌کننده‌ای!", show_alert=True)
                conn.close()
                return MAIN_MENU
            c.execute("SELECT 1 FROM siege_participants WHERE siege_id=? AND user_id=?", (siege_id, user_id))
            if c.fetchone():
                await query.answer("قبلا ملحق شدی!", show_alert=True)
                conn.close()
                return MAIN_MENU
            user_country = get_country(user_id)
            name = user_country['name'] if user_country else str(user_id)
            c.execute("INSERT INTO siege_participants (siege_id, user_id, joined_at) VALUES (?,?,?)", (siege_id, user_id, _dt.now().isoformat()))
            conn.commit()
            conn.close()
            await query.answer(f"✅ به محاصره «{target_name}» پیوستی!", show_alert=True)
            try:
                await context.bot.send_message(chat_id=REPORTS_CHANNEL, text=f"🏰 «{name}» به محاصره «{target_name}» پیوست! (🆔 {siege_id})")
            except: pass
            return MAIN_MENU
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"siege_callback: {e}", exc_info=True)
        await query.answer("خطا", show_alert=True)
    return MAIN_MENU


async def id_command(update: Update, context: CallbackContext):
    # /id - اگر ریپلای باشه آیدی اون طرف، وگرنه آیدی خودت
    try:
        if update.message and update.message.reply_to_message and update.message.reply_to_message.from_user:
            target = update.message.reply_to_message.from_user
            await update.message.reply_text(str(target.id))
        elif update.effective_user:
            await update.message.reply_text(str(update.effective_user.id))
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"id_command: {e}")

async def set_owner_by_chat(update: Update, context: CallbackContext):
    if not update.message or not update.effective_chat:
        return
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return
    user_id = update.effective_user.id if update.effective_user else None
    if not is_admin(user_id):
        try:
            await update.message.reply_text("⛔ فقط ادمین")
        except: pass
        return
    import re, sqlite3 as _sql
    m = re.match(r"^\s*تنظیم صاحب\s+(\d+)\s*$", update.message.text or "")
    if not m:
        # also handle typo تنیم
        m = re.match(r"^\s*تنیم صاحب\s+(\d+)\s*$", update.message.text or "")
        if not m:
            return
    new_owner = int(m.group(1))
    chat_id = chat.id
    country = get_country(chat_id)
    if not country:
        try:
            await update.message.reply_text("ℹ️ این گپ کشوری ندارد. اول «افزودن کشور بخارا» بزن.")
        except: pass
        return
    # انتقال مالکیت: user_id را عوض کن
    try:
        conn = _sql.connect(DATABASE_NAME)
        c = conn.cursor()
        # چک تکراری
        c.execute("SELECT 1 FROM countries WHERE user_id=?", (new_owner,))
        if c.fetchone():
            await update.message.reply_text("❌ این آیدی قبلاً صاحب کشور دیگری است. اول آن کشور را حذف کن.")
            conn.close()
            return
        # آپدیت PK
        c.execute("UPDATE countries SET user_id=? WHERE user_id=?", (new_owner, chat_id))
        # اگر owner_id ستون وجود داشت هم آپدیت کن (برای سازگاری)
        try:
            c.execute("SELECT owner_id FROM countries LIMIT 1")
            c.execute("UPDATE countries SET owner_id=? WHERE user_id=?", (new_owner, new_owner))
        except: pass
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ صاحب کشور «{country['name']}» به {new_owner} تغییر کرد.")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"set_owner: {e}", exc_info=True)
        try:
            await update.message.reply_text("❌ خطا در تنظیم صاحب.")
        except: pass


async def workshop_cfg_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.answer("دسترسی ندارید", show_alert=True)
        return ADMIN_MENU
    cfg = get_workshop_config()
    kb = []
    for lvl in range(1,6):
        data = get_workshop_level_config(lvl)
        soldier = data.get('soldier') or data.get('unit') or '-'
        amount = data.get('amount', 0)
        soldier_name = get_asset_display_name(soldier) if soldier != '-' else '-'
        cost = data.get('cost', 0)
        kb.append([InlineKeyboardButton(f"لول {lvl}: {soldier_name} x{amount} ({cost:,}💰)", callback_data=f'workshop_cfg_lvl_{lvl}')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    await q.edit_message_text("⚒️ تنظیم کارگاه - هر لول چه سربازی و چندتا در روز بدهد:\n(همه نوع نیرو موجود است)", reply_markup=InlineKeyboardMarkup(kb))
    return WORKSHOP_CFG_MENU

async def workshop_cfg_select_soldier(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    lvl = int(q.data.replace('workshop_cfg_lvl_', ''))
    context.user_data['cfg_lvl'] = lvl
    # لیست همه نیروهای پیاده
    all_soldiers = ['spearman_1','spearman_2','spearman_3','swordsman_1','swordsman_2','swordsman_3','archer_1','archer_2','archer_3','cavalry_light','cavalry_heavy','catapult','trebuchet']
    # همچنین هر نیروی سفارشی که ادمین قبلا اضافه کرده
    try:
        for it in get_all_equipment_items():
            if it['category'] == 'land_troops' and it['item_key'] not in all_soldiers:
                all_soldiers.append(it['item_key'])
    except: pass
    kb = []
    for s in all_soldiers:
        kb.append([InlineKeyboardButton(get_asset_display_name(s), callback_data=f'workshop_cfg_soldier_{s}')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='workshop_cfg_menu')])
    await q.edit_message_text(f"لول {lvl} - نوع سرباز را انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    return WORKSHOP_CFG_SOLDIER

async def workshop_cfg_get_amount(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    soldier = q.data.replace('workshop_cfg_soldier_', '')
    lvl = context.user_data.get('cfg_lvl')
    context.user_data['cfg_soldier'] = soldier
    await q.edit_message_text(f"لول {lvl} - {get_asset_display_name(soldier)}\n\nچندتا در روز بدهد؟ عدد وارد کن (1-100):")
    return WORKSHOP_CFG_AMOUNT

async def workshop_cfg_save_amount(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    try:
        amount = int((update.message.text or "").strip())
        if amount < 1 or amount > 100:
            raise ValueError
    except:
        await update.message.reply_text("❌ عدد باید 1 تا 100 باشد:")
        return WORKSHOP_CFG_AMOUNT
    lvl = context.user_data.get('cfg_lvl')
    soldier = context.user_data.get('cfg_soldier')
    context.user_data['cfg_amount'] = amount
    cfg = get_workshop_config()
    current = cfg.get(str(lvl), WORKSHOP_LEVELS.get(lvl, {}).copy())
    current['soldier'] = soldier
    current['amount'] = amount
    # keep cost and name
    await update.message.reply_text(f"✅ مقدار ثبت شد: {amount} × {get_asset_display_name(soldier)}\n\nحالا هزینه ارتقا به این لول را وارد کن (مثلاً 30000):")
    return WORKSHOP_CFG_COST

async def workshop_cfg_save_cost(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    try:
        cost = int((update.message.text or "").strip().replace(",", ""))
        if cost < 0:
            raise ValueError
    except:
        await update.message.reply_text("❌ هزینه باید عدد مثبت باشد:")
        return WORKSHOP_CFG_COST
    lvl = context.user_data.get('cfg_lvl')
    soldier = context.user_data.get('cfg_soldier')
    amount = context.user_data.get('cfg_amount')
    cfg = get_workshop_config()
    # load default name if exists
    default = WORKSHOP_LEVELS.get(lvl, {})
    cfg[str(lvl)] = {
        'name': default.get('name', f'لول {lvl}'),
        'cost': cost,
        'soldier': soldier,
        'amount': amount
    }
    save_workshop_config(cfg)
    await update.message.reply_text(f"✅ لول {lvl} ذخیره شد:\n{get_asset_display_name(soldier)} x{amount} - هزینه {cost:,}")
    for k in ['cfg_lvl','cfg_soldier','cfg_amount']:
        context.user_data.pop(k, None)
    # برگشت به منو
    # شبیه‌سازی callback برای نمایش مجدد
    class FakeQ:
        def __init__(self, user_id):
            self.from_user = type('u', (), {'id': user_id})()
        async def answer(self, *a, **kw): pass
        async def edit_message_text(self, *a, **kw):
            await update.message.reply_text(*a, **kw)
    # ساده: مستقیم منو را بفرست
    cfg = get_workshop_config()
    text = "⚒️ تنظیم کارگاه - بروز شد:\n"
    for l in range(1,6):
        d = cfg.get(str(l)) or WORKSHOP_LEVELS.get(l, {})
        s = d.get('soldier','-')
        a = d.get('amount',0)
        c = d.get('cost',0)
        text += f"لول {l}: {get_asset_display_name(s) if s!='-' else '-'} x{a} ({c:,})\n"
    await update.message.reply_text(text)
    return ADMIN_MENU


async def darayi_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    dari = get_all_darayi()
    kb = []
    for d in dari:
        kb.append([
            InlineKeyboardButton(f"👁️ {d['name']}", callback_data=f"darayi_view_{d['preset_id']}"),
            InlineKeyboardButton("✏️", callback_data=f"darayi_edit_{d['preset_id']}"),
            InlineKeyboardButton("🗑️", callback_data=f"darayi_del_{d['preset_id']}")
        ])
    kb.append([InlineKeyboardButton("➕ ساخت دارایی جدید", callback_data='darayi_create')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    text = "💎 مدیریت دارایی‌های سیو شده\n\n"
    if not dari:
        text += "هیچ دارایی سیو نشده."
    else:
        text += f"{len(dari)} دارایی ذخیره شده. برای مشاهده/ویرایش/حذف دکمه‌ها را بزن."
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    return DARAYI_MENU

async def darayi_view(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    pid = int(q.data.replace('darayi_view_', ''))
    d = get_darayi(pid)
    if not d:
        await q.edit_message_text("❌ یافت نشد")
        return await darayi_menu(update, context)
    data = d['data']
    txt = f"💎 دارایی «{d['name']}»\n\n"
    txt += f"• سرمایه: {data.get('capital',0):,}\n"
    txt += f"• جمعیت: {data.get('population',0):,}\n"
    txt += f"• غلات: {data.get('grains',0):,}\n"
    txt += f"• نفت: {data.get('oil_barrels',0):,}\n"
    for cat in ['land_troops']:
        if cat in data:
            txt += f"\n*{cat}:*\n"
            for k,v in data[cat].items():
                if v>0:
                    txt += f"  {get_asset_display_name(k)}: {v}\n"
    kb = [[InlineKeyboardButton("✏️ ویرایش", callback_data=f"darayi_edit_{pid}")],[InlineKeyboardButton("🔙 بازگشت", callback_data='darayi_menu')]]
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    return DARAYI_VIEW

async def darayi_edit_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    pid = int(q.data.replace('darayi_edit_', ''))
    context.user_data['edit_darayi_id'] = pid
    d = get_darayi(pid)
    kb = [[InlineKeyboardButton("💰 سرمایه", callback_data='darayi_field_capital')],[InlineKeyboardButton("🌾 غلات", callback_data='darayi_field_grains')],[InlineKeyboardButton("👫 جمعیت", callback_data='darayi_field_population')],[InlineKeyboardButton("⚔️ نیروها", callback_data='darayi_field_troops')],[InlineKeyboardButton("🔙 بازگشت", callback_data='darayi_menu')]]
    await q.edit_message_text(f"✏️ ویرایش «{d['name']}» - فیلد را انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    return DARAYI_EDIT_SELECT

async def darayi_field_prompt(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    field = q.data.replace('darayi_field_', '')
    context.user_data['edit_field'] = field
    if field == 'troops':
        # نمایش دکمه‌ای همه نیروها
        all_soldiers = ['spearman_1','spearman_2','spearman_3','swordsman_1','swordsman_2','swordsman_3','archer_1','archer_2','archer_3','cavalry_light','cavalry_heavy','catapult','trebuchet']
        try:
            for it in get_all_equipment_items():
                if it['category'] == 'land_troops' and it['item_key'] not in all_soldiers:
                    all_soldiers.append(it['item_key'])
        except: pass
        kb = []
        for s in all_soldiers:
            kb.append([InlineKeyboardButton(get_asset_display_name(s), callback_data=f'darayi_soldier_{s}')])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='darayi_menu')])
        await q.edit_message_text("⚔️ کدام نیرو را می‌خواهی ویرایش کنی؟", reply_markup=InlineKeyboardMarkup(kb))
        return DARAYI_EDIT_SELECT
    else:
        await q.edit_message_text(f"مقدار جدید برای {field} را وارد کن (عدد):")
        return DARAYI_EDIT_VALUE

async def darayi_soldier_selected(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    soldier = q.data.replace('darayi_soldier_', '')
    context.user_data['edit_soldier'] = soldier
    context.user_data['edit_field'] = 'troops'
    pid = context.user_data.get('edit_darayi_id')
    d = get_darayi(pid)
    current = d['data'].get('land_troops', {}).get(soldier, 0) if d else 0
    await q.edit_message_text(f"⚔️ {get_asset_display_name(soldier)}\nتعداد فعلی: {current}\n\nتعداد جدید را وارد کن (عدد):")
    return DARAYI_EDIT_VALUE

async def darayi_save_value(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    pid = context.user_data.get('edit_darayi_id')
    field = context.user_data.get('edit_field')
    d = get_darayi(pid)
    if not d:
        await update.message.reply_text("❌ یافت نشد")
        return ADMIN_MENU
    data = d['data']
    txt = (update.message.text or "").strip()
    try:
        if field == 'troops':
            soldier = context.user_data.get('edit_soldier')
            if not soldier:
                await update.message.reply_text("❌ سرباز انتخاب نشده. دوباره از منو انتخاب کن.")
                return DARAYI_EDIT_SELECT
            v = int(txt.replace(',', ''))
            if 'land_troops' not in data:
                data['land_troops'] = {}
            data['land_troops'][soldier] = v
            # پاک کن
            context.user_data.pop('edit_soldier', None)
        else:
            val = int(txt.replace(',', ''))
            data[field] = val
        update_darayi_data(pid, data)
        await update.message.reply_text(f"✅ «{field}» به {txt} تغییر کرد.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")
        return DARAYI_EDIT_VALUE
    return await darayi_menu_via_message(update, context)

async def darayi_menu_via_message(update: Update, context: CallbackContext):
    dari = get_all_darayi()
    kb = []
    for d in dari:
        kb.append([InlineKeyboardButton(f"👁️ {d['name']}", callback_data=f"darayi_view_{d['preset_id']}"),InlineKeyboardButton("✏️", callback_data=f"darayi_edit_{d['preset_id']}"),InlineKeyboardButton("🗑️", callback_data=f"darayi_del_{d['preset_id']}")])
    kb.append([InlineKeyboardButton("➕ ساخت دارایی جدید", callback_data='darayi_create')])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    await update.message.reply_text("💎 لیست دارایی‌ها:", reply_markup=InlineKeyboardMarkup(kb))
    return DARAYI_MENU

async def darayi_delete(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    pid = int(q.data.replace('darayi_del_', ''))
    delete_darayi(pid)
    await q.answer("حذف شد", show_alert=True)
    return await darayi_menu(update, context)

async def darayi_create_start(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("➕ ساخت دارایی جدید\n\nاسم دارایی را وارد کن (مثلاً منابع 1):")
    return DARAYI_CREATE_NAME

async def darayi_create_name(update: Update, context: CallbackContext) -> int:
    if not is_admin(update.effective_user.id):
        return ADMIN_MENU
    name = (update.message.text or "").strip()
    if not name or len(name) > 30:
        await update.message.reply_text("❌ اسم نامعتبر (1-30 کاراکتر):")
        return DARAYI_CREATE_NAME
    if get_darayi_by_name(name):
        await update.message.reply_text("❌ این اسم قبلاً وجود دارد:")
        return DARAYI_CREATE_NAME
    template = {'capital': 100000,'population': 1000000,'grains': 5000,'oil_barrels': 100,'satisfaction': 50,'land_troops': {'spearman_1': 10, 'archer_1': 5}}
    pid = save_darayi_preset(name, template)
    if pid:
        await update.message.reply_text(f"✅ دارایی «{name}» ساخته شد (آیدی {pid}).")
    else:
        await update.message.reply_text("❌ ساخت ناموفق")
    return await darayi_menu_via_message(update, context)

async def set_darayi_by_chat(update: Update, context: CallbackContext):
    if not update.message or not update.effective_chat:
        return
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return
    user_id = update.effective_user.id if update.effective_user else None
    if not is_admin(user_id):
        return
    import re
    m = re.match(r"^\s*تنظیم دارایی\s+(.+?)\s*$", update.message.text or "")
    if not m:
        return
    darayi_name = m.group(1).strip()
    darayi = get_darayi_by_name(darayi_name)
    if not darayi:
        try:
            await update.message.reply_text(f"❌ دارایی «{darayi_name}» یافت نشد.")
        except: pass
        return
    chat_id = chat.id
    country = get_country(chat_id)
    if not country:
        try:
            await update.message.reply_text("ℹ️ این گپ کشوری ندارد. اول «افزودن کشور بخارا» بزن.")
        except: pass
        return
    data = darayi['data']
    updates = {}
    for k in ['capital','population','grains','satisfaction']:
        if k in data:
            updates[k] = data[k]
    if 'land_troops' in data:
        updates['land_troops'] = data['land_troops']
    update_country(chat_id, updates)
    try:
        await update.message.reply_text(f"✅ دارایی «{darayi_name}» برای کشور «{country['name']}» اعمال شد!")
    except: pass


async def set_d_command(update: Update, context: CallbackContext):
    # /set_d در گپ: دارایی کشور اون گپ به دیفالت بازی برمی‌گرده
    if not update.message or not update.effective_chat:
        return
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text("⛔ این دستور فقط در گپ کار می‌کند.")
        return
    user_id = update.effective_user.id if update.effective_user else None
    if not is_admin(user_id):
        await update.message.reply_text("⛔ فقط ادمین")
        return
    chat_id = chat.id
    country = get_country(chat_id)
    if not country:
        await update.message.reply_text("ℹ️ این گپ کشوری ندارد. اول «افزودن کشور بخارا» بزن.")
        return
    defaults = get_dynamic_default_assets()
    # مقادیر دیفالت بازی
    reset_data = {
        'population': defaults.get('population', 15000000),
        'capital': defaults.get('capital', 100000000),
        'grains': defaults.get('grains', 5000),
        'satisfaction': defaults.get('satisfaction', 50),
        'security': defaults.get('security', 50),
        'farm_level': defaults.get('farm_level', 0),
        'fort_level': defaults.get('fort_level', 0),
        'workshop_level': defaults.get('workshop_level', 0),
        'storage_capacity': 100,
    }
    # نیروها صفر
    for cat in ['land_troops']:
        if cat in defaults:
            reset_data[cat] = {k: 0 for k in defaults[cat].keys()}
    update_country(chat_id, reset_data)
    await update.message.reply_text(f"✅ دارایی کشور «{country['name']}» به حالت دیفالت بازی برگشت!")

async def panel_in_group_handler(update: Update, context: CallbackContext) -> int:
    # "پنل" در گپ: مثل "منو" عمل می‌کند
    return await menu_in_group_handler(update, context)

async def panel_private_handler(update: Update, context: CallbackContext) -> int:
    if not update.message:
        return ConversationHandler.END
    # در پی‌وی: پنل را نشان بده
    user_id = update.effective_user.id
    if is_admin(user_id):
        country = get_country(user_id)
        if not country:
            return await admin_panel(update, context)
    return await show_main_menu(update, context)


async def delete_force_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    items = get_all_equipment_items()
    if not items:
        await q.edit_message_text("هیچ نیرویی برای حذف وجود ندارد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]]))
        return DELETE_FORCE_MENU
    kb = []
    for it in items:
        # نمایش همه نیروها حتی دیفالت
        kb.append([InlineKeyboardButton(f"🗑️ {it['display_name']} ({it['item_key']})", callback_data=f"delete_force_{it['item_id']}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    # برای جلوگیری از طولانی شدن پیام، فقط دکمه‌ها
    await q.edit_message_text(f"🗑️ حذف نیرو - {len(items)} نیرو موجود (حتی دیفالت) - روی هرکدام بزن تا حذف شود:", reply_markup=InlineKeyboardMarkup(kb))
    return DELETE_FORCE_MENU

async def delete_force_confirm(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    try:
        item_id = int(q.data.replace('delete_force_', ''))
        item = get_equipment_item_by_id(item_id)
        if not item:
            await q.answer("یافت نشد", show_alert=True)
            return await delete_force_menu(update, context)
        ok = delete_equipment_item(item_id)
        if ok:
            await q.answer(f"✅ {item['display_name']} حذف شد", show_alert=True)
        else:
            await q.answer("❌ حذف نشد", show_alert=True)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"delete_force: {e}")
        await q.answer("خطا", show_alert=True)
    return await delete_force_menu(update, context)


# --- حذف کشورها ---
async def delete_single_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    countries = get_all_countries()
    if not countries:
        await q.edit_message_text("هیچ کشوری وجود ندارد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')]]))
        return DELETE_SINGLE_SELECT
    kb = []
    for uid, name in countries:
        kb.append([InlineKeyboardButton(f"🗑️ {name}", callback_data=f"delete_single_{uid}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    await q.edit_message_text(f"🗑️ حذف تکی - {len(countries)} کشور:", reply_markup=InlineKeyboardMarkup(kb))
    return DELETE_SINGLE_SELECT

async def delete_single_confirm(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    try:
        uid = int(q.data.replace('delete_single_', ''))
        country = get_country(uid)
        if not country:
            await q.answer("یافت نشد", show_alert=True)
            return await delete_single_menu(update, context)
        delete_country(uid)
        await q.answer(f"✅ {country['name']} حذف شد", show_alert=True)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"delete_single: {e}")
    return await delete_single_menu(update, context)

async def delete_all_menu(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    countries = get_all_countries()
    kb = [
        [InlineKeyboardButton("💥 بله، همه را پاک کن", callback_data='delete_all_confirm')],
        [InlineKeyboardButton("❌ لغو", callback_data='admin_panel')]
    ]
    await q.edit_message_text(f"⚠️ هشدار! {len(countries)} کشور به طور کامل پاک خواهند شد. مطمئنی؟", reply_markup=InlineKeyboardMarkup(kb))
    return DELETE_ALL_CONFIRM

async def delete_all_confirm(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    if q.data != 'delete_all_confirm':
        return ADMIN_MENU
    countries = get_all_countries()
    for uid, _ in countries:
        try:
            delete_country(uid)
        except: pass
    await q.edit_message_text(f"💥 {len(countries)} کشور با موفقیت پاک شدند!")
    return ADMIN_MENU

# --- بلایای طبیعی ---
DISASTERS = {
    'earthquake': {'name': 'زلزله 🌋', 'desc': 'زلزله شدید', 'pop_loss': 0.05, 'capital_loss': 0.1, 'grain_loss': 0.2},
    'flood': {'name': 'سیل 🌊', 'desc': 'سیل ویرانگر', 'pop_loss': 0.03, 'capital_loss': 0.15, 'grain_loss': 0.3},
    'drought': {'name': 'خشکسالی ☀️', 'desc': 'خشکسالی طولانی', 'pop_loss': 0.02, 'capital_loss': 0.05, 'grain_loss': 0.5},
    'plague': {'name': 'طاعون 💀', 'desc': 'طاعون مرگبار', 'pop_loss': 0.1, 'capital_loss': 0.05, 'grain_loss': 0.1},
    'storm': {'name': 'طوفان 🌪️', 'desc': 'طوفان سهمگین', 'pop_loss': 0.04, 'capital_loss': 0.08, 'grain_loss': 0.15},
}

async def disaster_menu(update: Update, context: CallbackContext) -> int:
    import logging as _l
    _l.getLogger(__name__).info(f"disaster_menu triggered by {update.callback_query.from_user.id} data={update.callback_query.data}")
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.answer("دسترسی ندارید", show_alert=True)
        return ADMIN_MENU
    kb = []
    for key, d in DISASTERS.items():
        kb.append([InlineKeyboardButton(d['name'], callback_data=f"disaster_{key}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='admin_panel')])
    await q.edit_message_text("🌪️ بلایای طبیعی - نوع بلا را انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    return DISASTER_MENU

async def disaster_select_target(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    disaster_key = q.data.replace('disaster_', '')
    context.user_data['disaster_key'] = disaster_key
    countries = get_all_countries()
    kb = [[InlineKeyboardButton("🌍 همه کشورها", callback_data='disaster_target_all')]]
    for uid, name in countries:
        kb.append([InlineKeyboardButton(name, callback_data=f"disaster_target_{uid}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data='disaster_menu')])
    dname = DISASTERS.get(disaster_key, {}).get('name', disaster_key)
    await q.edit_message_text(f"🌪️ {dname} - هدف را انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    return DISASTER_TARGET

async def disaster_confirm(update: Update, context: CallbackContext) -> int:
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        return ADMIN_MENU
    disaster_key = context.user_data.get('disaster_key')
    target = q.data.replace('disaster_target_', '')
    disaster = DISASTERS.get(disaster_key)
    if not disaster:
        await q.edit_message_text("❌ بلا یافت نشد")
        return ADMIN_MENU
    targets = []
    if target == 'all':
        targets = get_all_countries()
    else:
        try:
            uid = int(target)
            c = get_country(uid)
            if c:
                targets = [(uid, c['name'])]
        except: pass
    if not targets:
        await q.edit_message_text("❌ هدفی یافت نشد")
        return ADMIN_MENU
    affected = []
    for uid, name in targets:
        c = get_country(uid)
        if not c:
            continue
        pop_loss = int(c.get('population',0) * disaster['pop_loss'])
        cap_loss = int(c.get('capital',0) * disaster['capital_loss'])
        grain_loss = int(c.get('grains',0) * disaster['grain_loss'])
        new_pop = max(0, c.get('population',0) - pop_loss)
        new_cap = max(0, c.get('capital',0) - cap_loss)
        new_grain = max(0, c.get('grains',0) - grain_loss)
        update_country(uid, {'population': new_pop, 'capital': new_cap, 'grains': new_grain})
        affected.append(name)
    # ارسال به کانال گزارش
    try:
        text = f"🌪️ بلای طبیعی: {disaster['name']}\n{disaster['desc']}\n\nهدف: {', '.join(affected)}\nتلفات: {disaster['pop_loss']*100:.0f}% جمعیت، {disaster['capital_loss']*100:.0f}% سرمایه"
        await context.bot.send_message(chat_id=REPORTS_CHANNEL, text=text)
    except: pass
    await q.edit_message_text(f"✅ {disaster['name']} برای {len(affected)} کشور اعمال شد!")
    return ADMIN_MENU

async def backup_database_job(context):
    import logging as _log
    try:
        # ارسال فایل دیتابیس به پی‌وی اونر
        await context.bot.send_document(chat_id=OWNER_ID, document=open(DATABASE_NAME, 'rb'), caption=f"💾 بکاپ دیتابیس - {__import__('datetime').datetime.now().strftime('%H:%M %d/%m/%Y')}")
        _log.getLogger(__name__).info("Backup sent to owner")
    except Exception as e:
        _log.getLogger(__name__).error(f"Backup failed: {e}")


async def help_text_command(update: Update, context: CallbackContext):
    # فقط ادمین
    try:
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("⛔ فقط ادمین می‌تواند راهنما را ببیند.")
            return
    except:
        return
    text = (
        "📖 <b>راهنمای دستورات نوشتاری ادمین</b>\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🏰 <b>داخل گپ:</b>\n"
        "• <code>اکتویت</code> — فعال‌سازی گپ\n"
        "• <code>دیاکتویت</code> — غیرفعال‌سازی\n"
        "• <code>افزودن کشور بخارا</code> — گپ را کشور کن\n"
        "• <code>تنظیم کشور بخارا</code> — تغییر اسم\n"
        "• <code>حذف کشور</code> — پاک کردن کشور گپ\n"
        "• <code>تنظیم صاحب 123456789</code> — انتقال مالکیت\n"
        "  └ <code>تنیم صاحب 123</code> هم کار می‌کند\n"
        "• <code>تنظیم دارایی منابع 1</code> — اعمال دارایی سیو شده\n"
        "• <code>/set_d</code> — ریست به دیفالت\n"
        "• <code>/id</code> — ریپلای روی پیام کسی → فقط آیدی\n"
        "• <code>پنل</code> / <code>منو</code> — باز کردن پنل\n\n"
        "💬 <b>پی‌وی:</b>\n"
        "• <code>مدیریت تجهیزات</code> — لیست نیروها\n"
        "• <code>راهنما</code> — همین پیام\n\n"
        "━━━━━━━━━━━━━━━"
    )
    try:
        await update.message.reply_text(text, parse_mode="HTML")
    except:
        try:
            await update.message.reply_text(text)
        except: pass

async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if update and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="متاسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا /start را ارسال کنید."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")








# === ADMIN UPDATE ASSETS SAFE PATCH ===
ADMIN_UPDATE_ASSETS_CALLBACK = "admin_update_assets"
ADMIN_UPDATE_ASSETS_BUTTON_TEXT = "\u0622\u067e \u062f\u0627\u0631\u0627\u06cc\u06cc"
ADMIN_UPDATE_ASSETS_DONE_TEXT = "\u0622\u067e\u062f\u06cc\u062a \u062f\u0627\u0631\u0627\u06cc\u06cc \u0627\u0646\u062c\u0627\u0645 \u0634\u062f \u2705"


def _admin_update_assets_chat_id(row):
    if isinstance(row, dict):
        return row.get("chat_id") or row.get("id")
    if isinstance(row, (list, tuple)) and row:
        return row[0]
    return getattr(row, "chat_id", None) or row


async def _admin_update_assets_broadcast(bot_instance):
    chat_ids = []
    try:
        if STATEMENT_CHANNEL:
            chat_ids.append(STATEMENT_CHANNEL)
    except Exception:
        pass
    try:
        for row in get_all_active_chats():
            cid = _admin_update_assets_chat_id(row)
            if cid:
                chat_ids.append(cid)
    except Exception as e:
        logger.error(f"Error reading active chats for asset update: {e}", exc_info=True)

    sent = set()
    for cid in chat_ids:
        key = str(cid)
        if key in sent:
            continue
        sent.add(key)
        try:
            await bot_instance.send_message(chat_id=cid, text=ADMIN_UPDATE_ASSETS_DONE_TEXT)
        except Exception as e:
            logger.error(f"Error sending asset update message to {cid}: {e}")


async def admin_update_assets_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = update.effective_user.id if update.effective_user else None
    if query:
        try:
            await query.answer()
        except Exception:
            pass
    if not is_admin(user_id):
        if query:
            await query.answer("\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc\u062f", show_alert=True)
        return ADMIN_MENU
    try:
        await daily_production_job(context)
        await _admin_update_assets_broadcast(context.bot)
        if query:
            await query.edit_message_text(ADMIN_UPDATE_ASSETS_DONE_TEXT)
    except Exception as e:
        logger.error(f"Error in admin_update_assets_handler: {e}", exc_info=True)
        if query:
            await query.edit_message_text("\u062e\u0637\u0627 \u062f\u0631 \u0622\u067e\u062f\u06cc\u062a \u062f\u0627\u0631\u0627\u06cc\u06cc")
    return ADMIN_MENU

# === END ADMIN UPDATE ASSETS SAFE PATCH ===


def main() -> None:
    init_db()
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue
    if job_queue:
        tehran_timezone = pytz.timezone('Asia/Tehran')
        job_time = time(hour=12, minute=0, tzinfo=tehran_timezone)
        job_queue.run_daily(daily_production_job, job_time, name="daily_production")
        # بکاپ 7 نوبت در روز به پی‌وی اونر
        import pytz as _pytz
        tehran = _pytz.timezone('Asia/Tehran')
        for h in [0, 3, 9, 12, 15, 18, 21]:
            job_queue.run_daily(backup_database_job, time(hour=h, minute=0, tzinfo=tehran), name=f"backup_{h}")

        job_queue.run_repeating(deliver_trades_job, interval=60, first=10)

        job_queue.run_repeating(deliver_attacks_job, interval=60, first=10)

        logger.info("Job daily_production, deliver_trades and deliver_attacks scheduled")
    else:
        logger.warning("Job queue not available")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(player_cat_info, pattern='^cat_player_info$'),
                CallbackQueryHandler(player_cat_military, pattern='^cat_player_military$'),
                CallbackQueryHandler(player_cat_economy, pattern='^cat_player_economy$'),
                CallbackQueryHandler(player_cat_political, pattern='^cat_player_political$'),
                CallbackQueryHandler(castle_menu, pattern='^castle_menu$'),
                CallbackQueryHandler(show_assets, pattern='^show_assets$'),
                CallbackQueryHandler(campaign_menu, pattern='^campaign_menu$'),
                CallbackQueryHandler(attack_menu, pattern='^attack_menu$'),
                CallbackQueryHandler(missile_attack_menu, pattern='^missile_attack_menu$'),
                CallbackQueryHandler(role_sena_menu, pattern='^role_sena_menu$'),
                CallbackQueryHandler(construction_proposal_start, pattern='^construction_proposal_start$'),
                CallbackQueryHandler(shop_menu_start, pattern='^shop_menu_start$'),
                CallbackQueryHandler(set_religion_menu, pattern='^religion_menu$'),
                CallbackQueryHandler(statement_proposal_start, pattern='^statement_proposal_start$'),
                CallbackQueryHandler(admin_panel, pattern='^admin_panel$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$'),
                CallbackQueryHandler(siege_menu, pattern='^siege_menu$'),
                CallbackQueryHandler(country_management, pattern='^country_management$'),
            ],
            SIEGE_SELECT_TARGET: [
                CallbackQueryHandler(siege_select_target, pattern='^siege_target_'),
                CallbackQueryHandler(siege_menu, pattern='^siege_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            SIEGE_CONFIRM: [
                CallbackQueryHandler(siege_confirm, pattern='^siege_confirm_'),
                CallbackQueryHandler(siege_menu, pattern='^siege_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ADMIN_MENU: [
                CallbackQueryHandler(add_country, pattern='^add_country$'),
                CallbackQueryHandler(delete_country_menu, pattern='^delete_country_menu$'),
                CallbackQueryHandler(list_countries, pattern='^list_countries$'),
                CallbackQueryHandler(edit_main_props, pattern='^edit_main_props$'),
                CallbackQueryHandler(edit_assets_menu, pattern='^edit_assets_menu$'),
                CallbackQueryHandler(admin_update_assets_handler, pattern='^admin_update_assets$'),
                CallbackQueryHandler(admin_cat_countries, pattern='^cat_admin_countries$'),
                CallbackQueryHandler(admin_cat_settings, pattern='^cat_admin_settings$'),
                CallbackQueryHandler(admin_cat_admins, pattern='^cat_admin_admins$'),
                CallbackQueryHandler(admin_cat_rewards, pattern='^cat_admin_rewards$'),
                CallbackQueryHandler(delete_single_menu, pattern='^delete_single_menu$'),
                CallbackQueryHandler(delete_all_menu, pattern='^delete_all_menu$'),
                CallbackQueryHandler(disaster_menu, pattern='^disaster_menu$'),
                CallbackQueryHandler(darayi_menu, pattern='^darayi_menu$'),
                CallbackQueryHandler(workshop_cfg_menu, pattern='^workshop_cfg_menu$'),
                CallbackQueryHandler(select_country_view_assets, pattern='^select_country_view_assets$'),
                CallbackQueryHandler(add_admin, pattern='^add_admin$'),
                CallbackQueryHandler(remove_admin, pattern='^remove_admin$'),
                CallbackQueryHandler(toggle_bot_active_status, pattern='^toggle_bot$'),
                CallbackQueryHandler(manage_global_buttons, pattern='^manage_global_buttons$'),
                CallbackQueryHandler(role_sena_limits_menu, pattern='^role_sena_limits_menu$'),
                CallbackQueryHandler(trade_settings, pattern='^trade_settings$'),
                CallbackQueryHandler(manage_notification_images, pattern='^manage_notification_images$'),
                CallbackQueryHandler(random_prize_menu, pattern='^random_prize_menu$'),
                CallbackQueryHandler(announce_top_oil, pattern='^announce_top_oil$'),
                CallbackQueryHandler(announce_top_satisfaction, pattern='^announce_top_satisfaction$'),
                CallbackQueryHandler(delete_force_menu, pattern='^delete_force_menu$'),
                CallbackQueryHandler(add_force_start, pattern='^add_force$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$'),
            ],
            ADD_FORCE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_force_get_name)
            ],
            ADD_FORCE_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_force_get_price)
            ],
            ADD_FORCE_GRAIN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_force_get_grain)
            ],
            WORKSHOP_CFG_MENU: [
                CallbackQueryHandler(workshop_cfg_select_soldier, pattern='^workshop_cfg_lvl_'),
                CallbackQueryHandler(delete_single_menu, pattern='^delete_single_menu$'),
                CallbackQueryHandler(delete_all_menu, pattern='^delete_all_menu$'),
                CallbackQueryHandler(disaster_menu, pattern='^disaster_menu$'),
                CallbackQueryHandler(darayi_menu, pattern='^darayi_menu$'),
                CallbackQueryHandler(workshop_cfg_menu, pattern='^workshop_cfg_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            WORKSHOP_CFG_SOLDIER: [
                CallbackQueryHandler(workshop_cfg_get_amount, pattern='^workshop_cfg_soldier_'),
                CallbackQueryHandler(delete_single_menu, pattern='^delete_single_menu$'),
                CallbackQueryHandler(delete_all_menu, pattern='^delete_all_menu$'),
                CallbackQueryHandler(disaster_menu, pattern='^disaster_menu$'),
                CallbackQueryHandler(darayi_menu, pattern='^darayi_menu$'),
                CallbackQueryHandler(workshop_cfg_menu, pattern='^workshop_cfg_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            WORKSHOP_CFG_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, workshop_cfg_save_amount)
            ],
            WORKSHOP_CFG_COST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, workshop_cfg_save_cost)
            ],
            DARAYI_MENU: [
                CallbackQueryHandler(darayi_view, pattern='^darayi_view_'),
                CallbackQueryHandler(darayi_edit_menu, pattern='^darayi_edit_'),
                CallbackQueryHandler(darayi_delete, pattern='^darayi_del_'),
                CallbackQueryHandler(darayi_create_start, pattern='^darayi_create$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            DARAYI_VIEW: [
                CallbackQueryHandler(darayi_edit_menu, pattern='^darayi_edit_'),
                CallbackQueryHandler(delete_single_menu, pattern='^delete_single_menu$'),
                CallbackQueryHandler(delete_all_menu, pattern='^delete_all_menu$'),
                CallbackQueryHandler(disaster_menu, pattern='^disaster_menu$'),
                CallbackQueryHandler(darayi_menu, pattern='^darayi_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            DARAYI_EDIT_SELECT: [
                CallbackQueryHandler(darayi_field_prompt, pattern='^darayi_field_'),
                CallbackQueryHandler(darayi_soldier_selected, pattern='^darayi_soldier_'),
                CallbackQueryHandler(delete_single_menu, pattern='^delete_single_menu$'),
                CallbackQueryHandler(delete_all_menu, pattern='^delete_all_menu$'),
                CallbackQueryHandler(disaster_menu, pattern='^disaster_menu$'),
                CallbackQueryHandler(darayi_menu, pattern='^darayi_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            DARAYI_EDIT_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, darayi_save_value)
            ],
            DARAYI_CREATE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, darayi_create_name)
            ],
            DELETE_FORCE_MENU: [
                CallbackQueryHandler(delete_force_confirm, pattern='^delete_force_'),
                CallbackQueryHandler(delete_force_menu, pattern='^delete_force_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            ADD_COUNTRY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_new_country)
            ],
            DELETE_COUNTRY_MENU: [
                CallbackQueryHandler(execute_delete_country, pattern='^execute_delete_country_'),
                CallbackQueryHandler(confirm_delete_country, pattern='^delete_country_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            EDIT_MAIN_PROPS: [
                CallbackQueryHandler(select_main_prop_to_edit, pattern='^edit_main_country_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            SELECT_MAIN_PROP: [
                CallbackQueryHandler(get_main_prop_value, pattern='^set_main_prop_'),
                CallbackQueryHandler(edit_main_props, pattern='^edit_main_props$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            GET_MAIN_PROP_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_main_prop_value)
            ],
            EDIT_ASSETS_MENU: [
                CallbackQueryHandler(select_asset_category, pattern='^edit_assets_country_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            SELECT_ASSET_CATEGORY: [
                CallbackQueryHandler(select_asset_item, pattern='^select_asset_category_'),
                CallbackQueryHandler(edit_assets_menu, pattern='^edit_assets_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            SELECT_ASSET_ITEM: [
                CallbackQueryHandler(get_asset_edit_value, pattern='^set_asset_item_'),
                CallbackQueryHandler(select_asset_category, pattern='^edit_assets_country_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            GET_ASSET_EDIT_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_asset_edit_value)
            ],
            SELECT_COUNTRY_TO_VIEW_ASSETS: [
                CallbackQueryHandler(handle_view_selected_country_assets, pattern='^view_assets_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            ATTACK_TARGET: [
                CallbackQueryHandler(select_attack_target, pattern='^attack_target_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            GET_ATTACK_TROOPS_DETAILS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_attack_troops_details)
            ],
            GET_ATTACK_SCENARIO_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_attack_scenario_input),
                MessageHandler(filters.PHOTO & ~filters.COMMAND, get_attack_scenario_input),
                CallbackQueryHandler(confirm_attack_scenario, pattern='^confirm_attack_scenario$')
            ],
            CONFIRM_ATTACK_SCENARIO: [
                CallbackQueryHandler(confirm_attack_scenario, pattern='^confirm_attack_scenario$')
            ],
            RELIGION_MENU: [
                CallbackQueryHandler(set_country_religion, pattern='^set_religion_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ADD_ADMIN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_add_admin)
            ],
            REMOVE_ADMIN: [
                CallbackQueryHandler(process_remove_admin, pattern='^remove_admin_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            MANAGE_GLOBAL_BUTTONS: [
                CallbackQueryHandler(toggle_global_button, pattern='^toggle_global_button_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            GET_PROPOSAL_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_proposal_content),
                MessageHandler(filters.PHOTO & ~filters.COMMAND, get_proposal_content),
                CallbackQueryHandler(final_send_proposal, pattern='^final_send_proposal$')
            ],
            SHOP_MENU: [
                CallbackQueryHandler(select_shop_category, pattern='^shop_category_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            SHOP_CATEGORY: [
                CallbackQueryHandler(select_shop_item, pattern='^shop_item_'),
                CallbackQueryHandler(shop_menu_start, pattern='^shop_menu_start$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            GET_SHOP_ITEM_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_shop_item_quantity)
            ],
            GET_STATEMENT_CONTENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_statement_content),
                MessageHandler(filters.PHOTO & ~filters.COMMAND, get_statement_content),
                MessageHandler(filters.VIDEO & ~filters.COMMAND, get_statement_content),
                MessageHandler(filters.ANIMATION & ~filters.COMMAND, get_statement_content),
                MessageHandler(filters.Document.ALL & ~filters.COMMAND, get_statement_content)
            ],
            CASTLE_MENU: [
                CallbackQueryHandler(farm_menu, pattern='^farm_menu$'),
                CallbackQueryHandler(fort_menu, pattern='^fort_menu$'),
                CallbackQueryHandler(workshop_menu, pattern='^workshop_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            FORT_MENU: [
                CallbackQueryHandler(upgrade_fort, pattern='^upgrade_fort$'),
                CallbackQueryHandler(castle_menu, pattern='^castle_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            WORKSHOP_MENU: [
                CallbackQueryHandler(upgrade_workshop, pattern='^upgrade_workshop$'),
                CallbackQueryHandler(castle_menu, pattern='^castle_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            COUNTRY_MANAGEMENT: [
                CallbackQueryHandler(farm_menu, pattern='^farm_menu$'),
                CallbackQueryHandler(military_exercise, pattern='^military_exercise$'),
                CallbackQueryHandler(send_message_to_user, pattern='^send_message_to_country$'),
                CallbackQueryHandler(trade_menu, pattern='^trade_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            INTERNET_CONTROL: [
                CallbackQueryHandler(nationalize_internet, pattern='^nationalize_internet$'),
                CallbackQueryHandler(upgrade_internet, pattern='^upgrade_internet$'),
                CallbackQueryHandler(process_internet_upgrade, pattern='^upgrade_to_'),
                CallbackQueryHandler(country_management, pattern='^country_management$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            REFINERY_MENU: [
                CallbackQueryHandler(upgrade_refinery, pattern='^upgrade_refinery$'),
                CallbackQueryHandler(country_management, pattern='^country_management$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            MILITARY_EXERCISE_TYPE: [
                CallbackQueryHandler(select_exercise_type, pattern='^exercise_'),
                CallbackQueryHandler(country_management, pattern='^country_management$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            GET_EXERCISE_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_exercise_code)
            ],
            TRADE_MENU: [
                CallbackQueryHandler(normal_trade, pattern='^normal_trade$'),
                CallbackQueryHandler(discreet_trade, pattern='^discreet_trade$'),
                CallbackQueryHandler(country_management, pattern='^country_management$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_SELECT_TARGET: [
                CallbackQueryHandler(select_trade_target, pattern='^trade_target_'),
                CallbackQueryHandler(trade_menu, pattern='^trade_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_DOMAIN_SELECTION: [
                CallbackQueryHandler(select_trade_domain, pattern='^trade_domain_'),
                CallbackQueryHandler(trade_menu, pattern='^trade_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_ADD_ITEMS: [
                CallbackQueryHandler(add_send_item, pattern='^add_send_item$'),
                CallbackQueryHandler(add_receive_item, pattern='^add_receive_item$'),
                CallbackQueryHandler(confirm_trade, pattern='^confirm_trade$'),
                CallbackQueryHandler(trade_menu, pattern='^trade_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_SEND_ITEM_CATEGORY: [
                CallbackQueryHandler(select_send_item_category, pattern='^trade_send_'),
                CallbackQueryHandler(select_trade_domain, pattern='^trade_domain_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_SEND_ITEM_SELECT: [
                CallbackQueryHandler(select_send_item, pattern='^trade_send_item_'),
                CallbackQueryHandler(add_send_item, pattern='^add_send_item$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_GET_SEND_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_send_amount)
            ],
            TRADE_RECEIVE_ITEM_CATEGORY: [
                CallbackQueryHandler(select_receive_item_category, pattern='^trade_receive_'),
                CallbackQueryHandler(add_receive_item, pattern='^add_receive_item$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_RECEIVE_ITEM_SELECT: [
                CallbackQueryHandler(select_receive_item, pattern='^trade_receive_item_'),
                CallbackQueryHandler(add_receive_item, pattern='^add_receive_item$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            TRADE_GET_RECEIVE_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_receive_amount)
            ],
            TRADE_CONFIRMATION: [
                CallbackQueryHandler(confirm_trade, pattern='^confirm_trade$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ADMIN_TRADE_SETTINGS: [
                CallbackQueryHandler(toggle_trade_enabled, pattern='^toggle_trade_enabled$'),
                CallbackQueryHandler(toggle_discreet_trade, pattern='^toggle_discreet_trade$'),
                CallbackQueryHandler(set_max_trades, pattern='^set_max_trades$'),
                CallbackQueryHandler(set_trade_channel, pattern='^set_trade_channel$'),
                CallbackQueryHandler(set_discreet_trade_channel, pattern='^set_discreet_trade_channel$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            SET_MAX_TRADES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_max_trades)
            ],
            SET_TRADE_CHANNEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_trade_channel)
            ],
            SELECT_USER_TO_MESSAGE: [
                CallbackQueryHandler(select_user_for_message, pattern='^select_user_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            GET_MESSAGE_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, send_user_message)
            ],
            MANAGE_NOTIFICATION_IMAGES: [
                CallbackQueryHandler(set_notification_image_handler, pattern="^set_(religion|internet_on|internet_off|trade_land|trade_air|trade_sea|attack|exercise_land|exercise_sea|exercise_air|missile_attack|film|game|music|top_oil|top_satisfaction)_image$"),
                CallbackQueryHandler(back_to_admin_panel, pattern="^admin_panel$")
            ],
            GET_NOTIFICATION_IMAGE: [
                MessageHandler(filters.PHOTO, save_notification_image),
                CallbackQueryHandler(back_to_admin_panel, pattern="^admin_panel$")
            ],
            RANDOM_PRIZE_MENU: [
                CallbackQueryHandler(select_prize_category, pattern='^prize_'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            SELECT_PRIZE_CATEGORY: [
                CallbackQueryHandler(select_prize_item, pattern='^prize_item_'),
                CallbackQueryHandler(random_prize_menu, pattern='^random_prize_menu$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            GET_PRIZE_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_prize_quantity)
            ],
            CONFIRM_RANDOM_PRIZE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_random_prize)
            ],
            MISSILE_ATTACK_SELECT_TARGET: [
                CallbackQueryHandler(select_missile_target, pattern='^missile_target_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            MISSILE_ATTACK_SELECT_MISSILE: [
                CallbackQueryHandler(select_missile_type, pattern='^select_missile_'),
                CallbackQueryHandler(missile_attack_menu, pattern='^missile_attack_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            MISSILE_ATTACK_GET_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_missile_quantity)
            ],
            MISSILE_ATTACK_SELECT_ZONE: [
                CallbackQueryHandler(select_missile_zone, pattern='^missile_zone_(residential|military|economic)$'),
                CallbackQueryHandler(missile_attack_menu, pattern='^missile_attack_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            MISSILE_ATTACK_CONFIRM: [
                CallbackQueryHandler(confirm_missile_attack, pattern='^confirm_missile_attack$'),
                CallbackQueryHandler(missile_change_zone, pattern='^missile_change_zone$'),
                CallbackQueryHandler(missile_attack_menu, pattern='^missile_attack_menu$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CAMPAIGN_SELECT_TARGET: [
                CallbackQueryHandler(campaign_select_target, pattern='^campaign_target_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CAMPAIGN_SELECT_TYPES: [
                CallbackQueryHandler(campaign_toggle_type, pattern='^campaign_toggle_(air|land|sea)$'),
                CallbackQueryHandler(campaign_start_input, pattern='^campaign_start_input$'),
                CallbackQueryHandler(campaign_back_targets, pattern='^campaign_back_targets$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CAMPAIGN_GET_EQUIPMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, campaign_get_equipment),
                CallbackQueryHandler(campaign_cancel, pattern='^campaign_cancel$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CAMPAIGN_GET_SCENARIO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, campaign_get_scenario),
                CallbackQueryHandler(campaign_cancel, pattern='^campaign_cancel$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CAMPAIGN_CONFIRM: [
                CallbackQueryHandler(campaign_final_send, pattern='^campaign_final_send$'),
                CallbackQueryHandler(campaign_cancel, pattern='^campaign_cancel$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ROLE_SENA_MENU: [
                CallbackQueryHandler(role_sena_pick_category, pattern='^role_sena_cat_(security|economic|sabotage|sena)$'),
                CallbackQueryHandler(role_sena_back, pattern='^role_sena_back$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ROLE_SENA_GET_CONTENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, role_sena_get_content),
                CallbackQueryHandler(role_sena_back, pattern='^role_sena_back$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            ROLE_SENA_LIMITS_MENU: [
                CallbackQueryHandler(role_sena_toggle_category, pattern='^role_sena_toggle_(security|economic|sabotage|sena)$'),
                CallbackQueryHandler(role_sena_set_limit_start, pattern='^role_sena_set_limit_(role|sena)$'),
                CallbackQueryHandler(role_sena_set_limit_start, pattern='^role_sena_set_max_chars$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            ROLE_SENA_GET_LIMIT_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, role_sena_save_limit_value),
                CallbackQueryHandler(back_to_admin_panel, pattern='^admin_panel$')
            ],
            CONSTRUCTION_CATEGORY: [
                CallbackQueryHandler(select_construction_category, pattern='^construction_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CONSTRUCTION_SELECT_PROJECT: [
                CallbackQueryHandler(select_construction_project, pattern='^select_project_'),
                CallbackQueryHandler(construction_proposal_start, pattern='^construction_proposal_start$'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
            CONSTRUCTION_CONFIRM: [
                CallbackQueryHandler(confirm_construction, pattern='^confirm_construction$'),
                CallbackQueryHandler(select_construction_category, pattern='^construction_'),
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$')
            ],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    # ConversationHandler مدیریت تجهیزات (ورود با پیام «مدیریت تجهیزات» در پی‌وی)
    equip_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.TEXT & filters.Regex(r'^\s*مدیریت تجهیزات\s*$'),
                equip_manage_entry
            )
        ],
        states={
            EQUIP_MANAGE_MENU: [
                CallbackQueryHandler(equip_add_start, pattern='^equip_add_start$'),
                CallbackQueryHandler(equip_preset_save_start, pattern='^equip_preset_save_start$'),
                CallbackQueryHandler(equip_preset_menu, pattern='^equip_preset_menu$'),
                CallbackQueryHandler(equip_preset_delete, pattern='^equip_preset_del_'),
                CallbackQueryHandler(equip_preset_load_confirm, pattern='^equip_preset_load_\\d+$'),
                CallbackQueryHandler(equip_new_list_start, pattern='^equip_new_list_start$'),
                CallbackQueryHandler(equip_new_list_apply, pattern='^equip_new_list_(keep|reset)$'),
                CallbackQueryHandler(equip_category_menu, pattern='^equip_category_menu$'),
                CallbackQueryHandler(equip_delete_category, pattern='^equip_del_cat_'),
                CallbackQueryHandler(equip_new_category_start, pattern='^equip_new_cat$'),
                CallbackQueryHandler(equip_close, pattern='^equip_close$'),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, equip_delete_by_text),
            ],
            EQUIP_ADD_GET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equip_add_get_name),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
            EQUIP_ADD_GET_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equip_add_get_price),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
            EQUIP_ADD_GET_CATEGORY: [
                CallbackQueryHandler(equip_pick_category, pattern='^equip_pick_cat_'),
                CallbackQueryHandler(equip_new_category_start, pattern='^equip_new_cat$'),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
            EQUIP_NEW_CATEGORY_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equip_new_category_save),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
            EQUIP_PRESET_SAVE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equip_preset_save),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
            EQUIP_PRESET_LOAD_CONFIRM: [
                CallbackQueryHandler(equip_preset_load_apply, pattern='^equip_preset_load_(keep|reset)$'),
                CallbackQueryHandler(equip_preset_menu, pattern='^equip_preset_menu$'),
                CallbackQueryHandler(equip_back_menu, pattern='^equip_back_menu$'),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", equip_close),
            MessageHandler(
                filters.TEXT & filters.Regex(r'^\s*مدیریت تجهیزات\s*$'),
                equip_manage_entry
            ),
        ],
        per_user=True,
        per_chat=True,
        allow_reentry=True,
    )

    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("set_d", set_d_command))
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r".*تنظیم دارایی.*"),
            set_darayi_by_chat
        ),
        group=-1
    )

    # هندلرهای تنظیم/افزودن کشور مستقیم در گپ (اکتیویت + افزودن)
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^\s*راهنما\s*$"),
            help_text_command
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r".*(?:تنظیم|افزودن) کشور.*"),
            set_country_by_chat
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r".*تنظیم صاحب.*"),
            set_owner_by_chat
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r".*تنیم صاحب.*"),
            set_owner_by_chat
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r".*حذف کشور.*"),
            delete_country_by_chat
        ),
        group=-1
    )

    # هندلرهای اکتویت/دیاکتویت/منو در گپ (با اولویت بالا تا قبل از conv_handler اجرا شوند)
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*اکتویت\s*$'),
            activate_chat_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*دیاکتویت\s*$'),
            deactivate_chat_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*منو\s*$'),
            menu_in_group_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*پنل\s*$'),
            panel_in_group_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.TEXT & filters.Regex(r'^\s*پنل\s*$'),
            panel_private_handler
        ),
        group=-1
    )

    # ابتدا equip_conv_handler ثبت شود تا روی متن «مدیریت تجهیزات» تقدم داشته باشد
    application.add_handler(equip_conv_handler)
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(edit_storage_capacity, pattern='^edit_storage_capacity$'))
    application.add_handler(CallbackQueryHandler(select_country_for_storage, pattern='^storage_country_'))
    application.add_handler(CallbackQueryHandler(set_storage_level, pattern='^storage_set_level_'))
    application.add_handler(CallbackQueryHandler(storage_custom_input_prompt, pattern='^storage_custom_input$'))
    # NOTE: get_new_storage_capacity به صورت global ثبت نمی‌شود تا مکالمات دیگر را هایجک نکند؛ ظرفیت از طریق حالت ADMIN_MENU و با چک storage_edit_user_id مدیریت می‌شود
    application.add_handler(CommandHandler("daily_production", run_daily_production_manually))

    application.add_handler(CallbackQueryHandler(siege_callback_handler, pattern='^siege_(return|join)_'))
    application.add_handler(CallbackQueryHandler(handle_proposal_callback, pattern='^(approve|reject)_'))
    application.add_handler(CallbackQueryHandler(handle_trade_response, pattern='^(accept|reject|cancel)_trade_'))
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
