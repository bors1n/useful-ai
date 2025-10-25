from tools.models import Tools, Category, Suggestion
from tools.forms import SuggestionForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count # Import Count for popular sorting

def home(request):
    """Home page view."""
    # Get popular tools (sorted by votes)
    popular_tools = Tools.objects.annotate(favorite_count=Count('favorite')).order_by('-favorite_count', 'name')[:8]
    
    # Get new tools (sorted by date_added)
    new_tools = Tools.objects.all().order_by('-date_added')[:4]
    
    context = {
        'popular_tools': popular_tools,
        'new_tools': new_tools,
    }
    
    return render(request, 'home.html', context)


def tool_detail(request, slug):
    """Tool detail page view."""
    tool = Tools.objects.get(slug=slug)
    context = {
        'tool': tool,
    }
    return render(request, 'tool_detail.html', context)


def upvote_tool(request, slug):
    """Handle tool upvoting."""
    if request.method == 'POST':
        tool = Tools.objects.get(slug=slug)
        tool.votes += 1
        tool.save()
    return redirect('tool_detail', slug=slug)


def about(request):
    """View function for the about page."""
    return render(request, 'about.html')

def gallery(request):
    """View function for the gallery page with sorting and pagination."""
    sort_by = request.GET.get('sort_by', 'name') # Default to sorting by name

    if sort_by == 'newest':
        tools = Tools.objects.all().order_by('-date_added')
    elif sort_by == 'popular':
        # Annotate with favorite count and order by it
        tools = Tools.objects.annotate(favorite_count=Count('favorite')).order_by('-favorite_count', 'name') # Add secondary sort by name for ties
    elif sort_by == 'name_desc':
        tools = Tools.objects.all().order_by('-name')
    else: # Default to sort by name
        tools = Tools.objects.all().order_by('name')
    
    # Pagination
    paginator = Paginator(tools, 16)  # Show 16 tools per page
    page_number = request.GET.get('page', 1)
    tools = paginator.get_page(page_number)
    
    context = {
        'tools': tools,
        'current_sort': sort_by, # Pass current sort to template
    }
    
    return render(request, 'gallery.html', context)

def suggestion(request):
    """View function for the suggest tool page."""
    form = SuggestionForm()
    
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.save()
            return redirect('home')
    
    context = {
        'form': form,
    }

    return render(request, 'suggest_tool.html', context)