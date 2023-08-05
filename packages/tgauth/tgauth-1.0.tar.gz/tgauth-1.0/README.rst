TgAuth [ Telegram Authentication ]

What is Telegram ?
=========================================================================

Telegram is a messaging app with a focus on speed and security, it’s super-fast, simple and free. You can use Telegram on all your devices at the same time — your messages sync seamlessly across any number of your phones, tablets or computers.
click this link for read more about Telegram. https://telegram.org/faq#q-what-is-telegram-what-do-i-do-here

What is Tgauth ? 
============================================================================

Tgauth is a package for authentication and authorization with Telegram Messenger. its provide the Token Based Authentication.

Dependencies
============================================================================

python requests module 
Create the Bot in telegram [ username and access token is needed ]

Dependency Package Installation
============================================================================

pip install requests

Demo Project
============================================================================

Click this link : https://tgauth.herokuapp.com/ 

Installation
============================================================================

From Pypi.
	
pip install tgauth
easy_install tgauth

From Github :
	
         clone tgauth from githib :  https://github.com/renjith-tring/tgauth
How It Works ?
============================================================================

Step by Step workflow

User click the Login With Telegram Button or http:// <site name> /tgauth/ ( eg: http://localhost:8000/tgauth/ )

Redirect to User Web version Telegram Account. ( http://www.awesomescreenshot.com/image/1064358/5a5e0e053c278d1cb88392460f75e7f3 )

Click the start Button in Telegram ( 
http://www.awesomescreenshot.com/image/1064361/2a3c3549174ab6c717d6e2d67e4f89ff
)
      4 . Click the link , it will redirect to the Server and ask for the Enter the OTP password
 (             http://www.awesomescreenshot.com/image/1064371/2954a708f030bfbc3b620f7cb0bb1d84
http://www.awesomescreenshot.com/image/1064373/a18a22e1a24cfad67b96f52df75d2298
)
      5. if user enter valid OTP it will redirect to the success page (
http://www.awesomescreenshot.com/image/1064376/1a3a43ccbd877c6be498702ebae6c58d
)


Configuration
============================================================================

Step 1 :

Settings.py 

TGAUTH_TOKEN = "*****************************************************" // token for your bot

TGAUTH_BOT_USERNAME = "********************************" // username for your bot

TG_AUTH_SITE_URL = "http://127.0.0.1:8000/" // site url like www.example.com 

TG_SUCCESS_URL = “ ” // redirect url after authentication , default it will display the dummy page with username after successful authentication

      5 . INSTALLED_APPS = (
                                                   'tgauth',
                                               )


Url.py 

 from django.conf.urls import patterns, include, url
 from django.views.generic import TemplateView
 from django.contrib import admin
 admin.autodiscover()
 urlpatterns = patterns('',

    url(r'^', include('tgauth.urls'))
  )


Step 2 :
python manage.py syncdb/migrate









	






