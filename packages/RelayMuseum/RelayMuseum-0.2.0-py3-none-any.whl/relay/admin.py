from django.contrib import admin

from relay.models import *

class RingInline(admin.TabularInline):
    model = Ring
    fk_name = 'relay'
    max_num = 6

class RelayAdmin(admin.ModelAdmin):
    inlines = [RingInline,]
    ordering = ['pos', 'name']
    list_display = ('pos', 'name')
    list_display_links = ('pos', 'name')
admin.site.register(Relay, RelayAdmin)

class TorchFileInline(admin.TabularInline):
    model = TorchFile
    fk_name = 'torch'

class TorchAdmin(admin.ModelAdmin):
    inlines = [TorchFileInline]
    ordering = ['relay', 'ring', 'pos', 'language']
    list_display = ['relay', 'ring', 'pos', 'language', 'participant']
    list_display_links = ['pos', 'language', 'participant']
    list_filter = ['relay']
    save_on_top = True
    search_fields = ['^language__name', '^participant__name', '^participant__cals_user__profile__display_name']
admin.site.register(Torch, TorchAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cals_user')
admin.site.register(Participant, ParticipantAdmin)

class TorchFileAdmin(admin.ModelAdmin):
    model = TorchFile
    list_display = ['category', 'torch', 'filename', 'mimetype']
    list_filter = ['category', 'mimetype']
admin.site.register(TorchFile, TorchFileAdmin)

admin.site.register(Language)
