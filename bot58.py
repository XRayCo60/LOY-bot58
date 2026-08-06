#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ø¨Ù‡ Ù†Ø§Ù… Ø®Ø¯Ø§ - Ø±Ø¨Ø§Øª Ø¬Ù†Ú¯ Ø¬Ù‡Ø§Ù†ÛŒ

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
DATABASE_NAME = "world_war_game3.db"
BOT_NAME = "Ø¬Ù†Ú¯â€ŒØ¬Ù‡Ø§Ù†ÛŒ"

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
    ROLE_SENA_GET_LIMIT_VALUE
) = range(86)

ASSET_NAMES = {
    'soldier': "Ø³Ø±Ø¨Ø§Ø² Ø³Ø§Ø¯Ù‡ ðŸ‘¤",
    'special_soldier': "Ø³Ø±Ø¨Ø§Ø² ÙˆÛŒÚ˜Ù‡ ðŸª–",
    'commando': "ØªÚ©Ø§ÙˆØ± ðŸ¥·",
    'sniper': "Ø§Ø³Ù†Ø§ÛŒÙ¾Ø± ðŸ’‚",
    'rpg_soldier': "Ø§Ø±Ù¾ÛŒØ¬ÛŒ Ø²Ù† ðŸ§¨",
    'leopard_tank': "ØªØ§Ù†Ú© (Leopard)",
    't90_tank': "ØªØ§Ù†Ú© (T-90)",
    'abrams_tank': "ØªØ§Ù†Ú© (Abrams)",
    'challenger_tank': "ØªØ§Ù†Ú© (Challenger)",
    'merkava_tank': "ØªØ§Ù†Ú© (Merkava)",
    'su57': "Ø¬Ù†Ú¯Ù†Ø¯Ù‡ (Su-57)",
    'f22': "Ø¬Ù†Ú¯Ù†Ø¯Ù‡ (F-22)",
    'su35': "Ø¬Ù†Ú¯Ù†Ø¯Ù‡ (Su-35)",
    'f35': "Ø¬Ù†Ú¯Ù†Ø¯Ù‡ (F-35)",
    'f16': "Ø¬Ù†Ú¯Ù†Ø¯Ù‡ (F-16)",
    'b2_spirit': "Ø¨Ù…Ø¨â€ŒØ§ÙÚ©Ù† (B-2 Spirit)",
    'b1_lancer': "Ø¨Ù…Ø¨â€ŒØ§ÙÚ©Ù† (B-1B Lancer)",
    'tu160': "Ø¨Ù…Ø¨â€ŒØ§ÙÚ©Ù† (Tu-160)",
    'tu95': "Ø¨Ù…Ø¨â€ŒØ§ÙÚ©Ù† (Tu-95)",
    'spy_drone': "Ù¾Ù‡Ø¨Ø§Ø¯ Ø¬Ø§Ø³ÙˆØ³ÛŒ ðŸ›¸",
    'kamikaze_drone': "Ù¾Ù‡Ø¨Ø§Ø¯ Ø§Ù†ØªØ­Ø§Ø±ÛŒ ðŸ›¸",
    'cruise_drone': "Ù¾Ù‡Ø¨Ø§Ø¯ Ú©Ø±ÙˆØ²",
    'hermes_drone': "Ù¾Ù‡Ø¨Ø§Ø¯ (Hermes)",
    'v2': "Ù…ÙˆØ´Ú© (V-2)",
    'df41': "Ù…ÙˆØ´Ú© (DF-41)",
    'kheibar': "Ù…ÙˆØ´Ú© (Ø®ÛŒØ¨Ø±Ø´Ú©Ù†)",
    'minuteman': "Ù…ÙˆØ´Ú© (Minuteman)",
    'satan2': "Ù…ÙˆØ´Ú© (Satan-2)",
    'nuclear_rocket': "Ù…ÙˆØ´Ú© Ù‡Ø³ØªÙ‡â€ŒØ§ÛŒ â˜¢ï¸",
    'm777': "ØªÙˆÙ¾Ø®Ø§Ù†Ù‡ (M777)",
    'pzh2000': "ØªÙˆÙ¾Ø®Ø§Ù†Ù‡ (PzH 2000)",
    'caesar': "ØªÙˆÙ¾Ø®Ø§Ù†Ù‡ (CAESAR)",
    'himars': "Ø±Ø§Ú©Øªâ€ŒØ§Ù†Ø¯Ø§Ø² (HIMARS)",
    'nora_b52': "ØªÙˆÙ¾Ø®Ø§Ù†Ù‡ (Nora B-52)",
    'uss_gerald': "Ù†Ø§Ùˆ (USS Gerald)",
    'uss_nimitz': "Ù†Ø§Ùˆ (USS Nimitz)",
    'fujian': "Ù†Ø§Ùˆ (Fujian)",
    'charles_de_gaulle': "Ù†Ø§Ùˆ (Charles de Gaulle)",
    'virginia_sub': "Ø²ÛŒØ±Ø¯Ø±ÛŒØ§ÛŒÛŒ (Virginia)",
    'patriots': "Ù¾Ø¯Ø§ÙÙ†Ø¯ (Patriots)",
    's300': "Ù¾Ø¯Ø§ÙÙ†Ø¯ (S-300)",
    'iron_dome': "Ù¾Ø¯Ø§ÙÙ†Ø¯ (Iron Dome)",
    's400': "Ù¾Ø¯Ø§ÙÙ†Ø¯ (S-400)",
    'thaad': "Ù¾Ø¯Ø§ÙÙ†Ø¯ (THAAD)",
    'mines': "Ù…ÛŒÙ†â€ŒÙ‡Ø§ÛŒ Ø²Ù…ÛŒÙ†ÛŒ âš ï¸",
    'oil_barrels': "Ù†ÙØª ðŸ›¢ï¸",
    'satisfaction': "Ø±Ø¶Ø§ÛŒØª ðŸ˜Š",
    'crypto': "Ø§Ø±Ø² Ø¯ÛŒØ¬ÛŒØªØ§Ù„ â‚¿",
    'security': "Ø§Ù…Ù†ÛŒØª ðŸ›¡ï¸",
    'daily_income': "Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡ ðŸ’¹",
    'population': "Ø¬Ù…Ø¹ÛŒØª ðŸ‘«",
    'capital': "Ø³Ø±Ù…Ø§ÛŒÙ‡ ðŸ’°",
    'internet_level': "Ø§ÛŒÙ†ØªØ±Ù†Øª (G)",
    'trade_land': "ØªØ¬Ø§Ø±Øª Ø²Ù…ÛŒÙ†ÛŒ ðŸŒ",
    'trade_air': "ØªØ¬Ø§Ø±Øª Ù‡ÙˆØ§ÛŒÛŒ âœˆï¸",
    'trade_sea': "ØªØ¬Ø§Ø±Øª Ø¯Ø±ÛŒØ§ÛŒÛŒ âš“",
    'attack': "Ø­Ù…Ù„Ù‡ Ù†Ø¸Ø§Ù…ÛŒ âš”ï¸",
    'hacker': "Ù‡Ú©Ø± Ø³Ø§ÛŒØ¨Ø±ÛŒ ðŸ’»",
    'refinery_level': "Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ù†ÙØª ðŸ›¢ï¸"
}

DEFAULT_ASSETS = {
    'population': 15000000,
    'capital': 100000000,
    'oil_barrels': 100,
    'satisfaction': 50,
    'daily_income': 0,
    'custom_income': 0,
    'loan_amount': 0,
    'loan_date': None,
    'crypto': 0,
    'religion': "islam",
    'security': 50,
    'internet_nationalized': False,
    'internet_level': 2,
    'refinery_level': 0,
    'land_troops': {
        'soldier': 0,
        'special_soldier': 0,
        'commando': 0,
        'sniper': 0,
        'rpg_soldier': 0,
        'leopard_tank': 0,
        't90_tank': 0,
        'abrams_tank': 0,
        'challenger_tank': 0,
        'merkava_tank': 0
    },
    'air_troops': {
        'su57': 0,
        'f22': 0,
        'su35': 0,
        'f35': 10,
        'f16': 0,
        'b2_spirit': 0,
        'b1_lancer': 0,
        'tu160': 0,
        'tu95': 0,
        'spy_drone': 0,
        'kamikaze_drone': 0,
        'cruise_drone': 0,
        'hermes_drone': 0
    },
    'rockets': {
        'v2': 0,
        'df41': 0,
        'kheibar': 0,
        'minuteman': 0,
        'satan2': 0,
        'nuclear_rocket': 0
    },
    'artillery': {
        'm777': 0,
        'pzh2000': 0,
        'caesar': 0,
        'himars': 0,
        'nora_b52': 0
    },
    'naval_troops': {
        'uss_gerald': 0,
        'uss_nimitz': 5,
        'fujian': 0,
        'charles_de_gaulle': 0,
        'virginia_sub': 0
    },
    'defenses': {
        'patriots': 0,
        's300': 0,
        'iron_dome': 0,
        's400': 0,
        'thaad': 0,
        'mines': 0
    },
    'cyber_troops': {
        'hacker': 0
    },
    'disabled_buttons': []
}

ASSET_PRICES = {
    'soldier': 5000,
    'special_soldier': 18000,
    'commando': 30000,
    'sniper': 42000,
    'rpg_soldier': 7500,
    'leopard_tank': 120000,
    't90_tank': 145000,
    'abrams_tank': 190000,
    'challenger_tank': 310000,
    'merkava_tank': 375000,
    'su57': 31000000,
    'f22': 24000000,
    'su35': 15000000,
    'f35': 37500000,
    'f16': 19000000,
    'b2_spirit': 155000000,
    'b1_lancer': 95000000,
    'tu160': 62000000,
    'tu95': 28000000,
    'spy_drone': 1200000,
    'kamikaze_drone': 500000,
    'cruise_drone': 755000,
    'hermes_drone': 950000,
    'v2': 1000000,
    'df41': 2200000,
    'kheibar': 3500000,
    'minuteman': 5000000,
    'satan2': 7700000,
    'nuclear_rocket': 600000000,
    'm777': 25000,
    'pzh2000': 38000,
    'caesar': 52000,
    'himars': 110000,
    'nora_b52': 250000,
    'uss_gerald': 30000000,
    'uss_nimitz': 41000000,
    'fujian': 45000000,
    'charles_de_gaulle': 55000000,
    'virginia_sub': 32000000,
    'patriots': 22000000,
    's300': 27000000,
    'iron_dome': 35000000,
    's400': 42000000,
    'thaad': 50000000,
    'mines': 50000,
    'oil_barrels': 0,
    'satisfaction': 0,
    'crypto': 100000,
    'security': 0,
    'daily_income': 0,
    'population': 0,
    'capital': 0,
    'internet_level': 0,
    'trade_land': 0,
    'trade_air': 0,
    'trade_sea': 0,
    'attack': 0,
    'hacker': 1000000,
    'internet_upgrade_3g': 15000000,
    'internet_upgrade_4g': 30000000,
    'internet_upgrade_5g': 45000000,
    'internet_upgrade_6g': 60000000,
    'internet_upgrade_7g': 75000000,
    'refinery_upgrade_level1': 25000000,
    'refinery_upgrade_level2': 50000000,
    'refinery_upgrade_level3': 75000000,
    'refinery_upgrade_level4': 100000000,
    'refinery_upgrade_level5': 125000000,
    'refinery_upgrade_level6': 150000000,
    'refinery_upgrade_level7': 175000000
}

ASSET_CATEGORIES_FOR_DISPLAY = [
    ('land_troops', 'Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø²Ù…ÛŒÙ†ÛŒ ðŸª–'),
    ('air_troops', 'Ù†ÛŒØ±ÙˆÛŒ Ù‡ÙˆØ§ÛŒÛŒ âœˆï¸'),
    ('naval_troops', 'Ù†ÛŒØ±ÙˆÛŒ Ø¯Ø±ÛŒØ§ÛŒÛŒ ðŸš¢'),
    ('rockets', 'Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ ðŸš€'),
    ('defenses', 'Ù¾Ø¯Ø§ÙÙ†Ø¯ ðŸ›¡ï¸'),
    ('cyber_troops', 'Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø³Ø§ÛŒØ¨Ø±ÛŒ ðŸ’»'),
]

BOT_MAIN_MENU_BUTTONS = [
    {"text": "ðŸ“Š Ù„ÛŒØ³Øª Ø¯Ø§Ø±Ø§ÛŒÛŒ", "callback_data": "show_assets"},
    {"text": "âš”ï¸ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ", "callback_data": "campaign_menu"},
    {"text": "🛸 حمله پهپادی", "callback_data": "drone_attack_menu"},
    {"text": "ðŸš€ Ø­Ù…Ù„Ù‡ Ù…ÙˆØ´Ú©ÛŒ", "callback_data": "missile_attack_menu"},
    {"text": "ðŸ“œ Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§", "callback_data": "role_sena_menu"},
    {"text": "ðŸ—ï¸ Ø§Ø±Ø³Ø§Ù„ Ø³Ø§Ø®Øª Ùˆ Ø³Ø§Ø²", "callback_data": "construction_proposal_start"},
    {"text": "ðŸ›’ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®Ø±ÛŒØ¯", "callback_data": "shop_menu_start"},
    {"text": "â˜ªï¸ ØªÙ†Ø¸ÛŒÙ… Ø¯ÛŒÙ†", "callback_data": "religion_menu"},
    {"text": "ðŸ“£ Ø§Ø±Ø³Ø§Ù„ Ø¨ÛŒØ§Ù†ÛŒÙ‡", "callback_data": "statement_proposal_start"},
    {"text": "ðŸ›ï¸ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ø´ÙˆØ±", "callback_data": "country_management"}
]

ADMIN_PANEL_BUTTONS = [
    {"text": "âž• Ø§ÙØ²ÙˆØ¯Ù† Ú©Ø´ÙˆØ± Ø¬Ø¯ÛŒØ¯", "callback_data": "add_country"},
    {"text": "ðŸ—‘ï¸ Ø­Ø°Ù Ú©Ø´ÙˆØ±", "callback_data": "delete_country_menu"},
    {"text": "ðŸ“‹ Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§", "callback_data": "list_countries"},
    {"text": "âš™ï¸ ÙˆÛŒØ±Ø§ÛŒØ´ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø§ØµÙ„ÛŒ", "callback_data": "edit_main_props"},
    {"text": "âš”ï¸ ÙˆÛŒØ±Ø§ÛŒØ´ Ù†ÛŒØ±ÙˆÙ‡Ø§ Ùˆ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§", "callback_data": "edit_assets_menu"},
    {"text": "\u0622\u067e \u062f\u0627\u0631\u0627\u06cc\u06cc", "callback_data": "admin_update_assets"},
    {"text": "📦 ویرایش ظرفیت انبار", "callback_data": "edit_storage_capacity"},
    {"text": "ðŸ“Š Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¯Ø§Ø±Ø§ÛŒÛŒ Ú©Ø´ÙˆØ±Ù‡Ø§", "callback_data": "select_country_view_assets"},
    {"text": "ðŸ‘‘ Ø§ÙØ²ÙˆØ¯Ù† Ø§Ø¯Ù…ÛŒÙ†", "callback_data": "add_admin"},
    {"text": "ðŸ—‘ Ø­Ø°Ù Ø§Ø¯Ù…ÛŒÙ†", "callback_data": "remove_admin"},
    {"text": "ðŸ”Œ Ø®Ø§Ù…ÙˆØ´/Ø±ÙˆØ´Ù† Ø±Ø¨Ø§Øª", "callback_data": "toggle_bot"},
    {"text": "âš™ï¸ Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ÛŒ Ø¹Ù…ÙˆÙ…ÛŒ", "callback_data": "manage_global_buttons"},
    {"text": "ðŸš¦ ØªØ¹ÛŒÛŒÙ† Ù…Ø­Ø¯ÙˆØ¯ÛŒØª", "callback_data": "role_sena_limits_menu"},
    {"text": "ðŸ¤ Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ø§Ø±Øª", "callback_data": "trade_settings"},
    {"text": "ðŸ–¼ï¸ Ù…Ø¯ÛŒØ±ÛŒØª Ø¹Ú©Ø³ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡â€ŒÙ‡Ø§", "callback_data": "manage_notification_images"},
    {"text": "ðŸŽ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…", "callback_data": "random_prize_menu"},
    {"text": "ðŸ›¢ï¸ Ø§Ø¹Ù„Ø§Ù… Ø¨Ø±ØªØ±ÛŒÙ† Ù†ÙØª", "callback_data": "announce_top_oil"},
    {"text": "ðŸ˜Š Ø§Ø¹Ù„Ø§Ù… Ø¨Ø±ØªØ±ÛŒÙ† Ø±Ø¶Ø§ÛŒØª", "callback_data": "announce_top_satisfaction"}
]

RELIGIONS = [
    ("islam", "Ø§Ø³Ù„Ø§Ù… â˜ªï¸"),
    ("christianity", "Ù…Ø³ÛŒØ­ÛŒØª âœï¸"),
    ("judaism", "ÛŒÙ‡ÙˆØ¯ÛŒØª âœ¡ï¸"),
    ("buddhism", "Ø¨ÙˆØ¯ÛŒØ³Ù… â˜¸ï¸"),
    ("hinduism", "Ù‡Ù†Ø¯ÙˆØ¦ÛŒØ³Ù… ðŸ•‰ï¸"),
    ("atheism", "Ø§Ù„Ø­Ø§Ø¯ âš›ï¸"),
]

PROPOSAL_TYPES = {
    "defense": "Ø¯ÙØ§Ø¹ÛŒ",
    "construction": "Ø³Ø§Ø®Øª Ùˆ Ø³Ø§Ø²",
    "economic": "Ø§Ù‚ØªØµØ§Ø¯ÛŒ",
    "attack": "Ø­Ù…Ù„Ù‡",
    "campaign": "Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ",
    "electricity_price": "ØªØºÛŒÛŒØ± Ù‚ÛŒÙ…Øª Ø¨Ø±Ù‚"
}

TRADE_DOMAINS = [
    ("land", "ØªØ¬Ø§Ø±Øª Ø²Ù…ÛŒÙ†ÛŒ ðŸŒ"),
    ("air", "ØªØ¬Ø§Ø±Øª Ù‡ÙˆØ§ÛŒÛŒ âœˆï¸"),
    ("sea", "ØªØ¬Ø§Ø±Øª Ø¯Ø±ÛŒØ§ÛŒÛŒ âš“")
]

