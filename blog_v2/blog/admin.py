from django.contrib import admin
from .models import Post, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name','email','post','created','active')
	list_filter  =  ('active','created','updated')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','slug','publish')
	list_filter = ('publish',)
	search_fields = ('title','body')
	prepopulated_fields = {'slug':('title',)} #Автоматически создает ЧПУ (friendly urls)
