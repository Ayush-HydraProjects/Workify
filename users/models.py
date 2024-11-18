from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class LayoffPrediction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    education_field = models.IntegerField(choices=[
        (0, "Human Resources"),
        (1, "Life Sciences"),
        (2, "Marketing"),
        (3, "Medical"),
        (4, "Other"),
        (5, "Technical Degree")
    ], default=0)
    job_role = models.IntegerField(choices=[
        (0, "Healthcare Representative"),
        (1, "Human Resources"),
        (2, "Laboratory Technician"),
        (3, "Network Engineer"),
        (4, "Operational Executive"),
        (5, "Project Manager"),
        (6, "Research Director"),
        (7, "Research Scientist"),
        (8, "Sales Executive"),
        (9, "Sales Representative"),
        (10, "Software Developer"),
        (11, "Team Lead")
    ], default=0)
    department = models.IntegerField(choices=[
        (0, "Defence"),
        (1, "Human Resources"),
        (2, "IT department"),
        (3, "Research & Development"),
        (4, "Sales"),
        (5, "Tech Development")
    ], default=0)
    industry = models.IntegerField(choices=[
        (0, "Aerospace"),
        (1, "Education"),
        (2, "Finance"),
        (3, "Fitness"),
        (4, "Food"),
        (5, "Healthcare"),
        (6, "Logistics"),
        (7, "Real Estate"),
        (8, "Retail"),
        (9, "Sales"),
        (10, "Transportation"),
        (11, "Travel")
    ], default=0)
    stage = models.IntegerField(choices=[
        (0, "Acquired"),
        (1, "Post-IPO"),
        (2, "Private Equity"),
        (3, "Seed"),
        (4, "Series A"),
        (5, "Series B"),
        (6, "Series C"),
        (7, "Series D"),
        (8, "Series E"),
        (9, "Series F"),
        (10, "Series G"),
        (11, "Series H"),
        (12, "Series I"),
        (13, "Series J"),
        (14, "Subsidiary"),
        (15, "Unknown")
    ], default=0)
    education = models.IntegerField()
    funds_raised = models.DecimalField(max_digits=10, decimal_places=2)
    performance_rating = models.IntegerField()
    job_satisfaction = models.IntegerField()
    job_involvement = models.IntegerField()
    years_at_company = models.IntegerField()
    years_in_current_role = models.IntegerField()
    years_with_curr_manager = models.IntegerField()
    monthly_income = models.IntegerField()
    num_companies_worked = models.IntegerField()
    gender = models.IntegerField(choices=[
        (0, "Male"),
        (1, "Female"),
        (2, "Other")
    ], default=0)

    def __str__(self):
        return f"Prediction Data (ID: {self.id})"

