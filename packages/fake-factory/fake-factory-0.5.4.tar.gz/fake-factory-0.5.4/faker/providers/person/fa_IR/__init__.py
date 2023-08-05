# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .. import Provider as PersonProvider


class Provider(PersonProvider):
    formats_female = (
        '{{first_name_female}} {{last_name}}',
        '{{first_name_female}} {{last_name}}',
        '{{first_name_female}} {{last_name}}',
        '{{first_name_female}} {{last_name}}',
        '{{first_name_female}} {{last_name}}',
        '{{prefix_female}} {{first_name_female}} {{last_name}}',
        '{{first_name_female}} {{last_name}} {{suffix}}',
        '{{prefix_female}} {{first_name_female}} {{last_name}} {{suffix}}'
    )

    formats_male = (
        '{{first_name_male}} {{last_name}}',
        '{{first_name_male}} {{last_name}}',
        '{{first_name_male}} {{last_name}}',
        '{{first_name_male}} {{last_name}}',
        '{{first_name_male}} {{last_name}}',
        '{{prefix_male}} {{first_name_male}} {{last_name}}',
        '{{first_name_male}} {{last_name}} {{suffix}}',
        '{{prefix_male}} {{first_name_male}} {{last_name}} {{suffix}}'
    )

    formats = formats_female + formats_male

    first_names_female = (
        # top 50 Female Names in Iran:
        # http://www.sabteahval.ir/Upload/Modules/Contents/asset100/name/d1391.htm
        'فاطمه', 'اسما', 'زهرا', 'عسل', 'نازنین زهرا', 'النا', 'زینب', 'سارا',
        'یسنا', 'آتنا', 'ریحانه', 'آیناز', 'هستی', 'محیا', 'ستایش', 'باران',
        'ثنا', 'هلیا', 'مریم', 'یلدا', 'فاطمه زهرا', 'ملیكا', 'سارینا',
        'نازنین', 'مهسا', 'آیلین', 'نرگس', 'حنانه', 'رقیه', 'كیانا', 'كوثر',
        'هانیه', 'مبینا', 'مهدیس', 'رها', 'آوا', 'اسرا', 'یگانه', 'نیایش',
        'حدیث', 'الینا', 'سوگند', 'مائده', 'پریا', 'معصومه', 'مهدیه',
        'آیدا', 'الناز', 'محدثه', 'یاسمین',
    )

    first_names_male = (
        # top 50 male Names in Iran:
        # http://www.sabteahval.ir/Upload/Modules/Contents/asset100/name/p1391.htm
        'امیر علی', 'پرهام', 'ابوالفضل', 'كیان', 'امیرحسین', 'متین',
        'محمد طاها', 'عرفان', 'محمد', 'دانیال', 'علی', 'آرمین', 'امیرمحمد',
        'آرتین', 'حسین', 'سبحان', 'مهدی', 'سینا', 'محمد مهدی', 'آریا',
        'محمدرضا', 'محمدپارسا', 'طاها', 'سجاد', 'امیررضا', 'آرش',
        'امیرعباس', 'نیما', 'علیرضا', 'عرشیا', 'محمدامین', 'مبین', 'محمدحسین',
        'یوسف', 'رضا', 'احسان', 'علی اصغر', 'آرین', 'امیرمهدی', 'محمدیاسین',
        'ماهان', 'عباس', 'پارسا', 'حسام', 'یاسین', 'علی رضا', 'ایلیا',
        'علی اكبر', 'محمدجواد', 'بنیامین'
    )

    first_names = first_names_female + first_names_male

    last_names = (
        'محمدی', 'محمد پور', 'اکبر پور', 'رضا زاده', 'مجتهدی', 'دایی', 'حمیدی',
        'کابلی', 'عبدالعلی', 'احمدی', 'اشرفی', 'علیجانی', 'ابوطالبی',
        'علی شاهی', 'الوندی', 'بهمنی', 'بهرامی', 'هنری', 'ایروانی', 'حریریان',
        'جعفر پور', 'جلالی', 'جلیلی', 'روحانی', 'خسروجردی', 'منصوری',
        'مهدیان', 'نوروزی', 'نوری', 'رسته', 'سماوات', 'سمسار', 'شادروان',
        'شاکری', 'سلطانی', 'شبیری', 'تحسینی', 'تنزیلی', 'طلوعی', 'ولاشجردی',
        'وثاق', 'ظفری', 'زمانی', 'زارع', 'زارعی', 'ربانی', 'شمشیری', 'صارمی',
        'صیادی', 'سرخوشیان', 'رستمی', 'رسولی', 'رفیعی', 'کریمی', 'کرمانی',
        'سعیدی', 'عباسی', 'پویان', 'ترکاشوند', 'زنجانی', 'تهرانی', 'جنتی',
        'صنایعی', 'جهانی', 'اشتری', 'چنگیزی', 'دادفر', 'سغیری', 'پارسا',
        'ضابطی', 'میردامادی', 'عقیلی', 'نامور', 'حسنی', 'لاهوتی', 'محجوب',
        'هاشمی', 'معروف', 'معین', 'هوشیار', 'هومن', 'هدایت', 'قاضی', 'ملکیان',
        'ضرغامی', 'یزدی', 'نوبختی', 'مجتبوی', 'نیلوفری', 'لاچینی', 'علی پور',
        'عبدالمالکی', 'فرجی', 'موسوی', 'همدانی', 'موحد', 'کمالی', 'گلپایگانی',
        'نعمتی', 'عزیزی', 'رودگر',
    )

    prefixes_male = ('جناب آقای', 'جناب آقای دکتر')
    prefixes_female = ('سرکار خانم', 'سرکار خانم دکتر')

    @classmethod
    def suffix(cls):
        return ''
