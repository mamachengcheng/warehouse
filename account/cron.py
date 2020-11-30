import datetime
import time
import decimal
from .models import Company, Companyvolumeperday, Prepayrecord


def save_companys_volume_per_day():
    companys = Company.objects.all()
    for item in companys:
        volume = item.get_volume_per_day()
        out = item.get_out_per_day()
        log = Companyvolumeperday.objects.create(company=item,volume=volume, out=out)
        print(log)
        print(item)
        print("当日库存体积"+str(volume))
        print("当日出库体积"+str(out))


def deduct_company_storage_fee():
    companys = Company.objects.all()
    year,month=get_last_year_month()
    # t = time.localtime()
    # year = t[0]
    # month = t[1]
    for item in companys:
        fee = item.count_storage_fee(year=year,month=month)
        item.prepayment = decimal.Decimal(item.prepayment) - decimal.Decimal(fee)
        item.save(commit=False)
        instruction = item.__str__() + str(year) + '年' + str(month) + '月' + '仓租费用：' + str(fee) + '欧元'
        Prepayrecord.objects.create(company=item,sum=-fee,type=5,instruction=instruction)
        item.save()
        print(instruction)


def get_last_year_month():
    t = time.localtime()
    last_month = t[1]-1 or 12
    if last_month == 12:
        year = t[0]-1
    else:
        year = t[0]
    return year, last_month
