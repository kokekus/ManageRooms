from django.db import models

# Create your models here.
class RoomInfo(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    projector_available = models.BooleanField(default=False)

class RoomReservation(models.Model):
    room_id = models.ForeignKey(RoomInfo, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date')


