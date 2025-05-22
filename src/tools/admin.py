from django.contrib import admin
from .models import Tools, Category, ContentImage, Comment, Suggestion

@admin.register(Tools)
class ToolsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date_added')
    list_filter = ('categories', 'date_added')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('tools', 'user', 'created_at')
    search_fields = ('tools__name', 'user__username')
    list_filter = ('tools', 'user', 'created_at')
    ordering = ('-created_at',)

    actions = ['delete_selected_comments']

    def delete_selected_comments(self, request, queryset):
        """Custom action to delete selected comments."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} comments were successfully deleted.")
    delete_selected_comments.short_description = "Delete selected comments"

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('tool_name', 'created_at')
    search_fields = ('tool_name', 'back_email')

    
