from django.db import models

# Create your models here.
# nps/models.py

class TargetAudience(models.Model):
    name = models.CharField(max_length=255)
    
class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_audience = models.ManyToManyField(TargetAudience)

    def __str__(self):
        return self.title   



class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Add other user-related fields as needed

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    # Add other question-related fields as needed

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    # Add other response-related fields as needed

class Score(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE)
    nps_score = models.IntegerField()
    # Add other score-related fields as needed

class Analytics(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    # Add fields to store analytics data
    # e.g., average NPS, trends, sentiment analysis results, etc.

class SpamReport(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    # Add other fields as needed

class FeedbackLoop(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    # Add fields for dynamic adjustments and improvements
