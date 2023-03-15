from django.urls import path
from qr.views import QrCodeScan, QrCodeView
app_name = 'qr'

urlpatterns = [
    path('', QrCodeView.as_view(), name='qrcode'),
    path('qrcode-scan', QrCodeScan.as_view(), name='qrscan'),
]