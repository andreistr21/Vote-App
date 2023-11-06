from django.contrib import admin
from vote.models import VoteForm, Votes, VoteFields

admin.site.register(VoteForm)
admin.site.register(Votes)
admin.site.register(VoteFields)
