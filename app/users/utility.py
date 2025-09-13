import random
import string
import uuid
from datetime import datetime

import pandas as pd
from django.contrib.auth.hashers import make_password
from django.db import transaction
from app.users.models import User
import os
import csv


def generate_username():
    # uuid.uuid4.__str__() -> c303282d-f2e6-46ca-a04a-35d3d873712d (takrorlanmas kod yasab beradi)
    temp_username = f"user_{uuid.uuid4().__str__().split('-')[1]}"
    while User.objects.filter(username=temp_username):
        temp_username = f"{temp_username}{random.randint(0, 9)}"
    return temp_username

def generate_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def import_squad_user_from_excel(file_path):
    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    for header_row in range(min(total_rows, 10)):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]

        if len(df.columns) >= 2:
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')

    required_columns = ["full_name", "phone_number"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
            )

    created_count = 0
    updated_count = 0
    credentials = []  # # username, password, full_name ni yig‘ish uchun

    with transaction.atomic():
        for _, row in df.iterrows():
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()

            if not phone_number:
                continue

            password = generate_password()
            hash_password = make_password(password)

            user, created = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    "username": generate_username(),
                    "full_name": full_name,
                    "role": User.UserRoles.SQUAD,
                    "password": hash_password,
                },
            )

            if created:
                created_count += 1
                # faqat yangi yaratilgan userlarni faylga yozamiz
                credentials.append([full_name, user.username, password])
            else:
                updated_count += 1

    # # 📂 credentials faylga yozish
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(os.path.dirname(file_path), f"user_credentials_{timestamp}.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["full_name", "username", "password"])
        writer.writerows(credentials)

    print(f"✅ Yaratilgan userlar credential faylga saqlandi: {output_file}")

    print(f"{created_count} ta yangi user yaratildi, {updated_count} ta user yangilandi.")
    print(f"Credentials saqlandi: {output_file}")

    return {"created": created_count, "updated": updated_count, "output_file": output_file}



def import_neighborhood_user_from_excel(file_path):
    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    for header_row in range(min(total_rows, 10)):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]

        if len(df.columns) >= 2:
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')

    required_columns = ["full_name", "phone_number"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
            )

    created_count = 0
    updated_count = 0
    credentials = []  # # username, password, full_name ni yig‘ish uchun

    with transaction.atomic():
        for _, row in df.iterrows():
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()

            if not phone_number:
                continue

            password = generate_password()
            hash_password = make_password(password)

            user, created = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    "username": generate_username(),
                    "full_name": full_name,
                    "role": User.UserRoles.NEIGHBORHOOD,
                    "password": hash_password,
                },
            )

            if created:
                created_count += 1
                # faqat yangi yaratilgan userlarni faylga yozamiz
                credentials.append([full_name, user.username, password])
            else:
                updated_count += 1

    # # 📂 credentials faylga yozish
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(os.path.dirname(file_path), f"user_credentials_{timestamp}.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["full_name", "username", "password"])
        writer.writerows(credentials)

    print(f"✅ Yaratilgan userlar credential faylga saqlandi: {output_file}")

    print(f"{created_count} ta yangi user yaratildi, {updated_count} ta user yangilandi.")
    print(f"Credentials saqlandi: {output_file}")

    return {"created": created_count, "updated": updated_count, "output_file": output_file}
