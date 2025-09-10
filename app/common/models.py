from django.db import models

class FarmExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/farms/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"
