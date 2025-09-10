# app/utils.py
import pandas as pd

from app.region.models import Farm


def import_farm_from_excel(file_path):
    df = pd.read_excel(file_path)

    # Excel ustunlari Farm model maydonlariga mos bo‘lishi kerak
    for _, row in df.iterrows():
        Farm.objects.get_or_create(
            INN=row["INN"],  # unique bo‘lgani uchun shunga qarab tekshiradi
            defaults={
                "full_name": row["full_name"],
                "location": row["location"],
                "phone_number": row["phone_number"],
            },
        )


   # region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
   #  district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
   #  massive = models.ForeignKey(Massive, on_delete=models.SET_NULL, blank=True, null=True)
   #  neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, blank=True, null=True)
   #  full_name = models.CharField(max_length=255)
   #  location = models.CharField(max_length=255)
   #  INN = models.CharField(max_length=20, unique=True)
   #  phone_number = models.CharField(max_length=13, unique=True)
   #  claster = models.CharField(max_length=255)
   #  cotton_area = models.FloatField()
   #  productivity = models.FloatField()
   #  gross_yield = models.FloatField()