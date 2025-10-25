from django.db import models
from datetime import date

# Create your models here.
class userdetails(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16)


class admindetails(models.Model):
    adminfullname = models.CharField(max_length=30)
    adminemail = models.EmailField(max_length=30)
    adminusername = models.CharField(max_length=20)
    adminpassword = models.CharField(max_length=16)


class studentdetails(models.Model):
    studentname = models.CharField(max_length=30)
    coursename = models.CharField(max_length=30)
    startdate = models.DateField()
    enddate = models.DateField()
    hoursspent = models.FloatField()  # since you allow decimal like 12.5
    completion = models.IntegerField()  # percentage (0–100)
    status = models.CharField(
        max_length=20,
        choices=[('Ongoing', 'Ongoing'),
                 ('Completed', 'Completed'),
                 ('Not Started', 'Not Started')]
    )

    def course_duration(self):
        return (self.enddate - self.startdate).days

    def is_completed(self):
        return self.status == "Completed"

    def progress_rate(self):
        total_days = self.course_duration()
        if total_days == 0:
            return 0
        remaining_days = (self.enddate - date.today()).days
        return round(100 * (1 - remaining_days / total_days), 2)
   


class Notification(models.Model):
    student = models.ForeignKey(userdetails, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)




# New Course model
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def total_students(self):
        return studentdetails.objects.filter(coursename=self.name).count()

    def completed_students(self):
        return studentdetails.objects.filter(coursename=self.name, status='Completed').count()

    def completion_rate(self):
        total = self.total_students()
        completed = self.completed_students()
        return round((completed / total) * 100, 2) if total > 0 else 0


# New Quiz model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course.name}: {self.question}"




# models.py
class QuizAttempt(models.Model):
    student = models.ForeignKey(userdetails, on_delete=models.CASCADE)
    coursename = models.CharField(max_length=100)
    score = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now=True)





class CourseVideo(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    # Optionally: add a duration/description field
    class Meta:
        verbose_name = 'Course Video'
        verbose_name_plural = 'Course Videos'

    def __str__(self):
        return f"{self.course.name} - {self.title}"



class VideoProgress(models.Model):
    student = models.ForeignKey(userdetails, on_delete=models.CASCADE)
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'video')

    def __str__(self):
        return f"{self.student.username} - {self.video.title}"
