from django.db import models
import django 
import datetime
from datetime import datetime,timedelta
from django.contrib.auth.models import User


## Key Model
class TelegramKey(models.Model):
	unique_key = models.CharField(max_length=200,verbose_name='Unique Key',null=True,blank=True)
	expiry_date = models.DateTimeField(verbose_name='Expiry Date',blank=True,null=True)

	def save(self, *args, **kwargs):
		if not 'force_insert' in kwargs:
			kwargs['force_insert'] = False
		if not 'force_update' in kwargs:
			kwargs['force_update'] = False
		if self.id:
			self.expiry_date = datetime.datetime.now()+timedelta(seconds=600)
		else:
			pass
		super(TelegramKey,self).save()

	if django.get_version() < 1.7:
		def __unicode__(self):
			return str(self.unique_key)
	else:
		def __str__(self):
			return str(self.unique_key)
	class Meta:
			verbose_name_plural=u'Unique Key'


class TempTelegramUser(models.Model):
	tuser = models.ForeignKey(User)
	activation_key = models.CharField(max_length=150,null=True,blank=True)
	random_pwd = models.CharField(max_length=10,null=True,blank=True)
	expiry_date = models.DateTimeField(verbose_name='Expiry Date',blank=True,null=True)

	def save(self, *args, **kwargs):
		if not 'force_insert' in kwargs:
			kwargs['force_insert'] = False
		if not 'force_update' in kwargs:
			kwargs['force_update'] = False
		if self.id:
			self.expiry_date = datetime.now()+timedelta(seconds=3600)
		else:
			pass
		super(TempTelegramUser,self).save()

	if django.get_version() < 1.7:
		def __unicode__(self):
			return str(self.tuser.username)
	else:
		def __str__(self):
			return str(self.tuser.username)
	class Meta:
			verbose_name_plural=u'OTP Login'










