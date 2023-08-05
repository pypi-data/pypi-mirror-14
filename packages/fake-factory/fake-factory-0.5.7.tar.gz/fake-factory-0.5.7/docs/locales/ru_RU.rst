
Language ru_RU
===============

``faker.providers.address``
---------------------------

::

	fake.longitude()
	# Decimal('-162.122790')

	fake.building_number()
	# u'22170'

	fake.street_address()
	# u'165 \u041a\u0443\u0434\u0440\u044f\u0432\u0446\u0435\u0432 Brooks'

	fake.postalcode_plus4()
	# u'11020-6133'

	fake.city_prefix()
	# u'North'

	fake.military_ship()
	# u'USNS'

	fake.country_code()
	# u'NA'

	fake.city()
	# u'\u041c\u0430\u043a\u0441\u0438\u043c\u043e\u0432ville'

	fake.zipcode_plus4()
	# u'99920-4376'

	fake.state_abbr()
	# u'WA'

	fake.latitude()
	# Decimal('-81.426849')

	fake.street_suffix()
	# u'Inlet'

	fake.city_suffix()
	# u'stad'

	fake.military_dpo()
	# u'Unit 7775 Box 6366'

	fake.country()
	# u'Bahamas'

	fake.secondary_address()
	# u'Apt. 130'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-119.783648')

	fake.postalcode()
	# u'99015'

	fake.address()
	# u'87379 \u0418\u0440\u0430\u0438\u0434\u0430 Stream\n\u041b\u044e\u0431\u043e\u043c\u0438\u0440bury, FM 47382'

	fake.state()
	# u'North Carolina'

	fake.military_state()
	# u'AE'

	fake.street_name()
	# u'\u0421\u0432\u044f\u0442\u043e\u0441\u043b\u0430\u0432 Mills'

	fake.zipcode()
	# u'90776'

	fake.postcode()
	# u'72208'

	fake.military_apo()
	# u'PSC 2573, Box 1832'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'4832356238716'

	fake.ean13()
	# u'7497623215783'

	fake.ean8()
	# u'09809031'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(251,152,108)'

	fake.color_name()
	# u'Cornsilk'

	fake.rgb_color_list()
	# (142, 55, 151)

	fake.rgb_color()
	# u'191,165,224'

	fake.safe_hex_color()
	# u'#bbcc00'

	fake.safe_color_name()
	# u'lime'

	fake.hex_color()
	# u'#252001'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\u041f\u0435\u0442\u0443\u0445\u043e\u0432\u0430 Group'

	fake.company_suffix()
	# u'LLC'

	fake.catch_phrase()
	# u'Re-contextualized solution-oriented installation'

	fake.bs()
	# u'enable cutting-edge experiences'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'795'

	fake.credit_card_provider(card_type=None)
	# u'VISA 16 digit'

	fake.credit_card_full(card_type=None)
	# u'VISA 16 digit\n\u041b\u0430\u0440\u0438\u0441\u0430 \u0413\u043e\u0440\u0448\u043a\u043e\u0432\u0430\n4409984066599857 05/23\nCVC: 769\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '07/24'

	fake.credit_card_number(card_type=None)
	# u'346694702094866'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'TRY'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '22'

	fake.month()
	# '09'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 1, 7, 46, 57)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 38)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2006, 1, 25, 10, 56, 3)

	fake.time(pattern="%H:%M:%S")
	# '23:09:26'

	fake.year()
	# '2014'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1648, 10, 22, 20, 24, 38)

	fake.day_of_week()
	# 'Sunday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 3, 2, 39, 31)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2011, 10, 13, 15, 47, 42)

	fake.unix_time()
	# 516627912

	fake.month_name()
	# 'March'

	fake.timezone()
	# u'America/Dominica'

	fake.time_delta()
	# datetime.timedelta(11175, 56273)

	fake.century()
	# u'XVII'

	fake.date(pattern="%Y-%m-%d")
	# '2004-01-09'

	fake.iso8601(tzinfo=None)
	# '1970-07-05T04:55:40'

	fake.date_time(tzinfo=None)
	# datetime(1991, 7, 5, 3, 0, 4)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2014, 10, 21, 17, 42, 55)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'message/rfc822'

	fake.file_name(category=None, extension=None)
	# u'iusto.mp3'

	fake.file_extension(category=None)
	# u'bmp'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'189.69.71.118'

	fake.url()
	# u'http://www.\u0433\u043e\u0440\u0448\u043a\u043e\u0432.org/'

	fake.company_email()
	# u'\u0440\u044b\u0431\u0430\u043a\u043e\u0432\u043d\u0438\u043a\u043e\u0434\u0438\u043c@\u0442\u0435\u0442\u0435\u0440\u0438\u043d.biz'

	fake.uri()
	# u'http://www.\u0444\u0438\u043b\u0430\u0442\u043e\u0432\u0430.com/faq.html'

	fake.domain_word(*args, **kwargs)
	# u'\u0441\u0435\u043b\u0435\u0437\u043d\u0435\u0432\u0430'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/624/755'

	fake.tld()
	# u'net'

	fake.free_email()
	# u'\u0434\u0430\u0440\u044c\u044f55@yahoo.com'

	fake.slug(*args, **kwargs)
	# u'suscipit-vel-id'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'\u0440\u043e\u043c\u0430\u043d\u043e\u0432\u0430.biz'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'f0f2:c217:99df:3d9a:382f:e19f:07f3:1348'

	fake.safe_email()
	# u'\u043b\u0430\u0440\u0438\u043e\u043d\u043e\u0432\u0430\u044e\u043b\u0438\u044f@example.net'

	fake.user_name(*args, **kwargs)
	# u'x\u0430\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u043e\u0432'

	fake.uri_path(deep=None)
	# u'category'

	fake.email()
	# u'\u0434\u0430\u043d\u0438\u043b\u043076@\u043a\u043e\u043c\u0438\u0441\u0441\u0430\u0440\u043e\u0432.com'

	fake.uri_page()
	# u'author'

	fake.mac_address()
	# u'b2:cc:9f:e7:f8:f0'

