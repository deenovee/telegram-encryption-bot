
File Encryption and Decryption Bot

This Python bot utilizes the Telegram API to enable file encryption and decryption within a group chat. Users can send files to the bot, and the bot will either encrypt or decrypt the file based on the user's provided password. The encrypted files are then sent to a specified group chat, while decrypted files are sent back to the original sender.

Setup

Telegram Bot Token: Obtain a Telegram Bot Token from BotFather and replace BOT_KEY in the keys.py file.

Group Chat ID: Identify the Group Chat ID where the bot will send encrypted files. Replace GROUP_CHAT_ID in the keys.py file.

File Storage Directory: The bot stores files in a directory named files. Ensure this directory exists, or create it manually.

Dependencies: Install the required Python packages using:

    ```bash
    pip install python-telegram-bot pycryptodome requests
    Run the Bot: Execute the bot.py file to start the bot. The bot will listen for incoming files and perform encryption or decryption based on the provided instructions.

Usage

Start Command: Send the /start command to the bot to initialize it. The bot will provide the Group Chat ID for reference.

Send a File: Users can send any file type to the bot. Additionally, users can include a caption with their chosen password to encrypt or decrypt the file.

Encryption: If the file is not already encrypted (ends with .enc), the bot will encrypt it using the provided password. The encrypted file will be sent to the specified group chat.

Decryption: If the file is already encrypted, the bot will decrypt it using the provided password. The decrypted file will be sent back to the original sender.

Encryption and Decryption Algorithm

Encryption: The bot uses the Advanced Encryption Standard (AES) algorithm in Cipher Block Chaining (CBC) mode. The provided password is used as the encryption key.

Decryption: To decrypt a file, the bot extracts the encryption key from the user-provided password. It then uses this key to decrypt the file and send it back to the user.

Timer and Cleanup

The bot includes a timer that runs in the background, automatically stopping the bot after 30 minutes. Before stopping, the bot clears the files directory to remove any temporary files.

Important Note

Ensure the bot has the necessary permissions in the group chat, such as the ability to read messages, send messages, and manage files.

Disclaimer: This bot is for educational purposes only, and users are responsible for its usage within the bounds of the law and Telegram's policies.





