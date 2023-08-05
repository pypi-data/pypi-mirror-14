
Language el_GR
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('38.391801')

	fake.region()
	# u'\u039a\u03bf\u03c1\u03b9\u03bd\u03b8\u03af\u03b1'

	fake.address()
	# u'\u039b\u03cd\u03c7\u03bd\u03c9\u03bd 97,\n404 74 \u0386\u03bc\u03c6\u03b9\u03c3\u03c3\u03b1'

	fake.street_address()
	# u'\u0392\u03b1\u03bc\u03b2\u03bf\u03c5\u03ba\u03ac\u03ba\u03b7 0'

	fake.postcode()
	# u'\u03a4\u039a 913 28'

	fake.street_name()
	# u'\u03a0\u03ac\u03c1. \u03a3\u03af\u03b2\u03b1\u03c2'

	fake.longitude()
	# Decimal('24.032970')

	fake.country()
	# u'\u039c\u03ac\u03bb\u03b9'

	fake.street_prefix()
	# u'\u039b\u03b5\u03c9\u03c6\u03cc\u03c1\u03bf\u03c2'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-1.888586')

	fake.street()
	# u'\u0391\u03c1\u03b3\u03bf\u03bb\u03b9\u03ba\u03bf\u03cd'

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'2'

	fake.country_code()
	# u'MZ'

	fake.line_address()
	# u'\u039b\u03b5\u03c9\u03c6\u03cc\u03c1\u03bf\u03c2 \u0396\u03b5\u03bd\u03af\u03c9\u03bd 9, 83906 \u03a7\u03b1\u03bb\u03ba\u03af\u03b4\u03b1'

	fake.latlng()
	# (40.258966, 25.871771)

	fake.city()
	# u'\u03a7\u03b1\u03bb\u03ba\u03af\u03b4\u03b1'

	fake.street_prefix_long()
	# u'\u03a0\u03bb\u03b1\u03c4\u03b5\u03af\u03b1'

	fake.street_prefix_short()
	# u'\u03a0\u03bb.'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'9556470080079'

	fake.ean13()
	# u'1718427605317'

	fake.ean8()
	# u'29354573'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(98,105,126)'

	fake.color_name()
	# u'CadetBlue'

	fake.rgb_color_list()
	# (42, 48, 65)

	fake.rgb_color()
	# u'120,58,79'

	fake.safe_hex_color()
	# u'#ff1100'

	fake.safe_color_name()
	# u'aqua'

	fake.hex_color()
	# u'#8e8166'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\u0392\u03b1\u03b2\u03ac\u03c3\u03b7-\u03a1\u03b1\u03c7\u03bc\u03b1\u03bd\u03af\u03b4\u03b7\u03c2'

	fake.company_suffix()
	# u'and Sons'

	fake.catch_phrase()
	# u'Automated scalable circuit'

	fake.bs()
	# u'transform interactive info-mediaries'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'537'

	fake.credit_card_provider(card_type=None)
	# u'VISA 13 digit'

	fake.credit_card_full(card_type=None)
	# u'VISA 13 digit\n\u0395\u03c5\u03b1\u03bd\u03b8\u03af\u03b1 \u0398\u03c9\u03bc\u03cc\u03c0\u03bf\u03c5\u03bb\u03bf\u03c2\n4149069536945 01/24\nCVC: 938\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '05/16'

	fake.credit_card_number(card_type=None)
	# u'30068088262218'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'MDL'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '16'

	fake.month()
	# '01'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 1, 54, 47)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2008, 12, 27, 3, 54, 41)

	fake.time(pattern="%H:%M:%S")
	# '07:43:49'

	fake.year()
	# '1995'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(553, 12, 24, 0, 35, 40)

	fake.day_of_week()
	# 'Thursday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 4, 15, 37, 19)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 8, 21, 18, 13, 45)

	fake.unix_time()
	# 62882865

	fake.month_name()
	# 'June'

	fake.timezone()
	# u'Europe/Podgorica'

	fake.time_delta()
	# datetime.timedelta(15631, 85402)

	fake.century()
	# u'X'

	fake.date(pattern="%Y-%m-%d")
	# '1979-06-09'

	fake.iso8601(tzinfo=None)
	# '2010-03-26T06:52:41'

	fake.date_time(tzinfo=None)
	# datetime(1991, 4, 30, 2, 42, 40)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 7, 28, 4, 17, 14)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'audio/vnd.rn-realaudio'

	fake.file_name(category=None, extension=None)
	# u'praesentium.mp4'

	fake.file_extension(category=None)
	# u'flac'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'43.66.156.204'

	fake.url()
	# u'http://triantakonstantis-kondylidis.gr/'

	fake.company_email()
	# u'tsomokos.panteleimon@theodorikakos.com'

	fake.uri()
	# u'http://www.giannoukos.com/'

	fake.domain_word(*args, **kwargs)
	# u'papananou'

	fake.image_url(width=None, height=None)
	# u'https://placeholdit.imgix.net/~text?txtsize=55&txt=957\xd7626&w=957&h=626'

	fake.tld()
	# u'gr'

	fake.free_email()
	# u'theodoulos.satlas@forthnet.gr'

	fake.slug(*args, **kwargs)
	# u'earum-eos-qui'

	fake.free_email_domain()
	# u'yahoo.gr'

	fake.domain_name()
	# u'gratsias.gr'

	fake.uri_extension()
	# u'.jsp'

	fake.ipv6()
	# u'891f:2759:5f3f:6a6d:f95a:e32c:213c:f0e1'

	fake.safe_email()
	# u'wmanopoulou@example.net'

	fake.user_name(*args, **kwargs)
	# u'meropi93'

	fake.uri_path(deep=None)
	# u'wp-content/tags'

	fake.email()
	# u'chorinou.diogenis@milea.com'

	fake.uri_page()
	# u'main'

	fake.mac_address()
	# u'41:82:2f:e4:e0:0c'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Geologist, engineering'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'\u03a0\u03bb\u03ad\u03bf\u03bd \u03b1\u03c1\u03ad\u03c3\u03b5\u03b9 \u03bc\u03bf\u03c5 \u03b7\u03bc\u03ad\u03c1\u03b1 \u03bc\u03b5\u03c4\u03c1\u03ac\u03b5\u03b9 \u03c0\u03b5\u03c1\u03b9\u03bc\u03ad\u03bd\u03bf\u03c5\u03bd. \u039c\u03ad\u03c3\u03b7\u03c2 \u03c0\u03c1\u03ce\u03c4\u03bf\u03b9 \u03b5\u03b3\u03ce \u03c3\u03c9\u03c3\u03c4\u03ac \u03c4\u03b1\u03be\u03b9\u03bd\u03bf\u03bc\u03b5\u03af \u03c3\u03b5 \u03c0\u03bf\u03c3\u03bf\u03c3\u03c4\u03cc \u03b8\u03b1 \u03b1\u03c4\u03cc\u03bc\u03bf\u03c5. \u03a0\u03b1\u03c1\u03b1\u03c0\u03ac\u03bd\u03c9 \u03b4\u03b9\u03bf\u03b9\u03ba\u03b7\u03c4\u03b9\u03ba\u03cc \u03c4\u03cd\u03c0\u03bf\u03c5\u03c2 \u03c4\u03bf\u03bd \u03c0\u03ae\u03c1\u03b5 \u03b4\u03af\u03bd\u03bf\u03bd\u03c4\u03b1\u03c2 \u03c0\u03c1\u03cc\u03c3\u03bb\u03b7\u03c8\u03b7 \u03c3\u03b5. \u039c\u03ad\u03c7\u03c1\u03b9 \u03c0\u03ac\u03c1\u03b5\u03b9\u03c2 \u03b4\u03bf\u03c5\u03bb\u03b5\u03cd\u03b5\u03b9 \u03b4\u03b5\u03bd \u03bc\u03c0\u03bf\u03c5\u03bd \u03ba\u03cc\u03bb\u03c0\u03b1.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'\u0394\u03b9\u03b5\u03c5\u03b8\u03c5\u03bd\u03c4\u03ad\u03c2 \u03c4\u03c9\u03bd \u03af\u03b4\u03b9\u03bf \u03b5\u03c0\u03b9\u03b4\u03b9\u03cc\u03c1\u03b8\u03c9\u03c3\u03b7 \u03b4\u03b9\u03b1\u03c6\u03ae\u03bc\u03b9\u03c3\u03b7 \u03b1\u03bd\u03ce\u03b4\u03c5\u03bd\u03b7.'

	fake.word()
	# u'\u03b5\u03ba\u03c4\u03b5\u03bb\u03ad\u03c3\u03b5\u03b9'

	fake.paragraphs(nb=3)
	# [   u'\u039a\u03bf\u03b9\u03c4\u03ac\u03b6\u03bf\u03bd\u03c4\u03b1\u03c2 \u03bc\u03b9\u03b1 \u03ba\u03ac\u03c4\u03b9 \u03c0\u03c1\u03bf\u03b2\u03bb\u03b7\u03bc\u03b1\u03c4\u03b9\u03ba\u03ae \u03c0\u03b1\u03c1\u03b1\u03c0\u03ac\u03bd\u03c9 \u03b8\u03b1 \u03bc\u03b1\u03c2 \u03ae\u03b4\u03b7 \u03b1\u03c0\u03bf\u03bc\u03cc\u03bd\u03c9\u03c3\u03b7. \u0395\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ae\u03c2 \u03b4\u03c5\u03c3\u03c4\u03c5\u03c7\u03ae\u03c2 \u03ba\u03ac\u03c4\u03b9 \u03b1\u03c0\u03b1\u03c1\u03b1\u03af\u03c4\u03b7\u03c4\u03bf. \u039b\u03b5\u03c2 \u03ba\u03bf\u03b9\u03c4\u03ac\u03b6\u03bf\u03bd\u03c4\u03b1\u03c2 \u03b1\u03bd\u03b1\u03c6\u03bf\u03c1\u03ac \u03c0\u03c1\u03bf\u03c3\u03bf\u03c7\u03ae. \u039c\u03bf\u03c5 \u03b5\u03ba\u03b8\u03ad\u03c3\u03b5\u03b9\u03c2 \u03c4\u03b9\u03c2 \u03b4\u03b9\u03ac\u03c3\u03b7\u03bc\u03b1 \u03b5\u03b4\u03ce \u03b8\u03ad\u03bb\u03b5\u03b9\u03c2 \u03c3\u03bf\u03c5 \u03b1\u03c0\u03b1\u03c1\u03ac\u03b4\u03b5\u03ba\u03c4\u03b7.',
	#     u'\u0386\u03c4\u03bf\u03bc\u03bf \u03af\u03b4\u03b9\u03bf \u03c0\u03b1\u03c1\u03b1\u03b4\u03ce\u03c3\u03b5\u03b9\u03c2 \u03b2\u03b3\u03ae\u03ba\u03b5 \u03b8\u03ad\u03bb\u03b5\u03b9\u03c2 \u03b7\u03bc\u03ad\u03c1\u03b1 \u03c4\u03b5\u03ba\u03bc\u03b7\u03c1\u03b9\u03ce\u03bd\u03b5\u03b9 \u03b1\u03b3\u03bf\u03c1\u03ac\u03b6\u03bf\u03bd\u03c4\u03b1\u03c2. \u0388\u03b3\u03c1\u03b1\u03c8\u03b5\u03c2 \u03bf \u03b3\u03c1\u03b1\u03bc\u03bc\u03ad\u03c2 \u03b5\u03c5\u03ba\u03bf\u03bb\u03cc\u03c4\u03b5\u03c1\u03bf \u03bc\u03c0\u03bf\u03c5\u03bd \u03c3\u03c4\u03bf \u03b2\u03bf\u03c5\u03c4\u03ae\u03be\u03bf\u03c5\u03bd \u03ad\u03c7\u03c9. \u0394\u03b9\u03b1\u03c6\u03ae\u03bc\u03b9\u03c3\u03b7 \u03ac\u03c4\u03bf\u03bc\u03bf \u03c4\u03c1\u03ad\u03be\u03b5\u03b9 \u03b1\u03bd\u03ac \u03ba\u03bf\u03b9\u03c4\u03ac\u03b6\u03bf\u03bd\u03c4\u03b1\u03c2 \u03b1\u03b8\u03cc\u03c1\u03c5\u03b2\u03b5\u03c2. \u03a3\u03b1\u03c2 \u03c3\u03bf\u03c5 \u03c0\u03c1\u03bf\u03c3\u03b8\u03ad\u03c3\u03b5\u03b9 \u03b1\u03c0\u03cc\u03bb\u03b1\u03c5\u03c3\u03b5 \u03b3\u03b5\u03b9\u03c4\u03bf\u03bd\u03b9\u03ac\u03c2 \u03c0\u03c1\u03bf\u03b3\u03c1\u03b1\u03bc\u03bc\u03b1\u03c4\u03b9\u03c3\u03c4\u03ad\u03c2 \u03c7\u03c1\u03b7\u03c3\u03b9\u03bc\u03bf\u03c0\u03bf\u03b9\u03bf\u03cd\u03bd\u03c4\u03b1\u03bd \u03bc\u03b9\u03b1\u03c2.',
	#     u'\u03a0\u03b9\u03bf \u03c3\u03ba\u03b5\u03c6\u03c4\u03b5\u03af\u03c2 \u03b5\u03b4\u03ce \u03b4\u03cd\u03bf \u03bc\u03b7\u03bd \u03b5\u03c0\u03b9\u03b4\u03b9\u03bf\u03c1\u03b8\u03ce\u03c3\u03b5\u03b9\u03c2. \u03a4\u03b5\u03c3\u03c3\u03b1\u03c1\u03ce\u03bd \u03c4\u03b9\u03c2 \u03ad\u03c7\u03c9 \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf \u03ad\u03bd\u03b1\u03c2 \u03ba\u03b5\u03b9\u03bc\u03ad\u03bd\u03c9\u03bd \u03c7\u03b1\u03c1\u03b1\u03ba\u03c4\u03b7\u03c1\u03b9\u03c3\u03c4\u03b9\u03ba\u03cc \u03c4\u03b9\u03c2 \u03bc\u03c0\u03bf\u03c5\u03bd. \u0388\u03c7\u03c9 \u03c3\u03c4\u03b1\u03bc\u03b1\u03c4\u03ac\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03bc\u03b5 \u03b3\u03bd\u03c9\u03c3\u03c4\u03ae.']

	fake.words(nb=3)
	# [   u'\u03b8\u03ad\u03bc\u03b1',
	#     u'\u03c0\u03b5\u03c2',
	#     u'\u03ba\u03ac\u03bd\u03b5\u03b9\u03c2']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'\u03a0\u03c1\u03bf\u03c3\u03c0\u03b1\u03b8\u03ae\u03c3\u03b5\u03b9\u03c2 \u03b1\u03c1\u03ad\u03c3\u03b5\u03b9 \u03b5\u03c0\u03b5\u03be\u03b5\u03c1\u03b3\u03b1\u03c3\u03af\u03b1 \u03ad\u03c4\u03bf\u03b9\u03bc\u03bf\u03c2 \u03bb\u03b9\u03b3\u03cc\u03c4\u03b5\u03c1\u03bf. \u0393\u03b5\u03b9\u03c4\u03bf\u03bd\u03b9\u03ac\u03c2 \u03c5\u03c8\u03b7\u03bb\u03cc\u03c4\u03b5\u03c1\u03b7 \u03c3\u03c4\u03b9\u03c2 \u03b1\u03c0\u03b1\u03c1\u03b1\u03af\u03c4\u03b7\u03c4\u03bf \u03c0\u03ac\u03bd\u03c4\u03c9\u03c2 \u03b2\u03b3\u03ae\u03ba\u03b5 \u03b4\u03c5\u03c3\u03c4\u03c5\u03c7\u03ae\u03c2 \u03c4\u03b1. \u0388\u03c3\u03c4\u03b5\u03bb\u03bd\u03b5 \u03c3\u03c4\u03b1 \u03c0\u03b5\u03c1\u03af\u03c0\u03bf\u03c5 \u03b8\u03ad\u03bb\u03b5\u03b9\u03c2 \u03c5\u03c0\u03bf\u03c8\u03ae\u03c6\u03b9\u03bf \u03c4\u03b7\u03c2 \u03ac\u03c1\u03b1 \u03b1\u03b8\u03cc\u03c1\u03c5\u03b2\u03b5\u03c2.'

	fake.sentences(nb=3)
	# [   u'\u03a6\u03c1\u03ac\u03c3\u03b7 \u03ba\u03b1\u03bd\u03cc\u03bd\u03b1 \u03c0\u03bb\u03ad\u03bf\u03bd \u03b4\u03af\u03bd\u03bf\u03bd\u03c4\u03b1\u03c2 \u03c0\u03c1\u03bf\u03c3\u03b8\u03ad\u03c3\u03b5\u03b9.',
	#     u'\u03a0\u03b5\u03c1\u03af\u03c0\u03bf\u03c5 \u03c4\u03b7\u03bd \u03c0\u03b5\u03c1\u03b9\u03bc\u03ad\u03bd\u03bf\u03c5\u03bd \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03c0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03b9\u03ba\u03ae\u03c2 \u03b5\u03ba\u03c4\u03b5\u03bb\u03ad\u03c3\u03b5\u03b9 \u03ac\u03c0\u03b5\u03b9\u03c1\u03b1.',
	#     u'\u0391\u03c0\u03af\u03c3\u03c4\u03b5\u03c5\u03c4\u03b1 \u03c0\u03b1\u03c1\u03ac\u03b3\u03bf\u03bd\u03c4\u03b5\u03c2 \u03c3\u03bf\u03c5 \u03c5\u03cc\u03c1\u03ba\u03b7 \u03c0\u03b7\u03b3\u03b1\u03af\u03bf\u03c5 \u03c4\u03bf\u03bd \u03c7\u03c1\u03b7\u03c3\u03b9\u03bc\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03ad.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'9Bi3ifGh@0'

	fake.locale()
	# u'ru_BG'

	fake.md5(raw_output=False)
	# 'd5227de9c867a3ea40535608e5683406'

	fake.sha1(raw_output=False)
	# '3b62737a1e8b7d3fa5f01ad40b9e408aa70b55d3'

	fake.null_boolean()
	# False

	fake.sha256(raw_output=False)
	# 'b8fb80d4ddcf3eeeb264ff8f9a74c00bc068a5c598e5d8e3a3af5ab6339aa689'

	fake.uuid4()
	# '0537540e-594b-48b8-b2c4-b81981d62052'

	fake.language_code()
	# u'el'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u039f\u03c1\u03c6\u03b1\u03bd\u03b9\u03ce\u03c4\u03b7\u03c2'

	fake.name_female()
	# u'\u0394\u03b9\u03bf\u03bd\u03c5\u03c3\u03af\u03b1 \u03a6\u03c1\u03b1\u03b3\u03ba\u03bf\u03c5\u03b4\u03ac\u03ba\u03b7'

	fake.prefix_male()
	# ''

	fake.prefix()
	# ''

	fake.name()
	# u'\u039a\u03af\u03bc\u03c9\u03bd-\u039a\u03bb\u03ae\u03bc\u03b7\u03c2 \u0392\u03ac\u03c3\u03c3\u03b7\u03c2'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'\u039c\u03b5\u03bb\u03ad\u03c4\u03b9\u03bf\u03c2 \u0395\u03c5\u03ba\u03b1\u03c1\u03c0\u03af\u03b4\u03b7\u03c2'

	fake.first_name()
	# u'\u039b\u03b1\u03bf\u03ba\u03c1\u03ac\u03c4\u03b7\u03c2'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'\u039c\u03b9\u03c7\u03ac\u03bb\u03b7\u03c2'

	fake.first_name_female()
	# u'\u0391\u03bd\u03b4\u03c1\u03bf\u03bc\u03ad\u03b4\u03b1'

	fake.last_name_female()
	# u'\u03a4\u03c3\u03ce\u03bd\u03b7'

	fake.last_name()
	# u'\u0392\u03bf\u03cd\u03ba\u03b1\u03c2'

	fake.prefix_female()
	# ''

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'(+30) 6981 078276'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'\u0398\u03b5\u03bf\u03b4\u03c9\u03c1\u03bf\u03c0\u03bf\u03cd\u03bb\u03bf\u03c5 303,\n23697 \u039a\u03cc\u03c1\u03b9\u03bd\u03b8\u03bf\u03c2',
	#     'birthdate': '1993-04-12',
	#     'mail': u'mastrogiannis.klimis@googlemail.gr',
	#     'name': u'\u0393\u03b1\u03bb\u03ae\u03bd\u03b7 \u03a3\u03c4\u03b1\u03c5\u03c1\u03af\u03b4\u03bf\u03c5',
	#     'sex': 'F',
	#     'username': u'georgakopoulou.panagia'}

	fake.profile(fields=None)
	# {   'address': u'\u03a7\u03b1\u03c4\u03b6\u03b7\u03c7\u03b1\u03c1\u03af\u03c3\u03c4\u03bf\u03c5 289-060,\n\u03a4\u039a 66756 \u03a0\u03c1\u03ad\u03b2\u03b5\u03b6\u03b1',
	#     'birthdate': '1997-12-21',
	#     'blood_group': 'B+',
	#     'company': u'\u0393\u03b1\u03b2\u03c1\u03b9\u03ae\u03bb, \u0393\u03b5\u03c9\u03c1\u03b3\u03b1\u03ba\u03cc\u03c0\u03bf\u03c5\u03bb\u03bf\u03c2 and \u0394\u03bf\u03c5\u03c1\u03ac\u03bd\u03b7\u03c2',
	#     'current_location': (Decimal('35.829671'), Decimal('23.109207')),
	#     'job': 'Accounting technician',
	#     'mail': u'marotesa.dramountani@yahoo.gr',
	#     'name': u'\u0394\u03ad\u03c3\u03c0\u03bf\u03b9\u03bd\u03b1 \u03a3\u03c0\u03b1\u03bd\u03bf\u03c7\u03c1\u03b9\u03c3\u03c4\u03bf\u03b4\u03bf\u03cd\u03bb\u03bf\u03c5',
	#     'residence': u'\u039a\u03b1\u03bb\u03ce\u03bd \u039d\u03b5\u03c1\u03ce\u03bd 24,\n\u03a4\u039a 804 70 \u0386\u03bc\u03c6\u03b9\u03c3\u03c3\u03b1',
	#     'sex': 'F',
	#     'ssn': u'789-66-0421',
	#     'username': u'stergianno93',
	#     'website': [u'http://voukas-douvali.org/', u'http://www.kouzoula.gr/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   5058,
	#     8677,
	#     6348,
	#     9613,
	#     u'http://www.stylianidou.gr/home.asp',
	#     u'Recusandae eveniet.',
	#     u'Sit excepturi ipsum.',
	#     -9147272478827.59,
	#     u'Dolorem explicabo.',
	#     u'Consequatur.')

	fake.pystr(max_chars=20)
	# u'Ullam doloremque ad.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 4.2572369895

	fake.pystruct(count=10, *value_types)
	# (   [   u'Explicabo omnis.',
	#         u'qchasapi@sefekos.net',
	#         u'Eum rerum at omnis.',
	#         u'magdalini75@smyrniotis-tsiatis.com',
	#         2710,
	#         u'Exercitationem.',
	#         u'kchatziaras@otenet.gr',
	#         Decimal('26.714858'),
	#         7421,
	#         -65.45565674405],
	#     {   u'dolores': 7072,
	#         u'et': Decimal('-91147064429.0'),
	#         u'ipsam': u'Qui unde.',
	#         u'nihil': 3216,
	#         u'quis': 3181,
	#         u'quisquam': u'Repellat dicta sit.',
	#         u'totam': -323.10077920034,
	#         u'ut': -828410210.2233,
	#         u'voluptates': u'Quam quasi et rerum.'},
	#     {   u'aspernatur': {   0: u'tilemachos33@gmail.com',
	#                            1: [   7566,
	#                                   datetime(2001, 5, 30, 23, 42, 58),
	#                                   datetime(1992, 9, 4, 15, 37, 10)],
	#                            2: {   0: u'Repellendus aut.',
	#                                   1: u'Incidunt et placeat.',
	#                                   2: [u'Maxime enim aut.', 756]}},
	#         u'cum': {   4: u'Quae facilis ut.',
	#                     5: [25.0, 6988, u'Quis deleniti sint.'],
	#                     6: {   4: u'Non et repellat eum.',
	#                            5: datetime(1981, 11, 21, 1, 29, 51),
	#                            6: [   datetime(1975, 4, 6, 8, 0, 53),
	#                                   u'nsaoulidis@googlemail.gr']}},
	#         u'delectus': {   2: u'Blanditiis mollitia.',
	#                          3: [   u'fthivaios@mammis.gr',
	#                                 u'charteros.klimentini@psyllakis-manta.gr',
	#                                 -275730.716280852],
	#                          4: {   2: 6804192583.579,
	#                                 3: 5538,
	#                                 4: [   u'Incidunt non vitae.',
	#                                        u'Dolorem veniam.']}},
	#         u'et': {   6: u'Voluptatem omnis ex.',
	#                    7: [-2554.98, -9.4673, u'Nulla dolores nemo.'],
	#                    8: {   6: Decimal('-944.539928633'),
	#                           7: u'http://rogaris-kolkas.gr/wp-content/tags/explore/homepage.html',
	#                           8: [u'Consequatur neque.', 8821]}},
	#         u'harum': {   8: u'Eos voluptatibus ut.',
	#                       9: [   u'Tempora ipsum at ut.',
	#                              datetime(2004, 8, 11, 23, 15, 34),
	#                              6140],
	#                       10: {   8: u'http://danelis.gr/post/',
	#                               9: 7857,
	#                               10: [2704, 6483]}},
	#         u'magni': {   3: 7315,
	#                       4: [   u'Iste veritatis.',
	#                              datetime(2003, 7, 3, 12, 50, 18),
	#                              u'http://www.chatzantonis.gr/'],
	#                       5: {   3: u'Minima eveniet.',
	#                              4: u'Quod quae.',
	#                              5: [   datetime(1980, 5, 25, 17, 11, 42),
	#                                     Decimal('-74250.4035233')]}},
	#         u'natus': {   7: u'Temporibus ipsa.',
	#                       8: [   Decimal('-534.0'),
	#                              u'http://www.vildos.com/category/',
	#                              6230],
	#                       9: {   7: -8820921286700.0,
	#                              8: u'Praesentium.',
	#                              9: [u'Voluptatum.', 7140]}},
	#         u'quaerat': {   9: Decimal('-6.67554586461E+12'),
	#                         10: [   u'Temporibus magni ea.',
	#                                 u'Asperiores soluta.',
	#                                 Decimal('6889515.0')],
	#                         11: {   9: 3609,
	#                                 10: Decimal('-3.46334652148E+12'),
	#                                 11: [   u'Minima distinctio.',
	#                                         u'http://rousianos-spasopoulos.net/']}},
	#         u'vel': {   1: u'http://driva.com/index.asp',
	#                     2: [   u'http://www.kitsou.org/homepage/',
	#                            u'http://www.chasapi-daniilidis.net/login.htm',
	#                            u'Non quae asperiores.'],
	#                     3: {   1: 4630,
	#                            2: u'Aut aut.',
	#                            3: [   u'Sed repellendus ut.',
	#                                   u'Aut ea atque qui.']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-199719217513')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'http://vasilakis-karatzaferis.org/',
	#     Decimal('-62397150.3004'),
	#     u'http://papananou.com/',
	#     u'http://www.sokolaki-mauroutsos.net/tag/author/',
	#     u'http://mpotza-iosifidis.com/',
	#     u'Omnis natus.',
	#     u'Id eveniet corrupti.']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'http://www.zeglina.com/homepage.htm',
	#     -6.4705470629472,
	#     -301365277.514,
	#     datetime(1980, 6, 16, 14, 43, 28),
	#     u'http://giannoukos.com/posts/search/faq/',
	#     u'kontakos.ion@sfyrlas-arampatzis.com',
	#     u'Explicabo alias.',
	#     Decimal('3.45879082'),
	#     u'Doloribus.')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'kleinaki.theofylaktos@mauroudis.com', Decimal('978405.46'), u'Laborum harum enim.', 7718, u'rgavriilidi@googlemail.gr', u'eustratios.asaridis@forthnet.gr', u'Vitae nobis iure.', 7195, 4542])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'consequatur': 7825,
	#     u'enim': u'http://www.apostolakis.gr/main/',
	#     u'fugit': u'Dignissimos.',
	#     u'inventore': u'Quia voluptatem nam.',
	#     u'natus': 685309.349,
	#     u'neque': u'Modi ipsum.',
	#     u'quae': u'Iste fugit repellat.',
	#     u'quam': u'http://tymviou.com/categories/terms/',
	#     u'sed': 9563,
	#     u'sint': u'Facilis occaecati.',
	#     u'vitae': Decimal('2.18767158107E+12'),
	#     u'voluptate': -11585862.901923}

	fake.pyint()
	# 8927

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'349-40-5130'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_9; rv:1.9.3.20) Gecko/2015-02-05 23:16:23 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.54.(X11; Linux i686; it-IT) Presto/2.9.161 Version/11.00'

	fake.windows_platform_token()
	# u'Windows NT 5.01'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows CE; Trident/3.0)'

	fake.user_agent()
	# u'Opera/8.89.(Windows NT 5.0; it-IT) Presto/2.9.181 Version/11.00'

	fake.chrome()
	# u'Mozilla/5.0 (Windows 95) AppleWebKit/5341 (KHTML, like Gecko) Chrome/15.0.845.0 Safari/5341'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; PPC Mac OS X 10_7_6'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows CE) AppleWebKit/532.48.3 (KHTML, like Gecko) Version/4.0.1 Safari/532.48.3'
