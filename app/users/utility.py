import random
import string
import pandas as pd
from django.contrib.auth.hashers import make_password
from django.db import transaction
from app.users.models import User


def generate_username(full_name: str) -> str:
    """
    Full name asosida noyob username yaratadi.
    Masalan: 'Ali Valiyev' -> 'ali.valiyev1234'
    """
    base_username = (
        full_name.strip()
        .lower()
        .replace(" ", ".")
        .replace("'", "")
    )
    random_digits = ''.join(random.choices(string.digits, k=4))
    username = f"{base_username}{random_digits}"

    # Username allaqachon mavjud bo‘lsa, qaytadan yaratamiz
    while User.objects.filter(username=username).exists():
        random_digits = ''.join(random.choices(string.digits, k=4))
        username = f"{base_username}{random_digits}"

    print("username:", username)
    return username


def generate_password(length: int = 8) -> str:
    """
    Tasodifiy parol yaratadi.
    """
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=length))
    print("password:", password)
    return password


def import_user_from_excel(file_path):
    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    # Fayldagi sarlavhani topish uchun birinchi 10 qatorni tekshiramiz
    for header_row in range(min(total_rows, 10)):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]

        print("Excel ustunlari:", df.columns.tolist())
        print("Birinchi qator:", df.head(1).to_dict())

        if len(df.columns) >= 2:
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

    # ustunlarni tozalash
    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')

    required_columns = ["full_name", "phone_number"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
            )

    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for _, row in df.iterrows():
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()

            if not phone_number:
                continue  # Telefon raqam bo‘lmasa, foydalanuvchini o‘tkazib yuboramiz

            password = generate_password()
            hash_password = make_password(password)

            user, created = User.objects.update_or_create(
                phone_number=phone_number,   # 🔑 filter
                defaults={
                    "username": generate_username(full_name),
                    "full_name": full_name,
                    "role": User.UserRoles.SQUAD,  # Qanaqa rol kerak bolsa oshani yozib ket
                    "password": hash_password,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

    print(f"{created_count} ta yangi user yaratildi, {updated_count} ta user yangilandi.")
    return {"created": created_count, "updated": updated_count}
