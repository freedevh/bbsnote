from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):  # 게시글 모델
    subject = models.CharField(max_length=200) # 문자열필드(CharField) 형태로 최대 길이 200자로 제한
    content = models.TextField() # 텍스트 필드
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True) # 날짜/시간 필드 / 객체가 처음 생성될 때 자동으로 현재 날짜/시간으로
    update_date = models.DateTimeField(auto_now=True) # 날짜/시간 필드 / 객체가 저장될 때마다 현재 날짜/시간으로 설정

    def __str__(self):
        return f'[{self.id}] {self.subject}' # Board를 불러올때, [id][제목] 형태로 객체를 출력

class Comment(models.Model): # 댓글 모델
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # like = models.IntegerField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f'[{self.board.id}:{self.board.subject} ] {self.content}'