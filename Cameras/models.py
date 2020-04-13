from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import requests
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger('cameras_app')
logger.setLevel(logging.DEBUG)
file_log = logging.FileHandler('cameras.log')
file_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)

logger.addHandler(file_log)
logger.addHandler(ch)

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
    def get_class_safe_name(self):
        return self.name.replace(" ", "-")

    def get_absolute_url(self):
        return reverse('cameras:school_detail', args=[self.id])

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
    room = models.CharField(max_length=32, db_index=True)
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
        max_length=1000,
        blank=True,
        help_text="This is the Username of the Camera. If first creating camera, you can ignore. It will be pre-filled."
        )
    password = models.CharField(
        max_length=1000,
        blank=True,
        help_text="This is the Password of the Camera. If first creating camera, you can ignore. It will be pre-filled."
        )
    slug = models.SlugField(editable=False)
    online = models.BooleanField(editable=False, default=False)

    def get_absolute_url(self):
        pass
    def open(self):
        if (self.model.controlable_device):
            r = requests.get(f"http://{self.ip_address}{self.model.openCommand}", auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return True
            else:
                return False

        return True


    def close(self):
        if (self.model.controlable_device):
            r = requests.get(f"http://{self.ip_address}{self.model.closeCommand}", auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return True
            else:
                return False

        return True

    def check_online(self):
        try:
            r = requests.get(f"http://{self.ip_address}", timeout=2)
            r.raise_for_status()
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            logger.error(f"Attempted Health Check to {self.__str__()} ({self.ip_address}) failed.")
            self.online = False
            return False
        except(requests.exceptions.HTTPError):
            logger.debug(f"Attempted Health Check to {self.__str__()} ({self.ip_address}) resulted in code: {r.status_code}")
            self.online = False
            return False
        else:
            logger.debug(f"Attempted Health Check to {self.__str__()} ({self.ip_address}) succeeded with status code: {r.status_code}")
            self.online = True
            return True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        if not self.username:
            self.username = self.model.username
        if not self.password:
            self.password = self.model.password
        self.check_online()



        super(Camera, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.school}_{self.room}"





