# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.template import loader
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import *
from .forms import *
# Create your views here.

def home(request, new_feed='0'):
	""" Render a homepage """
	tops = Answer.objects.values('user__username', 'user__id').annotate(answer_num=Count('user_id')).order_by('-answer_num')[:3]
	top_users = [(top['user__username'], top['user__id']) for top in tops]
	# questions = [1, 2, 3, 4, 5]
	questions = []
	answers = []
	if new_feed == '0':
		questions = Question.objects.annotate(follow_num = Count('followers')).order_by('-follow_num')
	elif new_feed == '1':
		questions = Question.objects.order_by('-time')
	else:
		answers = Answer.objects.values('content', 'time', 'user__username', 'question__content', 'question__id', 'user__id', 'question__category').annotate(vote_num = Count('voters')).order_by('-vote_num')
	return render(request, 'polls/home.html', context = {'top_users' : top_users, 'questions' : questions, 'new_feed' : new_feed, 'answers' : answers})

@login_required
def new_question(request):
	"""Add a new question. """
	if request.method != 'POST':
		# No data. Create a blank form
		form = QuestionForm()
	else:
		# Data submitted; process data
		form = QuestionForm(request.POST)
		if form.is_valid():
			new_ques = form.save(commit=False)
			new_ques.time = timezone.now()
			new_ques.user = request.user
			new_ques.save()
			return HttpResponseRedirect(reverse('polls:details', args=[new_ques.id]))
	context = {'form': form}
	return render(request, 'polls/new_question.html', context)

@login_required
def detail(request, question_id):
	template_name = 'polls/details.html'
	try:
		question = Question.objects.get(id=question_id)
		answers = Answer.objects.filter(question=question).order_by('-accepted','-time')
		comments = []
		votes = []
		follow = "Follow"
		if request.user in question.followers.all():
			follow = "Unfollow"
		follow_num = len(question.followers.all())
		for answer in answers:
			if request.user in answer.voters.all():
				votes.append((answer.id, 'Unvote', len(answer.voters.all())))
			else:
				votes.append((answer.id, 'Vote', len(answer.voters.all())))
			for comment in Comment.objects.filter(answer=answer):
				comments.append(comment)
	except:
		raise Http404("Question does not exist")
	context = {'question': question, 'answers' : answers, 'num' : len(answers), 'myform': AnswerForm(), 'comments': comments, 
				'cmtform' : CommentForm(), 'follow' : follow, 'follow_num' : follow_num, 'votes' : votes}
	return render(request, template_name, context)

@login_required
def new_answer(request, question_id):
	"""Add an answer"""
	question = Question.objects.get(id=question_id)
	if request.method != 'POST':
		# No data. Create a blank form
		form = AnswerForm()
	else:
		# Data submitted; process data
		form = AnswerForm(request.POST)
		if form.is_valid():
			new_ans = form.save(commit=False)
			new_ans.time = timezone.now()
			new_ans.accepted = False
			new_ans.question = question
			new_ans.user = request.user
			new_ans.save()
			return HttpResponseRedirect(reverse('polls:details', args=[question_id]))
	context = {'form' : form}
	return render(request, 'polls/new_answer.html', context)	

@login_required
def new_comment(request, answer_id):
	answer = Answer.objects.get(id=answer_id)
	if request.method != 'POST':
		form = CommentForm()
	else:
		form = CommentForm(request.POST)
		if form.is_valid():
			new_cmt = form.save(commit=False)
			new_cmt.time = timezone.now()
			new_cmt.user = request.user
			new_cmt.answer = answer
			new_cmt.save()
			return HttpResponseRedirect(reverse('polls:details', args=[answer.question_id]))
	context = {'form' : form}
	return render(request, 'polls/new_comment.html', context)

@login_required
def follow(request, question_id):
	question = Question.objects.get(id=question_id)
	if not request.user in question.followers.all():
		question.followers.add(request.user)
	else:
		question.followers.remove(request.user)
	return HttpResponseRedirect(reverse('polls:details', args=[question_id]))

@login_required
def vote(request, answer_id):
	answer = Answer.objects.get(id=answer_id)
	question_id = answer.question_id
	if not request.user in answer.voters.all():
		answer.voters.add(request.user)
	else:
		answer.voters.remove(request.user)
	return HttpResponseRedirect(reverse('polls:details', args=[question_id]))

@login_required
def profile(request, user_id):
	asked_questions = Question.objects.filter(user__id = user_id)
	user = User.objects.get(id = user_id)
	context = {'asked_questions' : asked_questions, 'user_id' : int(user_id), 'target_user' : user}
	return render(request, 'polls/profile.html', context)

@login_required
def user_answers(request, user_id):
	answers = Answer.objects.values('content', 'time', 'user__username', 'question__content', 'question__id', 'user__id', 'question__category').filter(user__id = user_id)
	# aqs = [(answer, Question.objects.get(id = answer.question_id)) for answer in answers]
	user = User.objects.get(id = user_id)
	context = {'answers': answers, 'user_id' : int(user_id), 'target_user' : user}
	return render(request, 'polls/user_answers.html', context)

@login_required
def user_follows(request, user_id):
	fl_questions = Question.objects.filter(followers = user_id)
	user = User.objects.get(id = user_id)
	context = {'fl_questions' : fl_questions, 'user_id' : int(user_id), 'target_user' : user}
	return render(request, 'polls/user_follows.html', context)

@login_required
def category(request, category):
	questions = Question.objects.filter(category=category)
	context = {'category' : category, 'questions' : questions}
	return render(request, 'polls/category.html', context)

@login_required
def search(request):
	keyword = request.POST['keyword']
	questions = []
	if keyword:
		questions = Question.objects.filter(content__contains=keyword)
	context = {'keyword' : keyword, 'questions' : questions}
	return render(request, 'polls/search.html', context)

@login_required
def accept(request, answer_id):
	answer = Answer.objects.get(id = answer_id)
	if answer.accepted:
		answer.accepted = False
	else:
		accepteds = Answer.objects.filter(accepted=True, question=answer.question_id)
		for ans in accepteds:
			ans.accepted = False
			ans.save()
		answer.accepted = True
	answer.save()
	return HttpResponseRedirect(reverse('polls:details', args=[answer.question_id]))

@login_required
def edit_profile(request, user_id):
	user = User.objects.get(id = user_id)
	error = False
	if request.user != user:
		error = True
	else:
		print ("YEAHHHHADSFADSFSD")
		if request.method != 'POST':
			# No data. Create a blank form
			profile_form = ProfileForm()
		else:
			# Data submitted; process data
			profile_form = ProfileForm(request.POST, instance=request.user.profile)
			if profile_form.is_valid():
				profile_form.save()
				return HttpResponseRedirect(reverse('polls:profile', args=[user_id]))
	context = {'error' : error, 'profile_form' : profile_form}
	return render(request, 'polls/edit_profile.html', context)