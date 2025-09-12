import pandas as pd
from django.db import transaction
from .models import Squad, SquadNumber
from app.region.models import Neighborhood
from ..users.models import User


def import_squad_from_excel(file_path):
    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    for header_row in range(min(total_rows, 10)):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
        if len(df.columns) >= 3:
            break
    else:
        raise ValueError("Excel faylda kerakli ustunlar topilmadi!")

    # Ustunlarni normalize qilish
    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')

    required_columns = ["squad_number", "full_name", "phone_number", "name"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Excel faylda '{col}' ustuni yo‘q! Hozirgi ustunlar: {df.columns.tolist()}"
            )

    created_count = 0
    updated_count = 0
    skipped_count = 0

    with transaction.atomic():
        for _, row in df.iterrows():
            squad_number_value = str(row.get("squad_number", "")).strip()
            neighborhood_name = str(row.get("name", "")).strip()
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()

            # Agar squad number yoki neighborhood bo'sh bo'lsa - o'tkazib yuboramiz
            if not squad_number_value or not neighborhood_name:
                skipped_count += 1
                continue

            # Bazadan mos obyektlarni topish
            squad_number = SquadNumber.objects.filter(number=squad_number_value).first()
            if not squad_number:
                print(f"⚠️ SquadNumber topilmadi: {squad_number_value}")
                skipped_count += 1
                continue

            neighborhood = Neighborhood.objects.filter(name__iexact=neighborhood_name).first()
            if not neighborhood:
                print(f"⚠️ Neighborhood topilmadi: {neighborhood_name}")
                skipped_count += 1
                continue

            user = User.objects.filter(full_name__iexact=full_name).first() if full_name else None

            # Squadni update_or_create qilamiz
            squad, created = Squad.objects.update_or_create(
                squad_number=squad_number,
                neighborhood=neighborhood,
                defaults={
                    "user": user,
                    "phone_number": phone_number if phone_number else None,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    print(f"✅ {created_count} ta yangi squad yaratildi, {updated_count} ta squad yangilandi, {skipped_count} ta qator o'tkazib yuborildi.")
    return {"created": created_count, "updated": updated_count, "skipped": skipped_count}
