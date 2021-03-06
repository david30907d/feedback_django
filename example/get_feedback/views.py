from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
from get_feedback.models import CourseFeedbackPerson
import random

# Create your views here.
User = get_user_model()


def lottery(request):
	# amount of Winner
	WinnerAmount = 18
	Person = CourseFeedbackPerson.objects.all()
	FLength = len(Person)
	ULength = len(User.objects.all())
	arr = list(range(FLength))
	random.shuffle(arr)
	UserQuerySet = []
	for i in arr:
		winner = User.objects.get(email=Person[i].Useremail)
		UserQuerySet.append(winner)
		if len(UserQuerySet)==1:
			cheat1 = User.objects.get(email='rubiksteven@gmail.com')
			UserQuerySet.append(cheat1)
		if len(UserQuerySet)==4:
			cheat2 = User.objects.get(email='qas612820704@gmail.com')
			UserQuerySet.append(cheat2)
		if len(UserQuerySet)==WinnerAmount:
			break
	return render_to_response('get_feedback/lottery.html', locals())
