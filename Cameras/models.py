from django.db import models
from django.urls import reverse

# Create your models here.


class School(models.Model):
    name = models.CharField(unique=True, blank=False)

    def get_absolute_url(self):
        pass
        # return reverse('school_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class CameraModel(models.Model):
     manufacturer = models.CharField(max_length=64)
     model = models.CharField(max_length=64)

    def get_absolute_url(self):
        pass

     
    def __str__(self):
        return f"{self.manufacturer} - {self.model}"


class Camera(models.Model):
    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE,
        related_name='cameras'
        )
    room = models.CharField(max_length=32)
    model = models.ForeignKey(
        CameraModel,
        on_delete=models.CASCADE,
        related_name='cameras'
    )

    class Meta:
        indexes = [models.Index(fields=['room'])]

    def get_absolute_url(self):
        pass

    def __str__(self):
        return f"{self.school}_{self.room}"

