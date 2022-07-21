from django.db import models

class Video(models.Model):
    """ A model for storing video as well its attributes like video size, duration, extension and created date"""
    video = models.FileField()
    size = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField()
    extension = models.CharField(max_length=3)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.name