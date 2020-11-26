from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):

    poll_question  = models.TextField()
    option_number = models.IntegerField(default=2)
    poll_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.poll_question


class Options(models.Model):

    poll_id = models.ForeignKey(Poll,to_field='id',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.poll_id} {self.name}"


class PollVoted(models.Model):

    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    poll_id = models.ForeignKey(Poll,to_field='id',on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)


