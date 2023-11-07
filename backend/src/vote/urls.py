from django.urls import path

from vote.views import MakeVoteView

app_name = "vote"
urlpatterns = [
    path("create-form/", MakeVoteView.as_view(), name="create_form"),
]
