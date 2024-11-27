import os 
from dotenv import load_dotenv
import requests
import threading
import telebot
bot = telebot.TeleBot("7187679071:AAEIAmt1_1ojcYoEkg3rvolhA0ZimrXfnvc")
load_dotenv()

URL = os.getenv('SMS_API_URL')
LOGIN = os.getenv('SMS_API_LOGIN')
PASSWORD = os.getenv('SMS_API_PASSWORD')

def send_sms( msg):
    try:    
        requests.post(URL, json={ "messages":[ msg ] }, auth=(LOGIN, PASSWORD))
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")


class SmsSend:
   
    @staticmethod
    def send_verification_code( phone, verification_code):
        text = f"Verification Code:  {verification_code}"
        sms = {"recipient":phone,"message-id":f"1","sms":{
                    "originator": "3700",
                        "content": {"text": text} }}
        threading.Thread(target=send_sms, args=(sms,)).start()   

    @staticmethod
    def send_verification_code_telegram( phone, verification_code):
        text = f"Verification Code:  {verification_code}"
        sms = {"recipient":phone,"message-id":f"1","sms":{
                    "originator": "3700",
                        "content": {"text": text} }}
        bot.send_message(chat_id=891196310, text=text)  
    
