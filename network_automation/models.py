from django.db import models

# Create your models here.

class Device(models.Model):

    # membuat field
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # membuat choice atau pilihan
    VENDOR_CHOICES = [
        ('mikrotik', 'mikrotik'),
        ('cisco', 'cisco')
    ]

    # membuat field berdasarkan choice
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)

    # menampilkan label hostname + ip_address
    def __str__(self):
        return "{} - {}".format(self.hostname, self.ip_address)
        
