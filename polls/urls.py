from django.conf.urls import url 

from . import views

app_name = 'polls'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^(?P<new_feed>[0-9]+)/$', views.home, name='home'),
	url(r'^question/(?P<question_id>[0-9]+)/$', views.detail, name='details'),
	url(r'^new_question/$', views.new_question, name='newquestion'),
	url(r'^new_answer/(?P<question_id>[0-9]+)/$', views.new_answer, name='newanswer'),
	url(r'^new_comment/(?P<answer_id>[0-9]+)/$', views.new_comment, name='newcomment'),
	url(r'^follow/(?P<question_id>[0-9]+)/$', views.follow, name='follow'),
	url(r'^accept/(?P<answer_id>[0-9]+)/$', views.accept, name='accept'),
	url(r'^vote/(?P<answer_id>[0-9]+)/$', views.vote, name='vote'),
	url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
	url(r'^profile/(?P<user_id>[0-9]+)/answers/$', views.user_answers, name='useranswers'),
	url(r'^profile/(?P<user_id>[0-9]+)/follows/$', views.user_follows, name='userfollows'),
	url(r'^category/(?P<category>\w+)/$', views.category, name='category'),
	url(r'^search/$', views.search, name="search")
]