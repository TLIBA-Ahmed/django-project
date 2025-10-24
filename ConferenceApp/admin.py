from django.contrib import admin

# Register your models here.
from .models import Conference, OrganizingCommittee, Submission
class submissionInline(admin.StackedInline):
    model = Submission
    extra = 1
    exclude=('submission_date',)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('conference_id', 'name', 'start_date', 'end_date', 'location')
    search_fields = ('name', 'theme', 'location')
    list_filter = ('theme', 'location', 'start_date', 'end_date')
    ordering = ('-start_date',)
    inlines = [submissionInline]

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'conference', 'submission_date','status')
    search_fields = ('title', 'user__first_name', 'user__last_name', 'conference__name')
    list_filter = ('conference', 'submission_date')
    ordering = ('-submission_date',)

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(OrganizingCommittee)
admin.site.register(Submission, SubmissionAdmin)