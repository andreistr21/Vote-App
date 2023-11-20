from django.urls import path

from vote.views import AdminVoteFormsListView, MakeVoteView

app_name = "vote"
urlpatterns = [
    path("create-form/", MakeVoteView.as_view(), name="create_form"),
    path("my-forms/", AdminVoteFormsListView.as_view(), name="my_forms"),
]
