from django.db import models
from django.urls import reverse

class School(models.Model):
    name = models.CharField(
        max_length=160,
        unique=True, 
        blank=False
        )
    technician = models.ForeignKey(
        'Auth.User',
        models.CASCADE,
        related_name='schools'
    )

    def get_absolute_url(self):
        pass
        # return reverse('school_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class CameraModel(models.Model):
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=64)

    controlable_device = models.BooleanField(
        verbose_name='is camera controllable?',
        name='is_controllable',
        default=True,
        help_text="Does this model have a moving iris?"
    )
    
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)


    openCommand = models.CharField(
        verbose_name="Url to Open Camera",
        help_text="Include beginning / character. For example: /cgi-bin/open",
        max_length = 140,
        blank=True
    )
    closeCommand = models.CharField(
        verbose_name="Url to Close Camera",
        help_text="Include beginning / character. For example: /cgi-bin/close",
        max_length = 140,
        blank=True
    )
    getCameraUrl = models.CharField(
        verbose_name="Url to get camera image",
        help_text="Include beginning / character. For example: /cgi-bin/camera",
        max_length = 140,
        blank=True
    )

    
     
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
    ip_address = models.GenericIPAddressField(
        protocol='IPv4', 
        help_text="This is the IP Address of the Camera"
        )

    username = models.CharField(
        max_length=1000
        )
    password = models.CharField(
        max_length=1000
        )

    class Meta:
        indexes = [models.Index(fields=['room'])]

    def get_absolute_url(self):
        pass

    def __str__(self):
        return f"{self.school}_{self.room}"

