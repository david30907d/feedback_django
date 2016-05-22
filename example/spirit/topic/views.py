# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from djconfig import config

from ..core.utils.paginator import paginate, yt_paginate
from ..core.utils.ratelimit.decorators import ratelimit
from ..category.models import Category
from ..comment.models import MOVED
from ..comment.forms import CommentForm
from ..comment.utils import comment_posted
from ..comment.models import Comment
from .models import Topic
from .forms import TopicForm
from . import utils
# below are imported by me
from django.utils import timezone # auto generate create time.
from get_feedback.models import Course,Course_feedback_Person
import decimal, json
from django.http.request import QueryDict


@login_required
@ratelimit(rate='1/10s')
def publish(request, category_id=None):
    if category_id:
        get_object_or_404(Category.objects.visible(),
                          pk=category_id)

    if request.method == 'POST':
        form = TopicForm(user=request.user, data=request.POST)
        cform = CommentForm(user=request.user, data=request.POST)

        if not request.is_limited and all([form.is_valid(), cform.is_valid()]):  # TODO: test!
            # wrap in transaction.atomic?
            topic = form.save()
            cform.topic = topic
            comment = cform.save()
            comment_posted(comment=comment, mentions=cform.mentions)
            return redirect(topic.get_absolute_url())
    else:
        form = TopicForm(user=request.user, initial={'category': category_id, })
        cform = CommentForm()

    context = {
        'form': form,
        'cform': cform
    }

    return render(request, 'spirit/topic/publish.html', context)


@login_required
def update(request, pk):
    topic = Topic.objects.for_update_or_404(pk, request.user)

    if request.method == 'POST':
        form = TopicForm(user=request.user, data=request.POST, instance=topic)
        category_id = topic.category_id

        if form.is_valid():
            topic = form.save()

            if topic.category_id != category_id:
                Comment.create_moderation_action(user=request.user, topic=topic, action=MOVED)

            return redirect(request.POST.get('next', topic.get_absolute_url()))
    else:
        form = TopicForm(user=request.user, instance=topic)

    context = {'form': form, }

    return render(request, 'spirit/topic/update.html', context)


def detail(request, pk, slug):
    topic = Topic.objects.get_public_or_404(pk, request.user)

    if topic.slug != slug:
        return HttpResponsePermanentRedirect(topic.get_absolute_url())

    utils.topic_viewed(request=request, topic=topic)

    comments = Comment.objects\
        .for_topic(topic=topic)\
        .with_likes(user=request.user)\
        .with_polls(user=request.user)\
        .order_by('date')

    comments = paginate(
        comments,
        per_page=config.comments_per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'topic': topic,
        'comments': comments,
    }
    
    # this part is for get_feedback

    if request.POST:
        data = request.POST.dict()
        context['course_object'] = post_feedback(data, slug, request.user)
    else:
        # This part is auto load statistic of course into Radar_chart!!
        context['course_object'] = auto_load_radarChart(slug)
        


    # This part is auto load statistic of course into Radar_chart!!

    return render(request, 'spirit/topic/detail.html', context)


def index_active(request):
    categories = Category.objects\
        .visible()\
        .parents()

    topics = Topic.objects\
        .visible()\
        .global_()\
        .with_bookmarks(user=request.user)\
        .order_by('-is_globally_pinned', '-last_active')\
        .select_related('category')

    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'categories': categories,
        'topics': topics
    }

    return render(request, 'spirit/topic/active.html', context)

