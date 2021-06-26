#!/usr/bin/python
import time
import subprocess
import os
import telegram
import urllib.request
import re
import json
import requests
import shutil
from spleeter.separator import Separator
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
import logging
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
flag11 = 0
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telegram.Bot(token=api_cont)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
    chat_id = update.message.chat.id
    print(chat_id)
    """Send a message when the command /start is issued."""
    update.message.reply_text("輸入yt videolink來分離此歌曲之樂器(ex: yt your.video.link)")
"""
def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print ("Command from client : %s  " %command)
"""
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def sendAudio(update, context):
    #youtube search
        global flag11
        chat_id = update.message.chat.id
        command = update.message.text
        if command.startswith('yt'):
            bot.sendMessage(chat_id=chat_id,text='下載中，請稍候...')
            param = command[3:]
            response = urlopen("https://www.youtube.com/results?search_query="+param)
            data = response.read()
            response.close()
            soup = BeautifulSoup(data,"html.parser")
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            #link = "https://www.youtube.com"+vid['href']
            global link
            link = param
            options = {
                'format': 'bestaudio/best',
                'outtmpl': 'down' +'.mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }]
            }
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([link])
            #watchid = vid['href']
            #watchid = watchid.replace('/watch?v=','')
            #title = vid['title']
            #print (title)
            os.system('mv -f down.mp3 aim.mp3')
            bot.sendMessage(chat_id=chat_id,text='輸入你想要區分的方法\n*請輸入數字(2 or 4 or 5, 輸入exit來取消)\n[2:(vocals / accompaniment)]\n[4:(vocals / bass / drums / other )]\n[5:(vocals / bass / drums / piano / other)]\n可能需要一段時間，請稍候')

            print (link)
            flag11 = 1
        elif command == 'exit':
            link = ''
            bot.sendMessage(chat_id=chat_id, text="Bye!")
        elif flag11 == 1:
                print (command)
                if command=='2':
                    bot.sendMessage(chat_id=chat_id,text='分析中，請稍候...')
                    separator = Separator('spleeter:2stems')
                    separator.separate_to_file('aim.mp3', 'audio_output')
                    os.system('ffmpeg -i audio_output/aim/vocals.wav -acodec mp3 audio_output/aim/vocals.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/vocals.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/accompaniment.wav -acodec mp3 audio_output/aim/accompaniment.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/accompaniment.mp3",'rb'))
                    shutil.rmtree('audio_output/aim')
                    link = ""
                    os.remove('aim.mp3')
                    flag11=0
                elif command=='4':
                    bot.sendMessage(chat_id=chat_id,text='分析中，請稍候...')
                    separator = Separator('spleeter:4stems')
                    separator.separate_to_file('aim.mp3', 'audio_output')
                    os.system('ffmpeg -i audio_output/aim/vocals.wav -acodec mp3 audio_output/aim/vocals.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/vocals.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/drums.wav -acodec mp3 audio_output/aim/drums.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/drums.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/bass.wav -acodec mp3 audio_output/aim/bass.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/bass.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/other.wav -acodec mp3 audio_output/aim/other.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/other.mp3",'rb'))
                    shutil.rmtree('audio_output/aim')
                    link = ""
                    os.remove('aim.mp3')
                    flag11=0
                elif command=='5':
                    bot.sendMessage(chat_id=chat_id,text='分析中，請稍候...')
                    separator = Separator('spleeter:5stems')
                    separator.separate_to_file('aim.mp3', 'audio_output')
                    os.system('ffmpeg -i audio_output/aim/vocals.wav -acodec mp3 audio_output/aim/vocals.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/vocals.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/drums.wav -acodec mp3 audio_output/aim/drums.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/drums.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/bass.wav -acodec mp3 audio_output/aim/bass.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/bass.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/piano.wav -acodec mp3 audio_output/aim/piano.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/piano.mp3",'rb'))
                    os.system('ffmpeg -i audio_output/aim/other.wav -acodec mp3 audio_output/aim/other.mp3')
                    bot.send_audio(chat_id=chat_id, audio=open("audio_output/aim/other.mp3",'rb'))
                    shutil.rmtree('audio_output/aim')
                    link = ""
                    os.remove('aim.mp3')
                    flag11=0
                else:
                    bot.sendMessage(chat_id=chat_id,text='輸入錯誤，請重新輸入')                    
        elif flag11==0:
            bot.sendMessage(chat_id, text="輸入格式錯誤ㄛ")
    #end youtube search



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(api_cont, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, sendAudio))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
if __name__ == "__main__":
    main()
