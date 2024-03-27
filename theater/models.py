from django.contrib.auth.models import User
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        ordering = "second_name"


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = "name"


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        ordering = "title"


class TheaterHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = "name"


class Performance(models.Model):
    show_time = models.DateTimeField()
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performances"
    )
    theater_hall = models.ForeignKey(
        TheaterHall,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    def __str__(self):
        return f"{self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return f"{self.created_at}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    def __str__(self):
        return f"{self.row} {self.seat}"
