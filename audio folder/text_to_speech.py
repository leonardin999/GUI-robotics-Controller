# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 09:50:36 2021

@author: Leonard
"""

import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
engine.setProperty('rate', 180)     # setting up new voice rate
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1)    # setting up volume level  between 0 and 1

"""VOICE"""
# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
    
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An')  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

# change_voice(engine, "vn_VN", "VoiceGenderFemale")
engine.say("Xin chào! Tôi là" + voice.name + "và tôi sẵn sàng trợ giúp. Điều khiển thủ công ở đây, điều khiển bằng giọng nói ở đó"
           "và chúng tôi sẽ chuẩn bị sẵn rô-bốt của bạn cho tất cả những gì bạn định làm. Hãy sử dụng giọng nói của bạn trong suốt quá trình."
           "Tôi ở đây để giúp bạn điều khiển rô bốt bằng chế độ rảnh tay trong giới hạn của tôi."
           "Được rồi, giới thiệu đủ rồi. Hãy cùng tìm hiểu!")
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()