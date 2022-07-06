import os
import telebot
import logging
from dotenv import load_dotenv, find_dotenv
from gnews import GNews as GoogleNews
import time, threading, schedule

load_dotenv(find_dotenv())

logging.basicConfig(filename="bot.txt", format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    encoding='utf-8', level=logging.DEBUG)
telebot.logger.setLevel(logging.DEBUG)
API_KEY = os.getenv("API_TOKEN")
URL_TELE = os.getenv("CTELE_URL")
URL_MESS = os.getenv("MESS_URL")
URL_CSLATE = os.getenv("CSLATE_URL")
URL_CNEWS = os.getenv("CNEWS_URL")
URL_CDESK = os.getenv("CDESK_URL")
news_list = ['cointelegraph', 'messari', 'cryptoslate', 'cryptonews', 'coindesk']


bot = telebot.TeleBot(API_KEY)

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']
	
# To register filter, you need to use method add_custom_filter.
bot.add_custom_filter(IsAdmin())

@bot.message_handler(is_admin=True, commands=['start'])
def set_timer(message):
    news(message.chat.id)
    print(message.chat.id)
    schedule.every(1).minutes.do(news, message.chat.id).tag(message.chat.id)

@bot.channel_post_handler(is_admin=True, commands=['start'])
def set_timer(message):
    news(message.chat.id)
    print(message.chat.id)
    schedule.every(1).minutes.do(news, message.chat.id).tag(message.chat.id)
   

def news(chat_id) -> None:
    
    for y in news_list:
        if y == 'cointelegraph':
            request = URL_TELE 
        elif y == 'messari':
            request = URL_MESS
        elif y == 'cryptoslate':
            request = URL_CSLATE
        elif y == 'cryptonews':
            request = URL_CNEWS
        elif y == 'coindesk':
            request = URL_CDESK
        else:
            bot.send_message(chat_id, "Wrong choice")
       
        
        googlenews = GoogleNews(period='6h', max_results=4)
        results = googlenews.get_news(request)
        if results == []:
            text = f"""
            No news in the last 6h for {y}
            """
            bot.send_message(chat_id, text = text)
        results.sort(key = lambda x:x['published date'],reverse=True)

        for x in results:
            if x['url'].startswith(request):
                text = (
                    f"{x['published date']}\n"
                    f"{x['url']}\n"
                )
                bot.send_message(chat_id, text=text)
            else: 
                text = f"""
                No news in the last 6h for {y}
                """
                bot.send_message(chat_id, text = text)
            

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

""" bot.infinity_polling(allowed_updates=util.update_types) """
