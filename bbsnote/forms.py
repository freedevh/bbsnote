from django import forms # 장고로부터 임포트
from bbsnote.models import Board, Comment

class BoardForm(forms.ModelForm): #모델폼을 상속받을게
    class Meta:
        model = Board
        fields = ['subject', 'content']
        # widgets = {
        #    'subject' : forms.TextInput(attrs={'class':'form-control'}),
        #    'content' : forms.Textarea(attrs={'class':'form-control','rows':10}),
        # }
        # labels = {
        #     'subject':'제목',
        #     'content':'내용',
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용'
        }        