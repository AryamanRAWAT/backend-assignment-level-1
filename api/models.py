from django.db import models

# Table to store user details
class user_details(models.Model):
    id = models.IntegerField(primary_key=True) #This column can be removed as django already provides an id column.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70,null=True)    #with null=True user is not required to fill this field.
    age = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    email = models.CharField(max_length=50,unique=True)
    web = models.CharField(max_length=50)

    class Meta:
        unique_together = ('id', 'first_name',)         #the combination of fields 'id' and 'first_name', ensuring uniqueness for pairs of values across the table.