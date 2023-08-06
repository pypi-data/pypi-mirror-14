from django.contrib import admin

from .admin_actions import stackspage_admin_actions
from .models import StacksPage, StacksPageSection


class StacksPageSectionInline(admin.StackedInline):
    model = StacksPageSection
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': (
                ('order', 'title_section'),
                ('title_menu', 'slug'),
                ('twitter_share_text',),
                ('content',)
            )
        }),
    )
    extra = 1
    prepopulated_fields = {"slug": ("title_menu",)}


def get_template_path_display(obj):
    """Enable 'Template' list_display to display properly."""
    return obj.get_template_path_display()

get_template_path_display.short_description = 'Template'


class StacksPageAdmin(admin.ModelAdmin):
    actions = stackspage_admin_actions
    fieldsets = (
        ('Page Meta', {
            'fields': (
                ('title', 'slug'),
                ('description', 'twitter_share_text', 'keywords'),
                ('canonical_image',),
                ('template_path',),
                ('publish',)
            )
        }),
    )
    publish_fieldsets = fieldsets + ((
        'Set Publish URL', {
            'fields': (
                ('live_url',),
            )
        }
    ),)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [StacksPageSectionInline]
    list_display = [
        'title',
        get_template_path_display,
        'live_url',
        'publish'
    ]
    save_as = True

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser or request.user.has_perm(
            'stacks_page.can_set_stacks_page_url'
        ):
            return self.publish_fieldsets
        return super(StacksPageAdmin, self).get_fieldsets(request, obj)

admin.site.register(StacksPage, StacksPageAdmin)
