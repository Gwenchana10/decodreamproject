from django.db import models

class RegisterUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords

    def __str__(self):
        return self.name

from django.db import models

class UserDesigns(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=255, unique=True)  # Unique design name
    image_path = models.CharField(max_length=500)  # Store image path
    input_image_path = models.CharField(max_length=500, default="", blank=True)  # New field
    promote = models.CharField(max_length=500)  # Promote field (True/False)
    type = models.CharField(max_length=100)  # Type of design
    created_at = models.DateTimeField(auto_now_add=True)  # Store timestamp

    def __str__(self):
        return f"{self.user.name} - {self.design_name} ({self.type})"


