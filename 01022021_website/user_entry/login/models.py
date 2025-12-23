from django.db import models

# Create your models here.

class Node(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    node_id = models.CharField(primary_key=True, max_length=100)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node'


class SensorData(models.Model):
    sensor = models.OneToOneField('SensorInfo', models.DO_NOTHING, primary_key=True)
    sensor_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    receive_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sensor_data'
        unique_together = (('sensor', 'receive_time'),)


class SensorInfo(models.Model):
    sensor_id = models.CharField(primary_key=True, max_length=100)
    sensor_type = models.CharField(max_length=100, blank=True, null=True)
    node = models.ForeignKey(Node, models.DO_NOTHING, blank=True, null=True)
    depth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_info'


class SensorList(models.Model):
    sensor_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_list'


class SensorThresold(models.Model):
    sensor = models.OneToOneField(SensorInfo, models.DO_NOTHING, primary_key=True)
    min_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    max_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    last_email = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_thresold'


class UserList(models.Model):
    uname = models.CharField(max_length=100, blank=True, null=True)
    upassword = models.CharField(max_length=100, blank=True, null=True)
    ph_no = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.CharField(primary_key=True, max_length=100)
    user_type = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    verify = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_list'
