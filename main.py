import os
import threading
import time
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from keys import Data
import requests

DATA = Data()

# Telegram Bot Token from BotFather
TOKEN = DATA._data['BOT_KEY']

# Your group chat ID
GROUP_CHAT_ID = DATA._data['GROUP_CHAT_ID']

# File storage directory
FILES_DIR = 'files'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Bot started. Send me a file, and I will encrypt and send it to the group.')


    # List all the group chats the bot is part of
    if update.message.chat.type == 'group':
        chat_id = update.message.chat_id

    await update.message.reply_text(f'Group Chat ID: {chat_id}')

async def handle_file(update: Update, context: CallbackContext) -> None:

    file_id = update.message.document.file_id
    file_info = await context.bot.get_file(file_id)
    file_url = file_info.file_path
    text = update.message.caption
    KEY = text.encode('utf-8')
    file_path = os.path.join(FILES_DIR, file_info.file_path.rsplit('/', 1)[-1])

    response = requests.get(file_url)

    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    if file_path.endswith('.enc'):
        # Decrypt the file with the provided password
        decrypted_file_path = decrypt_file(file_path, KEY)

        # Send the decrypted file back to the sender
        with open(decrypted_file_path, 'rb') as decrypted_file:
            await context.bot.send_document(update.message.chat_id, decrypted_file)
    else: 
        # Encrypt the file
        encrypted_file_path = encrypt_file(file_path, KEY)

        # Send the encrypted file to the group
        with open(encrypted_file_path, 'rb') as encrypted_file:
            await context.bot.send_document(GROUP_CHAT_ID, encrypted_file)


def encrypt_file(file_path: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, IV=get_random_bytes(16))

    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Pad the plaintext to match block size
    plaintext = pad(plaintext, AES.block_size)

    # Encrypt the plaintext
    ciphertext = cipher.encrypt(plaintext)

    # Save the encrypted file
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(ciphertext)

    return encrypted_file_path

def decrypt_file(encrypted_file_path: str, key: bytes) -> str:
    with open(encrypted_file_path, 'rb') as encrypted_file:
        ciphertext = encrypted_file.read()

    # Create an AES cipher object with the provided key
    cipher = AES.new(key, AES.MODE_CBC, IV=ciphertext[:AES.block_size])

    # Decrypt the ciphertext
    decrypted_data = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)

    # Save the decrypted file
    decrypted_file_path = encrypted_file_path.rstrip('.enc') + '_decrypted.txt'
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return decrypted_file_path

async def error(update: Update, context: CallbackContext) -> None:
    print(f'Update {update} caused error {context.error}')

def clear_files_directory():
    directory = 'files'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error clearing file/directory: {e}")

def stop_bot():
    print('Stopping bot...')
    clear_files_directory()  # Clear files/directory before stopping
    os._exit(0)

def main() -> None:
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Register file handler
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Error handler
    app.add_error_handler(error)

    print('Polling started...')
    # Start the Bot
    timer = threading.Timer(30 * 60, stop_bot)
    timer.start()
    
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    
    main()

