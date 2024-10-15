from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.course_code
    
class ApprovedResource(models.Model):
    title = models.CharField(max_length=100,unique=True, null=False)
    description = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=255, null=False)
    uploaded_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='uploaded_resources')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    approved_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_resources')

    def __str__(self):
        return self.title
    

class PendingResource(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    
    title = models.CharField(max_length=100, null=False,unique=True)
    description = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=255, null=False)
    uploaded_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='pending_resources')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    enroll_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='enrollments')
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return f"{self.enroll_id.username} enrolled in {self.course_id.name}"

class FacultyCourses(models.Model):
    faculty_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='faculty_courses')
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='faculty_courses')

    class Meta:
        unique_together = ('faculty_id', 'course_id')  # Ensures that each faculty-course pairing is unique

    def __str__(self):
        return f"{self.faculty_id.username} - {self.course_id.name}"

class Comment(models.Model):
    resource = models.ForeignKey('ApprovedResource', on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(null=False)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commented_by.username} on {self.resource.title}"