``faker.providers.job``
-----------------------

::

	fake.job()
	# u'\u041b\u043e\u0433\u043e\u043f\u0435\u0434'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'\u0416\u044f\u0442 \u0445\u0430\u0431\u044d\u043e \u043d\u044b\u043a \u043b\u0430\u0442\u0438\u043d\u044b \u0432\u0438\u0440\u0439\u0437 \u0434\u044b\u043b\u044b\u043a\u0442\u0443\u0447. \u0412\u044b\u0440\u043e \u044b\u0430\u043c \u0444\u044b\u0440\u0440\u0435 \u0432\u044d\u0440\u044b\u0430\u0440 \u0439\u043d \u0434\u044b\u0444\u044f\u043d\u0438\u044d\u0431\u0430\u0436. \u0422\u0435\u0431\u0438\u043a\u0432\u044e\u044d \u043a\u0432\u044e\u0438\u0436 \u043c\u0430\u0433\u043d\u0430 \u044d\u0436\u0442 \u043f\u044d\u0440\u0442\u0438\u043d\u0430\u043a\u0451\u0430 \u0432\u044b\u0440\u043e. \u041e\u0444\u0444\u044d\u043d\u0434\u0439\u0442 \u043b\u0443\u043f\u0442\u0430\u0442\u0443\u043c \u0437\u044e\u0447\u043a\u0451\u043f\u0438\u0442 \u043f\u043e\u043f\u044e\u043b\u044c\u043e \u0440\u044b\u043f\u0440\u044d\u0445\u044d\u043d\u0434\u0443\u043d\u0442 \u044b\u0430\u043c \u0431\u043b\u0430\u043d\u0434\u0438\u0442 \u0442\u0430\u043a\u0435\u043c\u0430\u0442\u044b\u0448.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'\u0414\u0435\u043a\u0442\u0430\u0436 \u043a\u0435\u0432\u0451\u0431\u044e\u0436 \u0434\u0438\u043a\u0443\u043d\u0442 \u0430\u0434\u043c\u043e\u0434\u0443\u043c \u044d\u0436\u0442 \u0430\u043d\u043a\u0438\u043b\u043b\u044c\u0430\u044b \u0447\u043e\u043d\u044d\u0442.'

	fake.word()
	# u'\u0448\u0430\u043f\u044d\u0440\u044d\u0442'

	fake.paragraphs(nb=3)
	# [   u'\u041a\u0432\u044e\u043e \u043f\u044d\u0440 \u0444\u0430\u043a\u0438\u043b\u0438\u0437 \u043a\u0432\u044e\u0438\u0436 \u043f\u043e\u0448\u0436\u0438\u043c \u0432\u0435\u043a\u0436 \u043c\u044e\u043d\u0434\u0439. \u0419\u043d \u0442\u0438\u043d\u043a\u0438\u0434\u044e\u043d\u0442 \u043e\u0434\u0435\u043e \u043c\u044b\u0438\u0441 \u043a\u0438\u0431\u043e \u043a\u043e\u043d\u0447\u044d\u0442\u044b\u0442\u044e\u0440 \u0437\u043a\u0440\u0438\u043f\u0442\u043e\u0440\u044d\u043c. \u0412\u0438\u0442\u044e\u043f\u044b\u0440\u0430\u0442\u0430 \u0434\u043e\u043a\u0442\u044e\u0436 \u043f\u043e\u043f\u044e\u043b\u044c\u043e \u0444\u0430\u0431\u0443\u043b\u0430\u0437 \u043f\u044d\u0440\u043a\u0439\u043f\u0435\u0442 \u044b\u043b\u044c\u0438\u0433\u044d\u043d\u0434\u0438 \u043c\u044d\u043b\u044c \u043e\u0434\u0435\u043e.',
	#     u'\u042d\u0442\u0451\u0430\u043c \u0442\u043e\u0440\u043a\u0432\u044e\u0430\u0442\u043e\u0437 \u0430\u0434\u043c\u043e\u0434\u0443\u043c \u0430\u043b\u044c\u044c\u0442\u044b\u0440\u0430 \u043c\u044b\u0430. \u0422\u043e\u043b\u043b\u0439\u0442 \u043e\u0444\u0444\u0435\u043a\u0439\u044f\u0436 \u043b\u044c\u0430\u043e\u0440\u044b\u044b\u0442 \u0442\u0438\u043d\u043a\u0438\u0434\u044e\u043d\u0442 \u043c\u0430\u0446\u0438\u043c \u044e\u0440\u0431\u0430\u043d\u0439\u0442\u0430\u0436 \u043a\u0432\u044e\u0430\u043d\u0434\u043e.',
	#     u'\u0410\u0434 \u0444\u0430\u043b\u043b\u044f \u0445\u044d\u043d\u0434\u0440\u044d\u0440\u0435\u0442 \u0440\u044b\u043a\u0432\u044e\u044b \u0447\u043e\u043d\u044d\u0442 \u044b\u043b\u043e\u043a\u0432\u044e\u044d\u043d\u0442\u0438\u0430\u043c \u0435\u0434\u043a\u0432\u044e\u044d \u0430\u043c\u044d\u0442. \u0424\u044e\u0433\u0438\u0442 \u0432\u044d\u043b \u0430\u043d\u043a\u0438\u043b\u043b\u044c\u0430\u044b \u044b\u0451\u044e\u0437 \u0444\u0430\u0431\u0443\u043b\u0430\u0437 \u0430\u043a\u043a\u0443\u0437\u0430\u0442\u0430. \u0414\u044d\u043b\u044c\u044c\u044b\u043d\u0451\u0442\u0451 \u0436\u044f\u0442 \u0448\u0430\u043f\u044d\u0440\u044d\u0442 \u0432\u044d\u0440\u044b\u0430\u0440 \u043f\u044d\u0440\u043a\u0439\u043f\u0435\u0442 \u0435\u044e\u0436 \u0442\u0430\u043b\u044c\u044d.']

	fake.words(nb=3)
	# [   u'\u0430\u043f\u044d\u0440\u0438\u0430\u043c',
	#     u'\u044d\u0440\u044e\u0434\u0438\u0442\u044f',
	#     u'\u044d\u0432\u044d\u0440\u0442\u0451']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'\u041f\u0430\u0443\u043b\u043e \u0430\u0442\u043e\u043c\u043e\u0440\u044e\u043c \u0444\u044b\u0440\u0440\u0435 \u0430\u0434 \u0436\u043e\u043b\u044e\u043c \u043e\u0434\u0435\u043e \u043f\u044d\u0440\u0442\u0438\u043d\u0430\u043a\u0451\u0430 \u043f\u044d\u0440\u0447\u0451\u0443\u0441. \u0410\u0442\u043a\u0432\u044e\u0435 \u0445\u0430\u0431\u044d\u043e \u043a\u043e\u043d\u043a\u044b\u043f\u0442\u0430\u043c \u0430\u043c\u044d\u0442 \u0432\u0438\u0442\u044e\u043f\u044d\u0440\u0430\u0442\u043e\u0440\u0435\u0431\u0443\u0437 \u043a\u0432\u044e\u0430\u043b\u044c\u0438\u0437\u043a\u0432\u044e\u044d. \u0416\u043a\u0430\u044b\u0432\u043e\u043b\u0430 \u0448\u044b\u043d\u0447\u0435\u0431\u044e\u0437 \u0434\u0435\u043a\u0430\u0442 \u0432\u0438\u0434\u0438\u0448\u0447\u044b \u0448\u044b\u043d\u0447\u0435\u0431\u044e\u0437 \u0433\u0440\u0430\u044d\u043a\u043e \u0445\u0451\u0437. \u0414\u044b\u0442\u044b\u0440\u0440\u044e\u0438\u0437\u0449\u044d\u0442 \u043a\u0443 \u0442\u0430\u043a\u0435\u043c\u0430\u0442\u044b\u0448 \u0433\u0440\u0430\u044d\u043a\u043e \u044d\u0432\u044d\u0440\u0442\u0451 \u0437\u044d\u043d\u0442\u044b\u043d\u0442\u0438\u0430\u044d.'

	fake.sentences(nb=3)
	# [   u'\u0420\u044d\u043f\u0443\u0434\u0451\u0430\u043d\u0434\u0430\u044d \u0442\u043e\u0442\u0430 \u044d\u043b\u044b\u043a\u0442\u0440\u0430\u043c \u0434\u043e\u043b\u044c\u043e\u0440 \u0434\u044b\u0444\u044f\u043d\u0438\u044d\u0431\u0430\u0436.',
	#     u'\u041f\u044b\u0440\u0438\u043a\u0443\u043b\u044c\u0430 \u0434\u044d\u043b\u044c\u044d\u043d\u0439\u0442 \u0442\u0435\u0431\u0438\u043a\u0432\u044e\u044d \u0432\u044d\u0440\u044b\u0430\u0440 \u0444\u044e\u0433\u0438\u0442 \u0442\u043e\u0442\u0430.',
	#     u'\u041e\u0444\u0444\u0435\u043a\u0439\u044f\u0436 \u0430\u0442\u043a\u0432\u044e\u0435 \u043d\u044b\u043a \u043f\u0440\u0451 \u0430\u0434 \u0430\u0437\u0436\u044e\u044b\u0432\u044b\u0440\u0438\u0442 \u043a\u0432\u044e\u0430\u044d\u0447\u0442\u0438\u043e \u043a\u044e\u043c.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'4y4RS(#x*Y'

	fake.locale()
	# u'en_MK'

	fake.md5(raw_output=False)
	# 'fd53183db31973c8bb2f868f4a0c4825'

	fake.sha1(raw_output=False)
	# '42e6770a2feadc4c4df5ad209019a4706ac5da4d'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# '1e09efc2310b6e963dae2a65ab233d88a639d653cdf781e738669f4723f2514c'

	fake.uuid4()
	# 'd1dd2064-0591-47dd-9d85-f9d01152703f'

	fake.language_code()
	# u'en'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u0421\u043c\u0438\u0440\u043d\u043e\u0432'

	fake.name_female()
	# u'\u041b\u044e\u0431\u043e\u0432\u044c \u0410\u043d\u0442\u043e\u043d\u043e\u0432\u0430'

	fake.prefix_male()
	# u'\u0442\u043e\u0432.'

	fake.prefix()
	# u'\u0433-\u0436\u0430'

	fake.name()
	# u'\u0433-\u0436\u0430 \u041d\u0438\u043d\u0430 \u042f\u043a\u0443\u0448\u0435\u0432\u0430'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'\u041b\u0443\u043a\u044c\u044f\u043d \u041a\u0440\u0430\u0441\u0438\u043b\u044c\u043d\u0438\u043a\u043e\u0432'

	fake.first_name()
	# u'\u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'\u041d\u0438\u043a\u043e\u043d'

	fake.first_name_female()
	# u'\u0418\u044f'

	fake.last_name_female()
	# u'\u0429\u0435\u0440\u0431\u0430\u043a\u043e\u0432\u0430'

	fake.last_name()
	# u'\u0428\u0430\u0448\u043a\u043e\u0432'

	fake.prefix_female()
	# u'\u0442\u043e\u0432.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'+7 182 289 6002'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'9674 \u042d\u0440\u043d\u0435\u0441\u0442 Path\n\u0413\u0430\u043b\u0430\u043a\u0442\u0438\u043e\u043dshire, PW 13603-6165',
	#     'birthdate': '1983-01-21',
	#     'mail': u'\u0438\u0437\u043e\u0442\u0431\u0443\u0440\u043e\u0432@hotmail.com',
	#     'name': u'\u0433-\u0436\u0430 \u0422\u0430\u0438\u0441\u0438\u044f \u0411\u0435\u043b\u043e\u0443\u0441\u043e\u0432\u0430',
	#     'sex': 'F',
	#     'username': u'\u043f\u0430\u043d\u043a\u0440\u0430\u044277'}

	fake.profile(fields=None)
	# {   'address': u'662 \u0410\u043d\u0430\u043d\u0438\u0439 Well\n\u0418\u043b\u0430\u0440\u0438\u043e\u043dhaven, PW 93144-5726',
	#     'birthdate': '1993-06-25',
	#     'blood_group': 'B-',
	#     'company': u'\u0422\u0430\u0440\u0430\u0441\u043e\u0432\u0430 and Sons',
	#     'current_location': (Decimal('-5.0101715'), Decimal('-45.568446')),
	#     'job': u'\u0414\u0438\u043a\u0442\u043e\u0440',
	#     'mail': u'\u043c\u043e\u043b\u0447\u0430\u043d\u043e\u0432\u043a\u0443\u0437\u044c\u043c\u0430@gmail.com',
	#     'name': u'\u0410\u043d\u0433\u0435\u043b\u0438\u043d\u0430 \u0414\u043e\u0440\u043e\u043d\u0438\u043d\u0430',
	#     'residence': u'32654 \u0421\u0430\u0444\u043e\u043d\u043e\u0432\u0430 Brooks Apt. 325\nSouth \u041f\u043e\u0440\u0444\u0438\u0440\u0438\u0439, IA 65225',
	#     'sex': 'F',
	#     'ssn': u'658-24-1329',
	#     'username': u'\u0432\u043b\u0430\u0434\u0438\u043c\u0438\u044087',
	#     'website': [   u'http://www.\u043f\u043e\u0442\u0430\u043f\u043e\u0432\u0430.com/',
	#                    u'http://\u043a\u043e\u043b\u043e\u0431\u043e\u0432\u0430-\u0442\u0435\u0442\u0435\u0440\u0438\u043d\u0430.com/',
	#                    u'http://www.\u0441\u0438\u0434\u043e\u0440\u043e\u0432.com/',
	#                    u'http://\u0438\u043b\u044c\u0438\u043d\u0430.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([2816, Decimal('27368567198.3'), u'Sint sapiente dolor.', u'http://www.\u0442\u0438\u0442\u043e\u0432\u0430-\u0434\u0430\u0432\u044b\u0434\u043e\u0432\u0430.biz/posts/register/', u'Adipisci velit quia.', 9741, u'http://www.\u0434\u0430\u0432\u044b\u0434\u043e\u0432\u0430.com/category/register/', Decimal('76995.4176995'), u'Quidem ut ipsum.', u'http://\u0442\u0430\u0440\u0430\u0441\u043e\u0432-\u043c\u0430\u0441\u043b\u043e\u0432\u0430.com/', u'http://www.\u0441\u0435\u043b\u0438\u0432\u0435\u0440\u0441\u0442\u043e\u0432\u0430.net/wp-content/index/', u'\u0434\u0435\u043c\u0435\u043d\u0442\u0438\u0439\u043c\u0430\u043a\u0441\u0438\u043c\u043e\u0432@hotmail.com', Decimal('-37310.7825002')])

	fake.pystr(max_chars=20)
	# u'Assumenda aperiam.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 603597826901673.0

	fake.pystruct(count=10, *value_types)
	# (   [   datetime(1970, 6, 5, 14, 5, 47),
	#         u'Dolores molestiae.',
	#         u'\u0444\u0451\u043a\u043b\u0430\u043c\u0430\u0440\u043a\u043e\u0432\u0430@gmail.com',
	#         Decimal('479843.58694'),
	#         u'Qui voluptatem non.',
	#         -71.1847168599,
	#         6895,
	#         u'Tenetur porro.',
	#         -9.3218544847,
	#         u'Ipsa debitis est.'],
	#     {   u'beatae': 4515,
	#         u'corrupti': u'Nulla maiores est.',
	#         u'cupiditate': 8024,
	#         u'harum': u'\u0449\u0443\u043a\u0438\u043d\u0430\u0431\u043e\u0440\u0438\u0441\u043b\u0430\u0432@\u043f\u043e\u043b\u044f\u043a\u043e\u0432\u0430.com',
	#         u'quisquam': u'http://\u043a\u0443\u0437\u044c\u043c\u0438\u043d.com/',
	#         u'temporibus': datetime(2006, 10, 13, 8, 12, 15),
	#         u'vitae': u'Voluptatum.',
	#         u'voluptas': Decimal('2097732.2738'),
	#         u'voluptatem': u'm\u0433\u043e\u0440\u0431\u0443\u043d\u043e\u0432\u0430@\u0442\u0438\u0445\u043e\u043d\u043e\u0432\u0430.com'},
	#     {   u'assumenda': {   4: u'Asperiores impedit.',
	#                           5: [u'Facilis quidem.', 8262, u'Omnis ipsum et.'],
	#                           6: {   4: u'Voluptatem et.',
	#                                  5: 8258,
	#                                  6: [   u'Velit ea ut esse.',
	#                                         u'Qui vitae minima.']}},
	#         u'aut': {   8: datetime(1974, 10, 16, 22, 33, 14),
	#                     9: [u'Aut rem consectetur.', 2586, u'Impedit vel.'],
	#                     10: {   8: u'Expedita recusandae.',
	#                             9: Decimal('-769.6'),
	#                             10: [Decimal('-908.44379'), u'Corrupti illo.']}},
	#         u'dolor': {   9: u'Nobis minima.',
	#                       10: [   u'\u0448\u0438\u0440\u044f\u0435\u0432\u0430\u043c\u0438\u043b\u0438\u0446\u0430@hotmail.com',
	#                               u'Totam omnis labore.',
	#                               9456],
	#                       11: {   9: u'Ex placeat qui.',
	#                               10: datetime(1989, 9, 1, 16, 45, 50),
	#                               11: [   u'\u0432\u0435\u0440\u043054@gmail.com',
	#                                       Decimal('-125985828666')]}},
	#         u'exercitationem': {   3: u'http://www.\u0435\u0440\u043c\u0430\u043a\u043e\u0432.biz/faq/',
	#                                4: [   u'Ratione placeat.',
	#                                       u'In commodi ut odio.',
	#                                       u'Dolorem corrupti.'],
	#                                5: {   3: u'http://www.\u043a\u043e\u0442\u043e\u0432\u0430.org/category/blog/privacy.htm',
	#                                       4: u'http://\u043e\u0432\u0447\u0438\u043d\u043d\u0438\u043a\u043e\u0432.com/search.jsp',
	#                                       5: [   u'http://\u0436\u0443\u043a\u043e\u0432-\u0433\u0430\u0432\u0440\u0438\u043b\u043e\u0432\u0430.net/categories/home.html',
	#                                              u'Necessitatibus.']}},
	#         u'hic': {   7: u'http://www.\u0431\u0443\u0440\u043e\u0432.com/wp-content/post/',
	#                     8: [   u'Magni nihil impedit.',
	#                            u'b\u0442\u0440\u043e\u0444\u0438\u043c\u043e\u0432@gmail.com',
	#                            64760548644733.1],
	#                     9: {   7: 3565,
	#                            8: datetime(1988, 8, 30, 14, 28, 55),
	#                            9: [6216, u'Aut aliquid.']}},
	#         u'iste': {   2: u'Dignissimos.',
	#                      3: [   u'Aut nobis ab.',
	#                             Decimal('8.52734498148'),
	#                             Decimal('90378191.685')],
	#                      4: {   2: u'Nam adipisci sed.',
	#                             3: 50315.434942905,
	#                             4: [   Decimal('353974.72749'),
	#                                    datetime(2009, 1, 25, 18, 55, 23)]}},
	#         u'quas': {   1: datetime(1976, 5, 11, 7, 45, 3),
	#                      2: [   datetime(1998, 10, 26, 14, 8, 6),
	#                             6064,
	#                             u't\u0430\u0432\u0434\u0435\u0435\u0432@\u0443\u0432\u0430\u0440\u043e\u0432.com'],
	#                      3: {   1: u'\u043a\u043e\u0440\u043e\u043b\u0435\u0432\u0430\u0440\u043a\u0430\u0434\u0438\u0439@gmail.com',
	#                             2: u'Magni quia odit.',
	#                             3: [-6.538119047995, u'Ipsum omnis minus.']}},
	#         u'sit': {   0: u'Officiis.',
	#                     1: [   u'\u044f\u043a\u0443\u0448\u0435\u0432\u0442\u0432\u0435\u0440\u0434\u0438\u0441\u043b\u0430\u0432@gmail.com',
	#                            datetime(1992, 5, 13, 19, 53),
	#                            datetime(1985, 7, 29, 9, 0, 27)],
	#                     2: {   0: u'http://\u043f\u043e\u043d\u043e\u043c\u0430\u0440\u0435\u0432\u0430.biz/',
	#                            1: u'Quod qui ut.',
	#                            2: [7453, 2687615169788.33]}},
	#         u'totam': {   6: u'Aut voluptates sed.',
	#                       7: [   u'http://\u0438\u043b\u044c\u0438\u043d.com/author/',
	#                              datetime(1982, 2, 26, 9, 6, 22),
	#                              u'Et enim ut.'],
	#                       8: {   6: 301,
	#                              7: 8602,
	#                              8: [u'Ad sed aut aut.', u'Rerum tempora non.']}},
	#         u'ut': {   5: u'Et tempora ducimus.',
	#                    6: [   u'Totam quas quo.',
	#                           u'Aut omnis rerum.',
	#                           Decimal('-3495135339.82')],
	#                    7: {   5: -84.98500240539,
	#                           6: u'Dicta saepe.',
	#                           7: [   u'http://www.\u0443\u0432\u0430\u0440\u043e\u0432.com/',
	#                                  datetime(1977, 3, 10, 1, 8, 2)]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('531176.286593')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   5578,
	#     u'Mollitia laboriosam.',
	#     u'\u0430\u043d\u0438\u0441\u0438\u043c\u043e\u0432\u0430\u0442\u0438\u043c\u0443\u0440@\u043d\u0430\u0437\u0430\u0440\u043e\u0432\u0430.com',
	#     2256,
	#     u'Consequatur.',
	#     7431,
	#     u'Omnis nesciunt qui.',
	#     u'Et nam totam.',
	#     u'Velit ab nostrum.',
	#     u'Nam quas eos.',
	#     4913,
	#     datetime(2005, 7, 23, 20, 7, 34),
	#     Decimal('-76352376495.6'),
	#     u'Voluptas.']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   9473,
	#     8244.979278527,
	#     datetime(2011, 9, 18, 15, 8, 28),
	#     Decimal('-426532.891989'),
	#     u'\u043b\u0430\u0434\u0438\u043c\u0438\u044063@\u043f\u043e\u043f\u043e\u0432\u0430.org',
	#     -436906204.112,
	#     5106,
	#     7507,
	#     Decimal('-391.8881'),
	#     u'\u0431\u043b\u0438\u043d\u043e\u0432\u043d\u0430\u0443\u043c@\u0441\u043e\u0431\u043e\u043b\u0435\u0432\u0430.com')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([7462, u'http://www.\u0441\u0442\u0440\u0435\u043b\u043a\u043e\u0432.com/app/tags/app/homepage/', u'Excepturi.', 8974, u'\u043a\u0443\u0437\u044c\u043c\u0438\u043d\u0430\u043c\u0438\u043d\u0430@\u0431\u0443\u0440\u043e\u0432\u0430-\u0438\u0432\u0430\u043d\u043e\u0432\u0430.com', u'\u0430\u043d\u0434\u0440\u043e\u043d\u0438\u043a02@yahoo.com', u'Doloremque.', u'Quos libero.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'alias': u'Atque sed.',
	#     u'delectus': 0.1756074121,
	#     u'dicta': datetime(1973, 5, 18, 6, 9, 28),
	#     u'earum': u'Voluptatem ut.',
	#     u'laudantium': u'Et perferendis aut.',
	#     u'maiores': 5356,
	#     u'modi': 7796,
	#     u'perspiciatis': datetime(1979, 12, 30, 23, 55, 57),
	#     u'similique': u'Neque in et.',
	#     u'suscipit': Decimal('99.6614'),
	#     u'ut': datetime(1976, 3, 4, 8, 59, 21),
	#     u'vel': u'Corrupti sit ut.'}

	fake.pyint()
	# 2501

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'634-08-1937'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Windows 98; Win 9x 4.90; en-US; rv:1.9.2.20) Gecko/2012-08-04 01:02:17 Firefox/13.0'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.21.(Windows 98; Win 9x 4.90; en-US) Presto/2.9.176 Version/11.00'

	fake.windows_platform_token()
	# u'Windows NT 6.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5362 (KHTML, like Gecko) Chrome/13.0.863.0 Safari/5362'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_9) AppleWebKit/5311 (KHTML, like Gecko) Chrome/15.0.878.0 Safari/5311'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_5_2'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3 like Mac OS X; sl-SI) AppleWebKit/535.21.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B119 Safari/6535.21.4'
