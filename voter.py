import telebot
import requests
import json
from keep_alive import keep_alive

keep_alive()

# Replace with your actual Telegram bot token
TOKEN = "7246289914:AAHcIgglbBWFJqG0W2c-SMz95e7X8LpYH2k"
bot = telebot.TeleBot(TOKEN)

# Define the API details
API_URL = "http://apps.ecs.gov.bd/ec-user-app/api/v2/private/user-voter-area?election_schedule_id=103"
HEADERS = {
    'user-agent': 'Dart/3.1 (dart:io)',
    'content-type': 'application/json; charset=UTF-8',
    'secret-key': '6iM9eN0170i7yB972sH73qu73La97M4375T1R75zT',
    'accept-encoding': 'gzip'
}

# States for the bot to track user inputs
user_data = {}

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "আস-সালামু 'আলাইকুম ওয়া রহমাতুল্লাহি ওয়া বারকাতুহু 🤍\n\nএই বটটির নির্মাতা মোঃ আতিকুর রহমান সুমন। এটি সুবিধার জন্য তৈরি করা হয়েছে। কেউ এর দ্বারা কোনো প্রকার দুর্নীতি করলে নির্মাতা দায়ী থাকবে না।\n\nঘোড়া মার্কা 🐎✌️\n\nদয়া করে আপনার আইডি কার্ড নম্বর প্রদান করুন (Please enter your ID No):")
    bot.register_next_step_handler(message, get_id_number)

# Get the ID number from the user
def get_id_number(message):
    user_id = message.from_user.id
    user_data[user_id] = {'search_value': message.text}
    bot.reply_to(message, "Please enter your Date of Birth (YYYY-MM-DD):")
    bot.register_next_step_handler(message, get_dob)

# Get the date of birth from the user and make the API request
def get_dob(message):
    user_id = message.from_user.id
    user_data[user_id]['dob'] = message.text
    make_api_request(message, user_data[user_id])

# Make the API request and handle the response
def make_api_request(message, data):
    payload = json.dumps({
        'dob': data['dob'],
        'search_value': data['search_value']
    })
    
    response = requests.post(API_URL, headers=HEADERS, data=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        result = response_data.get('result', [{}])[0]
        nid_info = response_data.get('nid_info', {})

        upazila = result.get('settings_name', 'N/A')
        center = result.get('institute_name', 'N/A')
        area = result.get('voter_area_name', 'N/A')
        serial_number = nid_info.get('sl_no', 'N/A')
        voter_no = nid_info.get('voter_no', 'N/A')

        response_text = (
            f"\n*ঘোড়া মার্কা* 🐎✌️\n━━━━━━━━━━━━━━━━━━━━\n*🔴UPAZILA*: {upazila}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n*🔴CENTER*: {center}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n*🔴AREA*: {area}\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n*🔴SERIAL NUMBER*: `{serial_number}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n*🔴VOTER NO*: `{voter_no}`\n━━━━━━━━━━━━━━━━━━━━\n"
        )

        bot.reply_to(message, response_text, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"Error: {response.status_code}\n{response.text}")
    
    # Ask for a new ID No. with a new message
    ask_new_id(message)

# Ask for a new ID No.
def ask_new_id(message):
    bot.send_message(message.chat.id, "Please enter a new ID No to get information (নতুন আইডি নম্বর প্রদান করুন):")
    bot.register_next_step_handler(message, get_id_number)

# Start polling
bot.polling()