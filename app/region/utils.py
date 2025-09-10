import pandas as pd
from app.region.models import Farm
from django.db import transaction

def import_farm_from_excel(file_path):
    # Fayldagi sarlavhani topish uchun birinchi 10 qatorni tekshiramiz
    for header_row in range(10):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
        if len(df.columns) >= 7:  # required_columns soni bilan solishtirish mumkin
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

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
            farm, created = Farm.objects.update_or_create(
                INN=inn,
                defaults={
                    "massive_name": str(row.get("massive_name", "")).strip(),
                    "full_name": str(row.get("full_name", "")).strip(),
                    "claster": str(row.get("claster", "")).strip(),
                    "cotton_area": str(row.get("cotton_area", "")).strip(),
                    "productivity": str(row.get("productivity", "")).strip(),
                    "gross_yield": str(row.get("gross_yield", "")).strip()
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    print(f"{created_count} ta yangi farm yaratildi, {updated_count} ta farm yangilandi.")
    return {"created": created_count, "updated": updated_count}
