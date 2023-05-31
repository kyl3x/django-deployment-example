from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

	user = models.OneToOneField(User,on_delete=models.CASCADE) ##one to one field to match against the default User model
	#on_delete=models.CASCADE is required - not in the notes!
	# additional
	portfolio_site = models.URLField(blank=True) #blank=True means it doesn't need filling in by user
	profile_pic = models.ImageField(upload_to='profile_pics', blank=True) ##profile_pics = subdirectory

	def __str__(self):
		return self.user.username ##in case this needs printing
