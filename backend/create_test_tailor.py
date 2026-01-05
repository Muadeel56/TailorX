#!/usr/bin/env python
"""
Script to create a test tailor account for testing purposes.
Run with: python manage.py shell < create_test_tailor.py
Or: python manage.py shell
Then copy-paste the code below.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

# Create test tailor account
tailor_email = 'testtailor@example.com'
tailor_password = 'testtailor123'

# Check if tailor already exists
if User.objects.filter(email=tailor_email).exists():
    tailor = User.objects.get(email=tailor_email)
    tailor.set_password(tailor_password)
    tailor.save()
    print(f"✓ Updated existing tailor account:")
else:
    tailor = User.objects.create_user(
        email=tailor_email,
        password=tailor_password,
        full_name='Test Tailor',
        phone='+1234567890',
        address='123 Test Street, Test City',
        user_type='TAILOR'
    )
    print(f"✓ Created new tailor account:")

print(f"  Email: {tailor_email}")
print(f"  Password: {tailor_password}")
print(f"  User ID: {tailor.id}")
print(f"  User Type: {tailor.user_type}")
print(f"\nYou can now login with these credentials in Postman!")


