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
from django.utils import timezone # auto generate create time.
from .models import Course
import decimal


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
        context['course_object'] = post_feedback(data)
    else:
        # This part is auto load statistic of course into Radar_chart!!
        context['course_object']= auto_load_radarChart(1)
        


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

#########################my function ###########################
@login_required
def auto_publish(request, category_id=4):
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

def post_feedback(post_data):
    models_dict = {
        'school' : 'NCHU',
        'name' : '演算法',
        'professor' : '范耀中',
        'create':timezone.localtime(timezone.now())
    }

    models_dict['feedback_freedom'] = ( int(post_data['feedback_check_present_TrueFalse'])*0.3 + int(post_data['feedback_punish_present_TrueFalse'])*0.7 )
    models_dict['feedback_knowledgeable'] = ( int(post_data['feedback_learn']) + int(post_data['feedback_gpa']) ) / 2
    models_dict['feedback_GPA'] = ( int(post_data['feedback_gpa']) )
    models_dict['feedback_easy'] = ( int(post_data['feedback_easy'])*0.7 + int(post_data['feedback_loading'])*0.1 + int(post_data['feedback_test_amount']) + int(post_data['feedback_test_hard'])*0.1  )
    models_dict['feedback_FU'] = ( int(post_data['feedback_atmosphere']) )

    # 如果有這門課的心得就get出來，沒有的話就先用這個人的評分存進db
    course_object, created = Course.objects.get_or_create(school='NCHU',name='演算法',professor='范耀中',defaults=models_dict) 
    course_object = accumulate_feedback(course_object, models_dict)

    return course_object

def auto_load_radarChart(pk):
    course_object = get_object_or_404(
        Course,pk=1
    )
    return course_object

def accumulate_feedback(course_object, models_dict):
    course_object.feedback_amount = course_object.feedback_amount + 1
    tot = int( course_object.feedback_amount )
    course_object.feedback_freedom = round(( course_object.feedback_freedom*(tot-1) + models_dict['feedback_freedom'] )/tot, 2)
    course_object.feedback_knowledgeable = round(( course_object.feedback_knowledgeable*(tot-1) + models_dict['feedback_knowledgeable'] )/tot, 2)
    course_object.feedback_GPA = round(( course_object.feedback_GPA*(tot-1) + models_dict['feedback_GPA'] )/tot, 2)
    course_object.feedback_easy = round(( course_object.feedback_easy*(tot-1) + models_dict['feedback_easy'] )/tot, 2)
    course_object.feedback_FU = round(( course_object.feedback_FU*(tot-1) + models_dict['feedback_FU'] )/tot, 2)
    course_object.save()
    return course_object

#########################my function ###########################
