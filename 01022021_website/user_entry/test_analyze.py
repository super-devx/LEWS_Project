import os
import django
import sys

# Setup Django environment
sys.path.append('c:\\\\Users\\\\DELL\\\\OneDrive\\\\Desktop\\\\LEWS_projectt\\\\LEWS_Project\\\\01022021_website\\\\user_entry')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_entry.settings")
django.setup()

from login.services.cross_correlation_service import analyze_cross_correlation

print("Testing N4 (Should work)")
result_n4 = analyze_cross_correlation('kerala_n4_ms1', 'kerala_n4_pr1', '2026-04-01 00:00:00', '2026-06-15 00:00:00')
print("N4 Error:", result_n4.get('error'))

print("\nTesting N1 vs N2")
result_n1_n2 = analyze_cross_correlation('kerala_n1_ms1', 'kerala_n2_ms1', '2026-03-25 00:00:00', '2026-06-15 00:00:00')
print("N1 vs N2 Error:", result_n1_n2.get('error'))

print("\nTesting N1 vs N3")
result_n1_n3 = analyze_cross_correlation('kerala_n1_ms1', 'kerala_n3_ms1', '2026-03-25 00:00:00', '2026-06-15 00:00:00')
print("N1 vs N3 Error:", result_n1_n3.get('error'))