CONSTRUCTION_PROJECTS = {
    "film": {
        "lunar_veil": {"name": "Lunar Veil", "cost": 180000000, "daily_income": 148500000, "description": "ÙÛŒÙ„Ù… ØªØ±Ø³Ù†Ø§Ú© Ø¨Ø§ Ù…ÙˆØ¶ÙˆØ¹ Ù…Ø§Ù‡ Ùˆ Ø±Ù…Ø² Ùˆ Ø±Ø§Ø²"},
        "neon_rift": {"name": "Neon Rift", "cost": 187654321, "daily_income": 168888889, "description": "ÙÛŒÙ„Ù… Ø¹Ù„Ù…ÛŒ ØªØ®ÛŒÙ„ÛŒ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ Ø³Ø§ÛŒØ¨Ø±Ù¾Ø§Ù†Ú©"},
        "midnight_echo": {"name": "Midnight Echo", "cost": 213456789, "daily_income": 192111110, "description": "ÙÛŒÙ„Ù… Ù‡ÛŒØ¬Ø§Ù†â€ŒØ§Ù†Ú¯ÛŒØ² Ø±ÙˆØ§Ù†Ø´Ù†Ø§Ø®ØªÛŒ Ø¨Ø§ Ø¯Ø§Ø³ØªØ§Ù†ÛŒ Ù¾ÛŒÚ†ÛŒØ¯Ù‡"},
        "crimson_twilight": {"name": "Crimson Twilight", "cost": 235000000, "daily_income": 198250000, "description": "ÙÛŒÙ„Ù… Ø¯Ø±Ø§Ù… Ù…Ù‡ÛŒØ¬ Ø¨Ø§ Ø¯Ø§Ø³ØªØ§Ù† Ø¹Ø§Ø´Ù‚Ø§Ù†Ù‡"},
        "nova_quest": {"name": "Nova Quest", "cost": 260000000, "daily_income": 195000000, "description": "ÙÛŒÙ„Ù… Ø¹Ù„Ù…ÛŒ ØªØ®ÛŒÙ„ÛŒ Ø¨Ø§ Ø¬Ù„ÙˆÙ‡â€ŒÙ‡Ø§ÛŒ ÙˆÛŒÚ˜Ù‡ Ø®ÛŒØ±Ù‡â€ŒÚ©Ù†Ù†Ø¯Ù‡"},
        "silver_horizon": {"name": "Silver Horizon", "cost": 280000000, "daily_income": 196000000, "description": "ÙÛŒÙ„Ù… Ù…Ø§Ø¬Ø±Ø§Ø¬ÙˆÛŒÛŒ Ø¯Ø± ÙØ¶Ø§ÛŒ ÙˆØ³ÛŒØ¹ Ùˆ Ù¾Ø± Ø±Ù…Ø² Ùˆ Ø±Ø§Ø²"},
        "ghost_river": {"name": "Ghost River", "cost": 320000000, "daily_income": 224000000, "description": "ÙÛŒÙ„Ù… ØªØ±Ø³Ù†Ø§Ú© Ø¨Ø§ Ø¯Ø§Ø³ØªØ§Ù†â€ŒÙ‡Ø§ÛŒ ÙØ±Ø§Ø·Ø¨ÛŒØ¹ÛŒ"},
        "frozen_echo": {"name": "Frozen Echo", "cost": 310000000, "daily_income": 260800000, "description": "ÙÛŒÙ„Ù… Ø¹Ù„Ù…ÛŒ ØªØ®ÛŒÙ„ÛŒ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ Ø¢ÛŒÙ†Ø¯Ù‡"},
        "silent_storm": {"name": "Silent Storm", "cost": 345678912, "daily_income": 311111020, "description": "ÙÛŒÙ„Ù… Ø§Ú©Ø´Ù† Ù…Ù‡ÛŒØ¬ Ø¯Ø± Ø¯Ù„ Ø·ÙˆÙØ§Ù†"}
    },
    "game": {
        "shadow_rider": {"name": "Shadow Rider", "cost": 210000000, "daily_income": 157500000, "description": "Ø¨Ø§Ø²ÛŒ Ù…Ø³Ø§Ø¨Ù‚Ù‡â€ŒØ§ÛŒ Ø¨Ø§ Ø³Ø±Ø¹Øª Ø¨Ø§Ù„Ø§ Ùˆ Ù‡ÛŒØ¬Ø§Ù†â€ŒØ§Ù†Ú¯ÛŒØ²"},
        "galactic_rush": {"name": "Galactic Rush", "cost": 215000000, "daily_income": 179750000, "description": "Ø¨Ø§Ø²ÛŒ Ù…Ø³Ø§Ø¨Ù‚Ù‡â€ŒØ§ÛŒ Ø¯Ø± ÙØ¶Ø§"},
        "star_haven": {"name": "Star Haven", "cost": 224567890, "daily_income": 202111101, "description": "Ø¨Ø§Ø²ÛŒ Ù…Ø§Ø¬Ø±Ø§Ø¬ÙˆÛŒÛŒ Ø¯Ø± ÙØ¶Ø§ Ø¨Ø§ Ú¯Ø±Ø§ÙÛŒÚ© Ø®ÛŒØ±Ù‡â€ŒÚ©Ù†Ù†Ø¯Ù‡"},
        "dark_realm": {"name": "Dark Realm", "cost": 270000000, "daily_income": 224000000, "description": "Ø¨Ø§Ø²ÛŒ Ù…Ø§Ø¬Ø±Ø§Ø¬ÙˆÛŒÛŒ ÙØ§Ù†ØªØ²ÛŒ"},
        "shadow_quest": {"name": "Shadow Quest", "cost": 278945612, "daily_income": 251051050, "description": "Ø¨Ø§Ø²ÛŒ Ù†Ù‚Ø´â€ŒØ¢ÙØ±ÛŒÙ†ÛŒ ØªØ§Ø±ÛŒÚ© Ø¨Ø§ Ø¯Ø§Ø³ØªØ§Ù† Ø¬Ø°Ø§Ø¨"},
        "galaxy_wars": {"name": "Galaxy Wars", "cost": 300000000, "daily_income": 210000000, "description": "Ø¨Ø§Ø²ÛŒ Ø§Ø³ØªØ±Ø§ØªÚ˜ÛŒÚ© Ø¯Ø± ÙØ¶Ø§ Ø¨Ø§ Ù†Ø¨Ø±Ø¯Ù‡Ø§ÛŒ Ù¾ÛŒÚ†ÛŒØ¯Ù‡"},
        "iron_forge": {"name": "Iron Forge", "cost": 350000000, "daily_income": 245000000, "description": "Ø¨Ø§Ø²ÛŒ Ù†Ù‚Ø´â€ŒØ¢ÙØ±ÛŒÙ†ÛŒ Ø­Ù…Ø§Ø³ÛŒ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ ÙØ§Ù†ØªØ²ÛŒ"},
        "iron_clash": {"name": "Iron Clash", "cost": 389123456, "daily_income": 350211110, "description": "Ø¨Ø§Ø²ÛŒ Ø§Ø³ØªØ±Ø§ØªÚ˜ÛŒÚ© Ø¬Ù†Ú¯ÛŒ Ø¯Ø± Ø¯Ù†ÛŒØ§ÛŒ Ù…Ø¯Ø±Ù†"},
        "stormbreaker": {"name": "Stormbreaker", "cost": 390000000, "daily_income": 326700000, "description": "Ø¨Ø§Ø²ÛŒ Ø§Ú©Ø´Ù† Ø¨Ø§ Ú¯Ø±Ø§ÙÛŒÚ© ÙÙˆÙ‚â€ŒØ§Ù„Ø¹Ø§Ø¯Ù‡"}
    },
    "music": {
        "digital_love": {"name": "Digital Love", "cost": 60000000, "daily_income": 48000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø§Ù„Ú©ØªØ±ÙˆÙ†ÛŒÚ©"},
        "global_peace": {"name": "Global Peace", "cost": 75000000, "daily_income": 60000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¨Ø±Ø§ÛŒ ØµÙ„Ø­ Ø¬Ù‡Ø§Ù†ÛŒ"},
        "war_anthem": {"name": "War Anthem", "cost": 100000000, "daily_income": 80000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¨Ø§ Ù…Ø¶Ø§Ù…ÛŒÙ† Ø¬Ù†Ú¯ÛŒ"},
        "sunset_dreams": {"name": "Sunset Dreams", "cost": 140000000, "daily_income": 116800000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ù…Ù„Ø§ÛŒÙ… Ùˆ Ø¯Ù„Ù†Ø´ÛŒÙ†"},
        "dawn_horizon": {"name": "Dawn Horizon", "cost": 145678912, "daily_income": 131111020, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø§Ù„Ù‡Ø§Ù…â€ŒØ¨Ø®Ø´ Ùˆ Ø²ÛŒØ¨Ø§"},
        "midnight_melody": {"name": "Midnight Melody", "cost": 150000000, "daily_income": 105000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¢Ø±Ø§Ù…Ø´â€ŒØ¨Ø®Ø´ Ùˆ Ø¯Ù„Ù†Ø´ÛŒÙ†"},
        "sunrise_serenade": {"name": "Sunrise Serenade", "cost": 180000000, "daily_income": 126000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ù…Ù„Ø§ÛŒÙ… Ùˆ Ø§Ù„Ù‡Ø§Ù…â€ŒØ¨Ø®Ø´"},
        "celestial_harmony": {"name": "Celestial Harmony", "cost": 190000000, "daily_income": 159000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¢Ø±Ø§Ù…â€ŒØ¨Ø®Ø´ Ùˆ Ø±ÙˆØ­Ø§Ù†ÛŒ"},
        "echoes_of_time": {"name": "Echoes of Time", "cost": 199876543, "daily_income": 179888888, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¢Ø±Ø§Ù…Ø´â€ŒØ¨Ø®Ø´ Ùˆ Ú©Ù„Ø§Ø³ÛŒÚ©"},
        "electric_dreams": {"name": "Electric Dreams", "cost": 290000000, "daily_income": 203000000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø§Ù„Ú©ØªØ±ÙˆÙ†ÛŒÚ© Ù¾Ø±Ø§Ù†Ø±Ú˜ÛŒ"},
        "pulse_wave": {"name": "Pulse Wave", "cost": 312345678, "daily_income": 281111110, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø§Ù„Ú©ØªØ±ÙˆÙ†ÛŒÚ© Ù¾Ø±Ø§Ù†Ø±Ú˜ÛŒ"},
        "electric_vibes": {"name": "Electric Vibes", "cost": 320000000, "daily_income": 267200000, "description": "Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø§Ù„Ú©ØªØ±ÙˆÙ†ÛŒÚ© Ù¾Ø±Ø§Ù†Ø±Ú˜ÛŒ"}
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
            assets TEXT,
            custom_income INTEGER DEFAULT 0,
            loan_amount INTEGER DEFAULT 0,
            loan_date TEXT,
            crypto INTEGER DEFAULT 0,
            security INTEGER DEFAULT 70,
            internet_nationalized INTEGER DEFAULT 0,
            internet_level INTEGER DEFAULT 2,
            refinery_level INTEGER DEFAULT 0
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
    # Ø¬Ø¯ÙˆÙ„ Ø±ÙˆÙ„/Ø³Ù†Ø§: Ø±Ø¯ÛŒØ§Ø¨ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø±ÙˆØ²Ø§Ù†Ù‡ Ù‡Ø± Ú©Ø§Ø±Ø¨Ø± Ø¯Ø± Ù‡Ø± Ø¯Ø³ØªÙ‡
    c.execute('''
        CREATE TABLE IF NOT EXISTS role_sena_usage (
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            day_key TEXT NOT NULL,
            used_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, category, day_key)
        )
    ''')
    # Ø¬Ø¯ÙˆÙ„ Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ Ø§Ú©ØªÙˆÛŒØªâ€ŒØ´Ø¯Ù‡ Ø¨Ø±Ø§ÛŒ Ù¾Ù„ÛŒØ±Ù‡Ø§
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
    # Ù…Ù‚Ø§Ø¯ÛŒØ± Ø¯ÛŒÙØ§Ù„Øª Ø±ÙˆÙ„/Ø³Ù†Ø§
    # Ù…Ø­Ø¯ÙˆØ¯ÛŒØª ØªØ¬Ù…Ø¹ÛŒ Ø¨Ø±Ø§ÛŒ Ø³Ù‡ Ø¨Ø®Ø´ Ø±ÙˆÙ„ (Ø§Ù…Ù†ÛŒØªÛŒ/Ø§Ù‚ØªØµØ§Ø¯ÛŒ/Ø®Ø±Ø§Ø¨Ú©Ø§Ø±ÛŒ) Ø¨Ù‡â€ŒØµÙˆØ±Øª ØªØ¹Ø¯Ø§Ø¯ Ù¾ÛŒØ§Ù… Ø¯Ø± Ø±ÙˆØ²
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_security_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_economic_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_sabotage_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_total_daily_limit', '10'))
    # Ø³Ù†Ø§
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('sena_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('sena_daily_limit', '3'))
    # Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ± Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ù¾ÛŒØ§Ù… Ø±ÙˆÙ„/Ø³Ù†Ø§ (Ù¾ÛŒØ´â€ŒÙØ±Ø¶: Ûµ ØµÙØ­Ù‡ Ã— 4096)
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ('role_sena_max_chars', str(5 * 4096)))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('trade_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('max_trades', '5'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('trade_channel', STATEMENT_CHANNEL))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('discreet_trade_enabled', '1'))
    c.execute("INSERT OR IGNORE INTO trade_settings (key, value) VALUES (?, ?)", ('discreet_trade_channel', STATEMENT_CHANNEL))
    c.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (OWNER_ID,))

    # Ø¬Ø¯Ø§ÙˆÙ„ Ù…Ø±Ø¨ÙˆØ· Ø¨Ù‡ Ù…Ø¯ÛŒØ±ÛŒØª Ù¾ÙˆÛŒØ§ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª
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
        CREATE TABLE IF NOT EXISTS equipment_presets (
            preset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            preset_name TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

    # Ø³ÛŒØ¯ Ú©Ø±Ø¯Ù† Ø§ÙˆÙ„ÛŒÙ‡ Ø§Ø² Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ø§Ú¯Ø± Ø®Ø§Ù„ÛŒ Ø¨Ø§Ø´Ø¯
    _seed_equipment_from_defaults_if_empty()


def calculate_storage_used(country):
    """محاسبه فضای استفاده‌شده انبار
       موشک = ۲ واحد، پهپاد = ۱ واحد
    """
    try:
        rockets = country.get('rockets', {}) or {}
        air_troops = country.get('air_troops', {}) or {}
        
        missile_units = sum(int(v) for v in rockets.values()) * 2
        drone_units = sum(int(v) for v in air_troops.values()) * 1
        
        return missile_units + drone_units
    except Exception:
        return 0
def _seed_equipment_from_defaults_if_empty():
    """Ø§Ú¯Ø± Ø¬Ø¯ÙˆÙ„ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø®Ø§Ù„ÛŒ Ø§Ø³ØªØŒ Ø§Ø² DEFAULT_ASSETS Ùˆ ASSET_NAMES Ø³ÛŒØ¯ Ù…ÛŒâ€ŒÚ©Ù†ÛŒÙ…."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM equipment_items")
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return

    now = datetime.now().isoformat()
    # Ø§ÙØ²ÙˆØ¯Ù† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§
    for cat_key, cat_disp in ASSET_CATEGORIES_FOR_DISPLAY:
        try:
            c.execute(
                "INSERT OR IGNORE INTO equipment_categories (cat_key, display_name, created_at) VALUES (?, ?, ?)",
                (cat_key, cat_disp, now)
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø³ÛŒØ¯ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ {cat_key}: {e}")

    # Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ Ø¨Ø± Ø§Ø³Ø§Ø³ DEFAULT_ASSETS
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
                    logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø³ÛŒØ¯ Ø¢ÛŒØªÙ… {item_key}: {e}")

    conn.commit()
    conn.close()
    logger.info("Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø§Ø² Ù…Ù‚Ø§Ø¯ÛŒØ± Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ø³ÛŒØ¯ Ø´Ø¯Ù†Ø¯.")


# ========== ØªÙˆØ§Ø¨Ø¹ Ù…Ø¯ÛŒØ±ÛŒØª Ù¾ÙˆÛŒØ§ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª ==========

def get_all_equipment_categories():
    """Ù„ÛŒØ³Øª Ù‡Ù…Ù‡ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ Ø§Ø² DB: [(cat_key, display_name), ...]"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT cat_key, display_name FROM equipment_categories ORDER BY cat_id")
    rows = c.fetchall()
    conn.close()
    return [(r[0], r[1]) for r in rows]


def get_all_equipment_items():
    """Ù„ÛŒØ³Øª Ù‡Ù…Ù‡ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§: [{item_id, item_key, display_name, category, price}, ...]"""
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
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM equipment_items WHERE item_id = ?", (item_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
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
    # Ø­Ø°Ù Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ Ù…ØªØ¹Ù„Ù‚ Ø¨Ù‡ Ø§ÛŒÙ† Ø¯Ø³ØªÙ‡
    c.execute("DELETE FROM equipment_items WHERE category = ?", (cat_key,))
    c.execute("DELETE FROM equipment_categories WHERE cat_key = ?", (cat_key,))
    conn.commit()
    conn.close()


def get_dynamic_asset_categories_for_display():
    """Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ† Ù¾ÙˆÛŒØ§ÛŒ ASSET_CATEGORIES_FOR_DISPLAY"""
    cats = get_all_equipment_categories()
    if not cats:
        return ASSET_CATEGORIES_FOR_DISPLAY
    return cats


def get_dynamic_asset_names():
    """Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ† Ù¾ÙˆÛŒØ§ÛŒ ASSET_NAMES (Ø¨Ø§ fallback)"""
    items = get_all_equipment_items()
    result = dict(ASSET_NAMES)  # Ú©Ù¾ÛŒ Ø§Ø² Ù¾ÛŒØ´â€ŒÙØ±Ø¶
    for it in items:
        result[it['item_key']] = it['display_name']
    return result


def get_dynamic_asset_prices():
    """Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ† Ù¾ÙˆÛŒØ§ÛŒ ASSET_PRICES (Ø¨Ø§ fallback)"""
    items = get_all_equipment_items()
    result = dict(ASSET_PRICES)  # Ú©Ù¾ÛŒ Ø§Ø² Ù¾ÛŒØ´â€ŒÙØ±Ø¶
    for it in items:
        result[it['item_key']] = it['price']
    return result


def get_dynamic_default_assets():
    """Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ† Ù¾ÙˆÛŒØ§ÛŒ DEFAULT_ASSETS (Ø¨Ø±Ø§ÛŒ Ø³Ø§Ø®ØªØ§Ø± Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ùˆ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§)"""
    base = copy.deepcopy(DEFAULT_ASSETS)
    items = get_all_equipment_items()
    cats = get_all_equipment_categories()

    if not items and not cats:
        return base

    # Ø­Ø°Ù Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ÛŒ Ù¾ÙˆÛŒØ§ Ú©Ù‡ Ø¯Ø± DB Ù†ÛŒØ³ØªÙ†Ø¯ ÙˆÙ„ÛŒ Ø¯Ø± base Ù‡Ø³ØªÙ†Ø¯ (Ø¨Ù‡ Ø¬Ø² Ú©Ù„ÛŒØ¯Ù‡Ø§ÛŒ Ø«Ø§Ø¨Øª)
    fixed_top_keys = {
        'population', 'capital', 'oil_barrels', 'satisfaction', 'daily_income',
        'custom_income', 'loan_amount', 'loan_date', 'crypto', 'religion',
        'security', 'internet_nationalized', 'internet_level', 'refinery_level',
        'disabled_buttons'
    }

    db_cat_keys = {c[0] for c in cats}
    for key in list(base.keys()):
        if key in fixed_top_keys:
            continue
        if isinstance(base[key], dict) and key not in db_cat_keys:
            # Ø¯Ø³ØªÙ‡â€ŒØ§ÛŒ Ú©Ù‡ Ø¯Ø± DB Ø­Ø°Ù Ø´Ø¯Ù‡
            del base[key]

    # Ø§Ø¶Ø§ÙÙ‡ Ú©Ø±Ø¯Ù† Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ÛŒ Ù…ÙˆØ¬ÙˆØ¯ Ø¯Ø± DB
    for cat_key, _ in cats:
        if cat_key not in base or not isinstance(base[cat_key], dict):
            base[cat_key] = {}

    # Ø³Ø§Ø®Øª Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ Ù‡Ø± Ø¯Ø³ØªÙ‡ Ø§Ø² DB
    for cat_key, _ in cats:
        base[cat_key] = {}
    for it in items:
        cat = it['category']
        if cat not in base:
            base[cat] = {}
        base[cat][it['item_key']] = 0

    return base


def save_equipment_preset(preset_name):
    """Ø°Ø®ÛŒØ±Ù‡ ÙˆØ¶Ø¹ÛŒØª ÙØ¹Ù„ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ùˆ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ø¨Ù‡ ØµÙˆØ±Øª ÛŒÚ© Ù¾Ø±ÛŒØ³Øª."""
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
        # Ø§Ú¯Ø± Ù‚Ø¨Ù„Ø§ Ø¨Ø§ Ù‡Ù…ÛŒÙ† Ø§Ø³Ù… Ø¨ÙˆØ¯Ù‡ØŒ Ø¢Ù¾Ø¯ÛŒØª Ú©Ù†
        try:
            c.execute(
                "UPDATE equipment_presets SET data = ?, created_at = ? WHERE preset_name = ?",
                (json.dumps(data, ensure_ascii=False), datetime.now().isoformat(), preset_name)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡ Ù¾Ø±ÛŒØ³Øª: {e}")
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
    """Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ ÛŒÚ© Ù¾Ø±ÛŒØ³Øª: Ø¬Ø§ÛŒÚ¯Ø²ÛŒÙ†ÛŒ Ú©Ø§Ù…Ù„ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ùˆ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§."""
    preset = get_equipment_preset(preset_id)
    if not preset:
        return False
    data = preset['data']

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # Ù¾Ø§Ú© Ú©Ø±Ø¯Ù† Ù‡Ù…Ù‡ Ú†ÛŒØ²
    c.execute("DELETE FROM equipment_items")
    c.execute("DELETE FROM equipment_categories")

    now = datetime.now().isoformat()
    # Ø§ÙØ²ÙˆØ¯Ù† Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§
    for cat in data.get('categories', []):
        try:
            c.execute(
                "INSERT INTO equipment_categories (cat_key, display_name, created_at) VALUES (?, ?, ?)",
                (cat['cat_key'], cat['display_name'], now)
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ø¯Ø³ØªÙ‡ {cat}: {e}")

    # Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§
    for it in data.get('items', []):
        try:
            c.execute(
                "INSERT INTO equipment_items (item_key, display_name, category, price, created_at) VALUES (?, ?, ?, ?, ?)",
                (it['item_key'], it['display_name'], it['category'], it.get('price', 0), now)
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ø¢ÛŒØªÙ… {it}: {e}")

    conn.commit()
    conn.close()

    if reset_countries_inventory:
        _reset_countries_inventory_to_new_schema()

    return True


def _reset_countries_inventory_to_new_schema():
    """Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª ØªÙ…Ø§Ù… Ú©Ø´ÙˆØ±Ù‡Ø§ Ø±Ø§ Ø¨Ù‡ Ø³Ø§Ø®ØªØ§Ø± Ø¬Ø¯ÛŒØ¯ Ø¨Ø§ Ù…Ù‚Ø¯Ø§Ø± ØµÙØ± Ø¨Ø§Ø²Ù†Ø´Ø§Ù†ÛŒ Ù…ÛŒâ€ŒÚ©Ù†Ø¯."""
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
    logger.info(f"Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª {len(user_ids)} Ú©Ø´ÙˆØ± Ø¨Ø§Ø²Ù†Ø´Ø§Ù†ÛŒ Ø´Ø¯.")


# ===================== ØªÙˆØ§Ø¨Ø¹ Ø±ÙˆÙ„/Ø³Ù†Ø§ =====================

# Ø­Ø¯Ø§Ú©Ø«Ø± Ø·ÙˆÙ„ ÛŒÚ© Ù¾ÛŒØ§Ù… ØªÙ„Ú¯Ø±Ø§Ù…
TELEGRAM_MSG_LIMIT = 4096


def _split_message(text, chunk_size=TELEGRAM_MSG_LIMIT):
    """ØªÙ‚Ø³ÛŒÙ… Ù…ØªÙ† Ø¨Ù‡ Ù‚Ø·Ø¹Ø§ØªÛŒ Ú©Ù‡ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… ØªÙ„Ú¯Ø±Ø§Ù… Ø¬Ø§ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯.
    Ø³Ø¹ÛŒ Ù…ÛŒâ€ŒÚ©Ù†Ø¯ Ø±ÙˆÛŒ Ø®Ø· Ø¬Ø¯ÛŒØ¯ ÛŒØ§ ÙØ§ØµÙ„Ù‡ Ø¨Ø´Ú©Ù†Ø¯ ØªØ§ Ú©Ù„Ù…Ø§Øª Ù†ØµÙ Ù†Ø´ÙˆÙ†Ø¯.
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
    """Ø§Ø±Ø³Ø§Ù„ ÛŒÚ© Ù…ØªÙ† Ø¨Ù„Ù†Ø¯ Ø¨Ù‡ Ú†Øª Ø¨Ø§ ØªÙ‚Ø³ÛŒÙ… Ø®ÙˆØ¯Ú©Ø§Ø± Ø¨Ù‡ Ú†Ù†Ø¯ Ù¾ÛŒØ§Ù… ØªÙ„Ú¯Ø±Ø§Ù….
    header ÙÙ‚Ø· Ø¯Ø± Ù¾ÛŒØ§Ù… Ø§ÙˆÙ„ Ù‚Ø±Ø§Ø± Ù…ÛŒâ€ŒÚ¯ÛŒØ±Ø¯.
    Ø§Ú¯Ø± Ù‡Ø¯Ø±+Ø¨Ø¯Ù†Ù‡ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¬Ø§ Ø´ÙˆØ¯ØŒ ÛŒÚ© Ù¾ÛŒØ§Ù… Ù…ÛŒâ€ŒÙØ±Ø³ØªØ¯.
    Ø¯Ø± ØµÙˆØ±Øª Ú†Ù†Ø¯ØªØ§ÛŒÛŒØŒ Ø´Ù…Ø§Ø±Ù‡ ØµÙØ­Ù‡ (Ù…Ø«Ù„ Â«ðŸ“„ 1/3Â») Ø¨Ù‡ Ø§Ø¨ØªØ¯Ø§ÛŒ Ù‡Ø± Ù¾ÛŒØ§Ù… Ø§ÙØ²ÙˆØ¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯.
    """
    header = header or ""
    body = body or ""
    single = f"{header}{body}"
    if len(single) <= TELEGRAM_MSG_LIMIT:
        try:
            await bot_instance.send_message(chat_id=chat_id, text=single, parse_mode=parse_mode)
        except Exception as e:
            logger.warning(f"Ø§Ø±Ø³Ø§Ù„ Ø¨Ø§ parse_mode={parse_mode} Ù†Ø§Ù…ÙˆÙÙ‚ ({e})ØŒ Ø¨Ø¯ÙˆÙ† parse_mode ØªÙ„Ø§Ø´ Ù…ÛŒâ€ŒÚ©Ù†Ù…")
            await bot_instance.send_message(chat_id=chat_id, text=single)
        return 1

    # Ø§Ú¯Ù‡ Ù‡Ø¯Ø± Ø®ÙˆØ¯Ø´ Ø¨Ø²Ø±Ú¯â€ŒØªØ± Ø§Ø² Ø­Ø¯ Ø¨ÙˆØ¯ØŒ Ø¬Ø¯Ø§ Ø¨ÙØ±Ø³Øª
    if len(header) > TELEGRAM_MSG_LIMIT - 16:
        for h_chunk in _split_message(header):
            try:
                await bot_instance.send_message(chat_id=chat_id, text=h_chunk, parse_mode=parse_mode)
            except Exception:
                await bot_instance.send_message(chat_id=chat_id, text=h_chunk)
        header = ""

    # Ø¨Ø¯Ù†Ù‡ Ø±Ø§ ØªÙ‚Ø³ÛŒÙ… Ù…ÛŒâ€ŒÚ©Ù†ÛŒÙ…
    available_for_first = TELEGRAM_MSG_LIMIT - len(header) - 16  # 16 Ø¨Ø±Ø§ÛŒ Ù¾ÛŒØ´â€ŒØ¨Ù†Ø¯ ØµÙØ­Ù‡
    available_for_rest = TELEGRAM_MSG_LIMIT - 16

    # Ø§ÙˆÙ„ Ø¨Ø®Ø´ Ø§ÙˆÙ„ Ø±Ùˆ Ø¨Ø§ Ø§Ù†Ø¯Ø§Ø²Ù‡â€ŒØ§ÛŒ Ù…ÛŒâ€ŒØ¨Ø±ÛŒÙ… Ú©Ù‡ Ø¨Ø§ Ù‡Ø¯Ø± Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¬Ø§ Ø¨Ø´Ù‡
    first_chunk = body[:available_for_first]
    # Ø³Ø¹ÛŒ Ú©Ù† Ø±ÙˆÛŒ Ø®Ø· Ø¬Ø¯ÛŒØ¯/ÙØ§ØµÙ„Ù‡ Ø¨Ø´Ú©Ù†ÛŒ
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
        prefix = f"ðŸ“„ {idx}/{total}\n" if total > 1 else ""
        if idx == 1 and header:
            text = f"{header}{prefix}{chunk}"
        else:
            text = f"{prefix}{chunk}"
        if len(text) > TELEGRAM_MSG_LIMIT:
            # Ø§Ù…Ù†ÛŒØª: Ø§Ú¯Ù‡ Ø¨Ù‡ Ù‡Ø± Ø¯Ù„ÛŒÙ„ÛŒ Ù‡Ù†ÙˆØ² Ø¨Ø²Ø±Ú¯ Ø¨ÙˆØ¯ØŒ Ø¨Ø¯ÙˆÙ† Ù‡Ø¯Ø±/prefix Ø¨ÙØ±Ø³Øª
            text = chunk[:TELEGRAM_MSG_LIMIT]
        try:
            await bot_instance.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
            sent += 1
        except Exception as e:
            logger.warning(f"Ø§Ø±Ø³Ø§Ù„ Ù‚Ø·Ø¹Ù‡ {idx}/{total} Ø¨Ø§ parse_mode Ù†Ø§Ù…ÙˆÙÙ‚: {e}Ø› Ø¨Ø¯ÙˆÙ† parse_mode ØªÙ„Ø§Ø´ Ù…ÛŒâ€ŒÚ©Ù†Ù…")
            try:
                await bot_instance.send_message(chat_id=chat_id, text=text)
                sent += 1
            except Exception as e2:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù‚Ø·Ø¹Ù‡ {idx}/{total} Ø¨Ù‡ {chat_id}: {e2}")
    return sent


ROLE_SENA_CATEGORIES = {
    'security': {'label': 'ðŸ›¡ï¸ Ø§Ù…Ù†ÛŒØªÛŒ', 'group': 'role'},
    'economic': {'label': 'ðŸ’¹ Ø§Ù‚ØªØµØ§Ø¯ÛŒ', 'group': 'role'},
    'sabotage': {'label': 'ðŸ’£ Ø®Ø±Ø§Ø¨Ú©Ø§Ø±ÛŒ', 'group': 'role'},
    'sena':     {'label': 'ðŸ“œ Ø³Ù†Ø§',     'group': 'sena'},
}


def _today_key_tehran():
    """Ú©Ù„ÛŒØ¯ Ø±ÙˆØ² ÙØ¹Ù„ÛŒ Ø¨Ù‡ ÙˆÙ‚Øª ØªÙ‡Ø±Ø§Ù†Ø› Ø±ÙˆØ² Ø¬Ø¯ÛŒØ¯ Ø³Ø§Ø¹Øª 12 Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù† Ø´Ø±ÙˆØ¹ Ù…ÛŒâ€ŒØ´ÙˆØ¯."""
    try:
        tz = pytz.timezone('Asia/Tehran')
        now = datetime.now(tz)
    except Exception:
        now = datetime.now()
    # Ø±ÙˆØ² Ø¬Ø¯ÛŒØ¯ Ø¨Ø¹Ø¯ Ø§Ø² Ø³Ø§Ø¹Øª 12 Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù† Ø´Ø±ÙˆØ¹ Ù…ÛŒâ€ŒØ´Ù‡
    if now.hour < 12:
        base = now - timedelta(days=1)
    else:
        base = now
    return base.strftime('%Y-%m-%d')


def role_sena_is_category_enabled(category):
    """Ø¨Ø±Ø±Ø³ÛŒ ÙØ¹Ø§Ù„ Ø¨ÙˆØ¯Ù† ÛŒÚ© Ø¯Ø³ØªÙ‡."""
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
    """group: 'role' ÛŒØ§ 'sena'"""
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
    """ØªØ¹Ø¯Ø§Ø¯ Ø§Ø³ØªÙØ§Ø¯Ù‡â€ŒØ´Ø¯Ù‡â€ŒÛŒ Ú©Ø§Ø±Ø¨Ø± Ø§Ù…Ø±ÙˆØ²."""
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
    """Ù…Ø¬Ù…ÙˆØ¹ Ø§Ø³ØªÙØ§Ø¯Ù‡â€ŒØ´Ø¯Ù‡â€ŒÛŒ Ú©Ø§Ø±Ø¨Ø± Ø¯Ø± ÛŒÚ© Ú¯Ø±ÙˆÙ‡ (role ÛŒØ§ sena) Ø§Ù…Ø±ÙˆØ²."""
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
    """ÛŒÚ© ÙˆØ§Ø­Ø¯ Ø¨Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡â€ŒÛŒ Ú©Ø§Ø±Ø¨Ø± Ø¯Ø± ÛŒÚ© Ø¯Ø³ØªÙ‡ Ø§Ù…Ø±ÙˆØ² Ø§Ø¶Ø§ÙÙ‡ Ú©Ù†."""
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
    """Ø¨Ø±Ø±Ø³ÛŒ Ø§ÛŒÙ†Ú©Ù‡ Ú©Ø§Ø±Ø¨Ø± Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ Ù¾ÛŒØ§Ù… Ø¬Ø¯ÛŒØ¯ Ø¯Ø± Ø§ÛŒÙ† Ø¯Ø³ØªÙ‡ Ø¨ÙØ±Ø³ØªØ¯ ÛŒØ§ Ù†Ù‡.
    Ø®Ø±ÙˆØ¬ÛŒ: (ok: bool, reason: str)
    """
    if category not in ROLE_SENA_CATEGORIES:
        return False, "Ø¯Ø³ØªÙ‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª."
    if not role_sena_is_category_enabled(category):
        return False, f"Ø¨Ø®Ø´ Â«{ROLE_SENA_CATEGORIES[category]['label']}Â» ØªÙˆØ³Ø· Ù…Ø¯ÛŒØ±ÛŒØª ØºÛŒØ±ÙØ¹Ø§Ù„ Ø´Ø¯Ù‡ Ø§Ø³Øª."
    group = ROLE_SENA_CATEGORIES[category]['group']
    limit = role_sena_get_limit(group)
    if limit <= 0:
        # Ù…Ø­Ø¯ÙˆØ¯ÛŒØª ØµÙØ± = ØºÛŒØ±ÙØ¹Ø§Ù„ Ø´Ø¯Ù† Ú©Ø§Ù…Ù„
        return False, "Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø§Ø±Ø³Ø§Ù„ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ø¨Ø®Ø´ Ø¨Ù‡ ØµÙØ± ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯Ù‡ Ø§Ø³Øª."
    used = role_sena_get_group_used(user_id, group)
    if used >= limit:
        if group == 'role':
            return False, f"Ø³Ù‡Ù…ÛŒÙ‡ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø´Ù…Ø§ Ø¨Ø±Ø§ÛŒ Ø±ÙˆÙ„â€ŒÙ‡Ø§ Ø¨Ù‡ Ù¾Ø§ÛŒØ§Ù† Ø±Ø³ÛŒØ¯Ù‡ ({used}/{limit}). ÙØ±Ø¯Ø§ Ø³Ø§Ø¹Øª Û±Û² Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù† Ø±ÛŒØ³Øª Ù…ÛŒâ€ŒØ´ÙˆØ¯."
        else:
            return False, f"Ø³Ù‡Ù…ÛŒÙ‡ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø´Ù…Ø§ Ø¨Ø±Ø§ÛŒ Ø³Ù†Ø§ Ø¨Ù‡ Ù¾Ø§ÛŒØ§Ù† Ø±Ø³ÛŒØ¯Ù‡ ({used}/{limit}). ÙØ±Ø¯Ø§ Ø³Ø§Ø¹Øª Û±Û² Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù† Ø±ÛŒØ³Øª Ù…ÛŒâ€ŒØ´ÙˆØ¯."
    return True, ""


# ===================== ØªÙˆØ§Ø¨Ø¹ Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ ÙØ¹Ø§Ù„ =====================

def is_chat_active(chat_id):
    """Ø¨Ø±Ø±Ø³ÛŒ Ø§ÛŒÙ†Ú©Ù‡ Ø¢ÛŒØ§ ÛŒÚ© Ú¯Ù¾ Ø¨Ø±Ø§ÛŒ Ù¾Ù„ÛŒØ±Ù‡Ø§ ÙØ¹Ø§Ù„ (Ø§Ú©ØªÙˆÛŒØªâ€ŒØ´Ø¯Ù‡) Ø§Ø³Øª ÛŒØ§ Ù†Ù‡."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM active_chats WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    return row is not None


def activate_chat(chat_id, title, activated_by):
    """Ú¯Ù¾ Ø±Ø§ Ø¨Ù‡ Ù„ÛŒØ³Øª Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ ÙØ¹Ø§Ù„ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒÚ©Ù†Ø¯."""
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
    c.execute("SELECT user_id, name, population, capital, daily_income, religion, oil_barrels, satisfaction, assets, custom_income, loan_amount, loan_date, crypto, security, internet_nationalized, internet_level, refinery_level FROM countries WHERE user_id = ?", (user_id,))
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
            "satisfaction": row[7],
            "assets": json.loads(row[8]) if row[8] else {},
            "custom_income": row[9],
            "loan_amount": row[10],
            "loan_date": row[11],
            "crypto": row[12],
            "security": row[13],
            "internet_nationalized": bool(row[14]),
            "internet_level": row[15],
            "refinery_level": row[16]
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
            security, internet_nationalized, internet_level, refinery_level
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        initial_data['population'],
        initial_data['capital'],
        initial_data['daily_income'],
        initial_data['religion'],
        initial_data['oil_barrels'],
        initial_data['satisfaction'],
        json.dumps(assets_json, ensure_ascii=False),
        initial_data['custom_income'],
        initial_data['loan_amount'],
        loan_date,
        initial_data['crypto'],
        initial_data['security'],
        int(initial_data['internet_nationalized']),
        initial_data['internet_level'],
        initial_data['refinery_level']
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

    set_clauses = []
    values = []

    for key, value in top_level_updates.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)

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
    internet_income = INTERNET_INCOME_RATES.get(country.get('internet_level', 2), 0)
    refinery_income = country.get('refinery_level', 0) * 25
    return base_income + custom_income + internet_income + refinery_income


async def daily_production_job(context: CallbackContext):
    logger.info("Ø´Ø±ÙˆØ¹ ØªÙˆØ²ÛŒØ¹ Ø®ÙˆØ¯Ú©Ø§Ø± Ø³ÙˆØ¯ Ùˆ ØªÙˆÙ„ÛŒØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡...")
    countries = get_all_countries()

    if not countries:
        logger.info("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ ØªÙˆØ²ÛŒØ¹ Ø³ÙˆØ¯ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯")
        return

    logger.info(f"ØªÙˆØ²ÛŒØ¹ Ø³ÙˆØ¯ Ùˆ ØªÙˆÙ„ÛŒØ¯ Ø¨Ù‡ {len(countries)} Ú©Ø´ÙˆØ±")

    for user_id, name in countries:
        country = get_country(user_id)
        if not country:
            continue

        total_income = calculate_daily_income(country)
        new_capital = country['capital'] + total_income

        updates = {'capital': new_capital}
        update_country(user_id, updates)

        logger.info(f"Ø¨Ø±Ø§ÛŒ Ú©Ø´ÙˆØ± {name} (ID: {user_id}): Ø³ÙˆØ¯ Ùˆ ØªÙˆÙ„ÛŒØ¯ Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯.")

        try:
            message = (
                f"ðŸŒ… Ø¨Ù‡ Ø±ÙˆØ² Ø¬Ø¯ÛŒØ¯ Ø®ÙˆØ´ Ø¢Ù…Ø¯ÛŒØ¯!\n"
                f"âœ… Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø´Ù…Ø§ Ø¨Ù‡ Ù…Ø¨Ù„Øº {total_income:,} Ø¨Ù‡ Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯\n"
                f"ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø¬Ø¯ÛŒØ¯: {new_capital:,}"
            )

            internet_income = INTERNET_INCOME_RATES.get(country.get('internet_level', 2), 0)
            message += f"\nðŸŒ Ø¯Ø±Ø¢Ù…Ø¯ Ø§ÛŒÙ†ØªØ±Ù†Øª: {internet_income:,}"

            refinery_income = country.get('refinery_level', 0) * 25
            if refinery_income > 0:
                message += f"\nðŸ›¢ï¸ Ø¯Ø±Ø¢Ù…Ø¯ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡: {refinery_income:,}"

            await context.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø¨Ù‡ Ú©Ø§Ø±Ø¨Ø± {user_id}: {e}")

    logger.info("ØªÙˆØ²ÛŒØ¹ Ø³ÙˆØ¯ Ùˆ ØªÙˆÙ„ÛŒØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯")


async def run_daily_production_manually(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return

    await daily_production_job(context)
    await update.message.reply_text("âœ… ØªÙˆØ²ÛŒØ¹ Ø³ÙˆØ¯ Ùˆ ØªÙˆÙ„ÛŒØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø¨Ù‡ ØµÙˆØ±Øª Ø¯Ø³ØªÛŒ Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯")


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
        # Ø¨Ø±Ø±Ø³ÛŒ ÙˆØ¶Ø¹ÛŒØª Ú©Ù„ÛŒ Ø±Ø¨Ø§Øª (Ù…Ø§Ù„Ú© Ù‡Ù…ÛŒØ´Ù‡ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù‡)
        if not get_bot_active_status() and user_id != OWNER_ID:
            if update.message:
                await update.message.reply_text("ðŸ¤– Ø±Ø¨Ø§Øª Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!")
            elif update.callback_query:
                await update.callback_query.answer("ðŸ¤– Ø±Ø¨Ø§Øª Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
            return ConversationHandler.END

        # ===== Ø­Ø§Ù„Øª Ù¾ÛŒâ€ŒÙˆÛŒ =====
        if chat_type == "private":
            # Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ: Ø¯Ø³ØªØ±Ø³ÛŒ Ú©Ø§Ù…Ù„
            if is_admin(user_id):
                country_data = get_country(user_id)
                if not country_data:
                    return await admin_panel(update, context)
                return await show_main_menu(update, context)

            # Ù¾Ù„ÛŒØ± Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ: ÙÙ‚Ø· Ù¾Ø§Ø³Ø® ÛŒÚ©Ø¨Ø§Ø±Ù‡ Ø¨Ù‡ /start
            if update.message:
                await update.message.reply_text(
                    "ðŸ‘‹ Ø³Ù„Ø§Ù…!\n\n"
                    "ðŸ—¨ï¸ Ú¯Ù¾ Ø®ÙˆØ¯ Ø±Ø§ Ø§Ø² Ø§Ø¯Ù…ÛŒÙ† ØªØ­ÙˆÛŒÙ„ Ø¨Ú¯ÛŒØ±ÛŒØ¯.\n"
                    "Ø±Ø¨Ø§Øª Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ Ø¨Ù‡ Ù¾ÛŒØ§Ù…â€ŒÙ‡Ø§ÛŒ Ø´Ù…Ø§ Ù¾Ø§Ø³Ø® Ù†Ù…ÛŒâ€ŒØ¯Ù‡Ø¯."
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    "Ú¯Ù¾ Ø®ÙˆØ¯ Ø±Ø§ Ø§Ø² Ø§Ø¯Ù…ÛŒÙ† ØªØ­ÙˆÛŒÙ„ Ø¨Ú¯ÛŒØ±ÛŒØ¯.", show_alert=True
                )
            return ConversationHandler.END

        # ===== Ø­Ø§Ù„Øª Ú¯Ù¾ =====
        # Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ú¯Ù¾: Ù¾Ù†Ù„ Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ù‡Ø± Ú¯Ù¾ÛŒ ÙØ¹Ø§Ù„ Ø§Ø³Øª
        if is_admin(user_id):
            country_data = get_country(user_id)
            if not country_data:
                return await admin_panel(update, context)
            return await show_main_menu(update, context)

        # Ù¾Ù„ÛŒØ± Ø¯Ø± Ú¯Ù¾: ÙÙ‚Ø· Ø¯Ø± Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ ÙØ¹Ø§Ù„â€ŒØ´Ø¯Ù‡ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ø¯
        chat_id = chat.id if chat else None
        if chat_id and is_chat_active(chat_id):
            country_data = get_country(user_id)
            if not country_data:
                msg = "âš ï¸ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ± Ø®ÙˆØ¯ Ø±Ø§ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯!\nÙ„Ø·ÙØ§Ù‹ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù‡ Ù…Ø§Ù„Ú© Ø±Ø¨Ø§Øª Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
                if update.message:
                    await update.message.reply_text(msg)
                elif update.callback_query:
                    await update.callback_query.answer(msg, show_alert=True)
                return ConversationHandler.END
            return await show_main_menu(update, context)
        else:
            # Ú¯Ù¾ ÙØ¹Ø§Ù„ Ù†ÛŒØ³ØªØ› Ø¨Ù‡ Ù¾Ù„ÛŒØ± Ù‡ÛŒÚ† Ù¾Ø§Ø³Ø®ÛŒ Ù†Ø¯ÛŒÙ… ØªØ§ Ø§Ø³Ù¾Ù… Ù†Ø´Ù‡
            return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in start: {e}", exc_info=True)
        try:
            if update.message:
                await update.message.reply_text("Ù…ØªØ§Ø³ÙØ§Ù†Ù‡ Ø®Ø·Ø§ÛŒÛŒ Ø±Ø® Ø¯Ø§Ø¯. Ù„Ø·ÙØ§Ù‹ /start Ø±Ø§ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
        except Exception:
            pass
        return ConversationHandler.END


async def show_main_menu(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        if not get_bot_active_status() and user_id != OWNER_ID:
            if update.callback_query:
                await update.callback_query.answer("ðŸ¤– Ø±Ø¨Ø§Øª Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
            return MAIN_MENU
        country = get_country(user_id)
        if not country:
            error_msg = "âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯. Ù„Ø·ÙØ§Ù‹ Ø¨Ø§ Ù…Ø§Ù„Ú© Ø±Ø¨Ø§Øª ØªÙ…Ø§Ø³ Ø¨Ú¯ÛŒØ±ÛŒØ¯."
            if update.callback_query:
                await update.callback_query.answer(error_msg, show_alert=True)
                await update.callback_query.edit_message_text(error_msg)
            else:
                await update.message.reply_text(error_msg)
            return ConversationHandler.END
        keyboard = []
        disabled_buttons = get_global_disabled_buttons()
        for btn in BOT_MAIN_MENU_BUTTONS:
            if btn['callback_data'] not in disabled_buttons:
                keyboard.append([InlineKeyboardButton(btn['text'], callback_data=btn['callback_data'])])
        if is_admin(user_id):
            keyboard.append([InlineKeyboardButton("ðŸ‘‘ Ù¾Ù†Ù„ Ù…Ø¯ÛŒØ±ÛŒØª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = f"Ø³Ù„Ø§Ù… Ø±Ù‡Ø¨Ø± {country['name']}!\nØ¨Ù‡ Ø±Ø¨Ø§Øª {BOT_NAME} Ø®ÙˆØ´ Ø¢Ù…Ø¯ÛŒØ¯.\nÙ„Ø·ÙØ§ ÛŒÚ© Ú¯Ø²ÛŒÙ†Ù‡ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:"
        if update.message:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error showing main menu: {e}", exc_info=True)
        if update.effective_chat:
            await update.effective_chat.send_message("Ù…ØªØ§Ø³ÙØ§Ù†Ù‡ Ø®Ø·Ø§ÛŒÛŒ Ø±Ø® Ø¯Ø§Ø¯. Ù„Ø·ÙØ§Ù‹ /start Ø±Ø§ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
    return MAIN_MENU


async def show_assets(update: Update, context: CallbackContext, target_user_id: int = None):
    query = update.callback_query
    if query:
        await query.answer()
    try:
        user_id = target_user_id if target_user_id else (query.from_user.id if query else update.effective_user.id)
        country = get_country(user_id)
        if not country:
            message = "âŒ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯."
            if query:
                await query.edit_message_text(message)
            else:
                await update.message.reply_text(message)
            return ConversationHandler.END
        total_income = calculate_daily_income(country)

        message = f"ðŸ›ï¸ *ÙˆØ¶Ø¹ÛŒØª Ú©Ø´ÙˆØ± {country.get('name', 'Ù†Ø§Ù…Ø¹Ù„ÙˆÙ…')}*\n\n"
        message += f"ðŸ‘« Ø¬Ù…Ø¹ÛŒØª: {country.get('population', 0):,}\n"
        message += f"ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {country.get('capital', 0):,}\n"
        message += f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {total_income:,}\n\n"

        message += f"ðŸ›¢ï¸ Ù†ÙØª: {country.get('oil_barrels', 0):,}\n"
        message += f"ðŸ˜Š Ø±Ø¶Ø§ÛŒØª: {country.get('satisfaction', 0)}%\n"
        message += f"ðŸ›¡ï¸ Ø§Ù…Ù†ÛŒØª: {country.get('security', 0)}%\n"
        message += f"â‚¿ Ø§Ø±Ø² Ø¯ÛŒØ¬ÛŒØªØ§Ù„: {country.get('crypto', 0):,}\n"
        religion_display_name = next((disp for code, disp in RELIGIONS if code == country.get('religion', '')), 'Ù†Ø§Ù…Ø¹Ù„ÙˆÙ…')
        message += f"â˜ªï¸ Ø¯ÛŒÙ†: {religion_display_name}\n"
        message += f"ðŸŒ Ø§ÛŒÙ†ØªØ±Ù†Øª: {country.get('internet_level', 2)}G\n"
        message += f"  â”” ÙˆØ¶Ø¹ÛŒØª: {'âœ… Ù…Ù„ÛŒ' if country.get('internet_nationalized', False) else 'âŒ ØºÛŒØ±Ù…Ù„ÛŒ'}\n"
        message += f"ðŸ›¢ï¸ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡: Ø³Ø·Ø­ {country.get('refinery_level', 0)}\n\n"
        used = calculate_storage_used(country)
        capacity = country.get("storage_capacity", 100)
        message += f"📦 انبار: {used} / {capacity} واحد\n\n"

        for category_key, category_display_name in get_dynamic_asset_categories_for_display():
            assets_dict = country.get(category_key, {})
            if isinstance(assets_dict, dict):
                message += f"*{category_display_name}:*\n"
                for item_key, count in assets_dict.items():
                    display_name = get_asset_display_name(item_key)
                    message += f"â€¢ {display_name}: {count:,}\n"
                message += "\n"

        keyboard = [[InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')]]
        if target_user_id and is_admin(update.effective_user.id):
            keyboard = [[InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ù¾Ù†Ù„ Ù…Ø¯ÛŒØ±ÛŒØª", callback_data='admin_panel')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query:
            await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_assets: {e}", exc_info=True)
        if query:
            await query.answer("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§.", show_alert=True)
        else:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§.")

    if target_user_id and is_admin(update.effective_user.id):
        return ADMIN_MENU
    return MAIN_MENU


async def admin_panel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        if update.message:
            await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        else:
            await update.callback_query.answer("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!", show_alert=True)
        return MAIN_MENU
    try:
        keyboard = []
        for btn in ADMIN_PANEL_BUTTONS:
            keyboard.append([InlineKeyboardButton(btn['text'], callback_data=btn['callback_data'])])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = "ðŸ‘‘ Ù¾Ù†Ù„ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ø´ÙˆØ±Ù‡Ø§"
        if update.message:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error showing admin panel: {e}", exc_info=True)
        if update.effective_chat:
            await update.effective_chat.send_message("Ù…ØªØ§Ø³ÙØ§Ù†Ù‡ Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ù¾Ù†Ù„ Ù…Ø¯ÛŒØ±ÛŒØª Ø±Ø® Ø¯Ø§Ø¯. Ù„Ø·ÙØ§Ù‹ /start Ø±Ø§ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
    return ADMIN_MENU


async def select_country_view_assets(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"view_assets_{user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§ÛŒØ´ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SELECT_COUNTRY_TO_VIEW_ASSETS
    except Exception as e:
        logger.error(f"Error in select_country_view_assets: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return ADMIN_MENU


async def handle_view_selected_country_assets(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("view_assets_", ""))
        return await show_assets(update, context, target_user_id=target_user_id)
    except Exception as e:
        logger.error(f"Error in handle_view_selected_country_assets: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø±Ø§ÛŒÛŒ Ú©Ø´ÙˆØ±")
        return ADMIN_MENU


async def edit_main_props(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ ÙˆÛŒØ±Ø§ÛŒØ´ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"edit_main_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ ÙˆÛŒØ±Ø§ÛŒØ´ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø§ØµÙ„ÛŒ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return EDIT_MAIN_PROPS
    except Exception as e:
        logger.error(f"Error in edit_main_props: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return ADMIN_MENU


async def select_main_prop_to_edit(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_edit = int(query.data.replace("edit_main_country_", ""))
        context.user_data['user_id_to_edit'] = user_id_to_edit
        country = get_country(user_id_to_edit)
        if not country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return ADMIN_MENU

        main_properties = [
            ('daily_income', "Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡ ðŸ’¹"),
            ('capital', "Ø³Ø±Ù…Ø§ÛŒÙ‡ ðŸ’°"),
            ('population', "Ø¬Ù…Ø¹ÛŒØª ðŸ‘«"),
            ('oil_barrels', "Ù†ÙØª ðŸ›¢ï¸"),
            ('satisfaction', "Ø±Ø¶Ø§ÛŒØª ðŸ˜Š"),
            ('security', "Ø§Ù…Ù†ÛŒØª Ú©Ø´ÙˆØ± ðŸ›¡ï¸"),
            ('crypto', "Ø§Ø±Ø² Ø¯ÛŒØ¬ÛŒØªØ§Ù„ â‚¿"),
            ('internet_level', "Ø³Ø·Ø­ Ø§ÛŒÙ†ØªØ±Ù†Øª ðŸŒ"),
            ('refinery_level', "Ø³Ø·Ø­ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ ðŸ›¢ï¸"),
        ]

        keyboard = []
        for prop_key, prop_name in main_properties:
            current_value = country.get(prop_key, 0)
            keyboard.append([InlineKeyboardButton(f"{prop_name} (ÙØ¹Ù„ÛŒ: {current_value:,})", callback_data=f"set_main_prop_{prop_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='edit_main_props')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"ÙˆÛŒØ±Ø§ÛŒØ´ ÙˆÛŒÚ˜Ú¯ÛŒâ€ŒÙ‡Ø§ÛŒ Ø§ØµÙ„ÛŒ Ø¨Ø±Ø§ÛŒ {country['name']}:\nÙ„Ø·ÙØ§Ù‹ ÙˆÛŒÚ˜Ú¯ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SELECT_MAIN_PROP
    except Exception as e:
        logger.error(f"Error in select_main_prop_to_edit: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø´ÙˆØ±")
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
        await query.edit_message_text(f"ÙˆÛŒØ±Ø§ÛŒØ´ {prop_display_name} Ø¨Ø±Ø§ÛŒ {country['name']}:\n"
                                      f"Ù…Ù‚Ø¯Ø§Ø± ÙØ¹Ù„ÛŒ: {current_value:,}\n"
                                      "Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ø¬Ø¯ÛŒØ¯ (Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­) Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Ø¨Ø±Ø§ÛŒ Ú©Ø§Ù‡Ø´ Ø§Ø² Ø¹Ù„Ø§Ù…Øª - Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯):")
        return GET_MAIN_PROP_VALUE
    except Exception as e:
        logger.error(f"Error in get_main_prop_value: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª ÙˆÛŒÚ˜Ú¯ÛŒ")
        return ADMIN_MENU


async def save_main_prop_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        prop_key = context.user_data.get('edit_main_prop_key')
        if not user_id_to_edit or not prop_key:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return await admin_panel(update, context)

        value_str = update.message.text.strip()
        if value_str.startswith('+') or value_str.startswith('-'):
            is_relative = True
            value = int(value_str)
        else:
            is_relative = False
            value = int(value_str)

        if prop_key in ['satisfaction', 'security'] and not (0 <= value <= 100):
            await update.message.reply_text(f"Ø¨Ø±Ø§ÛŒ {get_asset_display_name(prop_key)}ØŒ Ù…Ù‚Ø¯Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø¨ÛŒÙ† 0 ØªØ§ 100 Ø¨Ø§Ø´Ø¯. Ù„Ø·ÙØ§Ù‹ Ù…Ø¬Ø¯Ø¯Ø§Ù‹ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
            return GET_MAIN_PROP_VALUE
    except ValueError:
        await update.message.reply_text("Ù…Ù‚Ø¯Ø§Ø± ÙˆØ§Ø±Ø¯ Ø´Ø¯Ù‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return GET_MAIN_PROP_VALUE
    try:
        country = get_country(user_id_to_edit)
        if not country:
            await update.message.reply_text("Ø®Ø·Ø§: Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø´ÙˆØ± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return await admin_panel(update, context)

        if is_relative:
            new_value = country.get(prop_key, 0) + value
            if prop_key in ['satisfaction', 'security']:
                new_value = max(0, min(100, new_value))
        else:
            new_value = value

        update_country(user_id_to_edit, {prop_key: new_value})

        prop_display_name = get_asset_display_name(prop_key)
        await update.message.reply_text(f"âœ… {prop_display_name} Ø¨Ø±Ø§ÛŒ {country['name']} Ø¨Ù‡ {new_value:,} ØªØºÛŒÛŒØ± ÛŒØ§ÙØª.")
        context.user_data.pop('user_id_to_edit', None)
        context.user_data.pop('edit_main_prop_key', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_main_prop_value: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡â€ŒØ³Ø§Ø²ÛŒ ØªØºÛŒÛŒØ±Ø§Øª")
        return await admin_panel(update, context)


async def edit_assets_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ ÙˆÛŒØ±Ø§ÛŒØ´ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"edit_assets_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ ÙˆÛŒØ±Ø§ÛŒØ´ Ù†ÛŒØ±ÙˆÙ‡Ø§ Ùˆ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return EDIT_ASSETS_MENU
    except Exception as e:
        logger.error(f"Error in edit_assets_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return ADMIN_MENU


    application.add_handler(CallbackQueryHandler(edit_storage_capacity, pattern='^edit_storage_capacity$'))
    application.add_handler(CallbackQueryHandler(select_country_for_storage, pattern='^storage_country_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_storage_capacity))
async def edit_storage_capacity(update: Update, context: CallbackContext) -> int:
    """نمایش لیست کشورها برای ویرایش ظرفیت انبار"""
    query = update.callback_query
    await query.answer()
    
    try:
        countries = get_all_countries()
        if not countries:
            await query.edit_message_text("هیچ کشوری وجود ندارد.")
            return ADMIN_MENU
        
        keyboard = []
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"storage_country_{user_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("📦 کشوری را برای ویرایش ظرفیت انبار انتخاب کنید:", reply_markup=reply_markup)
        return ADMIN_MENU
        
    except Exception as e:
        logger.error(f"Error in edit_storage_capacity: {e}")
        await query.edit_message_text("خطا در بارگذاری لیست کشورها.")
        return ADMIN_MENU


async def select_country_for_storage(update: Update, context: CallbackContext) -> int:
    """انتخاب کشور و درخواست مقدار جدید ظرفیت"""
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
        
        await query.edit_message_text(
            f"📦 کشور: {country['name']}\n"
            f"ظرفیت فعلی: {current_capacity} واحد\n"
            f"استفاده شده: {used} واحد\n\n"
            "لطفاً ظرفیت جدید را وارد کنید (عدد بین ۵۰ تا ۵۰۰):"
        )
        return ADMIN_MENU
        
    except Exception as e:
        logger.error(f"Error in select_country_for_storage: {e}")
        await query.edit_message_text("خطا در انتخاب کشور.")
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
        if new_capacity < 50 or new_capacity > 500:
            await update.message.reply_text("ظرفیت باید بین ۵۰ تا ۵۰۰ باشد.")
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
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return ADMIN_MENU
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"select_asset_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='edit_assets_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"ÙˆÛŒØ±Ø§ÛŒØ´ Ù†ÛŒØ±ÙˆÙ‡Ø§ Ùˆ Ø¯Ø§Ø±Ø§ÛŒÛŒâ€ŒÙ‡Ø§ Ø¨Ø±Ø§ÛŒ {country['name']}:\nÙ„Ø·ÙØ§Ù‹ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SELECT_ASSET_CATEGORY
    except Exception as e:
        logger.error(f"Error in select_asset_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø´ÙˆØ±")
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
            await query.edit_message_text("âŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return await select_asset_category(update, context)
        keyboard = []
        for item_key in country[category_key].keys():
            current_count = country[category_key].get(item_key, 0)
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(f"{display_name} (ÙØ¹Ù„ÛŒ: {current_count:,})", callback_data=f"set_asset_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data=f"edit_assets_country_{user_id_to_edit}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(f"ÙˆÛŒØ±Ø§ÛŒØ´ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ {category_display_name} Ø¨Ø±Ø§ÛŒ {country['name']}:\nÙ„Ø·ÙØ§Ù‹ Ø¢ÛŒØªÙ… Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SELECT_ASSET_ITEM
    except Exception as e:
        logger.error(f"Error in select_asset_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§")
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

        await query.edit_message_text(f"ÙˆÛŒØ±Ø§ÛŒØ´ {item_display_name} Ø¨Ø±Ø§ÛŒ {country['name']}:\n"
                                      f"ØªØ¹Ø¯Ø§Ø¯ ÙØ¹Ù„ÛŒ: {current_count:,}\n"
                                      "Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ø¬Ø¯ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Ø¨Ø±Ø§ÛŒ Ú©Ø§Ù‡Ø´ Ø§Ø² Ø¹Ù„Ø§Ù…Øª - Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯):")
        return GET_ASSET_EDIT_VALUE
    except Exception as e:
        logger.error(f"Error in get_asset_edit_value: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø¢ÛŒØªÙ…")
        return SELECT_ASSET_ITEM


async def save_asset_edit_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        user_id_to_edit = context.user_data.get('user_id_to_edit')
        category_key = context.user_data.get('asset_category')
        item_key = context.user_data.get('asset_item')
        if not user_id_to_edit or not category_key or not item_key:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return await admin_panel(update, context)

        value_str = update.message.text.strip()
        if value_str.startswith('+') or value_str.startswith('-'):
            is_relative = True
            value = int(value_str)
        else:
            is_relative = False
            value = int(value_str)
    except ValueError:
        await update.message.reply_text("Ù…Ù‚Ø¯Ø§Ø± ÙˆØ§Ø±Ø¯ Ø´Ø¯Ù‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return GET_ASSET_EDIT_VALUE
    try:
        country = get_country(user_id_to_edit)
        if not country:
            await update.message.reply_text("Ø®Ø·Ø§: Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø´ÙˆØ± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
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

        await update.message.reply_text(f"âœ… {item_display_name} Ø¯Ø± {category_display_name} Ø¨Ø±Ø§ÛŒ {country['name']} Ø¨Ù‡ {new_count:,} ØªØºÛŒÛŒØ± ÛŒØ§ÙØª.")
        context.user_data.pop('user_id_to_edit', None)
        context.user_data.pop('asset_category', None)
        context.user_data.pop('asset_item', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_asset_edit_value: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡â€ŒØ³Ø§Ø²ÛŒ ØªØºÛŒÛŒØ±Ø§Øª")
        return await admin_panel(update, context)


# ========================== Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ (Campaign) ==========================

CAMPAIGN_TYPE_LABELS = {
    'air': 'âœˆï¸ Ù‡ÙˆØ§ÛŒÛŒ',
    'land': 'ðŸª– Ø²Ù…ÛŒÙ†ÛŒ',
    'sea': 'ðŸš¢ Ø¯Ø±ÛŒØ§ÛŒÛŒ'
}


async def campaign_menu(update: Update, context: CallbackContext) -> int:
    """Ù…Ø±Ø­Ù„Ù‡ Û±: Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù Ø¨Ø±Ø§ÛŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ."""
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯.")
            return MAIN_MENU
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != user_id]
        if not other_countries:
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ø­Ø§Ø¶Ø± Ù‡ÛŒÚ† Ú©Ø´ÙˆØ± Ø¯ÛŒÚ¯Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return MAIN_MENU

        # Ø±ÛŒØ³Øª Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ Ù…ÙˆÙ‚Øª
        context.user_data.pop('campaign', None)
        context.user_data['campaign'] = {
            'types': set(),  # 'air', 'land', 'sea'
        }

        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"campaign_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "âš”ï¸ *Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ*\n\n"
            "ðŸŽ¯ Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return CAMPAIGN_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in campaign_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ")
        return MAIN_MENU


async def campaign_select_target(update: Update, context: CallbackContext) -> int:
    """Ù…Ø±Ø­Ù„Ù‡ Û²: Ù†Ù…Ø§ÛŒØ´ Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§ (Ù‡ÙˆØ§ÛŒÛŒ/Ø²Ù…ÛŒÙ†ÛŒ/Ø¯Ø±ÛŒØ§ÛŒÛŒ)."""
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("campaign_target_", ""))
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return await campaign_menu(update, context)
        context.user_data.setdefault('campaign', {})
        context.user_data['campaign']['target_id'] = target_user_id
        context.user_data['campaign']['target_name'] = target_country['name']
        context.user_data['campaign']['types'] = set()
        return await _show_campaign_types_menu(update, context)
    except Exception as e:
        logger.error(f"Error in campaign_select_target: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù")
        return CAMPAIGN_SELECT_TARGET


async def _show_campaign_types_menu(update: Update, context: CallbackContext) -> int:
    """Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§ Ø¨Ø§ ØªÛŒÚ©."""
    campaign = context.user_data.get('campaign', {})
    selected = campaign.get('types', set())
    target_name = campaign.get('target_name', '')

    def btn(label_key, label_text):
        check = "âœ… " if label_key in selected else "â–«ï¸ "
        return InlineKeyboardButton(check + label_text, callback_data=f"campaign_toggle_{label_key}")

    keyboard = [
        [btn('air', 'Ù‡ÙˆØ§ÛŒÛŒ âœˆï¸')],
        [btn('land', 'Ø²Ù…ÛŒÙ†ÛŒ ðŸª–')],
        [btn('sea', 'Ø¯Ø±ÛŒØ§ÛŒÛŒ ðŸš¢')],
        [InlineKeyboardButton("âš”ï¸ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ", callback_data='campaign_start_input')],
        [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='campaign_back_targets')]
    ]
    text = (
        f"âš”ï¸ *Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¨Ù‡ {target_name}*\n\n"
        "ðŸŽ–ï¸ Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø§Ø¹Ø²Ø§Ù…ÛŒ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯ (Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ú†Ù†Ø¯ Ù†ÙˆØ¹ Ø±Ø§ Ù‡Ù…Ø²Ù…Ø§Ù† Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯):\n\n"
        "Ø³Ù¾Ø³ Ø±ÙˆÛŒ Â«âš”ï¸ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒÂ» Ø¨Ø²Ù†ÛŒØ¯ ØªØ§ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ùˆ Ø³Ù†Ø§Ø±ÛŒÙˆ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯."
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
    """Ø¨Ø±Ú¯Ø´Øª Ø¨Ù‡ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù."""
    return await campaign_menu(update, context)


async def campaign_start_input(update: Update, context: CallbackContext) -> int:
    """Ù…Ø±Ø­Ù„Ù‡ Û³: Ø¯Ø±Ø®ÙˆØ§Ø³Øª ÙˆØ§Ø±Ø¯ Ú©Ø±Ø¯Ù† Ù„ÛŒØ³Øª ØªØ¬Ù‡ÛŒØ²Ø§Øª."""
    query = update.callback_query
    await query.answer()
    campaign = context.user_data.get('campaign', {})
    selected = campaign.get('types', set())
    if not selected:
        await query.answer("âŒ Ø­Ø¯Ø§Ù‚Ù„ ÛŒÚ© Ù†ÙˆØ¹ Ù†ÛŒØ±Ùˆ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯!", show_alert=True)
        return CAMPAIGN_SELECT_TYPES

    target_name = campaign.get('target_name', '')
    types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in ['air', 'land', 'sea'] if t in selected)
    await query.edit_message_text(
        f"âš”ï¸ *Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¨Ù‡ {target_name}*\n"
        f"ðŸŽ–ï¸ Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§: {types_str}\n\n"
        "ðŸ“‹ Ù„Ø·ÙØ§Ù‹ *Ù„ÛŒØ³Øª ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø§Ø¹Ø²Ø§Ù…ÛŒ* Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯\n"
        "(Ù…Ø«Ø§Ù„: Â«ÛµÛ°Û°Û° Ø³Ø±Ø¨Ø§Ø²ØŒ Û±Û°Û° ØªØ§Ù†Ú©ØŒ Û²Û° Ø¬Ù†Ú¯Ù†Ø¯Ù‡Â»)",
        parse_mode="Markdown"
    )
    return CAMPAIGN_GET_EQUIPMENT


async def campaign_get_equipment(update: Update, context: CallbackContext) -> int:
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("âŒ Ù¾ÛŒØ§Ù… Ø®Ø§Ù„ÛŒ Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ù„ÛŒØ³Øª ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return CAMPAIGN_GET_EQUIPMENT
    context.user_data.setdefault('campaign', {})['equipment'] = text
    await update.message.reply_text(
        "âœ… Ù„ÛŒØ³Øª ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø«Ø¨Øª Ø´Ø¯.\n\n"
        "ðŸ“ Ø­Ø§Ù„Ø§ *Ø³Ù†Ø§Ø±ÛŒÙˆÛŒ Ø§ÙˆÙ„ÛŒÙ‡* Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ (Ø­Ø¯Ø§Ú©Ø«Ø± *Û±Û°Û°Û° Ú©Ø§Ø±Ø§Ú©ØªØ±*).\n\n"
        "Ù¾Ø³ Ø§Ø² Ø§Ø±Ø³Ø§Ù„ Ù…ØªÙ†ØŒ Ø¯Ú©Ù…Ù‡ Â«âœ… Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒÂ» Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯.",
        parse_mode="Markdown"
    )
    return CAMPAIGN_GET_SCENARIO


async def campaign_get_scenario(update: Update, context: CallbackContext) -> int:
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("âŒ Ø³Ù†Ø§Ø±ÛŒÙˆ Ø®Ø§Ù„ÛŒ Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† Ø³Ù†Ø§Ø±ÛŒÙˆ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:")
        return CAMPAIGN_GET_SCENARIO
    if len(text) > 1000:
        extra = len(text) - 1000
        await update.message.reply_text(
            f"âš ï¸ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Û±Û°Û°Û° Ú©Ø§Ø±Ø§Ú©ØªØ± Ø§Ø³ØªØ› Ù…ØªÙ† Ø´Ù…Ø§ {extra} Ú©Ø§Ø±Ø§Ú©ØªØ± Ø¨ÛŒØ´ØªØ± Ø§Ø³Øª.\n"
            "Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† Ú©ÙˆØªØ§Ù‡â€ŒØªØ±ÛŒ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
        )
        return CAMPAIGN_GET_SCENARIO

    context.user_data.setdefault('campaign', {})['scenario'] = text

    campaign = context.user_data['campaign']
    target_name = campaign.get('target_name', '')
    types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in ['air', 'land', 'sea'] if t in campaign.get('types', set()))

    preview = (
        f"âš”ï¸ *Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ*\n\n"
        f"ðŸŽ¯ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù: {target_name}\n"
        f"ðŸŽ–ï¸ Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§: {types_str}\n\n"
        f"ðŸ“‹ *ØªØ¬Ù‡ÛŒØ²Ø§Øª:*\n{campaign.get('equipment','-')}\n\n"
        f"ðŸ“ *Ø³Ù†Ø§Ø±ÛŒÙˆ:*\n{campaign.get('scenario','-')}"
    )
    keyboard = [
        [InlineKeyboardButton("âœ… Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ", callback_data='campaign_final_send')],
        [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='campaign_cancel')]
    ]
    await update.message.reply_text(preview, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return CAMPAIGN_CONFIRM


async def campaign_cancel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.pop('campaign', None)
    try:
        await query.edit_message_text("âŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ù„ØºÙˆ Ø´Ø¯.")
    except Exception:
        pass
    return await show_main_menu(update, context)


async def campaign_final_send(update: Update, context: CallbackContext) -> int:
    """Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† Ø¨Ø±Ø§ÛŒ ØªØ£ÛŒÛŒØ¯."""
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU
        campaign = context.user_data.get('campaign', {})
        target_id = campaign.get('target_id')
        target_name = campaign.get('target_name')
        types_set = campaign.get('types', set())
        equipment = campaign.get('equipment', '-')
        scenario = campaign.get('scenario', '-')

        if not target_id or not types_set:
            await query.edit_message_text("âŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù†Ø§Ù‚Øµ Ø§Ø³Øª. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†ÙˆÛŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU

        types_list = [t for t in ['air', 'land', 'sea'] if t in types_set]
        types_str = " + ".join(CAMPAIGN_TYPE_LABELS[t] for t in types_list)

        # Ù…ØªÙ† Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯Ù‡ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† (Ø³Ø§Ø¯Ù‡ØŒ Ø´Ø§Ù…Ù„ Ù‡Ù…Ù‡ Ø¬Ø²Ø¦ÛŒØ§Øª)
        admin_text = (
            f"âš”ï¸ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¬Ø¯ÛŒØ¯\n\n"
            f"Ø§Ø² Ú©Ø´ÙˆØ±: {country['name']} (ID: {user_id})\n"
            f"Ø¨Ù‡ Ú©Ø´ÙˆØ±: {target_name} (ID: {target_id})\n"
            f"Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§: {types_str}\n\n"
            f"ØªØ¬Ù‡ÛŒØ²Ø§Øª:\n{equipment}\n\n"
            f"Ø³Ù†Ø§Ø±ÛŒÙˆÛŒ Ø§ÙˆÙ„ÛŒÙ‡:\n{scenario}"
        )

        # Ø°Ø®ÛŒØ±Ù‡ proposal Ø¨Ø§ type Ø¬Ø¯ÛŒØ¯ 'campaign'
        # Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ Ø§Ø¶Ø§ÙÙ‡ Ø±Ø§ Ø¯Ø± text_content JSON-Ù…Ø§Ù†Ù†Ø¯ Ù…ÛŒâ€ŒÚ¯Ø°Ø§Ø±ÛŒÙ… ØªØ§ Ø­ÛŒÙ† ØªØ£ÛŒÛŒØ¯ Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ Ø´ÙˆØ¯
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
            [InlineKeyboardButton("âœ… ØªØ§ÛŒÛŒØ¯", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("âŒ Ø±Ø¯", callback_data=f"reject_{proposal_id}")]
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
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† {admin_id}: {e}")

        await query.edit_message_text(
            "âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¨Ø±Ø§ÛŒ Ø¨Ø±Ø±Ø³ÛŒ Ø§Ø¯Ù…ÛŒÙ† Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯.\n"
            "Ù¾Ø³ Ø§Ø² ØªØ£ÛŒÛŒØ¯ØŒ Ø®Ø¨Ø± Ø¢Ù† Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø¬Ù†Ú¯ Ù…Ù†ØªØ´Ø± Ø®ÙˆØ§Ù‡Ø¯ Ø´Ø¯."
        )

        context.user_data.pop('campaign', None)
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in campaign_final_send: {e}", exc_info=True)
        await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ.")
        return MAIN_MENU


# ============================== Ù¾Ø§ÛŒØ§Ù† Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ ==============================


# ============================== Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§ (Ù¾Ù„ÛŒØ±) ==============================

async def role_sena_menu(update: Update, context: CallbackContext) -> int:
    """Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§ Ø¨Ø±Ø§ÛŒ Ù¾Ù„ÛŒØ±: Û´ Ø¯Ú©Ù…Ù‡."""
    query = update.callback_query
    if query:
        await query.answer()
    try:
        user_id = (query.from_user.id if query else update.effective_user.id)
        country = get_country(user_id)
        if not country:
            text = "âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯."
            if query:
                await query.edit_message_text(text)
            else:
                await update.message.reply_text(text)
            return MAIN_MENU

        # Ø³Ø§Ø®Øª Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ Ø¨Ø§ Ù†Ù…Ø§ÛŒØ´ ÙˆØ¶Ø¹ÛŒØª
        def cat_btn(cat_key):
            info = ROLE_SENA_CATEGORIES[cat_key]
            enabled = role_sena_is_category_enabled(cat_key)
            group = info['group']
            limit = role_sena_get_limit(group)
            used = role_sena_get_group_used(user_id, group)
            if not enabled:
                txt = f"{info['label']} (âŒ ØºÛŒØ±ÙØ¹Ø§Ù„)"
            else:
                remaining = max(0, limit - used)
                txt = f"{info['label']}  â€¢  Ø¨Ø§Ù‚ÛŒÙ…Ø§Ù†Ø¯Ù‡: {remaining}/{limit}"
            return InlineKeyboardButton(txt, callback_data=f"role_sena_cat_{cat_key}")

        keyboard = [
            [cat_btn('security')],
            [cat_btn('economic')],
            [cat_btn('sabotage')],
            [cat_btn('sena')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "ðŸ“œ *Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§*\n\n"
            "Ø§Ø² Ø¨ÛŒÙ† Ú¯Ø²ÛŒÙ†Ù‡â€ŒÙ‡Ø§ÛŒ Ø²ÛŒØ± ÛŒÚ©ÛŒ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:\n"
            "â€¢ Ø§Ù…Ù†ÛŒØªÛŒØŒ Ø§Ù‚ØªØµØ§Ø¯ÛŒ Ùˆ Ø®Ø±Ø§Ø¨Ú©Ø§Ø±ÛŒ Ø¯Ø± Ø³Ù‡Ù…ÛŒÙ‡ Ø±ÙˆÙ„â€ŒÙ‡Ø§ Ù…Ø´ØªØ±Ú© Ù‡Ø³ØªÙ†Ø¯.\n"
            "â€¢ Ø³Ù†Ø§ Ø³Ù‡Ù…ÛŒÙ‡ Ø¬Ø¯Ø§Ú¯Ø§Ù†Ù‡ Ø¯Ø§Ø±Ø¯.\n"
            "ðŸ” Ø³Ù‡Ù…ÛŒÙ‡â€ŒÙ‡Ø§ Ù‡Ø± Ø±ÙˆØ² Ø³Ø§Ø¹Øª Û±Û² Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù† Ø±ÛŒØ³Øª Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯."
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
                await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§.")
            except Exception:
                pass
        return MAIN_MENU


async def role_sena_pick_category(update: Update, context: CallbackContext) -> int:
    """Ú©Ø§Ø±Ø¨Ø± ÛŒÚ©ÛŒ Ø§Ø² Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø±Ø¯Ù‡."""
    query = update.callback_query
    await query.answer()
    try:
        cat_key = query.data.replace("role_sena_cat_", "")
        if cat_key not in ROLE_SENA_CATEGORIES:
            await query.answer("Ø¯Ø³ØªÙ‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª", show_alert=True)
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
        # Ù…Ø­Ø¯ÙˆØ¯ÛŒØª ÙˆØ§Ù‚Ø¹ÛŒ ÙˆØ±ÙˆØ¯ÛŒ = min(max_chars, 4096) Ú†ÙˆÙ† ØªÙ„Ú¯Ø±Ø§Ù… Ø¨ÛŒØ´ØªØ± Ø§Ø² Û´Û°Û¹Û¶ Ù†Ù…ÛŒâ€ŒÙØ±Ø³ØªØ¯
        effective_input_limit = min(max_chars, TELEGRAM_MSG_LIMIT)

        if cat_key == 'sena':
            header = (
                f"ðŸ“œ *Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§*\n"
                f"ðŸ“Š Ø³Ù‡Ù…ÛŒÙ‡ Ø¨Ø§Ù‚ÛŒÙ…Ø§Ù†Ø¯Ù‡ Ø§Ù…Ø±ÙˆØ²: {remaining}/{limit}\n"
                f"ðŸ“ Ø­Ø¯Ø§Ú©Ø«Ø± Ø·ÙˆÙ„ Ø§ÛŒÙ† Ù¾ÛŒØ§Ù…: {effective_input_limit:,} Ú©Ø§Ø±Ø§Ú©ØªØ±\n"
                f"   (Ù‡Ø± ØµÙØ­Ù‡ = Û´Û°Û¹Û¶ Ú©Ø§Ø±Ø§Ú©ØªØ±Ø› Ø³Ù‚Ù Ú©Ù„ÛŒ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ†: {max_chars:,})\n\n"
                "Ù…ØªÙ† Ø³Ù†Ø§ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
            )
        else:
            header = (
                f"{info['label']}\n"
                f"ðŸ“Š Ø³Ù‡Ù…ÛŒÙ‡ Ø¨Ø§Ù‚ÛŒÙ…Ø§Ù†Ø¯Ù‡ Ø§Ù…Ø±ÙˆØ² (Ø±ÙˆÙ„): {remaining}/{limit}\n"
                f"ðŸ“ Ø­Ø¯Ø§Ú©Ø«Ø± Ø·ÙˆÙ„ Ø§ÛŒÙ† Ù¾ÛŒØ§Ù…: {effective_input_limit:,} Ú©Ø§Ø±Ø§Ú©ØªØ±\n"
                f"   (Ù‡Ø± ØµÙØ­Ù‡ = Û´Û°Û¹Û¶ Ú©Ø§Ø±Ø§Ú©ØªØ±Ø› Ø³Ù‚Ù Ú©Ù„ÛŒ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ†: {max_chars:,})\n\n"
                "Ù…ØªÙ† Ø±ÙˆÙ„ Ø®ÙˆØ¯ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
            )

        keyboard = [[InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='role_sena_back')]]
        await query.edit_message_text(header, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return ROLE_SENA_GET_CONTENT
    except Exception as e:
        logger.error(f"Error in role_sena_pick_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø³ØªÙ‡")
        return ROLE_SENA_MENU


async def role_sena_back(update: Update, context: CallbackContext) -> int:
    """Ø¨Ø±Ú¯Ø´Øª Ø¨Ù‡ Ù…Ù†ÙˆÛŒ Ø±ÙˆÙ„/Ø³Ù†Ø§."""
    context.user_data.pop('role_sena_category', None)
    return await role_sena_menu(update, context)


async def role_sena_get_content(update: Update, context: CallbackContext) -> int:
    """Ø¯Ø±ÛŒØ§ÙØª Ù…ØªÙ† Ø±ÙˆÙ„/Ø³Ù†Ø§ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ù…Ù‚ØµØ¯."""
    user_id = update.effective_user.id
    cat_key = context.user_data.get('role_sena_category')
    if not cat_key or cat_key not in ROLE_SENA_CATEGORIES:
        await update.message.reply_text("âŒ Ø¯Ø³ØªÙ‡ Ø§Ù†ØªØ®Ø§Ø¨ Ù†Ø´Ø¯Ù‡. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†ÙˆÛŒ Ø±ÙˆÙ„/Ø³Ù†Ø§ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
        return MAIN_MENU

    # Ø¨Ø±Ø±Ø³ÛŒ Ù…Ø¬Ø¯Ø¯ Ø³Ù‡Ù…ÛŒÙ‡ (Ù…Ù…Ú©Ù†Ù‡ Ø¨ÛŒÙ† Ø§Ù†ØªØ®Ø§Ø¨ Ùˆ Ø§Ø±Ø³Ø§Ù„ØŒ Ø§Ø¯Ù…ÛŒÙ† ØªØºÛŒÛŒØ± Ø¯Ø§Ø¯Ù‡ Ø¨Ø§Ø´Ù‡)
    ok, reason = role_sena_can_send(user_id, cat_key)
    if not ok:
        await update.message.reply_text(f"âŒ {reason}")
        return await role_sena_menu(update, context)

    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("âŒ Ù…ØªÙ† Ø®Ø§Ù„ÛŒ Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† Ø®ÙˆØ¯ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:")
        return ROLE_SENA_GET_CONTENT

    max_chars = role_sena_get_max_chars()
    effective_input_limit = min(max_chars, TELEGRAM_MSG_LIMIT)
    if len(text) > effective_input_limit:
        extra = len(text) - effective_input_limit
        await update.message.reply_text(
            f"âš ï¸ Ù…ØªÙ† Ø´Ù…Ø§ Ø§Ø² Ø­Ø¯Ø§Ú©Ø«Ø± Ù…Ø¬Ø§Ø² ({effective_input_limit:,} Ú©Ø§Ø±Ø§Ú©ØªØ±) Ø¨ÛŒØ´ØªØ± Ø§Ø³Øª.\n"
            f"ØªØ¹Ø¯Ø§Ø¯ Ø§Ø¶Ø§ÙÛŒ: {extra:,} Ú©Ø§Ø±Ø§Ú©ØªØ±.\n"
            f"(Ù‡Ø± ØµÙØ­Ù‡ = Û´Û°Û¹Û¶ Ú©Ø§Ø±Ø§Ú©ØªØ±ØŒ Ú©Ù‡ Ø³Ù‚Ù Ø®ÙˆØ¯ ØªÙ„Ú¯Ø±Ø§Ù… Ø¨Ø±Ø§ÛŒ ÛŒÚ© Ù¾ÛŒØ§Ù… Ø§Ø³Øª.)\n"
            "Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† Ú©ÙˆØªØ§Ù‡â€ŒØªØ±ÛŒ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
        )
        return ROLE_SENA_GET_CONTENT

    country = get_country(user_id)
    country_name = country.get('name', 'Ù†Ø§Ù…Ø´Ø®Øµ') if country else 'Ù†Ø§Ù…Ø´Ø®Øµ'
    info = ROLE_SENA_CATEGORIES[cat_key]

    try:
        if cat_key == 'sena':
            # Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ù‡Ù…Ù‡ Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ (Ø¨Ø§ ØªÙ‚Ø³ÛŒÙ… Ú†Ù†Ø¯Ù¾ÛŒØ§Ù…ÛŒ Ø¯Ø± ØµÙˆØ±Øª Ø·ÙˆÙ„Ø§Ù†ÛŒ Ø¨ÙˆØ¯Ù†)
            header = (
                f"ðŸ“œ Ø³Ù†Ø§ÛŒ Ø¬Ø¯ÛŒØ¯\n"
                f"Ø§Ø² Ú©Ø´ÙˆØ±: {country_name} (ID: {user_id})\n"
                f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
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
                    logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† {admin_id}: {e}")
            if not sent_any:
                await update.message.reply_text("âŒ Ø§Ø±Ø³Ø§Ù„ Ù…ÙˆÙÙ‚ Ù†Ø¨ÙˆØ¯. Ù„Ø·ÙØ§Ù‹ Ø¨Ø¹Ø¯Ø§Ù‹ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
                return ROLE_SENA_MENU
            # Ø«Ø¨Øª Ø§Ø³ØªÙØ§Ø¯Ù‡
            role_sena_increment_usage(user_id, cat_key)
            limit = role_sena_get_limit('sena')
            used = role_sena_get_group_used(user_id, 'sena')
            remaining = max(0, limit - used)
            await update.message.reply_text(
                f"âœ… Ø³Ù†Ø§ÛŒ Ø´Ù…Ø§ Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯.\n"
                f"ðŸ“Š Ø³Ù‡Ù…ÛŒÙ‡ Ø¨Ø§Ù‚ÛŒÙ…Ø§Ù†Ø¯Ù‡ Ø³Ù†Ø§: {remaining}/{limit}"
            )
        else:
            # Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ Ø¨Ø§ Ù†Ø§Ù… Ú©Ø´ÙˆØ± (Ø¨Ø§ ØªÙ‚Ø³ÛŒÙ… Ú†Ù†Ø¯Ù¾ÛŒØ§Ù…ÛŒ Ø¯Ø± ØµÙˆØ±Øª Ø·ÙˆÙ„Ø§Ù†ÛŒ Ø¨ÙˆØ¯Ù†)
            header_md = (
                f"{info['label']} â€” *{country_name}*\n"
                f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
            )
            sent_count = 0
            try:
                sent_count = await _send_long_message(
                    context.bot, ROLE_CHANNEL, header_md, text, parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ (Markdown): {e}", exc_info=True)
                # ØªÙ„Ø§Ø´ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø¨Ø¯ÙˆÙ† Markdown
                header_plain = (
                    f"{info['label']} â€” {country_name}\n"
                    f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
                )
                try:
                    sent_count = await _send_long_message(
                        context.bot, ROLE_CHANNEL, header_plain, text, parse_mode=None
                    )
                except Exception as e2:
                    logger.error(f"Ø®Ø·Ø§ Ø¯Ø± ØªÙ„Ø§Ø´ Ø¯ÙˆÙ… Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„: {e2}")
            if sent_count <= 0:
                await update.message.reply_text("âŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ø§Ù…ÙˆÙÙ‚ Ø¨ÙˆØ¯.")
                return ROLE_SENA_MENU
            role_sena_increment_usage(user_id, cat_key)
            limit = role_sena_get_limit('role')
            used = role_sena_get_group_used(user_id, 'role')
            remaining = max(0, limit - used)
            extra_info = f"\nðŸ“„ ØªÙ‚Ø³ÛŒÙ… Ø´Ø¯ Ø¨Ù‡ {sent_count} Ù¾ÛŒØ§Ù…" if sent_count > 1 else ""
            await update.message.reply_text(
                f"âœ… {info['label']} Ø´Ù…Ø§ Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯.{extra_info}\n"
                f"ðŸ“Š Ø³Ù‡Ù…ÛŒÙ‡ Ø¨Ø§Ù‚ÛŒÙ…Ø§Ù†Ø¯Ù‡ Ø±ÙˆÙ„â€ŒÙ‡Ø§: {remaining}/{limit}"
            )
    except Exception as e:
        logger.error(f"Error sending role/sena: {e}", exc_info=True)
        await update.message.reply_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
        return ROLE_SENA_MENU

    context.user_data.pop('role_sena_category', None)
    return await role_sena_menu(update, context)


# --------- Ù…Ø¯ÛŒØ±ÛŒØª Ù…Ø­Ø¯ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§ (Ù¾Ù†Ù„ Ø§Ø¯Ù…ÛŒÙ†) ---------

async def role_sena_limits_menu(update: Update, context: CallbackContext) -> int:
    """Ù…Ù†ÙˆÛŒ Ù…Ø¯ÛŒØ±ÛŒØª Ù…Ø­Ø¯ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§: Ûµ Ø¯Ú©Ù…Ù‡ (Û´ Ø¯Ø³ØªÙ‡ + Ø³Ù‚Ù Ù‡Ø§)."""
    query = update.callback_query
    if query:
        await query.answer()
    user_id = (query.from_user.id if query else update.effective_user.id)
    if not is_admin(user_id):
        if query:
            await query.answer("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!", show_alert=True)
        return ADMIN_MENU

    role_limit = role_sena_get_limit('role')
    sena_limit = role_sena_get_limit('sena')
    max_chars = role_sena_get_max_chars()

    def cat_btn_admin(cat_key):
        info = ROLE_SENA_CATEGORIES[cat_key]
        en = role_sena_is_category_enabled(cat_key)
        mark = "âœ…" if en else "âŒ"
        return InlineKeyboardButton(
            f"{mark} {info['label']}",
            callback_data=f"role_sena_toggle_{cat_key}"
        )

    keyboard = [
        [cat_btn_admin('security')],
        [cat_btn_admin('economic')],
        [cat_btn_admin('sabotage')],
        [cat_btn_admin('sena')],
        [InlineKeyboardButton(f"ðŸ”¢ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø±ÙˆÙ„â€ŒÙ‡Ø§: {role_limit}", callback_data='role_sena_set_limit_role')],
        [InlineKeyboardButton(f"ðŸ”¢ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø³Ù†Ø§: {sena_limit}", callback_data='role_sena_set_limit_sena')],
        [InlineKeyboardButton(f"ðŸ“ Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ± Ù‡Ø± Ù¾ÛŒØ§Ù…: {max_chars:,}", callback_data='role_sena_set_max_chars')],
        [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')]
    ]
    text = (
        "ðŸš¦ *ØªØ¹ÛŒÛŒÙ† Ù…Ø­Ø¯ÙˆØ¯ÛŒØª â€” Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§*\n\n"
        "Ø±ÙˆÛŒ Ù‡Ø± Ø¨Ø®Ø´ Ø¨Ø²Ù† ØªØ§ ÙØ¹Ø§Ù„/ØºÛŒØ±ÙØ¹Ø§Ù„ Ø´ÙˆØ¯.\n"
        "Ø±ÙˆÛŒ Ù…Ø­Ø¯ÙˆØ¯ÛŒØªâ€ŒÙ‡Ø§ Ø¨Ø²Ù† ØªØ§ ØªØ¹Ø¯Ø§Ø¯ Ø±Ø§ ØªØºÛŒÛŒØ± Ø¯Ù‡ÛŒ.\n\n"
        f"â€¢ Ø±ÙˆÙ„â€ŒÙ‡Ø§ (Ø§Ù…Ù†ÛŒØªÛŒ + Ø§Ù‚ØªØµØ§Ø¯ÛŒ + Ø®Ø±Ø§Ø¨Ú©Ø§Ø±ÛŒ): {role_limit} Ù¾ÛŒØ§Ù… Ø¯Ø± Ø±ÙˆØ²\n"
        f"â€¢ Ø³Ù†Ø§: {sena_limit} Ù¾ÛŒØ§Ù… Ø¯Ø± Ø±ÙˆØ²\n"
        f"â€¢ Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ± Ù‡Ø± Ù¾ÛŒØ§Ù…: {max_chars:,}\n"
        "ðŸ” Ø±ÛŒØ³Øª Ø®ÙˆØ¯Ú©Ø§Ø± Ø³Ø§Ø¹Øª Û±Û² Ø¸Ù‡Ø± ØªÙ‡Ø±Ø§Ù†."
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
        await query.answer("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!", show_alert=True)
        return ROLE_SENA_LIMITS_MENU
    cat_key = query.data.replace("role_sena_toggle_", "")
    if cat_key not in ROLE_SENA_CATEGORIES:
        return ROLE_SENA_LIMITS_MENU
    current = role_sena_is_category_enabled(cat_key)
    role_sena_set_category_enabled(cat_key, not current)
    return await role_sena_limits_menu(update, context)


async def role_sena_set_limit_start(update: Update, context: CallbackContext) -> int:
    """Ø´Ø±ÙˆØ¹ ÙˆØ§Ø±Ø¯ Ú©Ø±Ø¯Ù† Ù…Ù‚Ø¯Ø§Ø± Ø¬Ø¯ÛŒØ¯ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª ÛŒØ§ Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ±."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'role_sena_set_limit_role':
        context.user_data['role_sena_setting_target'] = 'role_limit'
        await query.edit_message_text(
            f"ðŸ”¢ Ù…Ù‚Ø¯Ø§Ø± Ø¬Ø¯ÛŒØ¯ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø±ÙˆÙ„â€ŒÙ‡Ø§ (Ù…Ø¬Ù…ÙˆØ¹ Ø§Ù…Ù†ÛŒØªÛŒ/Ø§Ù‚ØªØµØ§Ø¯ÛŒ/Ø®Ø±Ø§Ø¨Ú©Ø§Ø±ÛŒ) Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.\n"
            f"Ù…Ù‚Ø¯Ø§Ø± ÙØ¹Ù„ÛŒ: {role_sena_get_limit('role')}\n\n"
            "ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ØºÛŒØ±Ù…Ù†ÙÛŒ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Û° ÛŒØ¹Ù†ÛŒ ØºÛŒØ±ÙØ¹Ø§Ù„):"
        )
    elif data == 'role_sena_set_limit_sena':
        context.user_data['role_sena_setting_target'] = 'sena_limit'
        await query.edit_message_text(
            f"ðŸ”¢ Ù…Ù‚Ø¯Ø§Ø± Ø¬Ø¯ÛŒØ¯ Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø³Ù†Ø§ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.\n"
            f"Ù…Ù‚Ø¯Ø§Ø± ÙØ¹Ù„ÛŒ: {role_sena_get_limit('sena')}\n\n"
            "ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ØºÛŒØ±Ù…Ù†ÙÛŒ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Û° ÛŒØ¹Ù†ÛŒ ØºÛŒØ±ÙØ¹Ø§Ù„):"
        )
    elif data == 'role_sena_set_max_chars':
        context.user_data['role_sena_setting_target'] = 'max_chars'
        await query.edit_message_text(
            f"ðŸ“ Ø³Ù‚Ù Ú©Ø§Ø±Ø§Ú©ØªØ± Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ø§Ø±Ø³Ø§Ù„ Ø±ÙˆÙ„/Ø³Ù†Ø§ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.\n"
            f"Ù…Ù‚Ø¯Ø§Ø± ÙØ¹Ù„ÛŒ: {role_sena_get_max_chars():,}\n"
            f"(Ø¯ÛŒÙØ§Ù„Øª Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ÛŒ: {5 * 4096:,} = Ûµ ØµÙØ­Ù‡ Ã— Û´Û°Û¹Û¶)\n\n"
            f"â„¹ï¸ ØªÙˆØ¬Ù‡: Ú†ÙˆÙ† ØªÙ„Ú¯Ø±Ø§Ù… Ø¨Ø±Ø§ÛŒ *Ù‡Ø± Ù¾ÛŒØ§Ù…* ÙÙ‚Ø· {TELEGRAM_MSG_LIMIT:,} Ú©Ø§Ø±Ø§Ú©ØªØ± Ø§Ø¬Ø§Ø²Ù‡ Ù…ÛŒâ€ŒØ¯Ù‡Ø¯ØŒ\n"
            f"Ø­Ø¯Ø§Ú©Ø«Ø± Ø·ÙˆÙ„ Ù¾ÛŒØ§Ù… ÙˆØ±ÙˆØ¯ÛŒ Ù¾Ù„ÛŒØ± Ø¯Ø± Ø¹Ù…Ù„ = min(Ø§ÛŒÙ† Ø¹Ø¯Ø¯, {TELEGRAM_MSG_LIMIT:,}) Ø®ÙˆØ§Ù‡Ø¯ Ø¨ÙˆØ¯.\n\n"
            "ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:"
        )
    else:
        return ROLE_SENA_LIMITS_MENU
    return ROLE_SENA_GET_LIMIT_VALUE


async def role_sena_save_limit_value(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    target = context.user_data.get('role_sena_setting_target')
    if not target:
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø´Ù†Ø§Ø³Ø§ÛŒÛŒ ØªÙ†Ø¸ÛŒÙ…. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†Ùˆ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
        return await role_sena_limits_menu(update, context)
    text = (update.message.text or "").strip().replace(',', '')
    try:
        value = int(text)
        if value < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text("âŒ Ù…Ù‚Ø¯Ø§Ø± Ù†Ø§Ù…Ø¹ØªØ¨Ø±. ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ØºÛŒØ±Ù…Ù†ÙÛŒ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return ROLE_SENA_GET_LIMIT_VALUE

    if target == 'role_limit':
        role_sena_set_limit('role', value)
        await update.message.reply_text(f"âœ… Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø±ÙˆÙ„â€ŒÙ‡Ø§ Ø¨Ù‡ {value} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
    elif target == 'sena_limit':
        role_sena_set_limit('sena', value)
        await update.message.reply_text(f"âœ… Ù…Ø­Ø¯ÙˆØ¯ÛŒØª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø³Ù†Ø§ Ø¨Ù‡ {value} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
    elif target == 'max_chars':
        if value <= 0:
            await update.message.reply_text("âŒ Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ± Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯:")
            return ROLE_SENA_GET_LIMIT_VALUE
        set_setting('role_sena_max_chars', str(value))
        await update.message.reply_text(f"âœ… Ø­Ø¯Ø§Ú©Ø«Ø± Ú©Ø§Ø±Ø§Ú©ØªØ± Ù‡Ø± Ù¾ÛŒØ§Ù… Ø¨Ù‡ {value:,} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
    context.user_data.pop('role_sena_setting_target', None)
    return await role_sena_limits_menu(update, context)


# ============================ Ù¾Ø§ÛŒØ§Ù† Ø±ÙˆÙ„ Ùˆ Ø³Ù†Ø§ ============================


async def attack_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯.")
            return MAIN_MENU
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != user_id]
        if not other_countries:
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ø­Ø§Ø¶Ø± Ù‡ÛŒÚ† Ú©Ø´ÙˆØ± Ø¯ÛŒÚ¯Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return MAIN_MENU
        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"attack_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("âš”ï¸ Ù„Ø·ÙØ§ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return ATTACK_TARGET
    except Exception as e:
        logger.error(f"Error in attack_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return MAIN_MENU


async def select_attack_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        target_user_id = int(query.data.replace("attack_target_", ""))
        context.user_data['attack_target_id'] = target_user_id
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return await attack_menu(update, context)
        context.user_data['attack_target_name'] = target_country['name']
        await query.edit_message_text(f"Ø´Ù…Ø§ Ú©Ø´ÙˆØ± {target_country['name']} Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø±Ø¯ÛŒØ¯.\n"
                                      "Ù„Ø·ÙØ§ Ù„ÛŒØ³Øª Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø´Ø¯Ù‡ Ø¯Ø± Ø­Ù…Ù„Ù‡ Ø±Ø§ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯ (Ù…Ø«Ø§Ù„: '5000 Ø³Ø±Ø¨Ø§Ø²ØŒ 100 ØªØ§Ù†Ú©'):")
        return GET_ATTACK_TROOPS_DETAILS
    except Exception as e:
        logger.error(f"Error in select_attack_target: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù")
        return ATTACK_TARGET


async def get_attack_troops_details(update: Update, context: CallbackContext) -> int:
    try:
        attack_target_name = context.user_data.get('attack_target_name')
        if not attack_target_name:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù‡Ø¯Ù Ø­Ù…Ù„Ù‡. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†ÙˆÛŒ Ø­Ù…Ù„Ù‡ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU
        troops_details = update.message.text
        context.user_data['attack_troops_details'] = troops_details
        await update.message.reply_text(f"Ù„ÛŒØ³Øª Ù†ÛŒØ±ÙˆÙ‡Ø§ Ø«Ø¨Øª Ø´Ø¯.\n"
                                        "Ø§Ú©Ù†ÙˆÙ†ØŒ Ù„Ø·ÙØ§Ù‹ Ø³Ù†Ø§Ø±ÛŒÙˆÛŒ Ø­Ù…Ù„Ù‡ Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯.\n"
                                        "Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ù…ØªÙ† Ø±Ø§ Ø¯Ø± Ú†Ù†Ø¯ Ù¾ÛŒØ§Ù… Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ Ùˆ ÛŒØ§ Ø¹Ú©Ø³â€ŒÙ‡Ø§ÛŒ Ù…Ø±ØªØ¨Ø· Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.\n"
                                        "Ø¨Ø¹Ø¯ Ø§Ø² Ø§ØªÙ…Ø§Ù…ØŒ Ø¯Ú©Ù…Ù‡ 'ØªØ§ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        context.user_data['attack_scenario_text'] = []
        context.user_data['attack_scenario_photos'] = []
        keyboard = [[InlineKeyboardButton("âœ… ØªØ§ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§Ø±ÛŒÙˆ", callback_data='confirm_attack_scenario')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await update.message.reply_text("Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø³Ù†Ø§Ø±ÛŒÙˆ Ù¾Ø³ Ø§Ø² ÙˆØ§Ø±Ø¯ Ú©Ø±Ø¯Ù† ØªÙ…Ø§Ù…ÛŒ Ø§Ø·Ù„Ø§Ø¹Ø§ØªØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
        context.user_data['user_proposal_message_id'] = sent_message.message_id
        return GET_ATTACK_SCENARIO_INPUT
    except Exception as e:
        logger.error(f"Error in get_attack_troops_details: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø«Ø¨Øª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù†ÛŒØ±ÙˆÙ‡Ø§")
        return MAIN_MENU


async def get_attack_scenario_input(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    try:
        if update.message.text:
            context.user_data['attack_scenario_text'].append(update.message.text)
            await context.bot.send_message(chat_id, "Ù…ØªÙ† Ø³Ù†Ø§Ø±ÛŒÙˆ Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯. Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ø§Ø¯Ø§Ù…Ù‡ Ø¯Ù‡ÛŒØ¯ ÛŒØ§ Ø¯Ú©Ù…Ù‡ 'ØªØ§ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§Ø±ÛŒÙˆ' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        elif update.message.photo:
            photo_id = update.message.photo[-1].file_id
            context.user_data['attack_scenario_photos'].append(photo_id)
            await context.bot.send_message(chat_id, "Ø¹Ú©Ø³ Ø³Ù†Ø§Ø±ÛŒÙˆ Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯. Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ø§Ø¯Ø§Ù…Ù‡ Ø¯Ù‡ÛŒØ¯ ÛŒØ§ Ø¯Ú©Ù…Ù‡ 'ØªØ§ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§Ø±ÛŒÙˆ' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        else:
            await context.bot.send_message(chat_id, "Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† ÛŒØ§ Ø¹Ú©Ø³ Ù…Ø¹ØªØ¨Ø± Ø¨Ø±Ø§ÛŒ Ø³Ù†Ø§Ø±ÛŒÙˆ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
    except Exception as e:
        logger.error(f"Error in get_attack_scenario_input: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø³Ù†Ø§Ø±ÛŒÙˆ. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")

    keyboard = [[InlineKeyboardButton("âœ… ØªØ§ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø³Ù†Ø§Ø±ÛŒÙˆ", callback_data='confirm_attack_scenario')]]
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
                sent_message = await context.bot.send_message(chat_id, "Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø³Ù†Ø§Ø±ÛŒÙˆ Ù¾Ø³ Ø§Ø² ÙˆØ§Ø±Ø¯ Ú©Ø±Ø¯Ù† ØªÙ…Ø§Ù…ÛŒ Ø§Ø·Ù„Ø§Ø¹Ø§ØªØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
                context.user_data['user_proposal_message_id'] = sent_message.message_id
            except Exception as e2:
                logger.error(f"Failed to send new message: {e2}")
    else:
        try:
            sent_message = await context.bot.send_message(chat_id, "Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø³Ù†Ø§Ø±ÛŒÙˆ Ù¾Ø³ Ø§Ø² ÙˆØ§Ø±Ø¯ Ú©Ø±Ø¯Ù† ØªÙ…Ø§Ù…ÛŒ Ø§Ø·Ù„Ø§Ø¹Ø§ØªØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
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
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await context.bot.send_message(chat_id, "âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU
        attack_target_id = context.user_data.get('attack_target_id')
        attack_target_name = context.user_data.get('attack_target_name')
        troops_details = context.user_data.get('attack_troops_details', 'Ø¨Ø¯ÙˆÙ† Ø¬Ø²Ø¦ÛŒØ§Øª Ù†ÛŒØ±Ùˆ.')
        scenario_text_parts = context.user_data.get('attack_scenario_text', [])
        scenario_photos = context.user_data.get('attack_scenario_photos', [])
        user_proposal_message_id = context.user_data.get('user_proposal_message_id')
        full_scenario_text = "\n\n".join(scenario_text_parts) if scenario_text_parts else "Ø¨Ø¯ÙˆÙ† Ø³Ù†Ø§Ø±ÛŒÙˆ."
        if not attack_target_id:
            await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ø­Ù…Ù„Ù‡. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU
        target_country = get_country(attack_target_id)
        admin_message = (
            f"âš”ï¸ *Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø­Ù…Ù„Ù‡ Ø¬Ø¯ÛŒØ¯*\n\n"
            f"ðŸ‘¤ Ø¢ØºØ§Ø²Ú©Ù†Ù†Ø¯Ù‡: {country['name']} (ID: {user_id})\n"
            f"ðŸŽ¯ Ù‡Ø¯Ù Ø­Ù…Ù„Ù‡: {target_country['name']} (ID: {attack_target_id})\n\n"
            f"*Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø´Ø¯Ù‡:*\n{troops_details}\n\n"
            f"*Ø³Ù†Ø§Ø±ÛŒÙˆÛŒ Ø­Ù…Ù„Ù‡:*\n{full_scenario_text}"
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
            [InlineKeyboardButton("âœ… ØªØ§ÛŒÛŒØ¯ Ø­Ù…Ù„Ù‡", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("âŒ Ø±Ø¯ Ø­Ù…Ù„Ù‡", callback_data=f"reject_{proposal_id}")]
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
        await context.bot.send_message(chat_id, "âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø­Ù…Ù„Ù‡ Ø´Ù…Ø§ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯ Ùˆ Ø¯Ø± Ø­Ø§Ù„ Ø¨Ø±Ø±Ø³ÛŒ Ø§Ø³Øª. Ù…Ù†ØªØ¸Ø± Ù¾Ø§Ø³Ø® Ø¨Ù…Ø§Ù†ÛŒØ¯.")

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
        await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø­Ù…Ù„Ù‡")
        return MAIN_MENU


async def send_proposal_start(update: Update, context: CallbackContext, proposal_type: str) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯.")
            return MAIN_MENU
        context.user_data['current_proposal_type'] = proposal_type
        context.user_data['proposal_text_parts'] = []
        context.user_data['proposal_photo_ids'] = []
        proposal_display_name = PROPOSAL_TYPES.get(proposal_type, "Ø¯Ø±Ø®ÙˆØ§Ø³Øª")
        await query.edit_message_text(f"ðŸ“ Ù„Ø·ÙØ§Ù‹ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª {proposal_display_name} Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù†ÙˆÛŒØ³ÛŒØ¯.\n"
                                      "Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ù…ØªÙ† Ø±Ø§ Ø¯Ø± Ú†Ù†Ø¯ Ù¾ÛŒØ§Ù… Ùˆ Ù‡Ù…Ú†Ù†ÛŒÙ† Ø¹Ú©Ø³â€ŒÙ‡Ø§ÛŒ Ù…Ø±ØªØ¨Ø· Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.\n"
                                      "Ù¾Ø³ Ø§Ø² Ø§ØªÙ…Ø§Ù…ØŒ Ø¯Ú©Ù…Ù‡ 'Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        keyboard = [[InlineKeyboardButton("âœ… Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ", callback_data='final_send_proposal')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await query.message.reply_text("Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®ÙˆØ¯ØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
        context.user_data['user_proposal_message_id'] = sent_message.message_id
        return GET_PROPOSAL_TEXT
    except Exception as e:
        logger.error(f"Error in send_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø´Ø±ÙˆØ¹ Ø¯Ø±Ø®ÙˆØ§Ø³Øª")
        return MAIN_MENU


async def get_proposal_content(update: Update, context: CallbackContext) -> int:
    chat_id = update.effective_chat.id
    try:
        if update.message.text:
            context.user_data['proposal_text_parts'].append(update.message.text)
            await context.bot.send_message(chat_id, "Ù…ØªÙ† Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯. Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ø§Ø¯Ø§Ù…Ù‡ Ø¯Ù‡ÛŒØ¯ ÛŒØ§ Ø¯Ú©Ù…Ù‡ 'Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        elif update.message.photo:
            photo_id = update.message.photo[-1].file_id
            context.user_data['proposal_photo_ids'].append(photo_id)
            await context.bot.send_message(chat_id, "Ø¹Ú©Ø³ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯. Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ø§Ø¯Ø§Ù…Ù‡ Ø¯Ù‡ÛŒØ¯ ÛŒØ§ Ø¯Ú©Ù…Ù‡ 'Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ' Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯.")
        else:
            await context.bot.send_message(chat_id, "Ù„Ø·ÙØ§Ù‹ Ù…ØªÙ† ÛŒØ§ Ø¹Ú©Ø³ Ù…Ø¹ØªØ¨Ø± Ø¨Ø±Ø§ÛŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
    except Exception as e:
        logger.error(f"Error in get_proposal_content: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")

    keyboard = [[InlineKeyboardButton("âœ… Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ", callback_data='final_send_proposal')]]
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
                sent_message = await context.bot.send_message(chat_id, "Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®ÙˆØ¯ØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
                context.user_data['user_proposal_message_id'] = sent_message.message_id
            except Exception as e2:
                logger.error(f"Failed to send new message: {e2}")
    else:
        try:
            sent_message = await context.bot.send_message(chat_id, "Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù†Ù‡Ø§ÛŒÛŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®ÙˆØ¯ØŒ Ø¯Ú©Ù…Ù‡ Ø²ÛŒØ± Ø±Ø§ ÙØ´Ø§Ø± Ø¯Ù‡ÛŒØ¯:", reply_markup=reply_markup)
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
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await context.bot.send_message(chat_id, "âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU
        proposal_type = context.user_data.get('current_proposal_type')
        proposal_text_parts = context.user_data.get('proposal_text_parts', [])
        proposal_photo_ids = context.user_data.get('proposal_photo_ids', [])
        user_proposal_message_id = context.user_data.get('user_proposal_message_id')
        full_proposal_text = "\n\n".join(proposal_text_parts) if proposal_text_parts else "Ø¨Ø¯ÙˆÙ† Ø¬Ø²Ø¦ÛŒØ§Øª."
        proposal_display_name = PROPOSAL_TYPES.get(proposal_type, "Ø¯Ø±Ø®ÙˆØ§Ø³Øª")
        if not proposal_type:
            await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ù†ÙˆØ¹ Ø¯Ø±Ø®ÙˆØ§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU
        admin_message = (
            f"ðŸ“ *Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø¬Ø¯ÛŒØ¯ - {proposal_display_name}*\n\n"
            f"ðŸ‘¤ Ø§Ø²: {country['name']} (ID: {user_id})\n\n"
            f"*Ø¬Ø²Ø¦ÛŒØ§Øª Ø¯Ø±Ø®ÙˆØ§Ø³Øª:*\n{full_proposal_text}"
        )
        proposal_id = save_proposal(user_id, proposal_type, admin_message, proposal_photo_ids, user_proposal_message_id)
        admin_action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("âœ… ØªØ§ÛŒÛŒØ¯", callback_data=f"approve_{proposal_id}"),
             InlineKeyboardButton("âŒ Ø±Ø¯", callback_data=f"reject_{proposal_id}")]
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
        await context.bot.send_message(chat_id, f"âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª {proposal_display_name} Ø´Ù…Ø§ Ø¨Ù‡ Ø§Ø¯Ù…ÛŒÙ† Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯ Ùˆ Ø¯Ø± Ø­Ø§Ù„ Ø¨Ø±Ø±Ø³ÛŒ Ø§Ø³Øª. Ù…Ù†ØªØ¸Ø± Ù¾Ø§Ø³Ø® Ø¨Ù…Ø§Ù†ÛŒØ¯.")

        keys_to_remove = [
            'current_proposal_type', 'proposal_text_parts', 'proposal_photo_ids', 'user_proposal_message_id'
        ]
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in final_send_proposal: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª")
        return MAIN_MENU


async def handle_proposal_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if not is_admin(query.from_user.id):
        await query.answer("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ù†Ø¯ Ø§ÛŒÙ† Ø¹Ù…Ù„ Ø±Ø§ Ø§Ù†Ø¬Ø§Ù… Ø¯Ù‡Ù†Ø¯!", show_alert=True)
        return ADMIN_MENU
    try:
        action, proposal_id = query.data.split('_', 1)
        proposal = get_proposal(proposal_id)
        if not proposal:
            await query.edit_message_text("âŒ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ÛŒØ§ÙØª Ù†Ø´Ø¯ ÛŒØ§ Ù‚Ø¨Ù„Ø§Ù‹ Ø±Ø³ÛŒØ¯Ú¯ÛŒ Ø´Ø¯Ù‡ Ø§Ø³Øª.")
            return ADMIN_MENU
        user_id = proposal['user_id']
        country = get_country(user_id)
        proposal_display_name = PROPOSAL_TYPES.get(proposal['type'], "Ø¯Ø±Ø®ÙˆØ§Ø³Øª")
        status_text = "ØªØ§ÛŒÛŒØ¯" if action == "approve" else "Ø±Ø¯"
        update_proposal_status(proposal_id, action)
        try:
            if query.message.caption:
                await query.edit_message_caption(caption=f"{query.message.caption}\n\n*ÙˆØ¶Ø¹ÛŒØª: {status_text} Ø´Ø¯Ù‡ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† {query.from_user.first_name}*",
                                                 reply_markup=None,
                                                 parse_mode="Markdown")
            else:
                await query.edit_message_text(text=f"{query.message.text}\n\n*ÙˆØ¶Ø¹ÛŒØª: {status_text} Ø´Ø¯Ù‡ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† {query.from_user.first_name}*",
                                              reply_markup=None,
                                              parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error editing admin message for proposal {proposal_id}: {e}")
            if proposal['admin_message_id']:
                try:
                    await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                        message_id=proposal['admin_message_id'],
                                                        text=f"{proposal['text_content']}\n\n*ÙˆØ¶Ø¹ÛŒØª: {status_text} Ø´Ø¯Ù‡ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† {query.from_user.first_name}*",
                                                        parse_mode="Markdown",
                                                        reply_markup=None)
                except Exception as e:
                    logger.error(f"Error editing admin message via ID {proposal['admin_message_id']} for proposal {proposal_id}: {e}")
                    await query.message.reply_text(f"Ø¯Ø±Ø®ÙˆØ§Ø³Øª {proposal_id} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª {status_text} Ø´Ø¯. (Ø®Ø·Ø§ Ø¯Ø± ÙˆÛŒØ±Ø§ÛŒØ´ Ù¾ÛŒØ§Ù… Ø§ØµÙ„ÛŒ Ø§Ø¯Ù…ÛŒÙ†)")
            else:
                await query.message.reply_text(f"Ø¯Ø±Ø®ÙˆØ§Ø³Øª {proposal_id} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª {status_text} Ø´Ø¯. (Ù¾ÛŒØ§Ù… Ø§ØµÙ„ÛŒ Ø§Ø¯Ù…ÛŒÙ† ÛŒØ§ÙØª Ù†Ø´Ø¯.)")
        user_notification_text = (
            f"âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª {proposal_display_name} Ø´Ù…Ø§ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† *{query.from_user.first_name}* {status_text} Ø´Ø¯.\n"
        )
        # Ø¨Ø±Ø§ÛŒ campaign Ø§Ø² Ù†Ù…Ø§ÛŒØ´ Ø¬Ø²Ø¦ÛŒØ§Øª JSON Ø¯Ø± Ù¾ÛŒØ§Ù… Ú©Ø§Ø±Ø¨Ø± ØµØ±Ù Ù†Ø¸Ø± Ù…ÛŒâ€ŒÚ©Ù†ÛŒÙ…
        if proposal['type'] != "campaign" and len(proposal['text_content']) < 1000:
            user_notification_text += f"ðŸ”— Ø¬Ø²Ø¦ÛŒØ§Øª: {proposal['text_content']}"
        if proposal['type'] == "campaign" and action == "reject":
            user_notification_text = (
                f"âŒ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø´Ù…Ø§ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† *{query.from_user.first_name}* Ø±Ø¯ Ø´Ø¯."
            )

        # ===== Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ ØªØ£ÛŒÛŒØ¯ Ø´Ø¯: Ø§Ø±Ø³Ø§Ù„ Ø®Ø¨Ø± Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ WAR_CHANNEL =====
        if action == "approve" and proposal['type'] == "campaign":
            try:
                payload = {}
                marker = "[CAMPAIGN_DATA]"
                if marker in proposal['text_content']:
                    json_part = proposal['text_content'].split(marker, 1)[1].strip()
                    try:
                        payload = json.loads(json_part)
                    except Exception as e:
                        logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø§Ø±Ø³ CAMPAIGN_DATA: {e}")
                attacker_name = payload.get('attacker_name') or (get_country(proposal['user_id']) or {}).get('name', 'Ù†Ø§Ù…Ø¹Ù„ÙˆÙ…')
                target_name = payload.get('target_name') or proposal.get('target_country_name') or 'Ù†Ø§Ù…Ø¹Ù„ÙˆÙ…'
                types_list = payload.get('types', [])

                types_str = " + ".join(CAMPAIGN_TYPE_LABELS.get(t, t) for t in types_list) if types_list else "Ù†Ø§Ù…Ø´Ø®Øµ"

                channel_text = (
                    "âš”ï¸ *Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¬Ø¯ÛŒØ¯ Ø¢ØºØ§Ø² Ø´Ø¯!*\n"
                    "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
                    f"ðŸ—ºï¸ *Ú©Ø´ÙˆØ± Ù…Ù‡Ø§Ø¬Ù…:* {attacker_name}\n"
                    f"ðŸŽ¯ *Ú©Ø´ÙˆØ± Ù‡Ø¯Ù:* {target_name}\n"
                    f"ðŸŽ–ï¸ *Ù†ÙˆØ¹ Ù†ÛŒØ±ÙˆÙ‡Ø§:* {types_str}\n"
                    "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
                    "\nðŸ•Šï¸ Ø¨Ù‡ Ø§Ù…ÛŒØ¯ Ù¾ÛŒØ±ÙˆØ²ÛŒ..."
                )

                campaign_photo_id = get_notification_image('campaign') or get_notification_image('attack')
                if campaign_photo_id:
                    await context.bot.send_photo(
                        chat_id=WAR_CHANNEL,
                        photo=campaign_photo_id,
                        caption=channel_text,
                        parse_mode="Markdown"
                    )
                else:
                    await context.bot.send_message(
                        chat_id=WAR_CHANNEL,
                        text=channel_text,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„: {e}", exc_info=True)

            # Ø¨Ø§Ø²Ù†ÙˆÛŒØ³ÛŒ Ù¾ÛŒØ§Ù… Ú©Ø§Ø±Ø¨Ø± Ø¨Ø±Ø§ÛŒ Ø­Ø§Ù„Øª Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ
            user_notification_text = (
                f"âœ… Ù„Ø´Ú©Ø±â€ŒÚ©Ø´ÛŒ Ø´Ù…Ø§ ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† *{query.from_user.first_name}* ØªØ£ÛŒÛŒØ¯ Ø´Ø¯.\n"
                f"ðŸ“¢ Ø®Ø¨Ø± Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø¬Ù†Ú¯ Ù…Ù†ØªØ´Ø± Ø´Ø¯."
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
                f"âš”ï¸ Ø­Ù…Ù„Ù‡ Ø¬Ø¯ÛŒØ¯ ØªØ§ÛŒÛŒØ¯ Ø´Ø¯!\n\n"
                f"ðŸ—ºï¸ Ø§Ø²: {attacker['name']}\n"
                f"ðŸŽ¯ Ø¨Ù‡: {target['name']}\n"
                f"â±ï¸ Ø²Ù…Ø§Ù† Ø±Ø³ÛŒØ¯Ù† Ù†ÛŒØ±ÙˆÙ‡Ø§: {delivery_minutes} Ø¯Ù‚ÛŒÙ‚Ù‡ Ø¯ÛŒÚ¯Ø±"
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
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª", show_alert=True)
        return ADMIN_MENU


async def shop_menu_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"shop_category_{category_key}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("ðŸ›’ Ø¨Ù‡ Ø¨Ø®Ø´ Ø®Ø±ÛŒØ¯ Ø®ÙˆØ´ Ø¢Ù…Ø¯ÛŒØ¯! Ù„Ø·ÙØ§ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø®ÙˆØ¯ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SHOP_MENU
    except Exception as e:
        logger.error(f"Error in shop_menu_start: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø®Ø±ÛŒØ¯")
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
            await query.edit_message_text("âŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
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
                button_text = f"{item_display_name} (Ù‚ÛŒÙ…Øª: {formatted_price})"

                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"shop_item_{item_key}")])
                items_added = True
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¢ÛŒØªÙ… {item_key}: {e}")
        if not items_added:
            await query.answer("âš ï¸ Ù‡ÛŒÚ† Ø¢ÛŒØªÙ…ÛŒ Ø¯Ø± Ø§ÛŒÙ† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ¬ÙˆØ¯ Ù†ÛŒØ³Øª!", show_alert=True)
            return await shop_menu_start(update, context)
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='shop_menu_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        category_display_name = next(
            (disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key),
            category_key
        )

        await query.edit_message_text(
            f"ðŸ›ï¸ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ Ù…ÙˆØ¬ÙˆØ¯ Ø¯Ø± Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ '{category_display_name}':",
            reply_markup=reply_markup
        )
        return SHOP_CATEGORY

    except Exception as e:
        logger.error(f"Error in select_shop_category: {e}", exc_info=True)
        await query.edit_message_text("âš ï¸ Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ. Ù„Ø·ÙØ§Ù‹ Ø¨Ø¹Ø¯Ø§Ù‹ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
        return SHOP_MENU


async def select_shop_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        item_key = query.data.replace("shop_item_", "")
        current_shop_category = context.user_data.get('current_shop_category')
        if not current_shop_category:
            await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return await shop_menu_start(update, context)
        dynamic_prices = get_dynamic_asset_prices()
        price = dynamic_prices.get(item_key)
        if price is None:
            await query.edit_message_text("âŒ Ù‚ÛŒÙ…Øª Ø§ÛŒÙ† Ø¢ÛŒØªÙ… Ù†Ø§Ù…Ø´Ø®Øµ Ø§Ø³Øª.")
            return await select_shop_category(update, context)
        context.user_data['selected_shop_item_key'] = item_key
        context.user_data['selected_shop_item_price'] = price
        item_display_name = get_asset_display_name(item_key)
        await query.edit_message_text(f"Ø´Ù…Ø§ '{item_display_name}' Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø±Ø¯ÛŒØ¯.\n"
                                      f"Ù‚ÛŒÙ…Øª Ù‡Ø± ÙˆØ§Ø­Ø¯: {price:,} Ø³Ø±Ù…Ø§ÛŒÙ‡.\n"
                                      "Ù„Ø·ÙØ§Ù‹ ØªØ¹Ø¯Ø§Ø¯ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø®Ø±ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return GET_SHOP_ITEM_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_shop_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ…")
        return SHOP_CATEGORY


async def get_shop_item_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯. Ù„Ø·ÙØ§Ù‹ Ø¨Ø§ Ù…Ø§Ù„Ú© Ø±Ø¨Ø§Øª ØªÙ…Ø§Ø³ Ø¨Ú¯ÛŒØ±ÛŒØ¯.")
        return MAIN_MENU
    item_key = context.user_data.get('selected_shop_item_key')
    price = context.user_data.get('selected_shop_item_price')
    category_key = context.user_data.get('current_shop_category')
    if not item_key or price is None or not category_key:
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø®Ø±ÛŒØ¯. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†ÙˆÛŒ Ø®Ø±ÛŒØ¯ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
        return await shop_menu_start(update, context)
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ØªØ¹Ø¯Ø§Ø¯ ØµØ­ÛŒØ­ Ùˆ Ù…Ø«Ø¨Øª ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
            return GET_SHOP_ITEM_QUANTITY
    except ValueError:
        await update.message.reply_text("ØªØ¹Ø¯Ø§Ø¯ ÙˆØ§Ø±Ø¯ Ø´Ø¯Ù‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return GET_SHOP_ITEM_QUANTITY
    total_cost = quantity * price
    if country['capital'] < total_cost:
        await update.message.reply_text(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ ({country['capital']:,}) Ø¨Ø±Ø§ÛŒ Ø®Ø±ÛŒØ¯ {quantity:,} ÙˆØ§Ø­Ø¯ Ø§Ø² {get_asset_display_name(item_key)} Ø¨Ù‡ Ù‚ÛŒÙ…Øª {total_cost:,} Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª.")
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
        await update.message.reply_text(f"âœ… Ø®Ø±ÛŒØ¯ Ø´Ù…Ø§ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯!\n"
                                        f"{quantity:,} ÙˆØ§Ø­Ø¯ Ø§Ø² '{item_display_name}' Ø¨Ù‡ Ø¯Ø§Ø±Ø§ÛŒÛŒ Ø´Ù…Ø§ Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯.\n"
                                        f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡: {new_capital:,}")
        context.user_data.pop('selected_shop_item_key', None)
        context.user_data.pop('selected_shop_item_price', None)
        context.user_data.pop('current_shop_category', None)
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_shop_item_quantity: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†Ø¬Ø§Ù… Ø®Ø±ÛŒØ¯")
        return MAIN_MENU


async def statement_proposal_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯.")
            return MAIN_MENU
        context.user_data['statement_text_parts'] = []
        context.user_data['statement_photo_ids'] = []
        await query.edit_message_text("ðŸ“£ Ù„Ø·ÙØ§Ù‹ Ø¨ÛŒØ§Ù†ÛŒÙ‡ Ø®ÙˆØ¯ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.\n"
                                      "Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ù…ØªÙ† Ùˆ/ÛŒØ§ Ø¹Ú©Ø³ Ø±Ø§ Ø¯Ø± ÛŒÚ© Ù¾ÛŒØ§Ù… ÛŒØ§ Ú†Ù†Ø¯ Ù¾ÛŒØ§Ù… Ù…ØªÙˆØ§Ù„ÛŒ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯. "
                                      "Ø¨ÛŒØ§Ù†ÛŒÙ‡ Ø´Ù…Ø§ Ø¨Ù„Ø§ÙØ§ØµÙ„Ù‡ Ù¾Ø³ Ø§Ø² Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ Ø¹Ù…ÙˆÙ…ÛŒ ÙØ±Ø³ØªØ§Ø¯Ù‡ Ø®ÙˆØ§Ù‡Ø¯ Ø´Ø¯.")
        return GET_STATEMENT_CONTENT
    except Exception as e:
        logger.error(f"Error in statement_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø´Ø±ÙˆØ¹ Ø§Ø±Ø³Ø§Ù„ Ø¨ÛŒØ§Ù†ÛŒÙ‡")
        return MAIN_MENU


async def get_statement_content(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.effective_message.reply_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return MAIN_MENU
    try:
        if update.effective_message.photo:
            statement_text = update.effective_message.caption or ""
            statement_photo_id = update.effective_message.photo[-1].file_id
        else:
            statement_text = update.effective_message.text or ""
            statement_photo_id = None
        channel_message = f"ðŸ“£ *Ø¨ÛŒØ§Ù†ÛŒÙ‡ Ø§Ø² Ú©Ø´ÙˆØ± {country['name']}*\n\n{statement_text}"
        if statement_photo_id:
            await context.bot.send_photo(chat_id=STATEMENT_CHANNEL, photo=statement_photo_id,
                                         caption=channel_message, parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id=STATEMENT_CHANNEL, text=channel_message,
                                           parse_mode="Markdown")
        await update.effective_message.reply_text("âœ… Ø¨ÛŒØ§Ù†ÛŒÙ‡ Ø´Ù…Ø§ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ Ø¹Ù…ÙˆÙ…ÛŒ Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯!")

        if 'statement_text_parts' in context.user_data:
            del context.user_data['statement_text_parts']
        if 'statement_photo_ids' in context.user_data:
            del context.user_data['statement_photo_ids']

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_statement_content: {e}", exc_info=True)
        await update.effective_message.reply_text("âŒ Ù…ØªØ§Ø³ÙØ§Ù†Ù‡ Ø®Ø·Ø§ÛŒÛŒ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¨ÛŒØ§Ù†ÛŒÙ‡ Ø±Ø® Ø¯Ø§Ø¯.")
        return GET_STATEMENT_CONTENT


async def list_countries(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        if not countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ø´Ø¯Ù‡ Ø§Ø³Øª.")
            return ADMIN_MENU
        message = "Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§:\n\n"
        for user_id, name in countries:
            message += f"Ù†Ø§Ù…: {name}, ID: {user_id}\n"
        keyboard = [[InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in list_countries: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return ADMIN_MENU


async def add_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Ù„Ø·ÙØ§ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ Ú©Ø§Ø±Ø¨Ø± Ùˆ Ù†Ø§Ù… Ú©Ø´ÙˆØ± Ø±Ø§ Ø¨Ù‡ Ø§ÛŒÙ† ÙØ±Ù…Øª ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:\n`ID, Ù†Ø§Ù… Ú©Ø´ÙˆØ±`\n\nÙ…Ø«Ø§Ù„: `12345, Ø§ÛŒØ±Ø§Ù†`")
    return ADD_COUNTRY


async def create_new_country(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        text = update.message.text
        try:
            target_user_id_str, country_name = text.split(',', 1)
            target_user_id = int(target_user_id_str.strip())
            country_name = country_name.strip()
        except ValueError:
            await update.message.reply_text("ÙØ±Ù…Øª ÙˆØ§Ø±Ø¯ Ø´Ø¯Ù‡ ØµØ­ÛŒØ­ Ù†ÛŒØ³Øª. Ù„Ø·ÙØ§Ù‹ Ù…Ø¬Ø¯Ø¯Ø§Ù‹ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
            return ADD_COUNTRY
        if get_country(target_user_id):
            await update.message.reply_text(f"Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø§ Ø§ÛŒÙ† Ø¢ÛŒØ¯ÛŒ ({target_user_id}) Ø§Ø² Ù‚Ø¨Ù„ Ù…ÙˆØ¬ÙˆØ¯ Ø§Ø³Øª.")
            return ADD_COUNTRY
        create_country(target_user_id, country_name)
        await update.message.reply_text(f"âœ… Ú©Ø´ÙˆØ± '{country_name}' Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ø±Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø± Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {target_user_id} Ø«Ø¨Øª Ø´Ø¯.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in create_new_country: {e}", exc_info=True)
        await update.message.reply_text(f"Ø®Ø·Ø§ Ø¯Ø± Ø§ÛŒØ¬Ø§Ø¯ Ú©Ø´ÙˆØ± Ø¬Ø¯ÛŒØ¯: {str(e)}")
        return ADD_COUNTRY


async def delete_country_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        countries = get_all_countries()
        keyboard = []
        if not countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"delete_country_{user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return DELETE_COUNTRY_MENU
    except Exception as e:
        logger.error(f"Error in delete_country_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return ADMIN_MENU


async def confirm_delete_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_delete = int(query.data.replace("delete_country_", ""))

        country_data = get_country(user_id_to_delete)
        if not country_data:
            await query.edit_message_text("Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return ADMIN_MENU
        keyboard = [
            [InlineKeyboardButton("âœ… Ø¨Ù„Ù‡ØŒ Ø­Ø°Ù Ø´ÙˆØ¯", callback_data=f"execute_delete_country_{user_id_to_delete}")],
            [InlineKeyboardButton("âŒ Ø®ÛŒØ±ØŒ Ø§Ù†ØµØ±Ø§Ù", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"âš ï¸ Ø¢ÛŒØ§ Ù…Ø·Ù…Ø¦Ù†ÛŒØ¯ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ú©Ø´ÙˆØ± '{country_data['name']}' Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {user_id_to_delete} Ø±Ø§ Ø­Ø°Ù Ú©Ù†ÛŒØ¯ØŸ Ø§ÛŒÙ† Ø¹Ù…Ù„ ØºÛŒØ±Ù‚Ø§Ø¨Ù„ Ø¨Ø±Ú¯Ø´Øª Ø§Ø³Øª.", reply_markup=reply_markup)
        return DELETE_COUNTRY_MENU
    except Exception as e:
        logger.error(f"Error in confirm_delete_country: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø´ÙˆØ±")
        return ADMIN_MENU


async def execute_delete_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_delete = int(query.data.replace("execute_delete_country_", ""))

        country_data = get_country(user_id_to_delete)
        if not country_data:
            await query.edit_message_text("Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return ADMIN_MENU
        delete_country(user_id_to_delete)
        await query.edit_message_text(f"âœ… Ú©Ø´ÙˆØ± '{country_data['name']}' Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø­Ø°Ù Ø´Ø¯.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in execute_delete_country: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø­Ø°Ù Ú©Ø´ÙˆØ±")
        return ADMIN_MENU


async def set_religion_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ±ÛŒ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯.")
            return MAIN_MENU
        keyboard = []
        for code, display_name in RELIGIONS:
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"set_religion_{code}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"ðŸŒ Ø¯ÛŒÙ† ÙØ¹Ù„ÛŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§: {next((disp for code, disp in RELIGIONS if code == country['religion']), 'Ù†Ø§Ù…Ø¹Ù„ÙˆÙ…')}\n"
                                      "Ù„Ø·ÙØ§Ù‹ Ø¯ÛŒÙ† Ø¬Ø¯ÛŒØ¯ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return RELIGION_MENU
    except Exception as e:
        logger.error(f"Error in set_religion_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø¯ÛŒÙ†")
        return MAIN_MENU


async def set_country_religion(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        new_religion = query.data.replace("set_religion_", "")
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU

        religion_display_name = next((disp for code, disp in RELIGIONS if code == new_religion), new_religion)
        update_country(user_id, {'religion': new_religion})

        try:
            photo_id = get_notification_image("religion")
            message = f"ðŸŒ Ú©Ø´ÙˆØ± {country['name']} Ø¯ÛŒÙ† Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù‡ {religion_display_name} ØªØºÛŒÛŒØ± Ø¯Ø§Ø¯"

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
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø§Ø·Ù„Ø§Ø¹ Ø¯ÛŒÙ† Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„: {e}")

        await query.edit_message_text(f"âœ… Ø¯ÛŒÙ† Ú©Ø´ÙˆØ± Ø´Ù…Ø§ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ '{religion_display_name}' ØªØºÛŒÛŒØ± ÛŒØ§ÙØª.")
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in set_country_religion: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± Ø¯ÛŒÙ†")
        return RELIGION_MENU


async def add_admin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ Ú©Ø§Ø±Ø¨Ø±ÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø§Ø¯Ù…ÛŒÙ† Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
    return ADD_ADMIN


async def process_add_admin(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        user_id_to_add = update.message.text
        try:
            user_id_to_add = int(user_id_to_add)
        except ValueError:
            await update.message.reply_text("Ø¢ÛŒØ¯ÛŒ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
            return ADD_ADMIN
        if add_admin_to_db(user_id_to_add):
            await update.message.reply_text(f"âœ… Ú©Ø§Ø±Ø¨Ø± Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {user_id_to_add} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ Ø¹Ù†ÙˆØ§Ù† Ø§Ø¯Ù…ÛŒÙ† Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯.")
        else:
            await update.message.reply_text(f"Ú©Ø§Ø±Ø¨Ø± Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {user_id_to_add} Ø§Ø² Ù‚Ø¨Ù„ Ø§Ø¯Ù…ÛŒÙ† Ø§Ø³Øª.")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_add_admin: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§ÙØ²ÙˆØ¯Ù† Ø§Ø¯Ù…ÛŒÙ†")
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
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if not keyboard or len(keyboard) == 1:
            await query.edit_message_text("Ù‡ÛŒÚ† Ø§Ø¯Ù…ÛŒÙ† Ø¯ÛŒÚ¯Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ø§Ø¯Ù…ÛŒÙ†ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø­Ø°Ù Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return REMOVE_ADMIN
    except Exception as e:
        logger.error(f"Error in remove_admin: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§")
        return ADMIN_MENU


async def process_remove_admin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id_to_remove = int(query.data.replace("remove_admin_", ""))
        if remove_admin_from_db(user_id_to_remove):
            await query.edit_message_text(f"âœ… Ø§Ø¯Ù…ÛŒÙ† Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {user_id_to_remove} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø­Ø°Ù Ø´Ø¯.")
        else:
            await query.edit_message_text(f"âŒ Ú©Ø§Ø±Ø¨Ø± Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {user_id_to_remove} Ø§Ø¯Ù…ÛŒÙ† Ù†ÛŒØ³Øª ÛŒØ§ Ù†Ù…ÛŒâ€ŒØªÙˆØ§Ù† Ø¢Ù† Ø±Ø§ Ø­Ø°Ù Ú©Ø±Ø¯ (Ø´Ø§ÛŒØ¯ Ù…Ø§Ù„Ú© Ø¨Ø§Ø´Ø¯).")
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_remove_admin: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø­Ø°Ù Ø§Ø¯Ù…ÛŒÙ†")
        return ADMIN_MENU


async def toggle_bot_active_status(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_bot_active_status()
        set_bot_active_status(not current_status)
        new_status_text = "ÙØ¹Ø§Ù„" if not current_status else "ØºÛŒØ±ÙØ¹Ø§Ù„"
        await query.edit_message_text(f"âœ… ÙˆØ¶Ø¹ÛŒØª Ø±Ø¨Ø§Øª Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ '{new_status_text}' ØªØºÛŒÛŒØ± ÛŒØ§ÙØª.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in toggle_bot_active_status: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª Ø±Ø¨Ø§Øª")
        return ADMIN_MENU


async def manage_global_buttons(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        disabled_buttons = get_global_disabled_buttons()
        keyboard = []
        for btn in BOT_MAIN_MENU_BUTTONS:
            status = "âŒ ØºÛŒØ±ÙØ¹Ø§Ù„" if btn['callback_data'] in disabled_buttons else "âœ… ÙØ¹Ø§Ù„"
            keyboard.append([InlineKeyboardButton(f"{btn['text']} {status}", callback_data=f"toggle_global_button_{btn['callback_data']}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ÛŒ Ø¹Ù…ÙˆÙ…ÛŒ:\n"
                                      "Ø¨Ø±Ø§ÛŒ ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ Ø±ÙˆÛŒ Ø¢Ù†Ù‡Ø§ Ú©Ù„ÛŒÚ© Ú©Ù†ÛŒØ¯.", reply_markup=reply_markup)
        return MANAGE_GLOBAL_BUTTONS
    except Exception as e:
        logger.error(f"Error in manage_global_buttons: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§")
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
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª Ø¯Ú©Ù…Ù‡", show_alert=True)
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
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU
        for user_id, name in countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"select_user_{user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø§Ø±Ø¨Ø± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return SELECT_USER_TO_MESSAGE
    except Exception as e:
        logger.error(f"Error in send_message_to_user: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø§Ø±Ø¨Ø±Ø§Ù†")
        return ADMIN_MENU


async def select_user_for_message(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = int(query.data.replace("select_user_", ""))
        context.user_data['message_target_id'] = user_id

        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ú©Ø§Ø±Ø¨Ø± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return ADMIN_MENU

        await query.edit_message_text(f"Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø¨Ù‡ Ú©Ø§Ø±Ø¨Ø±: {country['name']}\nÙ„Ø·ÙØ§Ù‹ Ù¾ÛŒØ§Ù… Ø®ÙˆØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return GET_MESSAGE_TEXT
    except Exception as e:
        logger.error(f"Error in select_user_for_message: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø§Ø±Ø¨Ø±")
        return SELECT_USER_TO_MESSAGE


async def send_user_message(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        target_id = context.user_data.get('message_target_id')
        message_text = update.message.text

        if not target_id:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø§Ø±Ø¨Ø±. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return await admin_panel(update, context)

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=f"ðŸ“® Ù¾ÛŒØ§Ù…ÛŒ Ø§Ø² Ù…Ø¯ÛŒØ±ÛŒØª:\n\n{message_text}"
            )
            await update.message.reply_text(f"âœ… Ù¾ÛŒØ§Ù… Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ Ú©Ø§Ø±Ø¨Ø± Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯.")
        except Exception as e:
            await update.message.reply_text(f"âŒ Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù…: {str(e)}")

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in send_user_message: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù…")
        return ADMIN_MENU


async def country_management(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if not get_setting('country_management_active') == '1':
        await query.answer("â›” Ø¨Ø®Ø´ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ø´ÙˆØ± Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
        return MAIN_MENU

    try:
        keyboard = [
            [InlineKeyboardButton("ðŸŒ Ú©Ù†ØªØ±Ù„ Ø§ÛŒÙ†ØªØ±Ù†Øª", callback_data='internet_control')],
            [InlineKeyboardButton("ðŸ›¢ï¸ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ù†ÙØª", callback_data='refinery_menu')],
            [InlineKeyboardButton("ðŸ’‚â€â™‚ï¸ Ø±Ø²Ù…Ø§ÛŒØ´ Ù†Ø¸Ø§Ù…ÛŒ", callback_data='military_exercise')],
            [InlineKeyboardButton("ðŸ“© Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù…", callback_data='send_message_to_country')],
            [InlineKeyboardButton("ðŸ¤ ØªØ¬Ø§Ø±Øª", callback_data='trade_menu')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "ðŸ›ï¸ Ù…Ù†ÙˆÛŒ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ø´ÙˆØ±:",
            reply_markup=reply_markup
        )
        return COUNTRY_MANAGEMENT
    except Exception as e:
        logger.error(f"Error in country_management: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ø´ÙˆØ±")
        return MAIN_MENU


async def internet_control(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        country = get_country(query.from_user.id)
        status = "âœ… Ù…Ù„ÛŒ" if country['internet_nationalized'] else "âŒ ØºÛŒØ±Ù…Ù„ÛŒ"
        current_income = INTERNET_INCOME_RATES.get(country.get('internet_level', 2), 0)

        keyboard = [
            [InlineKeyboardButton(f"ÙˆØ¶Ø¹ÛŒØª: {status}", callback_data='nationalize_internet')],
            [InlineKeyboardButton(f"Ø§Ø±ØªÙ‚Ø§Ø¡ ({country['internet_level']}G)", callback_data='upgrade_internet')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"ðŸŒ Ú©Ù†ØªØ±Ù„ Ø§ÛŒÙ†ØªØ±Ù†Øª:\nÙˆØ¶Ø¹ÛŒØª: {status}\nØ³Ø·Ø­ ÙØ¹Ù„ÛŒ: {country['internet_level']}G\nØ¯Ø±Ø¢Ù…Ø¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {current_income:,}",
            reply_markup=reply_markup
        )
        return INTERNET_CONTROL
    except Exception as e:
        logger.error(f"Error in internet_control: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ú©Ù†ØªØ±Ù„ Ø§ÛŒÙ†ØªØ±Ù†Øª")
        return COUNTRY_MANAGEMENT


async def nationalize_internet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        new_status = not country['internet_nationalized']

        update_country(user_id, {'internet_nationalized': new_status})
        status = "âœ… Ù…Ù„ÛŒ" if new_status else "âŒ ØºÛŒØ±Ù…Ù„ÛŒ"

        try:
            event_type = "internet_on" if new_status else "internet_off"
            photo_id = get_notification_image(event_type)
            message = f"ðŸŒ Ú©Ø´ÙˆØ± {country['name']} Ø§ÛŒÙ†ØªØ±Ù†Øª Ø®ÙˆØ¯ Ø±Ø§ {'Ù…Ù„ÛŒ Ú©Ø±Ø¯' if new_status else 'Ø§Ø² Ø­Ø§Ù„Øª Ù…Ù„ÛŒ Ø®Ø§Ø±Ø¬ Ú©Ø±Ø¯'}"

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
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ ÙˆØ¶Ø¹ÛŒØª Ø§ÛŒÙ†ØªØ±Ù†Øª Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„: {e}")

        await query.answer(f"Ø§ÛŒÙ†ØªØ±Ù†Øª {status} Ø´Ø¯")
        return await internet_control(update, context)
    except Exception as e:
        logger.error(f"Error in nationalize_internet: {e}", exc_info=True)
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª Ø§ÛŒÙ†ØªØ±Ù†Øª", show_alert=True)
        return INTERNET_CONTROL


async def upgrade_internet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country['internet_level']

        if current_level >= 7:
            await query.answer("Ø§ÛŒÙ†ØªØ±Ù†Øª Ø´Ù…Ø§ Ø¯Ø± Ø¨Ø§Ù„Ø§ØªØ±ÛŒÙ† Ø³Ø·Ø­ (7G) Ø§Ø³Øª!", show_alert=True)
            return INTERNET_CONTROL
        keyboard = []
        for level in range(current_level + 1, 8):
            price = ASSET_PRICES[f'internet_upgrade_{level}g']
            income = INTERNET_INCOME_RATES.get(level, 0)
            keyboard.append([InlineKeyboardButton(
                f"Ø§Ø±ØªÙ‚Ø§Ø¡ Ø¨Ù‡ {level}G - Ù‡Ø²ÛŒÙ†Ù‡: {price:,} - Ø¯Ø±Ø¢Ù…Ø¯: +{income:,}/Ø±ÙˆØ²",
                callback_data=f"upgrade_to_{level}"
            )])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='internet_control')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "ðŸ”¼ Ù„Ø·ÙØ§Ù‹ Ø³Ø·Ø­ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return INTERNET_CONTROL
    except Exception as e:
        logger.error(f"Error in upgrade_internet: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø³Ø·ÙˆØ­ Ø§ÛŒÙ†ØªØ±Ù†Øª")
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
            await query.answer(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù‚ÛŒÙ…Øª Ø§Ø±ØªÙ‚Ø§Ø¡: {price:,}", show_alert=True)
            return await internet_control(update, context)

        new_capital = country['capital'] - price
        update_country(user_id, {
            'capital': new_capital,
            'internet_level': target_level
        })
        income = INTERNET_INCOME_RATES.get(target_level, 0)
        await query.answer(f"âœ… Ø§ÛŒÙ†ØªØ±Ù†Øª Ø´Ù…Ø§ Ø¨Ù‡ {target_level}G Ø§Ø±ØªÙ‚Ø§Ø¡ ÛŒØ§ÙØª! Ø¯Ø±Ø¢Ù…Ø¯ Ø±ÙˆØ²Ø§Ù†Ù‡: +{income:,}", show_alert=True)
        return await internet_control(update, context)
    except Exception as e:
        logger.error(f"Error in process_internet_upgrade: {e}", exc_info=True)
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±ØªÙ‚Ø§Ø¡ Ø§ÛŒÙ†ØªØ±Ù†Øª", show_alert=True)
        return INTERNET_CONTROL


async def trade_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if get_trade_setting('trade_enabled') != '1':
        await query.answer("â›” Ø³ÛŒØ³ØªÙ… ØªØ¬Ø§Ø±Øª Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
        return COUNTRY_MANAGEMENT

    try:
        keyboard = [
            [InlineKeyboardButton("ØªØ¬Ø§Ø±Øª Ø¹Ø§Ø¯ÛŒ", callback_data='normal_trade')]
        ]

        if get_trade_setting('discreet_trade_enabled') == '1':
            keyboard.append([InlineKeyboardButton("ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³", callback_data='discreet_trade')])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='country_management')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "ðŸ¤ Ù…Ù†ÙˆÛŒ ØªØ¬Ø§Ø±Øª:\n"
            "- ØªØ¬Ø§Ø±Øª Ø¹Ø§Ø¯ÛŒ: Ø¹Ù…ÙˆÙ…ÛŒ Ùˆ Ø¨Ø§ Ø§Ø·Ù„Ø§Ø¹ Ú©Ø§Ù…Ù„ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„\n"
            "- ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³: Ø®ØµÙˆØµÛŒ Ùˆ Ø¨Ø¯ÙˆÙ† Ø§ÙØ´Ø§ÛŒ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„",
            reply_markup=reply_markup
        )
        return TRADE_MENU
    except Exception as e:
        logger.error(f"Error in trade_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ ØªØ¬Ø§Ø±Øª")
        return COUNTRY_MANAGEMENT


async def normal_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['trade_type'] = 'normal'

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]

        if not other_countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ ØªØ¬Ø§Ø±Øª ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return TRADE_MENU
        keyboard = []
        for uid, name in other_countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"trade_target_{uid}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return TRADE_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in normal_trade: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ú©Ø´ÙˆØ±Ù‡Ø§")
        return TRADE_MENU


async def discreet_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['trade_type'] = 'discreet'

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]

        if not other_countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ ØªØ¬Ø§Ø±Øª ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return TRADE_MENU
        keyboard = []
        for uid, name in other_countries:
            keyboard.append([InlineKeyboardButton(name, callback_data=f"trade_target_{uid}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ù„Ø·ÙØ§Ù‹ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯ (ØªØ¬Ø§Ø±Øª Ù…Ø­Ø±Ù…Ø§Ù†Ù‡):",
            reply_markup=reply_markup
        )
        return TRADE_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in discreet_trade: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ú©Ø´ÙˆØ±Ù‡Ø§")
        return TRADE_MENU


async def select_trade_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_id = int(query.data.replace("trade_target_", ""))
        context.user_data['trade_target_id'] = target_id

        target_country = get_country(target_id)
        if not target_country:
            await query.edit_message_text("Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯!")
            return TRADE_MENU

        context.user_data['trade_target_name'] = target_country['name']

        keyboard = []
        for domain_key, domain_name in TRADE_DOMAINS:
            keyboard.append([InlineKeyboardButton(domain_name, callback_data=f"trade_domain_{domain_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='trade_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"ØªØ¬Ø§Ø±Øª Ø¨Ø§ {target_country['name']}\nÙ„Ø·ÙØ§Ù‹ Ø¯Ø§Ù…Ù†Ù‡ ØªØ¬Ø§Ø±Øª Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return TRADE_DOMAIN_SELECTION
    except Exception as e:
        logger.error(f"Error in select_trade_target: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù")
        return TRADE_MENU


async def select_trade_domain(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        domain_key = query.data.replace("trade_domain_", "")
        context.user_data['trade_domain'] = domain_key

        domain_display_name = next((name for key, name in TRADE_DOMAINS if key == domain_key), domain_key)

        await query.edit_message_text(
            f"Ø¯Ø§Ù…Ù†Ù‡ ØªØ¬Ø§Ø±Øª: {domain_display_name}\n"
            "Ù„Ø·ÙØ§Ù‹ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯ (ØªØ§ 3 Ø¢ÛŒØªÙ…):"
        )

        context.user_data['trade_items'] = {'send': [], 'receive': []}

        keyboard = [
            [InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø§Ø±Ø³Ø§Ù„ÛŒ", callback_data='add_send_item')],
            [InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø¯Ø±ÛŒØ§ÙØªÛŒ", callback_data='add_receive_item')],
            [InlineKeyboardButton("âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª", callback_data='confirm_trade')],
            [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='trade_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ù„Ø·ÙØ§Ù‹ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ Ø§Ø±Ø³Ø§Ù„ÛŒ Ùˆ Ø¯Ø±ÛŒØ§ÙØªÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return TRADE_ADD_ITEMS
    except Exception as e:
        logger.error(f"Error in select_trade_domain: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø§Ù…Ù†Ù‡ ØªØ¬Ø§Ø±Øª")
        return TRADE_SELECT_TARGET


async def add_send_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"trade_send_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡", callback_data="trade_send_capital")])
        keyboard.append([InlineKeyboardButton("ðŸ›¢ï¸ Ù†ÙØª", callback_data="trade_send_oil_barrels")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data=f"trade_domain_{context.user_data['trade_domain']}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ø§Ù†ØªØ®Ø§Ø¨ Ù…Ù†Ø¨Ø¹ Ø§Ø±Ø³Ø§Ù„ÛŒ:",
            reply_markup=reply_markup
        )
        return TRADE_SEND_ITEM_CATEGORY
    except Exception as e:
        logger.error(f"Error in add_send_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø§Ø±Ø³Ø§Ù„ÛŒ")
        return TRADE_ADD_ITEMS


async def add_receive_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"trade_receive_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡", callback_data="trade_receive_capital")])
        keyboard.append([InlineKeyboardButton("ðŸ›¢ï¸ Ù†ÙØª", callback_data="trade_receive_oil_barrels")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='add_receive_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ø§Ù†ØªØ®Ø§Ø¨ Ù…Ù†Ø¨Ø¹ Ø¯Ø±ÛŒØ§ÙØªÛŒ:",
            reply_markup=reply_markup
        )
        return TRADE_RECEIVE_ITEM_CATEGORY
    except Exception as e:
        logger.error(f"Error in add_receive_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø¯Ø±ÛŒØ§ÙØªÛŒ")
        return TRADE_ADD_ITEMS


async def select_send_item_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'trade_send_capital':
            context.user_data['current_trade_item'] = {'type': 'send', 'resource': 'capital'}
            await query.edit_message_text("ðŸ’° Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ø³Ø±Ù…Ø§ÛŒÙ‡â€ŒØ§ÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
            return TRADE_GET_SEND_AMOUNT

        if query.data == 'trade_send_oil_barrels':
            context.user_data['current_trade_item'] = {'type': 'send', 'resource': 'oil_barrels'}
            await query.edit_message_text("ðŸ›¢ï¸ Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ù†ÙØªÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
            return TRADE_GET_SEND_AMOUNT

        category_key = query.data.replace("trade_send_category_", "")
        context.user_data['current_trade_item'] = {'type': 'send', 'category': category_key}

        user_id = query.from_user.id
        country = get_country(user_id)
        if not country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU

        assets = country.get(category_key, {})
        keyboard = []
        for item_key, count in assets.items():
            if count > 0:
                display_name = get_asset_display_name(item_key)
                keyboard.append([InlineKeyboardButton(f"{display_name} (Ù…ÙˆØ¬ÙˆØ¯: {count})", callback_data=f"trade_send_item_{item_key}")])

        if not keyboard:
            await query.answer("Ù‡ÛŒÚ† Ø¢ÛŒØªÙ…ÛŒ Ø¯Ø± Ø§ÛŒÙ† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ù…ÙˆØ¬ÙˆØ¯ Ù†ÛŒØ³Øª!", show_alert=True)
            return TRADE_ADD_ITEMS

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='add_send_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø§Ø±Ø³Ø§Ù„ÛŒ Ø§Ø² Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ {category_display_name}:",
            reply_markup=reply_markup
        )
        return TRADE_SEND_ITEM_SELECT
    except Exception as e:
        logger.error(f"Error in select_send_item_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ")
        return TRADE_SEND_ITEM_CATEGORY


async def select_send_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("trade_send_item_", "")
        trade_item = context.user_data.get('current_trade_item', {})
        trade_item['resource'] = item_key
        context.user_data['current_trade_item'] = trade_item

        await query.edit_message_text(f"Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± {get_asset_display_name(item_key)} Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return TRADE_GET_SEND_AMOUNT
    except Exception as e:
        logger.error(f"Error in select_send_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø§Ø±Ø³Ø§Ù„ÛŒ")
        return TRADE_SEND_ITEM_SELECT


async def get_send_amount(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return MAIN_MENU
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("Ù…Ù‚Ø¯Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯.")
            return TRADE_GET_SEND_AMOUNT
    except ValueError:
        await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return TRADE_GET_SEND_AMOUNT
    trade_item = context.user_data.get('current_trade_item', {})
    if not trade_item:
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¢ÛŒØªÙ…. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
        return TRADE_ADD_ITEMS

    if trade_item.get('resource') == 'capital':
        if country['capital'] < amount:
            await update.message.reply_text(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ø³Ø±Ù…Ø§ÛŒÙ‡ ÙØ¹Ù„ÛŒ: {country['capital']:,}")
            return TRADE_GET_SEND_AMOUNT
    elif trade_item.get('resource') == 'oil_barrels':
        if country['oil_barrels'] < amount:
            await update.message.reply_text(f"Ù†ÙØª Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù†ÙØª ÙØ¹Ù„ÛŒ: {country['oil_barrels']:,}")
            return TRADE_GET_SEND_AMOUNT
    else:
        category = trade_item.get('category')
        resource = trade_item.get('resource')
        current_amount = country.get(category, {}).get(resource, 0)
        if current_amount < amount:
            display_name = get_asset_display_name(resource)
            await update.message.reply_text(f"Ù…ÙˆØ¬ÙˆØ¯ÛŒ {display_name} Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ: {current_amount:,}")
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
            await query.edit_message_text("ðŸ’° Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ø³Ø±Ù…Ø§ÛŒÙ‡â€ŒØ§ÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø¯Ø±ÛŒØ§ÙØª Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
            return TRADE_GET_RECEIVE_AMOUNT

        if query.data == 'trade_receive_oil_barrels':
            context.user_data['current_trade_item'] = {'type': 'receive', 'resource': 'oil_barrels'}
            await query.edit_message_text("ðŸ›¢ï¸ Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ù†ÙØªÛŒ Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø¯Ø±ÛŒØ§ÙØª Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
            return TRADE_GET_RECEIVE_AMOUNT

        category_key = query.data.replace("trade_receive_category_", "")
        context.user_data['current_trade_item'] = {'type': 'receive', 'category': category_key}

        keyboard = []
        for item_key in get_dynamic_default_assets().get(category_key, {}).keys():
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"trade_receive_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='add_receive_item')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø¯Ø±ÛŒØ§ÙØªÛŒ Ø§Ø² Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ {category_display_name}:",
            reply_markup=reply_markup
        )
        return TRADE_RECEIVE_ITEM_SELECT
    except Exception as e:
        logger.error(f"Error in select_receive_item_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ")
        return TRADE_RECEIVE_ITEM_CATEGORY


async def select_receive_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("trade_receive_item_", "")
        trade_item = context.user_data.get('current_trade_item', {})
        trade_item['resource'] = item_key
        context.user_data['current_trade_item'] = trade_item

        await query.edit_message_text(f"Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± {get_asset_display_name(item_key)} Ú©Ù‡ Ù…ÛŒâ€ŒØ®ÙˆØ§Ù‡ÛŒØ¯ Ø¯Ø±ÛŒØ§ÙØª Ú©Ù†ÛŒØ¯ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return TRADE_GET_RECEIVE_AMOUNT
    except Exception as e:
        logger.error(f"Error in select_receive_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø¯Ø±ÛŒØ§ÙØªÛŒ")
        return TRADE_RECEIVE_ITEM_SELECT


async def get_receive_amount(update: Update, context: CallbackContext) -> int:
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("Ù…Ù‚Ø¯Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯.")
            return TRADE_GET_RECEIVE_AMOUNT
    except ValueError:
        await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return TRADE_GET_RECEIVE_AMOUNT
    trade_item = context.user_data.get('current_trade_item', {})
    if not trade_item:
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¢ÛŒØªÙ…. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
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

        message = "ðŸ“¦ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒ Ø§Ù†ØªØ®Ø§Ø¨ Ø´Ø¯Ù‡ Ø¨Ø±Ø§ÛŒ ØªØ¬Ø§Ø±Øª:\n\n"
        message += "ðŸ“¤ *Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ú©Ø´ÙˆØ± Ù…Ù‚Ø§Ø¨Ù„:*\n"
        for item in trade_items['send']:
            if item.get('resource') == 'capital':
                message += f"â€¢ ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"â€¢ ðŸ›¢ï¸ Ù†ÙØª: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"â€¢ {display_name}: {item['amount']:,}\n"

        message += "\nðŸ“¥ *Ø¯Ø±ÛŒØ§ÙØª Ø§Ø² Ú©Ø´ÙˆØ± Ù…Ù‚Ø§Ø¨Ù„:*\n"
        for item in trade_items['receive']:
            if item.get('resource') == 'capital':
                message += f"â€¢ ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"â€¢ ðŸ›¢ï¸ Ù†ÙØª: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"â€¢ {display_name}: {item['amount']:,}\n"

        keyboard = [
            [InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø§Ø±Ø³Ø§Ù„ÛŒ", callback_data='add_send_item')],
            [InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ… Ø¯Ø±ÛŒØ§ÙØªÛŒ", callback_data='add_receive_item')],
            [InlineKeyboardButton("âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª", callback_data='confirm_trade')],
            [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='trade_menu')]
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
            await update.callback_query.answer("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§", show_alert=True)
        else:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§")
        return TRADE_ADD_ITEMS


async def confirm_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    try:
        if query.message:
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")
    except Exception as e:
        logger.warning(f"Could not edit message: {e}")
        await context.bot.send_message(chat_id, "Ø¯Ø± Ø­Ø§Ù„ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª...")

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
                    await query.answer(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ø³Ø±Ù…Ø§ÛŒÙ‡ ÙØ¹Ù„ÛŒ: {country['capital']:,}", show_alert=True)
                    return TRADE_ADD_ITEMS
            elif resource == 'oil_barrels':
                if country['oil_barrels'] < amount:
                    await query.answer(f"Ù†ÙØª Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù†ÙØª ÙØ¹Ù„ÛŒ: {country['oil_barrels']:,}", show_alert=True)
                    return TRADE_ADD_ITEMS
            else:
                category = item.get('category')
                if resource in country.get(category, {}):
                    if country[category][resource] < amount:
                        display_name = get_asset_display_name(resource)
                        await query.answer(f"Ù…ÙˆØ¬ÙˆØ¯ÛŒ {display_name} Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ: {country[category][resource]}", show_alert=True)
                        return TRADE_ADD_ITEMS
                else:
                    display_name = get_asset_display_name(resource)
                    await query.answer(f"Ø´Ù…Ø§ {display_name} Ù†Ø¯Ø§Ø±ÛŒØ¯!", show_alert=True)
                    return TRADE_ADD_ITEMS

        trade_id, delivery_minutes, secret_code = create_trade(
            user_id, target_user_id, domain,
            trade_items['send'],
            trade_items['receive'],
            trade_type
        )

        target_country = get_country(target_user_id)
        trade_display_name = "Ø¹Ø§Ø¯ÛŒ" if trade_type == "normal" else "Ù…Ø­Ø±Ù…Ø§Ù†Ù‡"
        domain_display_name = next((name for key, name in TRADE_DOMAINS if key == domain), domain)

        sender_country = get_country(user_id)

        message = (
            f"ðŸ“¬ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø¬Ø¯ÛŒØ¯!\n\n"
            f"ðŸ‘¤ Ø§Ø²: {sender_country['name']}\n"
            f"ðŸŒ Ø¯Ø§Ù…Ù†Ù‡: {domain_display_name}\n"
            f"ðŸ“¤ Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ø´Ù…Ø§:\n"
        )
        for item in trade_items['send']:
            if item.get('resource') == 'capital':
                message += f"â€¢ ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"â€¢ ðŸ›¢ï¸ Ù†ÙØª: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"â€¢ {display_name}: {item['amount']:,}\n"

        message += f"\nðŸ“¥ Ø¯Ø±ÛŒØ§ÙØª Ø§Ø² Ø´Ù…Ø§:\n"
        for item in trade_items['receive']:
            if item.get('resource') == 'capital':
                message += f"â€¢ ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {item['amount']:,}\n"
            elif item.get('resource') == 'oil_barrels':
                message += f"â€¢ ðŸ›¢ï¸ Ù†ÙØª: {item['amount']:,}\n"
            else:
                display_name = get_asset_display_name(item['resource'])
                message += f"â€¢ {display_name}: {item['amount']:,}\n"

        message += f"\nâ³ Ø²Ù…Ø§Ù† ØªØ­ÙˆÛŒÙ„: {delivery_minutes} Ø¯Ù‚ÛŒÙ‚Ù‡\n"
        message += f"ðŸ”’ Ù†ÙˆØ¹ ØªØ¬Ø§Ø±Øª: {trade_display_name}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("âœ… Ù‚Ø¨ÙˆÙ„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª", callback_data=f"accept_trade_{trade_id}"),
             InlineKeyboardButton("âŒ Ø±Ø¯ Ø¯Ø±Ø®ÙˆØ§Ø³Øª", callback_data=f"reject_trade_{trade_id}")]
        ])

        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=message,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø¨Ù‡ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù: {e}", exc_info=True)
            await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø¨Ù‡ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù. Ù„Ø·ÙØ§Ù‹ Ø§Ø·Ù…ÛŒÙ†Ø§Ù† Ø­Ø§ØµÙ„ Ú©Ù†ÛŒØ¯ Ú©Ù‡ Ø±Ø¨Ø§Øª Ø¨Ø±Ø§ÛŒ Ø¢Ù† Ú©Ø§Ø±Ø¨Ø± ÙØ¹Ø§Ù„ Ø§Ø³Øª.")
            return TRADE_ADD_ITEMS

        await query.edit_message_text(f"âœ… Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ù‡ {target_country['name']} Ø§Ø±Ø³Ø§Ù„ Ø´Ø¯. Ù…Ù†ØªØ¸Ø± ØªØ£ÛŒÛŒØ¯ Ø¢Ù†Ù‡Ø§ Ø¨Ø§Ø´ÛŒØ¯.")

        if trade_type == 'discreet':
            discreet_channel = get_trade_setting('discreet_trade_channel') or STATEMENT_CHANNEL
            admin_message = (
                f"ðŸ”’ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³ Ø¬Ø¯ÛŒØ¯!\n\n"
                f"ðŸ‘¤ ÙØ±Ø³ØªÙ†Ø¯Ù‡: {sender_country['name']} (ID: {user_id})\n"
                f"ðŸŽ¯ Ú¯ÛŒØ±Ù†Ø¯Ù‡: {target_country['name']} (ID: {target_user_id})\n"
                f"ðŸŒ Ø¯Ø§Ù…Ù†Ù‡: {domain_display_name}\n"
                f"ðŸ” Ú©Ø¯ ØªØ¬Ø§Ø±Øª: {secret_code}\n\n"
                f"Ø¨Ø±Ø§ÛŒ Ù„ØºÙˆ ØªØ¬Ø§Ø±Øª Ø§Ø² Ú©Ø¯ Ø¨Ø§Ù„Ø§ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯."
            )

            admin_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("âŒ Ù„ØºÙˆ ØªØ¬Ø§Ø±Øª", callback_data=f"cancel_trade_{trade_id}")]
            ])

            try:
                await context.bot.send_message(
                    chat_id=discreet_channel,
                    text=admin_message,
                    reply_markup=admin_keyboard
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„ ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³: {e}")

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
        await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø«Ø¨Øª ØªØ¬Ø§Ø±Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
        return TRADE_ADD_ITEMS


async def handle_trade_response(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        parts = query.data.split('_', 2)
        if len(parts) < 3:
            await query.answer("Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§ÛŒ ÙØ±Ø§Ø®ÙˆØ§Ù† Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª", show_alert=True)
            return MAIN_MENU

        action = parts[0]
        trade_id = parts[2]

        trade = get_trade(trade_id)
        if not trade:
            await query.edit_message_text("âŒ ØªØ¬Ø§Ø±Øª Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯ ÛŒØ§ Ù‚Ø¨Ù„Ø§Ù‹ Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø´Ø¯Ù‡ Ø§Ø³Øª.")
            return MAIN_MENU

        if action == "accept":
            receiver_country = get_country(trade['receiver_id'])
            if not receiver_country:
                await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
                return MAIN_MENU

            for item in trade['receive_resource']:
                resource = item.get('resource')
                amount = item.get('amount', 0)
                if resource == 'capital':
                    if receiver_country['capital'] < amount:
                        await query.answer(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ø³Ø±Ù…Ø§ÛŒÙ‡ ÙØ¹Ù„ÛŒ: {receiver_country['capital']:,}", show_alert=True)
                        return MAIN_MENU
                elif resource == 'oil_barrels':
                    if receiver_country['oil_barrels'] < amount:
                        await query.answer(f"Ù†ÙØª Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù†ÙØª ÙØ¹Ù„ÛŒ: {receiver_country['oil_barrels']:,}", show_alert=True)
                        return MAIN_MENU
                else:
                    category = item.get('category')
                    current_amount = receiver_country.get(category, {}).get(resource, 0)
                    if current_amount < amount:
                        display_name = get_asset_display_name(resource)
                        await query.answer(f"Ù…ÙˆØ¬ÙˆØ¯ÛŒ {display_name} Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ: {current_amount}", show_alert=True)
                        return MAIN_MENU

            update_trade_status(trade_id, "accepted")

            delivery_time = datetime.fromisoformat(trade['delivery_time'])
            now = datetime.now()
            remaining_minutes = max(0, int((delivery_time - now).total_seconds() / 60))

            await query.edit_message_text("âœ… Ø´Ù…Ø§ Ø§ÛŒÙ† ØªØ¬Ø§Ø±Øª Ø±Ø§ Ù‚Ø¨ÙˆÙ„ Ú©Ø±Ø¯ÛŒØ¯. Ù…Ù†Ø§Ø¨Ø¹ Ù¾Ø³ Ø§Ø² Ø²Ù…Ø§Ù† Ù…Ø´Ø®Øµ Ø´Ø¯Ù‡ Ù…Ù†ØªÙ‚Ù„ Ø®ÙˆØ§Ù‡Ù†Ø¯ Ø´Ø¯.")

            sender_country = get_country(trade['sender_id'])
            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"âœ… Ú©Ø´ÙˆØ± {receiver_country['name']} Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø±Ø§ Ù¾Ø°ÛŒØ±ÙØª. Ù…Ù†Ø§Ø¨Ø¹ Ù¾Ø³ Ø§Ø² {remaining_minutes} Ø¯Ù‚ÛŒÙ‚Ù‡ Ù…Ù†ØªÙ‚Ù„ Ø®ÙˆØ§Ù‡Ù†Ø¯ Ø´Ø¯."
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø·Ù„Ø§Ø¹ Ø¨Ù‡ ÙØ±Ø³ØªÙ†Ø¯Ù‡: {e}")

            if trade['trade_type'] == 'normal':
                trade_channel = get_trade_setting('trade_channel') or STATEMENT_CHANNEL
                try:
                    domain_display_name = next((name for key, name in TRADE_DOMAINS if key == trade['domain']), trade['domain'])
                    channel_message = (
                        f"ðŸ“Š ØªØ¬Ø§Ø±Øª Ø¬Ø¯ÛŒØ¯ ØªØ£ÛŒÛŒØ¯ Ø´Ø¯!\n\n"
                        f"ðŸŒ Ø¯Ø§Ù…Ù†Ù‡: {domain_display_name}\n"
                        f"ðŸ”„ Ú©Ø´ÙˆØ±Ù‡Ø§: {sender_country['name']} â†”ï¸ {receiver_country['name']}\n"
                        f"â³ Ø²Ù…Ø§Ù† ØªØ­ÙˆÛŒÙ„: {remaining_minutes} Ø¯Ù‚ÛŒÙ‚Ù‡"
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
                    logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ ØªØ¬Ø§Ø±Øª Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„: {e}")

        elif action == "reject":
            update_trade_status(trade_id, "rejected")
            await query.edit_message_text("âŒ Ø´Ù…Ø§ Ø§ÛŒÙ† ØªØ¬Ø§Ø±Øª Ø±Ø§ Ø±Ø¯ Ú©Ø±Ø¯ÛŒØ¯.")

            receiver_country = get_country(trade['receiver_id'])
            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"âŒ Ú©Ø´ÙˆØ± {receiver_country['name']} Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø±Ø§ Ø±Ø¯ Ú©Ø±Ø¯."
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø·Ù„Ø§Ø¹ Ø¨Ù‡ ÙØ±Ø³ØªÙ†Ø¯Ù‡: {e}")
        elif action == "cancel":
            if not is_admin(query.from_user.id):
                await query.answer("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ù†Ø¯ ØªØ¬Ø§Ø±Øª Ø±Ø§ Ù„ØºÙˆ Ú©Ù†Ù†Ø¯!", show_alert=True)
                return ADMIN_MENU

            update_trade_status(trade_id, "cancelled")
            await query.edit_message_text("âœ… ØªØ¬Ø§Ø±Øª Ù„ØºÙˆ Ø´Ø¯.")

            sender_country = get_country(trade['sender_id'])
            receiver_country = get_country(trade['receiver_id'])

            try:
                await context.bot.send_message(
                    chat_id=trade['sender_id'],
                    text=f"âŒ ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ø§ Ú©Ø´ÙˆØ± {receiver_country['name']} ØªÙˆØ³Ø· Ù…Ø¯ÛŒØ±ÛŒØª Ù„ØºÙˆ Ø´Ø¯."
                )
                await context.bot.send_message(
                    chat_id=trade['receiver_id'],
                    text=f"âŒ ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ø§ Ú©Ø´ÙˆØ± {sender_country['name']} ØªÙˆØ³Ø· Ù…Ø¯ÛŒØ±ÛŒØª Ù„ØºÙˆ Ø´Ø¯."
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø·Ù„Ø§Ø¹ Ø¨Ù‡ Ø·Ø±ÙÛŒÙ† ØªØ¬Ø§Ø±Øª: {e}")

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in handle_trade_response: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø¯Ø±Ø®ÙˆØ§Ø³Øª ØªØ¬Ø§Ø±Øª")
        return MAIN_MENU


async def deliver_trades_job(context: CallbackContext):
    logger.info("Ø¨Ø±Ø±Ø³ÛŒ ØªØ­ÙˆÛŒÙ„ ØªØ¬Ø§Ø±Øªâ€ŒÙ‡Ø§...")
    try:
        trades = get_trades_for_delivery()
        if not trades:
            logger.info("Ù‡ÛŒÚ† ØªØ¬Ø§Ø±ØªÛŒ Ø¨Ø±Ø§ÛŒ ØªØ­ÙˆÛŒÙ„ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return

        logger.info(f"ØªØ­ÙˆÛŒÙ„ {len(trades)} ØªØ¬Ø§Ø±Øª")

        for trade in trades:
            try:
                sender_id = trade['sender_id']
                receiver_id = trade['receiver_id']

                sender_country = get_country(sender_id)
                receiver_country = get_country(receiver_id)

                if not sender_country or not receiver_country:
                    logger.warning(f"Ú©Ø´ÙˆØ± ÙØ±Ø³ØªÙ†Ø¯Ù‡ ÛŒØ§ Ú¯ÛŒØ±Ù†Ø¯Ù‡ Ø¨Ø±Ø§ÛŒ ØªØ¬Ø§Ø±Øª {trade['id']} ÛŒØ§ÙØª Ù†Ø´Ø¯.")
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
                        f"âœ… ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ø§ Ú©Ø´ÙˆØ± {receiver_country['name']} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª ØªØ­ÙˆÛŒÙ„ Ø¯Ø§Ø¯Ù‡ Ø´Ø¯!"
                    )
                    await context.bot.send_message(
                        receiver_id,
                        f"âœ… ØªØ¬Ø§Ø±Øª Ø´Ù…Ø§ Ø¨Ø§ Ú©Ø´ÙˆØ± {sender_country['name']} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª ØªØ­ÙˆÛŒÙ„ Ø¯Ø§Ø¯Ù‡ Ø´Ø¯!"
                    )
                except Exception as e:
                    logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø¨Ù‡ Ú©Ø§Ø±Ø¨Ø±Ø§Ù†: {e}")

                logger.info(f"ØªØ¬Ø§Ø±Øª {trade['id']} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª ØªØ­ÙˆÛŒÙ„ Ø¯Ø§Ø¯Ù‡ Ø´Ø¯.")

            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ ØªØ¬Ø§Ø±Øª {trade['id']}: {e}")

        logger.info("ØªØ­ÙˆÛŒÙ„ ØªØ¬Ø§Ø±Øªâ€ŒÙ‡Ø§ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯.")
    except Exception as e:
        logger.error(f"Ø®Ø·Ø§ Ø¯Ø± ØªØ­ÙˆÛŒÙ„ ØªØ¬Ø§Ø±Øªâ€ŒÙ‡Ø§: {e}")


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
                    f"ðŸ’¥ Ø­Ù…Ù„Ù‡ Ø¨Ù‡ Ù…Ù‚ØµØ¯ Ø±Ø³ÛŒØ¯!\n\n"
                    f"âš”ï¸ Ø­Ù…Ù„Ù‡ Ø§Ø² Ú©Ø´ÙˆØ± {attacker['name']}\n"
                    f"ðŸŽ¯ Ø¨Ù‡ Ú©Ø´ÙˆØ± {target['name']}\n"
                    f"Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª ØªØ­ÙˆÛŒÙ„ Ø¯Ø§Ø¯Ù‡ Ø´Ø¯!"
                )
                await context.bot.send_message(
                    chat_id=STATEMENT_CHANNEL,
                    text=delivery_message
                )
            except Exception as e:
                logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… ØªØ­ÙˆÛŒÙ„ Ø­Ù…Ù„Ù‡: {e}")

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
            [InlineKeyboardButton(f"ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ ØªØ¬Ø§Ø±Øª: {'âœ… Ø±ÙˆØ´Ù†' if trade_enabled else 'âŒ Ø®Ø§Ù…ÙˆØ´'}", callback_data='toggle_trade_enabled')],
            [InlineKeyboardButton(f"ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³: {'âœ… Ø±ÙˆØ´Ù†' if discreet_enabled else 'âŒ Ø®Ø§Ù…ÙˆØ´'}", callback_data='toggle_discreet_trade')],
            [InlineKeyboardButton(f"Ø­Ø¯Ø§Ú©Ø«Ø± ØªØ¬Ø§Ø±Øª Ø±ÙˆØ²Ø§Ù†Ù‡: {max_trades}", callback_data='set_max_trades')],
            [InlineKeyboardButton(f"Ú©Ø§Ù†Ø§Ù„ Ø§Ø·Ù„Ø§Ø¹â€ŒØ±Ø³Ø§Ù†ÛŒ: {trade_channel}", callback_data='set_trade_channel')],
            [InlineKeyboardButton(f"Ú©Ø§Ù†Ø§Ù„ ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³: {discreet_channel}", callback_data='set_discreet_trade_channel')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "âš™ï¸ ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ø³ÛŒØ³ØªÙ… ØªØ¬Ø§Ø±Øª:\n"
            "Ø¯Ø± Ø§ÛŒÙ† Ø¨Ø®Ø´ Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ù…Ø±Ø¨ÙˆØ· Ø¨Ù‡ Ø³ÛŒØ³ØªÙ… ØªØ¬Ø§Ø±Øª Ø±Ø§ Ù…Ø¯ÛŒØ±ÛŒØª Ú©Ù†ÛŒØ¯.",
            reply_markup=reply_markup
        )
        return ADMIN_TRADE_SETTINGS
    except Exception as e:
        logger.error(f"Error in trade_settings: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ ØªÙ†Ø¸ÛŒÙ…Ø§Øª ØªØ¬Ø§Ø±Øª")
        return ADMIN_MENU


async def toggle_trade_enabled(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_trade_setting('trade_enabled')
        new_status = '0' if current_status == '1' else '1'
        set_trade_setting('trade_enabled', new_status)

        status_text = "ÙØ¹Ø§Ù„" if new_status == '1' else "ØºÛŒØ±ÙØ¹Ø§Ù„"
        await query.answer(f"ÙˆØ¶Ø¹ÛŒØª ØªØ¬Ø§Ø±Øª: {status_text}")
        return await trade_settings(update, context)
    except Exception as e:
        logger.error(f"Error in toggle_trade_enabled: {e}", exc_info=True)
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª ØªØ¬Ø§Ø±Øª", show_alert=True)
        return ADMIN_TRADE_SETTINGS


async def toggle_discreet_trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        current_status = get_trade_setting('discreet_trade_enabled')
        new_status = '0' if current_status == '1' else '1'
        set_trade_setting('discreet_trade_enabled', new_status)

        status_text = "ÙØ¹Ø§Ù„" if new_status == '1' else "ØºÛŒØ±ÙØ¹Ø§Ù„"
        await query.answer(f"ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³ {status_text} Ø´Ø¯")
        return await trade_settings(update, context)
    except Exception as e:
        logger.error(f"Error in toggle_discreet_trade: {e}", exc_info=True)
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± ØªØºÛŒÛŒØ± ÙˆØ¶Ø¹ÛŒØª ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³", show_alert=True)
        return ADMIN_TRADE_SETTINGS


async def set_max_trades(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "ðŸ”¢ Ù„Ø·ÙØ§Ù‹ Ø­Ø¯Ø§Ú©Ø«Ø± ØªØ¹Ø¯Ø§Ø¯ ØªØ¬Ø§Ø±Øª Ù…Ø¬Ø§Ø² Ø±ÙˆØ²Ø§Ù†Ù‡ Ø¨Ø±Ø§ÛŒ Ù‡Ø± Ú©Ø§Ø±Ø¨Ø± Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:"
    )
    return SET_MAX_TRADES


async def process_max_trades(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        max_trades = int(update.message.text)
        if max_trades <= 0:
            await update.message.reply_text("Ø¹Ø¯Ø¯ Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯.")
            return SET_MAX_TRADES

        set_trade_setting('max_trades', str(max_trades))
        await update.message.reply_text(f"âœ… Ø­Ø¯Ø§Ú©Ø«Ø± ØªØ¬Ø§Ø±Øª Ø±ÙˆØ²Ø§Ù†Ù‡ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ {max_trades} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
        return await admin_panel(update, context)
    except ValueError:
        await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return SET_MAX_TRADES
    except Exception as e:
        logger.error(f"Error in process_max_trades: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡â€ŒØ³Ø§Ø²ÛŒ ØªÙ†Ø¸ÛŒÙ…Ø§Øª")
        return SET_MAX_TRADES


async def set_trade_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['setting_channel_type'] = 'normal'

    await query.edit_message_text(
        "ðŸ“£ Ù„Ø·ÙØ§Ù‹ Ø¢ÛŒØ¯ÛŒ Ú©Ø§Ù†Ø§Ù„ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø§Ø·Ù„Ø§Ø¹â€ŒØ±Ø³Ø§Ù†ÛŒ ØªØ¬Ø§Ø±Øªâ€ŒÙ‡Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Ù…Ø«Ø§Ù„: @channel_username):"
    )
    return SET_TRADE_CHANNEL


async def set_discreet_trade_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['setting_channel_type'] = 'discreet'

    await query.edit_message_text(
        "ðŸ”’ Ù„Ø·ÙØ§Ù‹ Ø¢ÛŒØ¯ÛŒ Ú©Ø§Ù†Ø§Ù„ Ø±Ø§ Ø¨Ø±Ø§ÛŒ ØªØ¬Ø§Ø±Øªâ€ŒÙ‡Ø§ÛŒ Ù†Ø§Ù…Ø­Ø³ÙˆØ³ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯ (Ù…Ø«Ø§Ù„: @channel_username):"
    )
    return SET_TRADE_CHANNEL


async def process_trade_channel(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        channel_id = update.message.text.strip()
        channel_type = context.user_data.get('setting_channel_type', 'normal')
        if channel_type == 'discreet':
            set_trade_setting('discreet_trade_channel', channel_id)
            await update.message.reply_text(f"âœ… Ú©Ø§Ù†Ø§Ù„ ØªØ¬Ø§Ø±Øª Ù†Ø§Ù…Ø­Ø³ÙˆØ³ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ {channel_id} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
        else:
            set_trade_setting('trade_channel', channel_id)
            await update.message.reply_text(f"âœ… Ú©Ø§Ù†Ø§Ù„ Ø§Ø·Ù„Ø§Ø¹â€ŒØ±Ø³Ø§Ù†ÛŒ ØªØ¬Ø§Ø±Øª Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ {channel_id} ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯.")
        context.user_data.pop('setting_channel_type', None)
        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in process_trade_channel: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡â€ŒØ³Ø§Ø²ÛŒ ØªÙ†Ø¸ÛŒÙ…Ø§Øª")
        return SET_TRADE_CHANNEL


async def manage_notification_images(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = [
            [InlineKeyboardButton("ØªØºÛŒÛŒØ± Ø¯ÛŒÙ†", callback_data="set_religion_image")],
            [InlineKeyboardButton("Ù…Ù„ÛŒ Ú©Ø±Ø¯Ù† Ø§ÛŒÙ†ØªØ±Ù†Øª", callback_data="set_internet_on_image")],
            [InlineKeyboardButton("Ù„ØºÙˆ Ù…Ù„ÛŒ Ú©Ø±Ø¯Ù† Ø§ÛŒÙ†ØªØ±Ù†Øª", callback_data="set_internet_off_image")],
            [InlineKeyboardButton("ØªØ¬Ø§Ø±Øª Ø²Ù…ÛŒÙ†ÛŒ", callback_data="set_trade_land_image")],
            [InlineKeyboardButton("ØªØ¬Ø§Ø±Øª Ù‡ÙˆØ§ÛŒÛŒ", callback_data="set_trade_air_image")],
            [InlineKeyboardButton("ØªØ¬Ø§Ø±Øª Ø¯Ø±ÛŒØ§ÛŒÛŒ", callback_data="set_trade_sea_image")],
            [InlineKeyboardButton("Ø­Ù…Ù„Ù‡ Ù†Ø¸Ø§Ù…ÛŒ", callback_data="set_attack_image")],
            [InlineKeyboardButton("Ø±Ø²Ù…Ø§ÛŒØ´ Ø²Ù…ÛŒÙ†ÛŒ", callback_data="set_exercise_land_image")],
            [InlineKeyboardButton("Ø±Ø²Ù…Ø§ÛŒØ´ Ø¯Ø±ÛŒØ§ÛŒÛŒ", callback_data="set_exercise_sea_image")],
            [InlineKeyboardButton("Ø±Ø²Ù…Ø§ÛŒØ´ Ù‡ÙˆØ§ÛŒÛŒ", callback_data="set_exercise_air_image")],
            [InlineKeyboardButton("Ø­Ù…Ù„Ù‡ Ù…ÙˆØ´Ú©ÛŒ", callback_data="set_missile_attack_image")],
            [InlineKeyboardButton("Ø³Ø§Ø®Øª ÙÛŒÙ„Ù…", callback_data="set_film_image")],
            [InlineKeyboardButton("Ø³Ø§Ø®Øª Ø¨Ø§Ø²ÛŒ", callback_data="set_game_image")],
            [InlineKeyboardButton("Ø³Ø§Ø®Øª Ù…ÙˆØ³ÛŒÙ‚ÛŒ", callback_data="set_music_image")],
            [InlineKeyboardButton("Ø¨Ø±ØªØ±ÛŒÙ† Ù†ÙØª", callback_data="set_top_oil_image")],
            [InlineKeyboardButton("Ø¨Ø±ØªØ±ÛŒÙ† Ø±Ø¶Ø§ÛŒØª", callback_data="set_top_satisfaction_image")],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data="admin_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡ Ø¨Ø±Ø§ÛŒ ØªÙ†Ø¸ÛŒÙ… Ø¹Ú©Ø³:", reply_markup=reply_markup)
        return MANAGE_NOTIFICATION_IMAGES
    except Exception as e:
        logger.error(f"Error in manage_notification_images: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø¹Ú©Ø³ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡â€ŒÙ‡Ø§")
        return ADMIN_MENU


async def set_notification_image_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        event_type = query.data.replace("set_", "").replace("_image", "")
        context.user_data["notification_event_type"] = event_type

        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ø¹Ú©Ø³ Ø¬Ø¯ÛŒØ¯ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:")
        return GET_NOTIFICATION_IMAGE
    except Exception as e:
        logger.error(f"Error in set_notification_image_handler: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡")
        return MANAGE_NOTIFICATION_IMAGES


async def save_notification_image(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        if not update.message.photo:
            await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ú©Ø³ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
            return GET_NOTIFICATION_IMAGE

        event_type = context.user_data["notification_event_type"]
        photo_id = update.message.photo[-1].file_id

        set_notification_image(event_type, photo_id)
        await update.message.reply_text(f"âœ… Ø¹Ú©Ø³ Ø¨Ø±Ø§ÛŒ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡ {event_type} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø°Ø®ÛŒØ±Ù‡ Ø´Ø¯!")

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in save_notification_image: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø°Ø®ÛŒØ±Ù‡ Ø¹Ú©Ø³")
        return GET_NOTIFICATION_IMAGE


async def random_prize_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = []
        for category_key, category_name in get_dynamic_asset_categories_for_display():
            keyboard.append([InlineKeyboardButton(category_name, callback_data=f"prize_category_{category_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡", callback_data="prize_capital")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='admin_panel')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "ðŸŽ Ù…Ù†ÙˆÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…:\nÙ„Ø·ÙØ§Ù‹ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return RANDOM_PRIZE_MENU
    except Exception as e:
        logger.error(f"Error in random_prize_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…")
        return ADMIN_MENU


async def select_prize_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'prize_capital':
            context.user_data['prize_category'] = 'capital'
            await query.edit_message_text("ðŸ’° Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
            return GET_PRIZE_QUANTITY

        category_key = query.data.replace("prize_category_", "")
        context.user_data['prize_category'] = category_key

        keyboard = []
        for item_key in get_dynamic_default_assets().get(category_key, {}).keys():
            display_name = get_asset_display_name(item_key)
            keyboard.append([InlineKeyboardButton(display_name, callback_data=f"prize_item_{item_key}")])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='random_prize_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        category_display_name = next((disp for key, disp in get_dynamic_asset_categories_for_display() if key == category_key), category_key)
        await query.edit_message_text(
            f"Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø¬Ø§ÛŒØ²Ù‡ Ø§Ø² Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ {category_display_name}:",
            reply_markup=reply_markup
        )
        return SELECT_PRIZE_CATEGORY
    except Exception as e:
        logger.error(f"Error in select_prize_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ")
        return RANDOM_PRIZE_MENU


async def select_prize_item(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        item_key = query.data.replace("prize_item_", "")
        context.user_data['prize_item'] = item_key

        await query.edit_message_text(f"Ù„Ø·ÙØ§Ù‹ Ù…Ù‚Ø¯Ø§Ø± {get_asset_display_name(item_key)} Ø¨Ø±Ø§ÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return GET_PRIZE_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_prize_item: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ø¢ÛŒØªÙ… Ø¬Ø§ÛŒØ²Ù‡")
        return SELECT_PRIZE_CATEGORY


async def get_prize_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("Ù…Ù‚Ø¯Ø§Ø± Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯.")
            return GET_PRIZE_QUANTITY
    except ValueError:
        await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
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

    prize_description = f"ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {quantity:,}" if category == 'capital' else f"{get_asset_display_name(item)}: {quantity:,}"

    await update.message.reply_text(
        f"âœ… Ø¬Ø§ÛŒØ²Ù‡ ØªÙ†Ø¸ÛŒÙ… Ø´Ø¯!\n"
        f"ðŸ”¢ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¬Ø§ÛŒØ²Ù‡: {prize_description}\n"
        f"ðŸ” Ú©Ø¯ ØªØ£ÛŒÛŒØ¯: `{verification_code}`\n\n"
        "Ø¨Ø±Ø§ÛŒ Ø§Ø¬Ø±Ø§ÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…ØŒ Ú©Ø¯ ØªØ£ÛŒÛŒØ¯ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.",
        parse_mode="Markdown"
    )

    return CONFIRM_RANDOM_PRIZE


async def confirm_random_prize(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    try:
        entered_code = update.message.text.strip()
        saved_code = context.user_data.get('verification_code')

        if entered_code != saved_code:
            await update.message.reply_text("âŒ Ú©Ø¯ ØªØ£ÛŒÛŒØ¯ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return CONFIRM_RANDOM_PRIZE

        category = context.user_data.get('prize_category')
        item = context.user_data.get('prize_item')
        quantity = context.user_data.get('prize_quantity')

        countries = get_all_countries()
        if not countries:
            await update.message.reply_text("âŒ Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ø§Ù‡Ø¯Ø§ÛŒ Ø¬Ø§ÛŒØ²Ù‡ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return await admin_panel(update, context)

        winner_id, winner_name = random.choice(countries)
        winner_country = get_country(winner_id)

        if category == 'capital':
            new_capital = winner_country['capital'] + quantity
            update_country(winner_id, {'capital': new_capital})
            prize_description = f"ðŸ’° Ø³Ø±Ù…Ø§ÛŒÙ‡: {quantity:,}"
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
                text=f"ðŸŽ‰ ØªØ¨Ø±ÛŒÚ©! Ø´Ù…Ø§ Ø¨Ø±Ù†Ø¯Ù‡ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ… Ø´Ø¯ÛŒØ¯!\n"
                     f"ðŸŽ Ø¬Ø§ÛŒØ²Ù‡ Ø´Ù…Ø§: {prize_description}\n"
                     f"Ø§Ø² Ø·Ø±Ù Ù…Ø¯ÛŒØ±ÛŒØª Ø±Ø¨Ø§Øª Ø¬Ù†Ú¯ Ø¬Ù‡Ø§Ù†ÛŒ"
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø¨Ù‡ Ø¨Ø±Ù†Ø¯Ù‡: {e}")

        try:
            await context.bot.send_message(
                chat_id=STATEMENT_CHANNEL,
                text=f"ðŸŽ‰ Ø§Ø¹Ù„Ø§Ù… Ø¨Ø±Ù†Ø¯Ù‡ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…!\n\n"
                     f"ðŸ† Ø¨Ø±Ù†Ø¯Ù‡: {winner_name}\n"
                     f"ðŸŽ Ø¬Ø§ÛŒØ²Ù‡: {prize_description}\n"
                     f"Ø¨Ø§ Ø¢Ø±Ø²ÙˆÛŒ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ø±Ø§ÛŒ Ù‡Ù…Ù‡ Ú©Ø´ÙˆØ±Ù‡Ø§!"
            )
        except Exception as e:
            logger.error(f"Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±Ø³Ø§Ù„ Ø§Ø·Ù„Ø§Ø¹ÛŒÙ‡ Ø¨Ù‡ Ú©Ø§Ù†Ø§Ù„: {e}")

        await update.message.reply_text(
            f"âœ… Ø¬Ø§ÛŒØ²Ù‡ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ù‡ Ú©Ø´ÙˆØ± {winner_name} Ø§Ù‡Ø¯Ø§ Ø´Ø¯!\n"
            f"ðŸŽ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¬Ø§ÛŒØ²Ù‡: {prize_description}"
        )

        keys_to_remove = ['prize_category', 'prize_item', 'prize_quantity', 'verification_code']
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return await admin_panel(update, context)
    except Exception as e:
        logger.error(f"Error in confirm_random_prize: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø¬Ø±Ø§ÛŒ Ø¬Ø§ÛŒØ²Ù‡ Ø±Ù†Ø¯ÙˆÙ…")
        return ADMIN_MENU


async def military_exercise(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    disabled_buttons = get_global_disabled_buttons()
    if 'military_exercise' in disabled_buttons:
        await query.answer("â›” Ø±Ø²Ù…Ø§ÛŒØ´ Ù†Ø¸Ø§Ù…ÛŒ Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
        return COUNTRY_MANAGEMENT

    try:
        keyboard = [
            [InlineKeyboardButton("Ø²Ù…ÛŒÙ†ÛŒ", callback_data='exercise_land')],
            [InlineKeyboardButton("Ø¯Ø±ÛŒØ§ÛŒÛŒ", callback_data='exercise_sea')],
            [InlineKeyboardButton("Ù‡ÙˆØ§ÛŒÛŒ", callback_data='exercise_air')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Ù†ÙˆØ¹ Ø±Ø²Ù…Ø§ÛŒØ´ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return MILITARY_EXERCISE_TYPE
    except Exception as e:
        logger.error(f"Error in military_exercise: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø±Ø²Ù…Ø§ÛŒØ´")
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
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return MAIN_MENU

        category_map = {
            'land': 'land_troops',
            'sea': 'naval_troops',
            'air': 'air_troops'
        }
        category = category_map.get(exercise_type)
        if not category:
            await query.edit_message_text("âŒ Ù†ÙˆØ¹ Ø±Ø²Ù…Ø§ÛŒØ´ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª.")
            return MILITARY_EXERCISE_TYPE

        forces = country.get(category, {})
        total_forces = sum(forces.values())
        if total_forces == 0:
            await query.edit_message_text(f"âŒ Ø´Ù…Ø§ Ù†ÛŒØ±ÙˆÛŒ {exercise_type}ÛŒ Ù†Ø¯Ø§Ø±ÛŒØ¯!")
            return COUNTRY_MANAGEMENT

        await query.edit_message_text("Ù„Ø·ÙØ§Ù‹ Ú©Ø¯ 4 Ø±Ù‚Ù…ÛŒ Ø±Ø²Ù…Ø§ÛŒØ´ Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:")
        return GET_EXERCISE_CODE
    except Exception as e:
        logger.error(f"Error in select_exercise_type: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ø±Ø²Ù…Ø§ÛŒØ´")
        return MILITARY_EXERCISE_TYPE


async def get_exercise_code(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return MAIN_MENU
    try:
        code = update.message.text
        if not code.isdigit() or len(code) != 4:
            await update.message.reply_text("Ú©Ø¯ Ø¨Ø§ÛŒØ¯ 4 Ø±Ù‚Ù… Ø¨Ø§Ø´Ø¯. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
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
            f"Ø±Ø²Ù…Ø§ÛŒØ´ {exercise_type}ÛŒ ØªÙˆØ³Ø· Ú©Ø´ÙˆØ± {country['name']} Ø¨Ø§ Ú©Ø¯ {code} Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯.\n\n"
            f"Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ Ø´Ø±Ú©Øª Ú©Ù†Ù†Ø¯Ù‡: {total_forces:,}\n"
            f"Ø¯Ø±ØµØ¯ Ù…ÙˆÙÙ‚ÛŒØª: {success}%\n\n"
        )

        if success >= 85:
            report += "âœ… Ø±Ø²Ù…Ø§ÛŒØ´ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¹Ø§Ù„ÛŒ Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯. Ù†ÛŒØ±ÙˆÙ‡Ø§ Ø¨Ù‡ Ø®ÙˆØ¨ÛŒ Ø¢Ù…ÙˆØ²Ø´ Ø¯ÛŒØ¯Ù†Ø¯ Ùˆ Ø¢Ù…Ø§Ø¯Ú¯ÛŒ Ù†Ø¸Ø§Ù…ÛŒ Ø§ÙØ²Ø§ÛŒØ´ ÛŒØ§ÙØª."
        elif success >= 75:
            report += "ðŸŸ¢ Ø±Ø²Ù…Ø§ÛŒØ´ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯. Ù†Ù‚Ø§Ø· Ù‚ÙˆØª Ùˆ Ø¶Ø¹Ù Ø´Ù†Ø§Ø³Ø§ÛŒÛŒ Ø´Ø¯Ù†Ø¯."
        else:
            report += "ðŸ”´ Ø±Ø²Ù…Ø§ÛŒØ´ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ù…ØªÙˆØ³Ø·ÛŒ Ø§Ù†Ø¬Ø§Ù… Ø´Ø¯. Ù†ÛŒØ§Ø² Ø¨Ù‡ Ø¢Ù…ÙˆØ²Ø´ Ø¨ÛŒØ´ØªØ± Ù†ÛŒØ±ÙˆÙ‡Ø§ Ø§Ø­Ø³Ø§Ø³ Ù…ÛŒâ€ŒØ´ÙˆØ¯."

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

        await update.message.reply_text("âœ… Ú¯Ø²Ø§Ø±Ø´ Ø±Ø²Ù…Ø§ÛŒØ´ Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ù…Ù†ØªØ´Ø± Ø´Ø¯.")

        keys_to_remove = ['exercise_type', 'exercise_code']
        for key in keys_to_remove:
            if key in context.user_data:
                del context.user_data[key]

        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in get_exercise_code: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ Ø±Ø²Ù…Ø§ÛŒØ´")
        return GET_EXERCISE_CODE


async def missile_attack_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    disabled_buttons = get_global_disabled_buttons()
    if 'missile_attack_menu' in disabled_buttons:
        await query.answer("â›” Ø­Ù…Ù„Ù‡ Ù…ÙˆØ´Ú©ÛŒ Ù…ÙˆÙ‚ØªØ§Ù‹ ØºÛŒØ±ÙØ¹Ø§Ù„ Ø§Ø³Øª!", show_alert=True)
        return MAIN_MENU

    try:
        countries = get_all_countries()
        other_countries = [(uid, name) for uid, name in countries if uid != query.from_user.id]
        if not other_countries:
            await query.edit_message_text("Ø¯Ø± Ø­Ø§Ù„ Ø­Ø§Ø¶Ø± Ù‡ÛŒÚ† Ú©Ø´ÙˆØ± Ø¯ÛŒÚ¯Ø±ÛŒ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return MAIN_MENU
        keyboard = []
        for target_user_id, target_name in other_countries:
            keyboard.append([InlineKeyboardButton(target_name, callback_data=f"missile_target_{target_user_id}")])
        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("ðŸš€ Ù„Ø·ÙØ§ Ú©Ø´ÙˆØ±ÛŒ Ø±Ø§ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ Ù…ÙˆØ´Ú©ÛŒ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:", reply_markup=reply_markup)
        return MISSILE_ATTACK_SELECT_TARGET
    except Exception as e:
        logger.error(f"Error in missile_attack_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø±ÛŒØ§ÙØª Ù„ÛŒØ³Øª Ú©Ø´ÙˆØ±Ù‡Ø§")
        return MAIN_MENU


async def select_missile_target(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        target_user_id = int(query.data.replace("missile_target_", ""))
        context.user_data['missile_target_id'] = target_user_id
        target_country = get_country(target_user_id)
        if not target_country:
            await query.edit_message_text("âŒ Ú©Ø´ÙˆØ± Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return await missile_attack_menu(update, context)
        context.user_data['missile_target_name'] = target_country['name']

        user_id = query.from_user.id
        country = get_country(user_id)
        rockets = dict(country.get('rockets', {}) or {})

        # Ø§ÙØ²ÙˆØ¯Ù† Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒÛŒ Ú©Ù‡ Ø¯Ø± DB Ø¯Ø± Ø¯Ø³ØªÙ‡ rockets Ù‡Ø³ØªÙ†Ø¯ ÙˆÙ„ÛŒ Ø¨Ù‡ Ù‡Ø± Ø¯Ù„ÛŒÙ„ Ø¯Ø± country Ù†ÛŒØ³ØªÙ†Ø¯
        try:
            db_items = get_all_equipment_items()
            for it in db_items:
                if it['category'] == 'rockets' and it['item_key'] not in rockets:
                    rockets[it['item_key']] = country.get('rockets', {}).get(it['item_key'], 0)
        except Exception as e:
            logger.warning(f"Ø®Ø·Ø§ Ø¯Ø± Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ Ø¨Ø§ DB: {e}")

        keyboard = []
        for rocket, count in rockets.items():
            if count and count > 0:
                display_name = get_asset_display_name(rocket)
                keyboard.append([InlineKeyboardButton(f"{display_name} (Ù…ÙˆØ¬ÙˆØ¯: {count})", callback_data=f"select_missile_{rocket}")])

        if not keyboard:
            await query.edit_message_text(
                "âŒ Ø´Ù…Ø§ Ù…ÙˆØ´Ú©ÛŒ Ø¨Ø±Ø§ÛŒ Ø­Ù…Ù„Ù‡ Ù†Ø¯Ø§Ø±ÛŒØ¯!\n\n"
                "â„¹ï¸ Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ Ø¨Ø§ÛŒØ¯ Ø¯Ø± Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Â«Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ ðŸš€Â» (Ø¨Ø§ Ú©Ù„ÛŒØ¯ rockets) Ù‚Ø±Ø§Ø± Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù†Ø¯.\n"
                "Ø§Ú¯Ø± Ø§Ø¯Ù…ÛŒÙ† Ù…ÙˆØ´Ú© Ø¬Ø¯ÛŒØ¯ÛŒ Ø§Ø¶Ø§ÙÙ‡ Ú©Ø±Ø¯Ù‡ØŒ Ù…Ø·Ù…Ø¦Ù† Ø´ÙˆÛŒØ¯ Ø¢Ù† Ø±Ø§ Ø¯Ø± Ø¯Ø³ØªÙ‡ Â«Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§Â» Ø³Ø§Ø®ØªÙ‡ Ø§Ø³Øª.\n"
                "Ø³Ù¾Ø³ Ø¢Ù† Ø±Ø§ Ø§Ø² Ù…Ù†ÙˆÛŒ Â«ðŸ›’ Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ø®Ø±ÛŒØ¯Â» ØªÙ‡ÛŒÙ‡ Ú©Ù†ÛŒØ¯."
            )
            return MAIN_MENU

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='missile_attack_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"ðŸŽ¯ Ù‡Ø¯Ù: *{target_country['name']}*\n\n"
            "ðŸš€ Ù„Ø·ÙØ§Ù‹ Ù†ÙˆØ¹ Ù…ÙˆØ´Ú© Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_SELECT_MISSILE
    except Exception as e:
        logger.error(f"Error in select_missile_target: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù")
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
            f"Ø´Ù…Ø§ {get_asset_display_name(missile_type)} Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ø±Ø¯ÛŒØ¯.\n"
            f"Ù…ÙˆØ¬ÙˆØ¯ÛŒ: {missile_count}\n"
            "Ù„Ø·ÙØ§Ù‹ ØªØ¹Ø¯Ø§Ø¯ Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ÛŒ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø¨Ø±Ø§ÛŒ Ø´Ù„ÛŒÚ© Ø±Ø§ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯:"
        )
        return MISSILE_ATTACK_GET_QUANTITY
    except Exception as e:
        logger.error(f"Error in select_missile_type: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù†ÙˆØ¹ Ù…ÙˆØ´Ú©")
        return MISSILE_ATTACK_SELECT_MISSILE


async def get_missile_quantity(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    country = get_country(user_id)
    if not country:
        await update.message.reply_text("âŒ Ú©Ø´ÙˆØ± Ø´Ù…Ø§ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return MAIN_MENU
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            await update.message.reply_text("ØªØ¹Ø¯Ø§Ø¯ Ø¨Ø§ÛŒØ¯ Ø¨Ø²Ø±Ú¯ØªØ± Ø§Ø² ØµÙØ± Ø¨Ø§Ø´Ø¯.")
            return MISSILE_ATTACK_GET_QUANTITY

        missile_type = context.user_data.get('missile_type')
        if not missile_type:
            await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù†ÙˆØ¹ Ù…ÙˆØ´Ú©. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU

        available = country.get('rockets', {}).get(missile_type, 0)
        if available < quantity:
            await update.message.reply_text(f"ØªØ¹Ø¯Ø§Ø¯ Ù…ÙˆØ´Ú©â€ŒÙ‡Ø§ÛŒ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù…ÙˆØ¬ÙˆØ¯ÛŒ: {available}")
            return MISSILE_ATTACK_GET_QUANTITY

        context.user_data['missile_quantity'] = quantity

        target_name = context.user_data.get('missile_target_name')
        missile_name = get_asset_display_name(missile_type)

        # Ù…Ø±Ø­Ù„Ù‡ Ø¬Ø¯ÛŒØ¯: Ø§Ù†ØªØ®Ø§Ø¨ Ù…Ù†Ø·Ù‚Ù‡ Ù‡Ø¯Ù
        keyboard = [
            [InlineKeyboardButton("ðŸ˜ï¸ Ù…Ù†Ø·Ù‚Ù‡ Ù…Ø³Ú©ÙˆÙ†ÛŒ", callback_data='missile_zone_residential')],
            [InlineKeyboardButton("ðŸª– Ù…Ù†Ø·Ù‚Ù‡ Ù†Ø¸Ø§Ù…ÛŒ", callback_data='missile_zone_military')],
            [InlineKeyboardButton("ðŸ­ Ù…Ù†Ø·Ù‚Ù‡ Ø§Ù‚ØªØµØ§Ø¯ÛŒ", callback_data='missile_zone_economic')],
            [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='missile_attack_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"ðŸš€ *{quantity} Ù…ÙˆØ´Ú© {missile_name}* Ø¨Ù‡ Ø³Ù…Øª *{target_name}*\n\n"
            "ðŸŽ¯ Ù„Ø·ÙØ§Ù‹ *Ù†ÙˆØ¹ Ù…Ù†Ø·Ù‚Ù‡ Ù‡Ø¯Ù* Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_SELECT_ZONE
    except ValueError:
        await update.message.reply_text("Ù„Ø·ÙØ§Ù‹ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ÙˆØ§Ø±Ø¯ Ú©Ù†ÛŒØ¯.")
        return MISSILE_ATTACK_GET_QUANTITY
    except Exception as e:
        logger.error(f"Error in get_missile_quantity: {e}", exc_info=True)
        await update.message.reply_text("Ø®Ø·Ø§ Ø¯Ø± Ù¾Ø±Ø¯Ø§Ø²Ø´ ØªØ¹Ø¯Ø§Ø¯ Ù…ÙˆØ´Ú©")
        return MISSILE_ATTACK_GET_QUANTITY


# --------- Ø«Ø§Ø¨Øªâ€ŒÙ‡Ø§ÛŒ Ù…Ù†Ø·Ù‚Ù‡ ---------
MISSILE_ZONE_LABELS = {
    'residential': 'ðŸ˜ï¸ Ù…Ù†Ø·Ù‚Ù‡ Ù…Ø³Ú©ÙˆÙ†ÛŒ',
    'military': 'ðŸª– Ù…Ù†Ø·Ù‚Ù‡ Ù†Ø¸Ø§Ù…ÛŒ',
    'economic': 'ðŸ­ Ù…Ù†Ø·Ù‚Ù‡ Ø§Ù‚ØªØµØ§Ø¯ÛŒ'
}


async def select_missile_zone(update: Update, context: CallbackContext) -> int:
    """Ø§Ù†ØªØ®Ø§Ø¨ Ù…Ù†Ø·Ù‚Ù‡ Ù‡Ø¯Ù Ù…ÙˆØ´Ú© Ùˆ Ù†Ù…Ø§ÛŒØ´ Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´ ØªØ£ÛŒÛŒØ¯ Ù†Ù‡Ø§ÛŒÛŒ."""
    query = update.callback_query
    await query.answer()
    try:
        zone_key = query.data.replace("missile_zone_", "")
        if zone_key not in MISSILE_ZONE_LABELS:
            await query.answer("Ù…Ù†Ø·Ù‚Ù‡ Ù†Ø§Ù…Ø¹ØªØ¨Ø± Ø§Ø³Øª", show_alert=True)
            return MISSILE_ATTACK_SELECT_ZONE
        context.user_data['missile_zone'] = zone_key

        target_name = context.user_data.get('missile_target_name', '')
        missile_type = context.user_data.get('missile_type')
        missile_name = get_asset_display_name(missile_type) if missile_type else ''
        quantity = context.user_data.get('missile_quantity', 0)
        zone_label = MISSILE_ZONE_LABELS[zone_key]

        keyboard = [
            [InlineKeyboardButton("âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø´Ù„ÛŒÚ©", callback_data='confirm_missile_attack')],
            [InlineKeyboardButton("ðŸ”™ ØªØºÛŒÛŒØ± Ù…Ù†Ø·Ù‚Ù‡", callback_data='missile_change_zone')],
            [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='missile_attack_menu')]
        ]
        await query.edit_message_text(
            f"ðŸš€ *Ù¾ÛŒØ´â€ŒÙ†Ù…Ø§ÛŒØ´ Ø­Ù…Ù„Ù‡ Ù…ÙˆØ´Ú©ÛŒ*\n"
            f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
            f"ðŸŽ¯ Ú©Ø´ÙˆØ± Ù‡Ø¯Ù: *{target_name}*\n"
            f"ðŸ’£ Ù†ÙˆØ¹ Ù…ÙˆØ´Ú©: *{missile_name}*\n"
            f"ðŸ”¢ ØªØ¹Ø¯Ø§Ø¯: *{quantity}*\n"
            f"ðŸ—ºï¸ Ù…Ù†Ø·Ù‚Ù‡ Ù‡Ø¯Ù: *{zone_label}*\n"
            f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\n"
            f"Ø¢ÛŒØ§ Ù…Ø·Ù…Ø¦Ù†ÛŒØ¯ØŸ",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return MISSILE_ATTACK_CONFIRM
    except Exception as e:
        logger.error(f"Error in select_missile_zone: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù…Ù†Ø·Ù‚Ù‡ Ù‡Ø¯Ù.")
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
    
async def refinery_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country.get('refinery_level', 0)
        daily_income = current_level * 25

        keyboard = [
            [InlineKeyboardButton(f"Ø§Ø±ØªÙ‚Ø§Ø¡ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ (Ø³Ø·Ø­ ÙØ¹Ù„ÛŒ: {current_level})", callback_data='upgrade_refinery')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='country_management')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"ðŸ›¢ï¸ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ù†ÙØª:\nØ³Ø·Ø­ ÙØ¹Ù„ÛŒ: {current_level}\nØ¯Ø±Ø¢Ù…Ø¯ Ø±ÙˆØ²Ø§Ù†Ù‡: +{daily_income}\n\n"
            "Ù‡Ø± Ø³Ø·Ø­ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ 25 ÙˆØ§Ø­Ø¯ Ø¨Ù‡ Ø¯Ø±Ø¢Ù…Ø¯ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒÚ©Ù†Ø¯.",
            reply_markup=reply_markup
        )
        return REFINERY_MENU
    except Exception as e:
        logger.error(f"Error in refinery_menu: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡")
        return COUNTRY_MANAGEMENT


async def upgrade_refinery(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        user_id = query.from_user.id
        country = get_country(user_id)
        current_level = country.get('refinery_level', 0)

        if current_level >= 7:
            await query.answer("Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ø´Ù…Ø§ Ø¯Ø± Ø¨Ø§Ù„Ø§ØªØ±ÛŒÙ† Ø³Ø·Ø­ (7) Ø§Ø³Øª!", show_alert=True)
            return REFINERY_MENU

        next_level = current_level + 1
        price = ASSET_PRICES[f'refinery_upgrade_level{next_level}']

        if country['capital'] < price:
            await query.answer(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ù‚ÛŒÙ…Øª Ø§Ø±ØªÙ‚Ø§Ø¡: {price:,}", show_alert=True)
            return REFINERY_MENU

        new_capital = country['capital'] - price
        update_country(user_id, {
            'capital': new_capital,
            'refinery_level': next_level
        })

        upgrade_message = (
            f"ðŸ›¢ï¸ Ú©Ø´ÙˆØ± {country['name']} Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ù†ÙØª Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù‡ Ø³Ø·Ø­ {next_level} Ø§Ø±ØªÙ‚Ø§Ø¡ Ø¯Ø§Ø¯!\n\n"
            f"ðŸ’° Ù‡Ø²ÛŒÙ†Ù‡ Ø§Ø±ØªÙ‚Ø§Ø¡: {price:,}\n"
            f"ðŸ’¹ Ø¯Ø±Ø¢Ù…Ø¯ Ø±ÙˆØ²Ø§Ù†Ù‡ Ø¬Ø¯ÛŒØ¯: +{next_level * 25}"
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

        await query.answer(f"âœ… Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡ Ø¨Ù‡ Ø³Ø·Ø­ {next_level} Ø§Ø±ØªÙ‚Ø§Ø¡ ÛŒØ§ÙØª!", show_alert=True)
        return await refinery_menu(update, context)
    except Exception as e:
        logger.error(f"Error in upgrade_refinery: {e}", exc_info=True)
        await query.answer("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø±ØªÙ‚Ø§Ø¡ Ù¾Ø§Ù„Ø§ÛŒØ´Ú¯Ø§Ù‡", show_alert=True)
        return REFINERY_MENU


async def construction_proposal_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        keyboard = [
            [InlineKeyboardButton("ÙÛŒÙ„Ù… ðŸŽ¬", callback_data='construction_film')],
            [InlineKeyboardButton("Ø¨Ø§Ø²ÛŒ ðŸŽ®", callback_data='construction_game')],
            [InlineKeyboardButton("Ù…ÙˆØ³ÛŒÙ‚ÛŒ ðŸŽµ", callback_data='construction_music')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "ðŸ—ï¸ Ù„Ø·ÙØ§Ù‹ Ù†ÙˆØ¹ Ù¾Ø±ÙˆÚ˜Ù‡ Ø³Ø§Ø®Øª Ùˆ Ø³Ø§Ø² Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_CATEGORY
    except Exception as e:
        logger.error(f"Error in construction_proposal_start: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù…Ù†ÙˆÛŒ Ø³Ø§Ø®Øª Ùˆ Ø³Ø§Ø²")
        return MAIN_MENU


async def select_construction_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        category = query.data.replace('construction_', '')
        context.user_data['construction_category'] = category

        projects = CONSTRUCTION_PROJECTS.get(category, {})
        if not projects:
            await query.edit_message_text("âŒ Ù¾Ø±ÙˆÚ˜Ù‡â€ŒØ§ÛŒ Ø¯Ø± Ø§ÛŒÙ† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return CONSTRUCTION_CATEGORY

        keyboard = []
        for project_id, project in projects.items():
            keyboard.append([InlineKeyboardButton(
                f"{project['name']} - Ù‡Ø²ÛŒÙ†Ù‡: {project['cost']:,}",
                callback_data=f"select_project_{project_id}"
            )])

        keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='construction_proposal_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"Ù¾Ø±ÙˆÚ˜Ù‡â€ŒÙ‡Ø§ÛŒ {category}:\nÙ„Ø·ÙØ§Ù‹ Ù¾Ø±ÙˆÚ˜Ù‡ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_SELECT_PROJECT
    except Exception as e:
        logger.error(f"Error in select_construction_category: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ù†Ù…Ø§ÛŒØ´ Ù¾Ø±ÙˆÚ˜Ù‡â€ŒÙ‡Ø§")
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
            await query.edit_message_text("âŒ Ù¾Ø±ÙˆÚ˜Ù‡ Ù…ÙˆØ±Ø¯ Ù†Ø¸Ø± ÛŒØ§ÙØª Ù†Ø´Ø¯.")
            return CONSTRUCTION_SELECT_PROJECT

        context.user_data['construction_project'] = project

        keyboard = [
            [InlineKeyboardButton("âœ… ØªØ£ÛŒÛŒØ¯ Ùˆ Ø³Ø§Ø®Øª", callback_data='confirm_construction')],
            [InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data=f'construction_{category}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"ðŸ—ï¸ Ù¾Ø±ÙˆÚ˜Ù‡: {project['name']}\n"
            f"ðŸ“ ØªÙˆØ¶ÛŒØ­Ø§Øª: {project['description']}\n"
            f"ðŸ’° Ù‡Ø²ÛŒÙ†Ù‡: {project['cost']:,}\n"
            f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {project['daily_income']:,}\n\n"
            "Ø¢ÛŒØ§ Ù…Ø§ÛŒÙ„ Ø¨Ù‡ Ø³Ø§Ø®Øª Ø§ÛŒÙ† Ù¾Ø±ÙˆÚ˜Ù‡ Ù‡Ø³ØªÛŒØ¯ØŸ",
            reply_markup=reply_markup
        )
        return CONSTRUCTION_CONFIRM
    except Exception as e:
        logger.error(f"Error in select_construction_project: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ù†ØªØ®Ø§Ø¨ Ù¾Ø±ÙˆÚ˜Ù‡")
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
            await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ù¾Ø±ÙˆÚ˜Ù‡. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯.")
            return MAIN_MENU

        if country['capital'] < project['cost']:
            await query.answer(f"Ø³Ø±Ù…Ø§ÛŒÙ‡ Ø´Ù…Ø§ Ú©Ø§ÙÛŒ Ù†ÛŒØ³Øª! Ø³Ø±Ù…Ø§ÛŒÙ‡ Ù…ÙˆØ±Ø¯ Ù†ÛŒØ§Ø²: {project['cost']:,}", show_alert=True)
            return CONSTRUCTION_CONFIRM

        new_capital = country['capital'] - project['cost']
        new_daily_income = country['daily_income'] + project['daily_income']

        update_country(user_id, {
            'capital': new_capital,
            'daily_income': new_daily_income
        })

        message_templates = {
            'film': (
                f"ðŸŽ¬ ÛŒÚ© ÙÛŒÙ„Ù… Ø¬Ø¯ÛŒØ¯ ØªÙˆØ³Ø· Ú©Ø´ÙˆØ± {country['name']} Ø³Ø§Ø®ØªÙ‡ Ø´Ø¯!\n\n"
                f"ðŸ“½ ÙÛŒÙ„Ù…: {project['name']}\n"
                f"ðŸ“ ØªÙˆØ¶ÛŒØ­Ø§Øª: {project['description']}\n\n"
                f"ðŸ’° Ø¨ÙˆØ¯Ø¬Ù‡: {project['cost']:,}\n"
                f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {project['daily_income']:,}"
            ),
            'game': (
                f"ðŸŽ® ÛŒÚ© Ø¨Ø§Ø²ÛŒ Ø¬Ø¯ÛŒØ¯ ØªÙˆØ³Ø· Ú©Ø´ÙˆØ± {country['name']} Ø³Ø§Ø®ØªÙ‡ Ø´Ø¯!\n\n"
                f"ðŸ•¹ Ø¨Ø§Ø²ÛŒ: {project['name']}\n"
                f"ðŸ“ ØªÙˆØ¶ÛŒØ­Ø§Øª: {project['description']}\n\n"
                f"ðŸ’° Ø¨ÙˆØ¯Ø¬Ù‡: {project['cost']:,}\n"
                f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {project['daily_income']:,}"
            ),
            'music': (
                f"ðŸŽµ ÛŒÚ© Ø¢Ù„Ø¨ÙˆÙ… Ù…ÙˆØ³ÛŒÙ‚ÛŒ Ø¬Ø¯ÛŒØ¯ ØªÙˆØ³Ø· Ú©Ø´ÙˆØ± {country['name']} Ø³Ø§Ø®ØªÙ‡ Ø´Ø¯!\n\n"
                f"ðŸŽ¶ Ø¢Ù„Ø¨ÙˆÙ…: {project['name']}\n"
                f"ðŸ“ ØªÙˆØ¶ÛŒØ­Ø§Øª: {project['description']}\n\n"
                f"ðŸ’° Ø¨ÙˆØ¯Ø¬Ù‡: {project['cost']:,}\n"
                f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {project['daily_income']:,}"
            )
        }

        announcement = message_templates.get(category, "")
        if not announcement:
            announcement = (
                f"ðŸ—ï¸ ÛŒÚ© Ù¾Ø±ÙˆÚ˜Ù‡ Ø¬Ø¯ÛŒØ¯ ØªÙˆØ³Ø· Ú©Ø´ÙˆØ± {country['name']} Ø³Ø§Ø®ØªÙ‡ Ø´Ø¯!\n\n"
                f"ðŸ“Œ Ù†Ø§Ù…: {project['name']}\n"
                f"ðŸ“ ØªÙˆØ¶ÛŒØ­Ø§Øª: {project['description']}\n\n"
                f"ðŸ’° Ø¨ÙˆØ¯Ø¬Ù‡: {project['cost']:,}\n"
                f"ðŸ’¹ Ø³ÙˆØ¯ Ø±ÙˆØ²Ø§Ù†Ù‡: {project['daily_income']:,}"
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

        await query.edit_message_text(f"âœ… Ù¾Ø±ÙˆÚ˜Ù‡ {project['name']} Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø³Ø§Ø®ØªÙ‡ Ø´Ø¯!")
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Error in confirm_construction: {e}", exc_info=True)
        await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø³Ø§Ø®Øª Ù¾Ø±ÙˆÚ˜Ù‡")
        return CONSTRUCTION_CONFIRM


async def announce_top_oil(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT name, oil_barrels FROM countries ORDER BY oil_barrels DESC LIMIT 5")
        top_countries = c.fetchall()
        conn.close()

        if not top_countries:
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU

        message = "ðŸ›¢ï¸ Ú©Ø´ÙˆØ±Ù‡Ø§ÛŒ Ø¨Ø±ØªØ± Ø§Ø² Ù†Ø¸Ø± Ø°Ø®Ø§ÛŒØ± Ù†ÙØªÛŒ:\n\n"
        for i, (name, oil) in enumerate(top_countries, 1):
            message += f"{i}. {name}: {oil:,} Ø¨Ø´Ú©Ù‡\n"

        photo_id = get_notification_image('top_oil')
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

        await query.edit_message_text("âœ… Ù„ÛŒØ³Øª Ø¨Ø±ØªØ±ÛŒÙ†â€ŒÙ‡Ø§ÛŒ Ù†ÙØª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø§Ø¹Ù„Ø§Ù… Ø´Ø¯.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in announce_top_oil: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø¹Ù„Ø§Ù… Ø¨Ø±ØªØ±ÛŒÙ†â€ŒÙ‡Ø§ÛŒ Ù†ÙØª")
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
            await query.edit_message_text("Ù‡ÛŒÚ† Ú©Ø´ÙˆØ±ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…Ø§ÛŒØ´ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.")
            return ADMIN_MENU

        message = "ðŸ˜Š Ú©Ø´ÙˆØ±Ù‡Ø§ÛŒ Ø¨Ø±ØªØ± Ø§Ø² Ù†Ø¸Ø± Ø±Ø¶Ø§ÛŒØª Ù…Ø±Ø¯Ù…ÛŒ:\n\n"
        for i, (name, satisfaction) in enumerate(top_countries, 1):
            message += f"{i}. {name}: {satisfaction}%\n"

        photo_id = get_notification_image('top_satisfaction')
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

        await query.edit_message_text("âœ… Ù„ÛŒØ³Øª Ø¨Ø±ØªØ±ÛŒÙ†â€ŒÙ‡Ø§ÛŒ Ø±Ø¶Ø§ÛŒØª Ø¯Ø± Ú©Ø§Ù†Ø§Ù„ Ø§Ø¹Ù„Ø§Ù… Ø´Ø¯.")
        return ADMIN_MENU
    except Exception as e:
        logger.error(f"Error in announce_top_satisfaction: {e}", exc_info=True)
        await query.edit_message_text("Ø®Ø·Ø§ Ø¯Ø± Ø§Ø¹Ù„Ø§Ù… Ø¨Ø±ØªØ±ÛŒÙ†â€ŒÙ‡Ø§ÛŒ Ø±Ø¶Ø§ÛŒØª")
        return ADMIN_MENU


# ========================== Ù…Ø¯ÛŒØ±ÛŒØª Ù¾ÙˆÛŒØ§ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª (UI) ==========================

async def equip_manage_entry(update: Update, context: CallbackContext) -> int:
    """ÙˆØ±ÙˆØ¯ÛŒ Ù¾ÛŒØ§Ù…ÛŒ: 'Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª' Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ."""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§/Ù…Ø§Ù„Ú© Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    return await show_equipment_manage_menu(update, context)


async def show_equipment_manage_menu(update: Update, context: CallbackContext) -> int:
    """Ù†Ù…Ø§ÛŒØ´ Ù„ÛŒØ³Øª Ù‡Ù…Ù‡ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ + Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ÛŒ Ø§ÙØ²ÙˆØ¯Ù†/Ø³ÛŒÙˆ/Ù„ÛŒØ³Øªâ€ŒÙ‡Ø§."""
    items = get_all_equipment_items()
    cats = get_all_equipment_categories()
    cat_map = {c[0]: c[1] for c in cats}

    text_lines = ["ðŸ› ï¸ *Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª*\n"]
    if not items:
        text_lines.append("Ù‡ÛŒÚ† ØªØ¬Ù‡ÛŒØ²ÛŒ Ø«Ø¨Øª Ù†Ø´Ø¯Ù‡ Ø§Ø³Øª.")
    else:
        # Ú¯Ø±ÙˆÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¨Ø± Ø§Ø³Ø§Ø³ Ø¯Ø³ØªÙ‡
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
                    f"`{it['item_id']}` â€¢ {it['display_name']} â€” Ù‚ÛŒÙ…Øª: {it['price']:,}"
                )
        # Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§ÛŒÛŒ Ú©Ù‡ Ø¯Ø³ØªÙ‡â€ŒØ´ÙˆÙ† Ø¯Ø± Ø¬Ø¯ÙˆÙ„ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ù†ÛŒØ³Øª
        orphan_cats = [c for c in by_cat.keys() if c not in cat_map]
        for cat_key in orphan_cats:
            text_lines.append(f"\n*Ø¯Ø³ØªÙ‡ Ù†Ø§Ù…Ø´Ø®Øµ ({cat_key})*")
            for it in by_cat[cat_key]:
                text_lines.append(
                    f"`{it['item_id']}` â€¢ {it['display_name']} â€” Ù‚ÛŒÙ…Øª: {it['price']:,}"
                )

    text_lines.append("\n\nØ¨Ø±Ø§ÛŒ Ø­Ø°ÙØŒ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ ØªØ¬Ù‡ÛŒØ² Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.")
    message_text = "\n".join(text_lines)

    keyboard = [
        [InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† ØªØ¬Ù‡ÛŒØ²", callback_data='equip_add_start')],
        [InlineKeyboardButton("ðŸ’¾ Ø°Ø®ÛŒØ±Ù‡ (Ø³ÛŒÙˆ) Ù„ÛŒØ³Øª", callback_data='equip_preset_save_start')],
        [InlineKeyboardButton("ðŸ“‚ Ù„ÛŒØ³Øªâ€ŒÙ‡Ø§ÛŒ Ø°Ø®ÛŒØ±Ù‡â€ŒØ´Ø¯Ù‡", callback_data='equip_preset_menu')],
        [InlineKeyboardButton("ðŸ†• Ø³Ø§Ø®Øª Ù„ÛŒØ³Øª Ø¬Ø¯ÛŒØ¯ (Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ)", callback_data='equip_new_list_start')],
        [InlineKeyboardButton("ðŸ—‚ï¸ Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§", callback_data='equip_category_menu')],
        [InlineKeyboardButton("âŒ Ø¨Ø³ØªÙ†", callback_data='equip_close')]
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
        # Ø§Ø­ØªÙ…Ø§Ù„ Ø®Ø·Ø§ÛŒ Ø·ÙˆÙ„ Ù¾ÛŒØ§Ù…: Ø³Ø§Ø¯Ù‡â€ŒØªØ± Ø¨ÙØ±Ø³Øª
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "ðŸ› ï¸ Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª\n\n(Ù„ÛŒØ³Øª Ø®ÛŒÙ„ÛŒ Ø·ÙˆÙ„Ø§Ù†ÛŒÙ‡Ø› Ø§Ø² Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯)",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "ðŸ› ï¸ Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª\n\n(Ù„ÛŒØ³Øª Ø®ÛŒÙ„ÛŒ Ø·ÙˆÙ„Ø§Ù†ÛŒÙ‡Ø› Ø§Ø² Ø¯Ú©Ù…Ù‡â€ŒÙ‡Ø§ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ú©Ù†ÛŒØ¯)",
                reply_markup=reply_markup
            )
    return EQUIP_MANAGE_MENU


async def equip_delete_by_text(update: Update, context: CallbackContext) -> int:
    """Ø­Ø°Ù ØªØ¬Ù‡ÛŒØ² Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ (Ù¾ÛŒØ§Ù… Ù…ØªÙ†ÛŒ Ø¯Ø± Ø­Ø§Ù„Øª Ù…Ø¯ÛŒØ±ÛŒØª)."""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("â›”ï¸ ÙÙ‚Ø· Ø§Ø¯Ù…ÛŒÙ†â€ŒÙ‡Ø§ Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø±Ù†Ø¯!")
        return ConversationHandler.END
    text = (update.message.text or "").strip()
    if not text.isdigit():
        await update.message.reply_text(
            "âŒ Ù„Ø·ÙØ§Ù‹ ÙÙ‚Ø· ÛŒÚ© Ø¹Ø¯Ø¯ (Ø¢ÛŒØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²) Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯. Ø¨Ø±Ø§ÛŒ Ø®Ø±ÙˆØ¬ Ø§Ø² Ù…Ù†Ùˆ Ø¯Ú©Ù…Ù‡ âŒ Ø¨Ø³ØªÙ† Ø±Ø§ Ø¨Ø²Ù†ÛŒØ¯."
        )
        return EQUIP_MANAGE_MENU
    item_id = int(text)
    item = get_equipment_item_by_id(item_id)
    if not item:
        await update.message.reply_text(f"âŒ ØªØ¬Ù‡ÛŒØ²ÛŒ Ø¨Ø§ Ø¢ÛŒØ¯ÛŒ {item_id} ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return EQUIP_MANAGE_MENU
    ok = delete_equipment_item(item_id)
    if ok:
        await update.message.reply_text(
            f"âœ… ØªØ¬Ù‡ÛŒØ² Â«{item['display_name']}Â» (Ø¢ÛŒØ¯ÛŒ {item_id}) Ø­Ø°Ù Ø´Ø¯."
        )
    else:
        await update.message.reply_text("âŒ Ø­Ø°Ù Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯.")
    return await show_equipment_manage_menu(update, context)


# ---- Ø§ÙØ²ÙˆØ¯Ù† ØªØ¬Ù‡ÛŒØ² ----

async def equip_add_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['equip_new'] = {}
    await query.edit_message_text(
        "âž• Ø§ÙØ²ÙˆØ¯Ù† ØªØ¬Ù‡ÛŒØ² Ø¬Ø¯ÛŒØ¯\n\n"
        "Ù„Ø·ÙØ§Ù‹ *Ù†Ø§Ù… Ù†Ù…Ø§ÛŒØ´ÛŒ* ØªØ¬Ù‡ÛŒØ² Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ (Ù…Ø«Ù„Ø§Ù‹: Â«ØªØ§Ù†Ú© T-14Â»):",
        parse_mode="Markdown"
    )
    return EQUIP_ADD_GET_NAME


async def equip_add_get_name(update: Update, context: CallbackContext) -> int:
    name = (update.message.text or "").strip()
    if not name:
        await update.message.reply_text("âŒ Ù†Ø§Ù… Ù†Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ø¯ Ø®Ø§Ù„ÛŒ Ø¨Ø§Ø´Ø¯. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:")
        return EQUIP_ADD_GET_NAME
    context.user_data.setdefault('equip_new', {})['display_name'] = name
    await update.message.reply_text(
        f"âœ… Ù†Ø§Ù… Ø«Ø¨Øª Ø´Ø¯: {name}\n\n"
        "Ø­Ø§Ù„Ø§ *Ù‚ÛŒÙ…Øª* (Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ØŒ Ù…Ø«Ù„Ø§Ù‹ 50000) Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:",
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
        await update.message.reply_text("âŒ Ù‚ÛŒÙ…Øª Ø¨Ø§ÛŒØ¯ ÛŒÚ© Ø¹Ø¯Ø¯ ØµØ­ÛŒØ­ ØºÛŒØ±Ù…Ù†ÙÛŒ Ø¨Ø§Ø´Ø¯. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯:")
        return EQUIP_ADD_GET_PRICE
    context.user_data.setdefault('equip_new', {})['price'] = price

    # Ù†Ù…Ø§ÛŒØ´ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§
    cats = get_all_equipment_categories()
    keyboard = []
    for cat_key, cat_disp in cats:
        keyboard.append([InlineKeyboardButton(cat_disp, callback_data=f"equip_pick_cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("âž• Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¬Ø¯ÛŒØ¯", callback_data='equip_new_cat')])
    keyboard.append([InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='equip_back_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"âœ… Ù‚ÛŒÙ…Øª Ø«Ø¨Øª Ø´Ø¯: {price:,}\n\n"
        "Ù„Ø·ÙØ§Ù‹ *Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ* ØªØ¬Ù‡ÛŒØ² Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
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
        await query.edit_message_text("âŒ Ø®Ø·Ø§ Ø¯Ø± Ø¯Ø§Ø¯Ù‡â€ŒÙ‡Ø§. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø§Ø² Ù…Ù†Ùˆ Ø´Ø±ÙˆØ¹ Ú©Ù†ÛŒØ¯.")
        return await show_equipment_manage_menu(update, context)

    # Ø³Ø§Ø®Øª item_key ÛŒÚ©ØªØ§ Ø§Ø² Ø±ÙˆÛŒ Ù†Ø§Ù…
    item_key = _make_unique_item_key(display_name)
    new_id = add_equipment_item(item_key, display_name, cat_key, price)
    if not new_id:
        await query.edit_message_text(
            f"âŒ Ø§ÙØ²ÙˆØ¯Ù† Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯ (Ø§Ø­ØªÙ…Ø§Ù„Ø§Ù‹ Ú©Ù„ÛŒØ¯ ØªÚ©Ø±Ø§Ø±ÛŒ Ø§Ø³Øª: {item_key})."
        )
    else:
        await query.edit_message_text(
            f"âœ… ØªØ¬Ù‡ÛŒØ² Ø¬Ø¯ÛŒØ¯ Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯:\n"
            f"â€¢ Ø¢ÛŒØ¯ÛŒ: `{new_id}`\n"
            f"â€¢ Ù†Ø§Ù…: {display_name}\n"
            f"â€¢ Ú©Ù„ÛŒØ¯ Ø¯Ø§Ø®Ù„ÛŒ: `{item_key}`\n"
            f"â€¢ Ø¯Ø³ØªÙ‡: {cat_key}\n"
            f"â€¢ Ù‚ÛŒÙ…Øª: {price:,}",
            parse_mode="Markdown"
        )
    context.user_data.pop('equip_new', None)
    return await show_equipment_manage_menu(update, context)


def _make_unique_item_key(display_name):
    """Ø³Ø§Ø®Øª Ú©Ù„ÛŒØ¯ ÛŒÚ©ØªØ§ Ø§Ø² Ø±ÙˆÛŒ Ù†Ø§Ù… Ù†Ù…Ø§ÛŒØ´ÛŒ (Ø§Ù†Ú¯Ù„ÛŒØ³ÛŒ-Ø³Ø§Ø²ÛŒ Ø³Ø§Ø¯Ù‡ + Ø´Ù…Ø§Ø±Ù†Ø¯Ù‡)."""
    # Ø¨Ø±Ø¯Ø§Ø´ØªÙ† Ú©Ø§Ø±Ø§Ú©ØªØ±Ù‡Ø§ÛŒ ØºÛŒØ±Ù„Ø§ØªÛŒÙ†/ØºÛŒØ± Ø¹Ø¯Ø¯ÛŒ
    base = re.sub(r'[^a-zA-Z0-9]+', '_', display_name).strip('_').lower()
    if not base:
        base = "item"
    candidate = base
    counter = 1
    existing = {it['item_key'] for it in get_all_equipment_items()}
    # Ù‡Ù…ÛŒÙ†Ø·ÙˆØ± Ø¨Ø§ÛŒØ¯ Ø¨Ø§ Ú©Ù„ÛŒØ¯Ù‡Ø§ÛŒ Ø«Ø§Ø¨Øª Ù¾ÛŒØ´â€ŒÙØ±Ø¶ Ù‡Ù… ØªØ¯Ø§Ø®Ù„ Ù†Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù‡
    existing |= set(ASSET_NAMES.keys())
    while candidate in existing:
        counter += 1
        candidate = f"{base}_{counter}"
    return candidate


async def equip_new_category_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¬Ø¯ÛŒØ¯\n\n"
        "Ù†Ø§Ù… Ù†Ù…Ø§ÛŒØ´ÛŒ Ø¯Ø³ØªÙ‡ Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯ (Ù…Ø«Ù„Ø§Ù‹: Â«Ù†ÛŒØ±ÙˆÙ‡Ø§ÛŒ ÙØ¶Ø§ÛŒÛŒ ðŸš€Â»):"
    )
    return EQUIP_NEW_CATEGORY_NAME


async def equip_new_category_save(update: Update, context: CallbackContext) -> int:
    display_name = (update.message.text or "").strip()
    if not display_name:
        await update.message.reply_text("âŒ Ù†Ø§Ù… Ø®Ø§Ù„ÛŒ Ø§Ø³Øª. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø¨ÙØ±Ø³ØªÛŒØ¯:")
        return EQUIP_NEW_CATEGORY_NAME
    # Ø³Ø§Ø®Øª cat_key ÛŒÚ©ØªØ§
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
            f"âœ… Ø¯Ø³ØªÙ‡ Â«{display_name}Â» Ø§Ø¶Ø§ÙÙ‡ Ø´Ø¯ (Ú©Ù„ÛŒØ¯: `{candidate}`)",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("âŒ Ø§ÙØ²ÙˆØ¯Ù† Ø¯Ø³ØªÙ‡ Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯.")
    # Ø¨Ø±Ú¯Ø´Øª Ø¨Ù‡ Ø§ÙØ²ÙˆØ¯Ù† ØªØ¬Ù‡ÛŒØ² ÛŒØ§ Ù…Ù†Ùˆ
    if context.user_data.get('equip_new'):
        # Ú©Ø§Ø±Ø¨Ø± Ø¯Ø± Ù…ÛŒØ§Ù†Ù‡ Ø§ÙØ²ÙˆØ¯Ù† ØªØ¬Ù‡ÛŒØ² Ø¨ÙˆØ¯
        cats = get_all_equipment_categories()
        keyboard = []
        for cat_key, cat_disp in cats:
            keyboard.append([InlineKeyboardButton(cat_disp, callback_data=f"equip_pick_cat_{cat_key}")])
        keyboard.append([InlineKeyboardButton("âž• Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¬Ø¯ÛŒØ¯", callback_data='equip_new_cat')])
        keyboard.append([InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='equip_back_menu')])
        await update.message.reply_text(
            "Ø§Ú©Ù†ÙˆÙ† Ø¯Ø³ØªÙ‡ ØªØ¬Ù‡ÛŒØ² Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return EQUIP_ADD_GET_CATEGORY
    return await show_equipment_manage_menu(update, context)


# ---- Ù…Ù†ÙˆÛŒ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ (Ù…Ø¯ÛŒØ±ÛŒØª) ----

async def equip_category_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    cats = get_all_equipment_categories()
    text = "ðŸ—‚ï¸ *Ù…Ø¯ÛŒØ±ÛŒØª Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§*\n\nØ¨Ø±Ø§ÛŒ Ø­Ø°Ù ÛŒÚ© Ø¯Ø³ØªÙ‡ØŒ Ø±ÙˆÛŒ Ø¢Ù† Ú©Ù„ÛŒÚ© Ú©Ù†ÛŒØ¯ (ØªÙ…Ø§Ù… ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø¢Ù† Ø¯Ø³ØªÙ‡ Ù†ÛŒØ² Ø­Ø°Ù Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯):"
    keyboard = []
    for cat_key, cat_disp in cats:
        keyboard.append([InlineKeyboardButton(f"ðŸ—‘ï¸ {cat_disp}", callback_data=f"equip_del_cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("âž• Ø§ÙØ²ÙˆØ¯Ù† Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒ Ø¬Ø¯ÛŒØ¯", callback_data='equip_new_cat')])
    keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='equip_back_menu')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_delete_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    cat_key = query.data.replace("equip_del_cat_", "")
    delete_equipment_category(cat_key)
    await query.answer(f"Ø¯Ø³ØªÙ‡ Â«{cat_key}Â» Ø­Ø°Ù Ø´Ø¯", show_alert=True)
    return await show_equipment_manage_menu(update, context)


# ---- Ù¾Ø±ÛŒØ³Øªâ€ŒÙ‡Ø§ ----

async def equip_preset_save_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "ðŸ’¾ *Ø°Ø®ÛŒØ±Ù‡ Ù„ÛŒØ³Øª ØªØ¬Ù‡ÛŒØ²Ø§Øª*\n\n"
        "ÛŒÚ© Ù†Ø§Ù… Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ù„ÛŒØ³Øª Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯ (Ù…Ø«Ù„Ø§Ù‹: Â«Ø¬Ù†Ú¯ Ø¬Ù‡Ø§Ù†ÛŒ 2Â»):",
        parse_mode="Markdown"
    )
    return EQUIP_PRESET_SAVE_NAME


async def equip_preset_save(update: Update, context: CallbackContext) -> int:
    name = (update.message.text or "").strip()
    if not name:
        await update.message.reply_text("âŒ Ù†Ø§Ù… Ø®Ø§Ù„ÛŒ Ø§Ø³Øª. Ø¯ÙˆØ¨Ø§Ø±Ù‡ Ø¨ÙØ±Ø³ØªÛŒØ¯:")
        return EQUIP_PRESET_SAVE_NAME
    ok = save_equipment_preset(name)
    if ok:
        await update.message.reply_text(f"âœ… Ù„ÛŒØ³Øª Ø¨Ø§ Ù†Ø§Ù… Â«{name}Â» Ø°Ø®ÛŒØ±Ù‡ Ø´Ø¯.")
    else:
        await update.message.reply_text("âŒ Ø°Ø®ÛŒØ±Ù‡â€ŒØ³Ø§Ø²ÛŒ Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯.")
    return await show_equipment_manage_menu(update, context)


async def equip_preset_menu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    presets = get_all_equipment_presets()
    text = "ðŸ“‚ *Ù„ÛŒØ³Øªâ€ŒÙ‡Ø§ÛŒ Ø°Ø®ÛŒØ±Ù‡â€ŒØ´Ø¯Ù‡ ØªØ¬Ù‡ÛŒØ²Ø§Øª*\n\n"
    if not presets:
        text += "Ù‡ÛŒÚ† Ù„ÛŒØ³Øª Ø°Ø®ÛŒØ±Ù‡â€ŒØ´Ø¯Ù‡â€ŒØ§ÛŒ Ù†Ø¯Ø§Ø±ÛŒØ¯."
    else:
        for p in presets:
            text += f"â€¢ `{p['preset_id']}` â€” {p['preset_name']}\n"
        text += "\nØ¨Ø±Ø§ÛŒ Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ ÛŒØ§ Ø­Ø°ÙØŒ Ø±ÙˆÛŒ Ù†Ø§Ù… Ú©Ù„ÛŒÚ© Ú©Ù†ÛŒØ¯."
    keyboard = []
    for p in presets:
        keyboard.append([
            InlineKeyboardButton(f"ðŸ“¥ {p['preset_name']}", callback_data=f"equip_preset_load_{p['preset_id']}"),
            InlineKeyboardButton("ðŸ—‘ï¸", callback_data=f"equip_preset_del_{p['preset_id']}")
        ])
    keyboard.append([InlineKeyboardButton("ðŸ”™ Ø¨Ø§Ø²Ú¯Ø´Øª", callback_data='equip_back_menu')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_preset_delete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = int(query.data.replace("equip_preset_del_", ""))
    delete_equipment_preset(preset_id)
    await query.answer("Ù„ÛŒØ³Øª Ø­Ø°Ù Ø´Ø¯", show_alert=True)
    return await equip_preset_menu(update, context)


async def equip_preset_load_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = int(query.data.replace("equip_preset_load_", ""))
    preset = get_equipment_preset(preset_id)
    if not preset:
        await query.edit_message_text("âŒ Ù„ÛŒØ³Øª ÛŒØ§ÙØª Ù†Ø´Ø¯.")
        return await show_equipment_manage_menu(update, context)
    context.user_data['preset_to_load'] = preset_id
    text = (
        f"ðŸ“¥ Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ù„ÛŒØ³Øª: *{preset['preset_name']}*\n\n"
        f"ØªØ¹Ø¯Ø§Ø¯ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§: {len(preset['data'].get('categories', []))}\n"
        f"ØªØ¹Ø¯Ø§Ø¯ ØªØ¬Ù‡ÛŒØ²Ø§Øª: {len(preset['data'].get('items', []))}\n\n"
        "Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ú©Ø´ÙˆØ±Ù‡Ø§ÛŒ Ù…ÙˆØ¬ÙˆØ¯ Ú†Ù‡ Ø´ÙˆØ¯ØŸ"
    )
    keyboard = [
        [InlineKeyboardButton("âœ… Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ Ø­ÙØ¸ Ø´ÙˆØ¯", callback_data='equip_preset_load_keep')],
        [InlineKeyboardButton("ðŸ”„ Ù…ÙˆØ¬ÙˆØ¯ÛŒ Ù‡Ù…Ù‡ Ú©Ø´ÙˆØ±Ù‡Ø§ ØµÙØ± Ø´ÙˆØ¯", callback_data='equip_preset_load_reset')],
        [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='equip_preset_menu')]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_PRESET_LOAD_CONFIRM


async def equip_preset_load_apply(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    preset_id = context.user_data.get('preset_to_load')
    if not preset_id:
        await query.edit_message_text("âŒ Ø®Ø·Ø§: Ù„ÛŒØ³ØªÛŒ Ø¨Ø±Ø§ÛŒ Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ø§Ù†ØªØ®Ø§Ø¨ Ù†Ø´Ø¯Ù‡ Ø§Ø³Øª.")
        return await show_equipment_manage_menu(update, context)
    reset = query.data == 'equip_preset_load_reset'
    ok = load_equipment_preset(preset_id, reset_countries_inventory=reset)
    context.user_data.pop('preset_to_load', None)
    if ok:
        msg = "âœ… Ù„ÛŒØ³Øª Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ø´Ø¯."
        if reset:
            msg += "\nðŸ”„ Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ù‡Ù…Ù‡ Ú©Ø´ÙˆØ±Ù‡Ø§ ØµÙØ± Ø´Ø¯."
        else:
            msg += "\nðŸ’¾ Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ Ú©Ø´ÙˆØ±Ù‡Ø§ Ø­ÙØ¸ Ø´Ø¯."
        await query.edit_message_text(msg)
    else:
        await query.edit_message_text("âŒ Ø¨Ø§Ø±Ú¯Ø°Ø§Ø±ÛŒ Ø§Ù†Ø¬Ø§Ù… Ù†Ø´Ø¯.")
    return await show_equipment_manage_menu(update, context)


# ---- Ø³Ø§Ø®Øª Ù„ÛŒØ³Øª Ø¬Ø¯ÛŒØ¯ (Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ) ----

async def equip_new_list_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = (
        "ðŸ†• *Ø³Ø§Ø®Øª Ù„ÛŒØ³Øª Ø¬Ø¯ÛŒØ¯*\n\n"
        "Ø§ÛŒÙ† Ø¹Ù…Ù„ ØªÙ…Ø§Ù… ØªØ¬Ù‡ÛŒØ²Ø§Øª Ùˆ Ø¯Ø³ØªÙ‡â€ŒØ¨Ù†Ø¯ÛŒâ€ŒÙ‡Ø§ÛŒ ÙØ¹Ù„ÛŒ Ø±Ø§ Ø­Ø°Ù Ù…ÛŒâ€ŒÚ©Ù†Ø¯.\n"
        "Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ú©Ø´ÙˆØ±Ù‡Ø§ Ú†Ù‡ Ø´ÙˆØ¯ØŸ"
    )
    keyboard = [
        [InlineKeyboardButton("âœ… Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ Ø­ÙØ¸ Ø´ÙˆØ¯", callback_data='equip_new_list_keep')],
        [InlineKeyboardButton("ðŸ”„ Ù…ÙˆØ¬ÙˆØ¯ÛŒ Ù‡Ù…Ù‡ Ú©Ø´ÙˆØ±Ù‡Ø§ ØµÙØ± Ø´ÙˆØ¯", callback_data='equip_new_list_reset')],
        [InlineKeyboardButton("âŒ Ù„ØºÙˆ", callback_data='equip_back_menu')]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return EQUIP_MANAGE_MENU


async def equip_new_list_apply(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    reset = query.data == 'equip_new_list_reset'

    # Ù¾Ø§Ú© Ú©Ø±Ø¯Ù† Ù‡Ù…Ù‡ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ùˆ Ø¢ÛŒØªÙ…â€ŒÙ‡Ø§
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM equipment_items")
    c.execute("DELETE FROM equipment_categories")
    conn.commit()
    conn.close()

    if reset:
        _reset_countries_inventory_to_new_schema()

    msg = "âœ… Ù„ÛŒØ³Øª Ø¬Ø¯ÛŒØ¯ Ø§ÛŒØ¬Ø§Ø¯ Ø´Ø¯ (Ù‡Ù…Ù‡ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ùˆ Ø¯Ø³ØªÙ‡â€ŒÙ‡Ø§ Ù¾Ø§Ú© Ø´Ø¯Ù†Ø¯)."
    if reset:
        msg += "\nðŸ”„ Ù…ÙˆØ¬ÙˆØ¯ÛŒ ØªØ¬Ù‡ÛŒØ²Ø§Øª Ù‡Ù…Ù‡ Ú©Ø´ÙˆØ±Ù‡Ø§ ØµÙØ± Ø´Ø¯."
    else:
        msg += "\nðŸ’¾ Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙØ¹Ù„ÛŒ Ú©Ø´ÙˆØ±Ù‡Ø§ Ø­ÙØ¸ Ø´Ø¯."
    await query.edit_message_text(msg)
    return await show_equipment_manage_menu(update, context)


# ---- Ø¨Ø³ØªÙ† Ù…Ù†Ùˆ ----

async def equip_close(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text("âœ… Ù…Ù†ÙˆÛŒ Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª Ø¨Ø³ØªÙ‡ Ø´Ø¯.")
    except Exception:
        pass
    # Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ state Ù…ÙˆÙ‚Øª
    context.user_data.pop('equip_new', None)
    context.user_data.pop('preset_to_load', None)
    return ConversationHandler.END


async def equip_back_menu(update: Update, context: CallbackContext) -> int:
    return await show_equipment_manage_menu(update, context)


# ============================== Ù…Ø¯ÛŒØ±ÛŒØª Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ ÙØ¹Ø§Ù„ ==============================

async def activate_chat_handler(update: Update, context: CallbackContext) -> int:
    """Ø¨Ø§ ØªØ§ÛŒÙ¾ Â«Ø§Ú©ØªÙˆÛŒØªÂ» ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ú¯Ù¾ØŒ Ø¢Ù† Ú¯Ù¾ Ø±Ø§ Ø¨Ù‡ Ù„ÛŒØ³Øª Ú¯Ù¾â€ŒÙ‡Ø§ÛŒ ÙØ¹Ø§Ù„ Ø§Ø¶Ø§ÙÙ‡ Ù…ÛŒâ€ŒÚ©Ù†Ø¯."""
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id
    if not is_admin(user_id):
        # Ú©Ø§Ø±Ø¨Ø± Ø¹Ø§Ø¯ÛŒ Ù†Ù…ÛŒâ€ŒØªÙˆÙ†Ù‡ Ø§Ú©ØªÙˆÛŒØª Ú©Ù†Ù‡
        return ConversationHandler.END
    if is_chat_active(chat.id):
        await update.message.reply_text(
            f"â„¹ï¸ Ø§ÛŒÙ† Ú¯Ù¾ Ù‚Ø¨Ù„Ø§Ù‹ ÙØ¹Ø§Ù„ Ø´Ø¯Ù‡ Ø§Ø³Øª.\n"
            f"ðŸ†” Ø´Ù†Ø§Ø³Ù‡ Ú¯Ù¾: `{chat.id}`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    activate_chat(chat.id, chat.title or "Ø¨Ø¯ÙˆÙ† Ø¹Ù†ÙˆØ§Ù†", user_id)
    await update.message.reply_text(
        f"âœ… Ø§ÛŒÙ† Ú¯Ù¾ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ø±Ø§ÛŒ Ù¾Ù„ÛŒØ±Ù‡Ø§ ÙØ¹Ø§Ù„ Ø´Ø¯.\n"
        f"ðŸ†” Ø´Ù†Ø§Ø³Ù‡ Ú¯Ù¾: `{chat.id}`\n\n"
        "Ø§Ø² Ø§ÛŒÙ† Ø¨Ù‡ Ø¨Ø¹Ø¯ØŒ Ù¾Ù„ÛŒØ±Ù‡Ø§ Ù…ÛŒâ€ŒØªÙˆØ§Ù†Ù†Ø¯ Ø¨Ø§ /start ÛŒØ§ Â«Ù…Ù†ÙˆÂ» Ø¯Ø± Ù‡Ù…ÛŒÙ† Ú¯Ù¾ Ø¨Ù‡ Ø±Ø¨Ø§Øª Ø¯Ø³ØªØ±Ø³ÛŒ Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ù†Ø¯.\n"
        "Ø¨Ø±Ø§ÛŒ ØºÛŒØ±ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒØŒ Ú©Ù„Ù…Ù‡ Â«Ø¯ÛŒØ§Ú©ØªÙˆÛŒØªÂ» Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def deactivate_chat_handler(update: Update, context: CallbackContext) -> int:
    """Ø¨Ø§ ØªØ§ÛŒÙ¾ Â«Ø¯ÛŒØ§Ú©ØªÙˆÛŒØªÂ» ØªÙˆØ³Ø· Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ú¯Ù¾ØŒ Ø¢Ù† Ú¯Ù¾ Ø§Ø² Ù„ÛŒØ³Øª Ø®Ø§Ø±Ø¬ Ù…ÛŒâ€ŒØ´ÙˆØ¯."""
    if not update.message or not update.effective_chat:
        return ConversationHandler.END
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        return ConversationHandler.END
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return ConversationHandler.END
    if not is_chat_active(chat.id):
        await update.message.reply_text("â„¹ï¸ Ø§ÛŒÙ† Ú¯Ù¾ Ø§Ø² Ù‚Ø¨Ù„ ÙØ¹Ø§Ù„ Ù†Ø¨ÙˆØ¯Ù‡ Ø§Ø³Øª.")
        return ConversationHandler.END
    deactivate_chat(chat.id)
    await update.message.reply_text("âœ… Ø§ÛŒÙ† Ú¯Ù¾ Ø§Ø² Ø­Ø§Ù„Øª ÙØ¹Ø§Ù„ Ø®Ø§Ø±Ø¬ Ø´Ø¯. Ù¾Ù„ÛŒØ±Ù‡Ø§ Ø¯ÛŒÚ¯Ø± Ø¯Ø± Ø§ÛŒÙ† Ú¯Ù¾ Ø¨Ù‡ Ø±Ø¨Ø§Øª Ø¯Ø³ØªØ±Ø³ÛŒ Ù†Ø¯Ø§Ø±Ù†Ø¯.")
    return ConversationHandler.END


async def menu_in_group_handler(update: Update, context: CallbackContext) -> int:
    """Ø¨Ø§ ØªØ§ÛŒÙ¾ Â«Ù…Ù†ÙˆÂ» Ø¯Ø± Ú¯Ù¾:
       - Ø§Ú¯Ø± Ø§Ø¯Ù…ÛŒÙ†: Ù¾Ù†Ù„ Ø§Ø¯Ù…ÛŒÙ† Ø¯Ø± Ù‡Ù…Ø§Ù† Ú¯Ù¾
       - Ø§Ú¯Ø± Ù¾Ù„ÛŒØ± Ùˆ Ú¯Ù¾ ÙØ¹Ø§Ù„: Ù…Ù†ÙˆÛŒ Ø§ØµÙ„ÛŒ Ù¾Ù„ÛŒØ±
       - Ø¯Ø± ØºÛŒØ± Ø§ÛŒÙ† ØµÙˆØ±Øª Ø³Ú©ÙˆØª
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
        # Ú¯Ù¾ ÙØ¹Ø§Ù„ Ù†ÛŒØ³ØªØŒ Ù¾Ø§Ø³Ø® Ù†Ø¯ÛŒÙ…
        return ConversationHandler.END
    country_data = get_country(user_id)
    if not country_data:
        await update.message.reply_text(
            "âš ï¸ Ø´Ù…Ø§ Ù‡Ù†ÙˆØ² Ú©Ø´ÙˆØ± Ø®ÙˆØ¯ Ø±Ø§ Ø«Ø¨Øª Ù†Ú©Ø±Ø¯Ù‡â€ŒØ§ÛŒØ¯!\nÙ„Ø·ÙØ§Ù‹ Ø¢ÛŒØ¯ÛŒ Ø¹Ø¯Ø¯ÛŒ Ø®ÙˆØ¯ Ø±Ø§ Ø¨Ù‡ Ù…Ø§Ù„Ú© Ø±Ø¨Ø§Øª Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
        )
        return ConversationHandler.END
    return await show_main_menu(update, context)


async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if update and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ù…ØªØ§Ø³ÙØ§Ù†Ù‡ Ø®Ø·Ø§ÛŒÛŒ Ø±Ø® Ø¯Ø§Ø¯. Ù„Ø·ÙØ§Ù‹ Ø¯ÙˆØ¨Ø§Ø±Ù‡ ØªÙ„Ø§Ø´ Ú©Ù†ÛŒØ¯ ÛŒØ§ /start Ø±Ø§ Ø§Ø±Ø³Ø§Ù„ Ú©Ù†ÛŒØ¯."
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

        job_queue.run_repeating(deliver_trades_job, interval=60, first=10)

        job_queue.run_repeating(deliver_attacks_job, interval=60, first=10)

        logger.info("Job daily_production, deliver_trades and deliver_attacks scheduled")
    else:
        logger.warning("Job queue not available")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
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
                CallbackQueryHandler(country_management, pattern='^country_management$'),
            ],
            ADMIN_MENU: [
                CallbackQueryHandler(add_country, pattern='^add_country$'),
                CallbackQueryHandler(delete_country_menu, pattern='^delete_country_menu$'),
                CallbackQueryHandler(list_countries, pattern='^list_countries$'),
                CallbackQueryHandler(edit_main_props, pattern='^edit_main_props$'),
                CallbackQueryHandler(edit_assets_menu, pattern='^edit_assets_menu$'),
                CallbackQueryHandler(admin_update_assets_handler, pattern='^admin_update_assets$'),
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
                CallbackQueryHandler(back_to_main_menu, pattern='^back_main$'),
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
                MessageHandler(filters.PHOTO & ~filters.COMMAND, get_statement_content)
            ],
            COUNTRY_MANAGEMENT: [
                CallbackQueryHandler(internet_control, pattern='^internet_control$'),
                CallbackQueryHandler(refinery_menu, pattern='^refinery_menu$'),
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
    # ConversationHandler Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª (ÙˆØ±ÙˆØ¯ Ø¨Ø§ Ù¾ÛŒØ§Ù… Â«Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§ØªÂ» Ø¯Ø± Ù¾ÛŒâ€ŒÙˆÛŒ)
    equip_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.TEXT & filters.Regex(r'^\s*Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª\s*$'),
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
                filters.TEXT & filters.Regex(r'^\s*Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§Øª\s*$'),
                equip_manage_entry
            ),
        ],
        per_user=True,
        per_chat=True,
        allow_reentry=True,
    )

    # Ù‡Ù†Ø¯Ù„Ø±Ù‡Ø§ÛŒ Ø§Ú©ØªÙˆÛŒØª/Ø¯ÛŒØ§Ú©ØªÙˆÛŒØª/Ù…Ù†Ùˆ Ø¯Ø± Ú¯Ù¾ (Ø¨Ø§ Ø§ÙˆÙ„ÙˆÛŒØª Ø¨Ø§Ù„Ø§ ØªØ§ Ù‚Ø¨Ù„ Ø§Ø² conv_handler Ø§Ø¬Ø±Ø§ Ø´ÙˆÙ†Ø¯)
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*Ø§Ú©ØªÙˆÛŒØª\s*$'),
            activate_chat_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*Ø¯ÛŒØ§Ú©ØªÙˆÛŒØª\s*$'),
            deactivate_chat_handler
        ),
        group=-1
    )
    application.add_handler(
        MessageHandler(
            (filters.ChatType.GROUPS) & filters.TEXT & filters.Regex(r'^\s*Ù…Ù†Ùˆ\s*$'),
            menu_in_group_handler
        ),
        group=-1
    )

    # Ø§Ø¨ØªØ¯Ø§ equip_conv_handler Ø«Ø¨Øª Ø´ÙˆØ¯ ØªØ§ Ø±ÙˆÛŒ Ù…ØªÙ† Â«Ù…Ø¯ÛŒØ±ÛŒØª ØªØ¬Ù‡ÛŒØ²Ø§ØªÂ» ØªÙ‚Ø¯Ù… Ø¯Ø§Ø´ØªÙ‡ Ø¨Ø§Ø´Ø¯
    application.add_handler(equip_conv_handler)
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("daily_production", run_daily_production_manually))
    application.add_handler(CallbackQueryHandler(edit_storage_capacity, pattern='^edit_storage_capacity$'))
    application.add_handler(CallbackQueryHandler(select_country_for_storage, pattern='^storage_country_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_storage_capacity))
    application.add_handler(CallbackQueryHandler(handle_proposal_callback, pattern='^(approve|reject)_'))
    application.add_handler(CallbackQueryHandler(handle_trade_response, pattern='^(accept|reject|cancel)_trade_'))
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
