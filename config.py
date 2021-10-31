import os

CHROMEDRIVERPATH = os.getenv('CHROMEDRIVERPATH', 'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
URL_PRODUK = os.getenv('URL_PRODUK','https://shopee.co.id/Aerostreet-31-34-Energy-Peach-Sepatu-Sneakers-Casual-Sport-Sekolah-Pria-Wanita-Aero-Street-i.177400943.3315336435')
DATETIME_FLASHSALE = os.getenv('DATETIME_FLASHSALE','2021-10-31 18:51:00')
PINSHOPEEPAY = os.getenv('PINSHOPEEPAY', ['0', '0', '0', '0', '0', '0'])
ADDITIONAL_VALUE = os.getenv('ADDITIONAL_VALUE', ['32'])