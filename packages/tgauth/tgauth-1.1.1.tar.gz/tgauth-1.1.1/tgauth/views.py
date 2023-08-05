# Create your views here
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tgauth.exceptions import MissingParameter
from tgauth.models import TempTelegramUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
import uuid
import random
import string
from md5 import md5
from django.http import HttpResponse, HttpResponseRedirect
from tgauth.models import TelegramKey
from django.shortcuts import render_to_response

tg_uname = getattr(settings,'TGAUTH_BOT_USERNAME','') ## Telegram Bot usernaamae
tg_token = getattr(settings,'TGAUTH_TOKEN','') ## Telegram Bot toekn

'''
Creating the unique code for authenticatin 
'''

def get_unique_code():
	char_set = string.ascii_uppercase + string.digits
	unique_code = ''.join(random.sample(char_set*6, 24))

	return unique_code

''' Main function '''

def tgauth(request):
	''' 
	Checking the 'USERNAME' and 'BOT TOKEN ' is there in settings.py 
	'''

	if not tg_uname and tg_token:
		raise(MissingParameter,'Telegram bot username or Telegram bot token')
	unique_code = get_unique_code()
	telegram_key = TelegramKey()
	telegram_key.unique_key = unique_code
	telegram_key.save()
	authenticatoin_url = "https://telegram.me/"+str(tg_uname)+"?start="+str(telegram_key.unique_key)
	return HttpResponseRedirect(authenticatoin_url)
@csrf_exempt
def otptg(request,otp_telegram):

	if not request.POST:
		try:
			otp = TempTelegramUser.objects.get(activation_key=otp_telegram)
		except TempTelegramUser.DoesNotExist:
			raise ValueError ('activation key is not found')
		if otp :
			return render_to_response('tglogin.html', {"name":otp.tuser.first_name,'activekey':otp.activation_key})
	else:
		try:
			otp = TempTelegramUser.objects.get(activation_key=otp_telegram)
			rp = request.POST.get
			if rp('otpkey') and rp('activekey'):
				try:
					telegram = TempTelegramUser.objects.get(activation_key=rp('activekey'),random_pwd=rp('otpkey'))
				except TempTelegramUser.DoesNotExist:
					return render_to_response('tglogin.html', {"name":otp.tuser.first_name,'activekey':otp.activation_key,'error':" Activation key and OTP password mismatching please try again"})

				user=authenticate(username=telegram.tuser.username)
				if user:
					login(request,user)
					tg_succes_url = getattr(settings, 'TG_SUCCESS_URL', '')
					if  tg_succes_url:
						return HttpResponseRedirect(sauth_after_auth_url)
					else:
						return HttpResponseRedirect(reverse('telegramsuccess'))
		except TempTelegramUser.DoesNotExist:
			raise ValueError ('activation key is not found')



@login_required
def telegramsuccess(request):
	output = '''
	<html>
		<head>
			<title> Authentication successfull </title>
		</head>
		<body>
		<h1> Hi {0} successfully authenticated  with {1}</h1>

		</body>
	</html>'''.format(request.user.first_name,"Telegram Messenger")

	return HttpResponse(output)



