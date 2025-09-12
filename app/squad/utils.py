import pandas as pd
from django.db import transaction
from .models import Squad, SquadNumber
from app.region.models import Neighborhood
from ..users.models import User


def import_squad_from_excel(file_path):
    pass
    # all_rows = pd.read_excel(file_path, header=None)
    # total_rows = len(all_rows)
    #
    # for header_row in range(min(total_rows, 10)):
    #     df = pd.read_excel(file_path, header=header_row)
    #     df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
    #
    #     print("Excel ustunlari:", df.columns.tolist())
    #     print("Birinchi qator:", df.head(1).to_dict())
    #
    #     if len(df.columns) >= 3:
    #         break
    # else:
    #     raise ValueError("Excel faylda kerakli sarlavha topilmadi!")
    #
    # df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')
    #
    # required_columns = ["squad_number", "full_name", "phone_number", "name"]
    # for col in required_columns:
    #     if col not in df.columns:
    #         raise ValueError(
    #             f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
    #         )
    #
    # created_count = 0
    # updated_count = 0
    #
    # with transaction.atomic():
    #     for _, row in df.iterrows():
    #         number = str(row.get("squad_number", "")).strip()
    #         full_name = str(row.get("full_name", "")).strip()
    #         phone_number = str(row.get("phone_number", "")).strip()
    #         name = str(row.get("name", "")).strip()
    #
    #         user = User.objects.filter(full_name=full_name).first() if full_name else None
    #         if number:
    #             squad_number = SquadNumber.objects.filter(squad_number=number).first()
    #
    #         massie = Massive.objects.filter(name=massive_name).first()v
    #         if not massive:
    #             raise ValueError(f"Massive topilmadi: {massive_name}")
    #
    #         phone_number = user.phone_number if user else None
    #
    #         print('massive_name', massive_name)
    #         print('full_name', full_name)
    #         print('name', name)
    #         print('user', user)
    #
    #         neighborhood, created = Neighborhood.objects.update_or_create(
    #             massive=massive,
    #             name=name,
    #             user=user,
    #             phone_number=phone_number,
    #         )
    #
    #         if created:
    #             created_count += 1
    #         else:
    #             updated_count += 1
    #
    # print(f"{created_count} ta yangi mahalla yaratildi, {updated_count} ta mahalla yangilandi.")
    # return {"created": created_count, "updated": updated_count}
