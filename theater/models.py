from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        ordering = ["second_name"]


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        ordering = ["title"]


class TheaterHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Performance(models.Model):
    show_time = models.DateTimeField()
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE
    )
    theater_hall = models.ForeignKey(
        TheaterHall,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.play.title + " " + str(self.show_time)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        ordering = ["-created_at"]


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

    @staticmethod
    def validate_ticket(row, seat, theater_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, theater_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(theater_hall, theater_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {theater_hall_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.performance.theater_hall,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]
