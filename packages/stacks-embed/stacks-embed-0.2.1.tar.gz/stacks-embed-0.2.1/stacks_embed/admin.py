from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import StacksEmbed, StacksEmbedList, StacksEmbedListEmbed


class StacksEmbedAdmin(TextPlusStuffRegisteredModelAdmin):
    list_display = (
        'name',
        'display_title',
        'canonical_url',
        'service',
        'date_created'
    )
    list_filter = ('service',)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during video creation
        """
        exclude = None
        fields = '__all__'
        if obj is None:
            fields = ('canonical_url',)
        else:
            exclude = ('service', 'id_on_service')
        kwargs.update({'exclude': exclude, 'fields': fields})
        return super(StacksEmbedAdmin, self).get_form(request, obj, **kwargs)


class StacksEmbedListEmbedInline(admin.StackedInline):
    model = StacksEmbedListEmbed
    exclude = ('embeds',)


class StacksEmbedListAdmin(TextPlusStuffRegisteredModelAdmin):
    inlines = [StacksEmbedListEmbedInline]
    list_display = ('name', 'display_title', 'date_created', 'date_modified')

admin.site.register(StacksEmbed, StacksEmbedAdmin)
admin.site.register(StacksEmbedList, StacksEmbedListAdmin)
