from django.views.generic import DetailView

from .models import StacksPage


class StacksPageDetailView(DetailView):
    queryset = StacksPage.objects.prefetch_related('sections')
    context_object_name = 'page'

    def get_template_names(self):
        """
        Returns the template associated with this StacksPage instance
        (as dictated by its `template_path` attribute)
        """
        obj = self.get_object()
        return [obj.template_path]

    def get_context_data(self, **kwargs):
        context = super(StacksPageDetailView, self).get_context_data(**kwargs)
        page_sections = [
            {
                'title_section': section.title_section,
                'order': section.order,
                'title_menu': section.title_menu,
                'slug': section.slug,
                'content': section.content.as_html(
                    extra_context={
                        'live_url': self.object.live_url,
                        'social_share_text': (
                            section.twitter_share_text or
                            self.object.twitter_share_text
                        ),
                        'page_slug': self.object.slug,
                        'page_pk': self.object.pk,
                        'section_slug': section.slug
                    }
                )
            }
            for section in self.object.sections.order_by('order')
        ]
        context.update({
            'page_sections': page_sections
        })
        return context
