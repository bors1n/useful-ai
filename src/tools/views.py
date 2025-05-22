from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from .models import Tools, Favorite, Comment
from .forms import CommentForm

def tool_detail(request, slug):
    tool = get_object_or_404(Tools, slug=slug)
    is_favorite = False
    
    # Check if the tool is favorited by the current user
    if request.user.is_authenticated:
        is_favorite = tool.is_favorited_by(request.user)

    comments = tool.comments.all() # get comments related to the tool
    comment_count = comments.count() #get number of comments
    form = CommentForm() # initialize the comment form 

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.tools = tool
                comment.user = request.user
                comment.save()
                return redirect('tool_detail', slug=slug)
        else:
            return redirect('login')
    
    context = {
        'tool': tool,
        'is_favorite': is_favorite,
        'comments': comments,
        'comment_count': comment_count,
        'form': form,
    }
    return render(request, 'tool_detail.html', context)



@login_required
def toggle_favorite(request, tool_id):
    """Add/remove a tool from user's favorites"""
    tool = get_object_or_404(Tools, id=tool_id)
    user = request.user
    
    # Check if the tool is already favorited
    favorite, created = Favorite.objects.get_or_create(user=user, tool=tool)
    
    # If it was already favorited and not newly created, delete it
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    # If it's an AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_favorite': is_favorite
        })
    
    # Otherwise redirect back to the tool detail page
    return redirect(reverse('tool_detail', kwargs={'slug': tool.slug})) 

