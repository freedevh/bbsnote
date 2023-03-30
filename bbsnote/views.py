from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def profile(request):
    return redirect('myProfile.html')
def index(request):
    # 입력인자
    page = request.GET.get('page', 1) #페이지값이 있으면 가져오고 없으면 1로 초기화
    # 조회
    board_list = Board.objects.order_by('-create_date') # http://127.0.0.1:8000/bbsnote/ = create_date에서 -를 빼면 위에서부터 작성한 순서대로 나열됨 -를 추가하면 반대임
    # 페이징 처리
    paginator = Paginator(board_list, 3)
    page_obj = paginator.get_page(page) # 12번줄의 page를 여기로 불러온다
    context = {'board_list': page_obj}
    # return HttpResponse("bbsnote에 오신 것을 환영합니다")
    return render(request, 'bbsnote/board_list.html', context)  

def detail(request, board_id):
    board = Board.objects.get(id=board_id) # (id=board_id) = select * from bbsnote_Board wher id=5
    context = {'board': board}
    return render(request, 'bbsnote/board_detail.html', context)  

@login_required(login_url='common:login')
def comment_create(request, board_id):
    if request.method == 'POST':
        board = Board.objects.get(id=board_id)
    # comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
    # comment.save()  # 20~21번 코드는 밑에 22번줄 코드와 같은 결과
        board.comment_set.create(content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
    #   return redirect('bbsnote:detail', board_id=board.id)   bbsnote:detail 으로 리다이렉트 
    return redirect('bbsnote:detail', board_id=board_id)

@login_required(login_url='common:login')
def board_create(request):
    if request.method == 'POST':  #요청 리퀘스트 들어왔는데 포스트로 왔으면
        form = BoardForm(request.POST) #리퀘스트.포스트를 보드리폼에 넘겨줘
        if form.is_valid():  #만약에 폼의 값이 있으면
            board = form.save(commit=False) # 실행은 시키되 저장은 아직 = 오토커밋 시키지마 잠깐 기다려라
            # board.create_date = timezone.now()  #이것은 없어도 게시글 저장에는 문제 없다
            board.author = request.user
            board.save()
            return redirect('index') # 저장 잘되있으면 bbsnote:index' 가라
    else:
        form = BoardForm() # forms.py의 class BoardForm
    return render(request, 'bbsnote/board_form.html', {'form':form})

@login_required(login_url='common:login')
def board_modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id) 
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False) # False 여서 완전이 아닌 임시저장
            board.author = request.user
            board.update_date = timezone.now()  # 수정일시 저장
            board.save()
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        form = BoardForm(instance=board) 
    context = {'form': form}
    return render(request, 'bbsnote/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:     # 작성자와 수정자가 다르면 밑에 삭제 권한이 없습니다 뜨게끔
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    board.delete()
    return redirect('bbsnote:index')

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다!")
        return redirect('bbsnote:detail', board_id=comment.board.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auahor = request.user
            comment.save()
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment':comment, 'form':form}
    return render(request, 'bbsnote/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=comment.board.id)
    comment.delete()
    return redirect('bbsnote:detail', board_id=comment.board.id)   