######################### my function ###########################
@login_required
def auto_publish(request, category_id=3):
    with open("/home/david/htdocs/feedback_django/example/spirit/topic/json/O.json","r",encoding='UTF-8') as file:
        jsonContent = json.load(file)
        # print(jsonContent['course'][0])
        
        # <QueryDict: {'comment': ['fuck'], 'category': ['5'], 'csrfmiddlewaretoken': ['TrhHjnBCe5pAHjeSKGN4n3kbY3m7SvXh'], 'title': ['auto']}>
        jsondict = {'category': ['3'], 'comment': ['this is test'],
            'csrfmiddlewaretoken': ['TrhHjnBCe5pAHjeSKGN4n3kbY3m7SvXh'], 'title':  ['json works']}
        qdict = QueryDict('',mutable=True)
        qdict.update(jsondict)

    if category_id:
        get_object_or_404(Category.objects.visible(),
                          pk=category_id)

    form = TopicForm(user=request.user, data=qdict)
    cform = CommentForm(user=request.user, data=qdict)
    print(form)
    print(form.is_valid())
    print(cform.is_valid())
    if all([form.is_valid(), cform.is_valid()]):  # TODO: test!
        # wrap in transaction.atomic?
        topic = form.save()
        cform.topic = topic
        comment = cform.save()
        comment_posted(comment=comment, mentions=cform.mentions)
        return redirect(topic.get_absolute_url())

    context = {
        'form': form,
        'cform': cform
    }
    return render(request, 'spirit/topic/publish.html', context)

def post_feedback(post_data, slug, requestUser):
    modelDict = return_modelDict(slug) # return 會把slug的網址的'-'給切開，然後以school、name、professor當作primary key創model

    modelDict = gradeFormula(modelDict, post_data)

    # 因為要先存在這門課才可以post，所以就可以大膽的直接用get
    course_object = Course.objects.get(school=modelDict['school'],name=modelDict['name'],professor=modelDict['professor']) 
    record_attendee_of_Feedback(course_object, requestUser)
    course_object = accumulate_feedback(course_object, modelDict)

    return course_object

def gradeFormula(modelDict, post_data):
    modelDict['feedback_freedom'] = ( int(post_data['feedback_check_present_TrueFalse'])/4 + int(post_data['feedback_punish_present_TrueFalse'])*3/4 )
    modelDict['feedback_knowledgeable'] = ( int(post_data['feedback_learn']) + int(post_data['feedback_gpa']) ) / 2
    modelDict['feedback_GPA'] = ( int(post_data['feedback_gpa']) )
    modelDict['feedback_easy'] = ( int(post_data['feedback_easy'])*3/4 + int(post_data['feedback_loading'])/12 + int(post_data['feedback_test_amount'])/12 + int(post_data['feedback_test_hard'])/12  )
    modelDict['feedback_FU'] = ( int(post_data['feedback_atmosphere']) )
    return modelDict

def auto_load_radarChart(slug):
    modelDict = return_modelDict(slug)
    course_object, created = Course.objects.get_or_create(school=modelDict['school'],name=modelDict['name'],professor=modelDict['professor'],defaults=modelDict)
    return course_object

def accumulate_feedback(course_object, modelDict):
    course_object.feedback_amount = course_object.feedback_amount + 1
    tot = int( course_object.feedback_amount )
    course_object.feedback_freedom = round(( course_object.feedback_freedom*(tot-1) + modelDict['feedback_freedom'] )/tot, 2)
    course_object.feedback_knowledgeable = round(( course_object.feedback_knowledgeable*(tot-1) + modelDict['feedback_knowledgeable'] )/tot, 2)
    course_object.feedback_GPA = round(( course_object.feedback_GPA*(tot-1) + modelDict['feedback_GPA'] )/tot, 2)
    course_object.feedback_easy = round(( course_object.feedback_easy*(tot-1) + modelDict['feedback_easy'] )/tot, 2)
    course_object.feedback_FU = round(( course_object.feedback_FU*(tot-1) + modelDict['feedback_FU'] )/tot, 2)
    course_object.create = timezone.localtime(timezone.now()) # update the last post time

    course_object.save()
    return course_object

def return_modelDict(slug):
    slug = slug.split('-')
    modelDict = {
        'school' : slug[0],
        'name' : slug[1],
        'professor' : slug[2],
        'feedback_freedom' : 0,
        'feedback_knowledgeable' : 0,
        'feedback_GPA' : 0,
        'feedback_easy' : 0,
        'feedback_FU' : 0,
        'create':timezone.localtime(timezone.now())
    }
    return modelDict

def record_attendee_of_Feedback(course_object, requestUser):
    p = Course_feedback_Person.objects.create(Course_of_Feedback=course_object, Useremail=requestUser.email, create=timezone.localtime(timezone.now()))
    print(p.Course_of_Feedback)
#########################my function ###########################
