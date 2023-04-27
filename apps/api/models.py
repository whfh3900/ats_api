from django.db import models

# Create your models here.

class Tagghist(models.Model):
    id = models.AutoField(primary_key=True)
    CORP_ID = models.CharField(max_length=20)
    MODEL_ID = models.CharField(max_length=30)
    UPLD_FILE_NM =  models.CharField(max_length=50)
    REG_DT = models.DateTimeField()
    
    def __str__(self):
        return self.id
