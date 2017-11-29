from django import forms

from .models import Question, Answer, Comment
from django.conf import settings 

class QuestionForm(forms.ModelForm):
	# category = forms.Select(choices = settings.CATEGORIES)
	class Meta:
		model = Question
		fields = ['content', 'category']
		labels = {'content' : '', 'category' : 'Category'}
		widgets = {'content': forms.Textarea(attrs={'class' : 'form-control', 'rows' : 5, 'placeholder' : 'Ask something plz :('}), 
					'category': forms.Select(choices = [(c, c) for c in settings.CATEGORIES])}

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content']
		labels = {'content' : ''}
		widgets = {'content' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 5, 'placeholder' : 'Help me, pls :)!'})}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
		labels = {'content' : ''}
		widgets = {'content' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 1, 'placeholder' : 'Reply...'})}