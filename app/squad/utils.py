import pandas as pd
from django.db import transaction
from .models import Squad, SquadNumber
from app.region.models import Neighborhood
from ..users.models import User


# def import_squad_from_excel(file_path):
#     pass
#     all_rows = pd.read_excel(file_path, header=None)
#     total_rows = len(all_rows)
#
#     for header_row in range(min(total_rows, 10)):
#         df = pd.read_excel(file_path, header=header_row)
#         df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
#
#         print("Excel ustunlari:", df.columns.tolist())
#         print("Birinchi qator:", df.head(1).to_dict())
#
#         if len(df.columns) >= 3:
#             break
#     else:
#         raise ValueError("Excel faylda kerakli sarlavha topilmadi!")
#
#     df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')
#
#     required_columns = ["squad_number", "full_name", "phone_number", "name"]
#     for col in required_columns:
#         if col not in df.columns:
#             raise ValueError(
#                 f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
#             )
#
#     created_count = 0
#     updated_count = 0
#
#     with transaction.atomic():
#         for _, row in df.iterrows():
#             number = str(row.get("squad_number", "")).strip()
#             full_name = str(row.get("full_name", "")).strip()
#             phone_number = str(row.get("phone_number", "")).strip()
#             name = str(row.get("name", "")).strip()
#
#             if full_name:
#                 user = User.objects.filter(full_name=full_name).first() if full_name else None
#
#             if number:
#                 squad_number = SquadNumber.objects.filter(number=number).first()
#
#             neighborhood = Neighborhood.objects.filter(name=name).first()
#             print('neighborhood ** ', neighborhood)
#             if not neighborhood:
#                 raise ValueError(f"Massive topilmadi: {neighborhood}")
#
#             print('full_name', full_name)
#             print('name', name)
#             print('user', user)
#             print('squad_number', squad_number)
#             print('Neighborhood', neighborhood)
#
#             squad, created = Squad.objects.update_or_create(
#                 user=user,
#                 squad_number=squad_number,
#                 neighborhood=neighborhood,
#             )
#
#             if created:
#                 created_count += 1
#             else:
#                 updated_count += 1
#
#     print(f"{created_count} ta yangi mahalla yaratildi, {updated_count} ta mahalla yangilandi.")
#     return {"created": created_count, "updated": updated_count}

def import_squad_from_excel(file_path):

    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    # Kerakli sarlavhani aniqlash
    df = None
    for header_row in range(min(total_rows, 10)):
        temp_df = pd.read_excel(file_path, header=header_row)
        temp_df = temp_df.loc[:, ~temp_df.columns.str.contains('^Unnamed', case=False)]

        # Ustunlarni tozalash
        temp_df.columns = (
            temp_df.columns
            .str.strip()
            .str.lower()
            .str.replace(u'\xa0', ' ', regex=False)
        )

        print("Tekshirilayotgan ustunlar:", temp_df.columns.tolist())

        if {"squad_number", "full_name", "phone_number", "name"} <= set(temp_df.columns):
            df = temp_df
            break

    if df is None:
        raise ValueError(f"Excel faylda kerakli sarlavha topilmadi! Hozirgi ustunlar: {temp_df.columns.tolist()}")

    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for _, row in df.iterrows():
            number = str(row.get("squad_number", "")).strip()
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()
            name = str(row.get("name", "")).strip()

            if not number or not name:
                print("⚠️ Qator tashlab ketildi:", row.to_dict())
                continue

            user = None
            if phone_number:
                user = User.objects.filter(phone_number=phone_number).first()
            elif full_name:
                user = User.objects.filter(full_name__iexact=full_name.strip()).first()

            squad_number = SquadNumber.objects.filter(number=number).first()
            neighborhood = Neighborhood.objects.filter(name=name).first()

            if not neighborhood:
                raise ValueError(f"Massive topilmadi: {name}")

            squad, created = Squad.objects.update_or_create(
                squad_number=squad_number,
                neighborhood=neighborhood,
                defaults={
                    "user": user,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    print(f"✅ {created_count} ta yangi otryad yaratildi, {updated_count} ta yangilandi.")
    return {"created": created_count, "updated": updated_count}
