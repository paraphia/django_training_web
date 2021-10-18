from django.shortcuts import render, get_object_or_404
from django.utils.timezone import activate
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #Модули для создани пагинации
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'
		
def post_list(request):
	objects_list = Post.published.all() 	 #Берем все записи из БД
	paginator    = Paginator(objects_list,2) #По 2 статьи на каждой странице
	page 		 = request.GET.get('page') 	 #берем GET параметр page 
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,'blog/post/list.html',{'page':page,'posts':posts})

def post_detail(request,year,month,day,post):
	post = get_object_or_404(Post,slug = post,publish__year = year,publish__month=month,publish__day=day)
	comments = post.comments.filter(active = True)
	new_comment = None
	if request.method == "POST":
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=True)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()
	return render(request,'blog/post/detail.html',{'post':post,'comment_form':comment_form,'comments':comments,'new_comment': new_comment})

def post_share(request,post_id):
	post = get_object_or_404(Post,id=post_id,status = 'published')
	sent = False
	if(request.method == 'POST'):
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			# Отправка электронной почты 
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recomends you reading {}'.format(cd['name'],cd['email'],post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
			send_mail(subject,message,'admin@email.ru',[cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html',{'post':post,'form': form,'sent':sent})