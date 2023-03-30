from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bbsnote.models import Board, Comment

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")  # 회원가입시 필수요건 

    class Meta:
        model = User
        fields = ("username", "email") # 튜플형식인 이유는 아이디와 비밀번호 값이 바뀌면 안되므로

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용'
        }        