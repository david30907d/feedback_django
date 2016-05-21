from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
import random

# Create your views here.
User = get_user_model()

def lottery(request):
	u = User.objects.all()
	length = len(u)
	arr = list(range(length))
	random.shuffle(arr)
	print(arr)
	UserQuerySet = []
	for i in arr:
		UserQuerySet.append(u[i])
	return render_to_response('get_feedback/lottery.html', locals())