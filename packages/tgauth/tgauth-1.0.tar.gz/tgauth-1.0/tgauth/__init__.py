import requests
import json
from time import sleep
from tgauth.models import TelegramKey,TempTelegramUser
from tgauth.exceptions import MissingParameter
import threading
import time
import requests
from django.conf import settings
from django.contrib.auth.models import User
import random
import string
import hashlib,sha,os,md5



tg_token = getattr(settings,'TGAUTH_TOKEN','')
url = 'https://api.telegram.org/bot%s/' % tg_token

def get_salt():
    char_set = string.ascii_uppercase + string.digits
    unique_code = ''.join(random.sample(char_set*6,12))
    salt = sha.new(str(unique_code)).hexdigest()[:8]
    return salt

def get_unique_code():
  char_set = string.ascii_uppercase + string.digits
  unique_code = ''.join(random.sample(char_set*6, 6))
  return unique_code

def extract_unique_code(uniquecode):
  # Extracts the unique_code from the sent /start command.
    return uniquecode.split()[1] if len(uniquecode.split()) > 1 else None

def get_key_from_telegramkey(unique_code):
  try:
      code = TelegramKey.objects.get(unique_key=unique_code)
  except TelegramKey.DoesNotExist:
      return False
  return True


class TelegramThreading(object):
    """ TelegramThreading class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start() 

    def run(self):
        last_update = 0
        count = 0
        while True:
            get_updates = json.loads(requests.get(url + 'getUpdates' ).content)
            for update in get_updates['result']:
                if last_update < update['update_id']:
                    last_update = update['update_id']
                    update['is_send'] = False
                    if 'message' in update:
                        unique_code = unique_code = extract_unique_code(update['message']['text'])
                        if unique_code is not None:
                            unique_key = get_key_from_telegramkey(unique_code)
                            if unique_key:
                                if User.objects.filter(username=update['message']['chat']['id']):
                                    try:
                                        print "user alreday existing"
                                        user = User.objects.get(username=update['message']['chat']['id'])
                                        random_password = get_unique_code()
                                        user.set_password(random_password)
                                        user.save()
                                        temptg = TempTelegramUser.objects.get(tuser__id=user.id)
                                        salt = get_salt()
                                        temptg.activation_key = md5.new(salt + str(user.username)).hexdigest()
                                        temptg.random_pwd = random_password
                                        temptg.save()

                                    except User.DoesNotExist:
                                        pass

                                else:
                                    print "not existing"
                                    user = User.objects.create(username=update['message']['chat']['id'])
                                    if 'first_name' or 'last_name' is not None in  update['message']:
                                        user.first_name = update['message']['chat']['first_name']
                                        user.last_name  = update['message']['chat']['last_name']
                                    random_password = get_unique_code()
                                    user.set_password(random_password)
                                    user.save()

                                    temptg = TempTelegramUser()
                                    temptg.tuser = User.objects.get(id=user.id)
                                    salt = get_salt()
                                    temptg.activation_key = md5.new(salt + str(user.username)).hexdigest()
                                    temptg.random_pwd = random_password
                                    temptg.save()
                                if not update['is_send'] == 'True':
                                  site_url = getattr(settings,'TG_AUTH_SITE_URL','')
                                  if site_url:
                                      active_url = site_url+'validate/otp/'+str(temptg.activation_key)
                                      reply = "Hello click this link %s and this is your OTP password %s" %(active_url,random_password)
                                      requests.get(url + 'sendMessage', params=dict(chat_id=user.username, text=reply))
                                      update['is_send'] = True

                                      print update
                                      print "make the value is in True"
                                  
                                  else:
                                      raise ValueError(" TG_AUTH_SITE_URL is missing in your settings.py")

                              

example = TelegramThreading()
time.sleep(1)
