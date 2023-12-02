from django.urls import path

from vote.views import (
    AdminVoteFormsListView,
    CreateVoteFormView,
    CreateVoteView,
    DeleteVoteView,
)

app_name = "vote"
urlpatterns = [
    path("create-form/", CreateVoteFormView.as_view(), name="create_form"),
    path("my-forms/", AdminVoteFormsListView.as_view(), name="my_forms"),
    # TODO: Add test
    path("create-vote/", CreateVoteView.as_view(), name="create_vote"),
    # TODO: Add test
    path("delete-vote/", DeleteVoteView.as_view(), name="delete_vote"),
]
