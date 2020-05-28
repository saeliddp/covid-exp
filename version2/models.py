from django.db import models
import datetime
# Create your models here.
class Respondent(models.Model):
    # primary key will be autogenerated
    age = models.CharField(max_length=50, default="None") # since age is a range
    gender = models.CharField(max_length=50, default="None")
    education = models.CharField(max_length=50, default="None")
    ip_addr = models.CharField(max_length=50, default="0.0.0.0")
    mturk_id = models.CharField(max_length=50, default="None")
    browser = models.CharField(max_length=70, default="None")
    curr_q = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.age + ", " + self.gender + ", " + self.education
    
class Algorithm(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Query(models.Model):
    # the name of the query (i.e. 'women's world cup')
    query_name = models.CharField(max_length=100)
    # this id of the query in the txt files
    # there is no query with id 0
    query_id = models.PositiveSmallIntegerField(default=0)
    num_fake = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.query_name
    
class Response(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    chosen_alg = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="chosen")
    unchosen_alg = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="unchosen")
    # if we want to store more accurate time data, change this
    time_elapsed = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return "Query: " + self.query.query_name + "Choice: " + self.chosen_alg.name
    
    

    