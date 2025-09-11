# import pandas as pd
# from app.region.models import Farm
# from django.db import transaction
#
# def import_farm_from_excel(file_path):
#     # Fayldagi sarlavhani topish uchun birinchi 10 qatorni tekshiramiz
#     for header_row in range(10):
#         df = pd.read_excel(file_path, header=header_row)
#         df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
#         if len(df.columns) >= 7:  # required_columns soni bilan solishtirish mumkin
#             break
#     else:
#         raise ValueError("Excel faylda kerakli sarlavha topilmadi!")
#
#     df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')
#     print("Topilgan ustunlar:", df.columns.tolist())
#
#     required_columns = ["massive_name", "full_name", "inn", "claster", "cotton_area", "productivity", "gross_yield"]
#     for col in required_columns:
#         if col not in df.columns:
#             raise ValueError(f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}")
#
#     created_count = 0
#     updated_count = 0
#
#     with transaction.atomic():
#         for _, row in df.iterrows():
#             inn = str(row.get("inn", "")).strip()
#             if not inn:
#                 continue
#             farm, created = Farm.objects.update_or_create(
#                 INN=inn,
#                 defaults={
#                     "region": 1,
#                     "district": 1,
#                     "massive_name": str(row.get("massive_name", "")).strip(),
#                     "full_name": str(row.get("full_name", "")).strip(),
#                     "claster": str(row.get("claster", "")).strip(),
#                     "cotton_area": str(row.get("cotton_area", "")).strip(),
#                     "productivity": str(row.get("productivity", "")).strip(),
#                     "gross_yield": str(row.get("gross_yield", "")).strip()
#                 },
#             )
#
#             if created:
#                 created_count += 1
#             else:
#                 updated_count += 1
#
#     print(f"{created_count} ta yangi farm yaratildi, {updated_count} ta farm yangilandi.")
#     return {"created": created_count, "updated": updated_count}


import pandas as pd
from django.db import transaction
from .models import Farm, Massive, District, Region, Neighborhood


def import_farm_from_excel(file_path):
    # Fayldagi sarlavhani topish uchun birinchi 10 qatorni tekshiramiz
    for header_row in range(10):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
        if len(df.columns) >= 7:
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

    # ustunlarni tozalash
    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')
    print("Topilgan ustunlar:", df.columns.tolist())

    required_columns = ["massive_name", "full_name", "inn", "claster", "cotton_area", "productivity", "gross_yield"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}")

    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for _, row in df.iterrows():
            inn = str(row.get("inn", "")).strip()
            if not inn:
                continue

            # Excel'dan massiv nomini olish
            massive_name = str(row.get("massive_name", "")).strip()

            # Bazadan massivni qidiramiz
            massive_obj = None
            if massive_name:
                massive_obj, _ = Massive.objects.get_or_create(
                    name=massive_name,
                    defaults={
                        # bu yerda agar kerak bo‘lsa District/plan/crop_area ham to‘ldirish mumkin
                        "district": District.objects.first(),  # vaqtincha birinchi District
                        "plan": 0,
                        "crop_area": 0
                    }
                )

            # Neighborhoodni xohlasa shu yerda ham qidirib topish mumkin
            neighborhood_obj = None
            # if massive_name:
            #     neighborhood_obj, _ = Neighborhood.objects.get_or_create(
            #         name=massive_name,
            #         defaults={
            #             # bu yerda agar kerak bo‘lsa District/plan/crop_area ham to‘ldirish mumkin
            #             "district": District.objects.first(),  # vaqtincha birinchi District
            #             "plan": 0,
            #             "crop_area": 0
            #         }
            #     )
            # # Misol: neighborhood_obj = Neighborhood.objects.filter(name=...).first()

            print('massive_name', massive_name)

            farm, created = Farm.objects.update_or_create(
                INN=inn,
                defaults={
                    "region": Region.objects.first(),     # vaqtincha birinchi Region
                    "district": District.objects.first(), # vaqtincha birinchi District
                    "massive": massive_obj,
                    "neighborhood": neighborhood_obj,
                    "massive_name": massive_name,
                    "full_name": str(row.get("full_name", "")).strip(),
                    "claster": str(row.get("claster", "")).strip(),
                    "cotton_area": float(row.get("cotton_area", 0)),
                    "productivity": float(row.get("productivity", 0)),
                    "gross_yield": float(row.get("gross_yield", 0)),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    print(f"{created_count} ta yangi farm yaratildi, {updated_count} ta farm yangilandi.")
    return {"created": created_count, "updated": updated_count}
