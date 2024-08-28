import telebot
from telebot import types
import os

# Botunuzun API anahtarını buraya yapıştırın
TOKEN = '7116709968:AAGUBZh0Yjbt9ohHvoNBycnhk_fe-dcf_Bc'
bot = telebot.TeleBot(TOKEN)

# Dosya yolu ve adı
FILE_PATH = 'received_file.py'

def create_main_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Yardım')
    item2 = types.KeyboardButton('Ayarlar')
    markup.add(item1, item2)
    return markup

def create_settings_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Dosyayı Çalıştır')
    item2 = types.KeyboardButton('Dosyayı Sil')
    item3 = types.KeyboardButton('Ana Menü')
    markup.add(item1, item2, item3)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_main_markup()
    welcome_message = ("Merhaba! Python dosyası gönderebilirsiniz.\n"
                       "Lütfen aşağıdaki butonlardan birini seçin.")
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'yardım')
def send_help(message):
    help_message = ("Yardım:\n"
                    "1. Python dosyasını göndermek için dosyayı yükleyin.\n"
                    "2. Dosyayı çalıştırmak için 'Ayarlar' menüsündeki 'Dosyayı Çalıştır' butonuna tıklayın.\n"
                    "3. Dosyayı silmek için 'Ayarlar' menüsündeki 'Dosyayı Sil' butonuna tıklayın.")
    bot.send_message(message.chat.id, help_message, reply_markup=create_main_markup())

@bot.message_handler(func=lambda message: message.text.lower() == 'ayarlar')
def send_settings(message):
    settings_message = ("Ayarlar:\n"
                        "1. 'Dosyayı Çalıştır' - Yüklediğiniz Python dosyasını çalıştırır.\n"
                        "2. 'Dosyayı Sil' - Yüklediğiniz Python dosyasını siler.\n"
                        "3. 'Ana Menü' - Ana menüye geri döner.")
    bot.send_message(message.chat.id, settings_message, reply_markup=create_settings_markup())

@bot.message_handler(func=lambda message: message.text.lower() == 'dosyayı çalıştır')
def run_file(message):
    if os.path.exists(FILE_PATH):
        try:
            exec(open(FILE_PATH).read())
            bot.reply_to(message, "Dosya başarıyla çalıştırıldı!")
        except Exception as e:
            bot.reply_to(message, f"Dosya çalıştırılamadı: {e}")
    else:
        bot.reply_to(message, "Yüklenmiş bir dosya bulunmuyor.", reply_markup=create_settings_markup())

@bot.message_handler(func=lambda message: message.text.lower() == 'dosyayı sil')
def delete_file(message):
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
        bot.reply_to(message, "Dosya başarıyla silindi.", reply_markup=create_settings_markup())
    else:
        bot.reply_to(message, "Silinecek dosya bulunmuyor.", reply_markup=create_settings_markup())

@bot.message_handler(func=lambda message: message.text.lower() == 'ana menü')
def back_to_main(message):
    markup = create_main_markup()
    bot.send_message(message.chat.id, "Ana menüye döndünüz.", reply_markup=markup)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.file_name.endswith('.py'):
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(FILE_PATH, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "Python dosyası başarıyla alındı.", reply_markup=create_main_markup())
    else:
        bot.reply_to(message, "Lütfen bir Python dosyası gönderin.", reply_markup=create_main_markup())

bot.polling()