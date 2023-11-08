from django.conf import settings
from django.db import models


class VoteForm(models.Model):
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="vote_forms",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000, null=True, blank=True)
    statistics_type = models.PositiveSmallIntegerField(
        choices=((1, "Open"), (2, "Closed")), default=1
    )
    votes_type = models.PositiveSmallIntegerField(
        choices=((1, "Single choice"), (2, "Multiple choice")), default=1
    )

    # TODO: Add constraint: closing should be bigger then created
    closing = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    vote_fields: models.QuerySet["VoteFields"]
    votes: models.QuerySet["Votes"]

    class Meta:
        verbose_name = "VoteForm"
        verbose_name_plural = "VoteForms"

    def __str__(self):
        return f"Form: {self.name}"


class VoteFields(models.Model):
    form = models.ForeignKey(
        VoteForm,
        related_name="vote_fields",
        on_delete=models.CASCADE,
        blank=True,
    )
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=200, null=True, blank=True)

    votes: models.QuerySet["Votes"]

    class Meta:
        verbose_name = "VoteFields"
        verbose_name_plural = "VoteFields"

    def __str__(self):
        return f"Vote fields: {self.form} — {self.name}"


class Votes(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="votes",
        on_delete=models.CASCADE,
    )
    form = models.ForeignKey(
        VoteForm, related_name="votes", on_delete=models.CASCADE
    )
    # TODO: Add validation, so only defined in vote fields can be chosen.
    vote = models.ForeignKey(
        VoteFields,
        related_name="votes",
        on_delete=models.CASCADE,
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Votes"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"Vote: {self.vote}"
