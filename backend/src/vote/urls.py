from django.urls import path

from vote.views import AdminVoteFormsListView, CreateVoteView, MakeVoteView

app_name = "vote"
urlpatterns = [
    path("create-form/", MakeVoteView.as_view(), name="create_form"),
    # TODO: Add test
    path("my-forms/", AdminVoteFormsListView.as_view(), name="my_forms"),
    # TODO: Add test
    path("create-vote/", CreateVoteView.as_view(), name="create_vote"),
]
