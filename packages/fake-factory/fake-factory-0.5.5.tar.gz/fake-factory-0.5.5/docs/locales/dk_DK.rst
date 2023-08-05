
Language dk_DK
===============

``faker.providers.address``
---------------------------

::

	fake.longitude()
	# Decimal('-94.300906')

	fake.building_number()
	# u'11216'

	fake.street_address()
	# u'48921 Sophie Extension Suite 642'

	fake.postalcode_plus4()
	# u'57164-7820'

	fake.city_prefix()
	# u'West'

	fake.military_ship()
	# u'USCGC'

	fake.country_code()
	# u'BR'

	fake.city()
	# u'Ren\xe9fort'

	fake.zipcode_plus4()
	# u'97301-8297'

	fake.state_abbr()
	# u'FL'

	fake.latitude()
	# Decimal('-62.204752')

	fake.street_suffix()
	# u'Loaf'

	fake.city_suffix()
	# u'berg'

	fake.military_dpo()
	# u'Unit 4941 Box 0763'

	fake.country()
	# u'Malaysia'

	fake.secondary_address()
	# u'Apt. 324'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('38.762207')

	fake.postalcode()
	# u'48410'

	fake.address()
	# u'Unit 1924 Box 8617\nDPO AE 12197'

	fake.state()
	# u'Utah'

	fake.military_state()
	# u'AE'

	fake.street_name()
	# u'Caroline Brooks'

	fake.zipcode()
	# u'42541'

	fake.postcode()
	# u'98944'

	fake.military_apo()
	# u'PSC 0485, Box 4491'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'3326802009568'

	fake.ean13()
	# u'0240640877079'

	fake.ean8()
	# u'90894978'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(174,132,167)'

	fake.color_name()
	# u'Indigo'

	fake.rgb_color_list()
	# (33, 232, 131)

	fake.rgb_color()
	# u'31,138,228'

	fake.safe_hex_color()
	# u'#55aa00'

	fake.safe_color_name()
	# u'gray'

	fake.hex_color()
	# u'#5f551c'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Olesen-Johansen'

	fake.company_suffix()
	# u'and Sons'

	fake.catch_phrase()
	# u'Programmable radical knowledgebase'

	fake.bs()
	# u'benchmark dynamic methodologies'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'340'

	fake.credit_card_provider(card_type=None)
	# u'Diners Club / Carte Blanche'

	fake.credit_card_full(card_type=None)
	# u'Mastercard\nLeif Skov\n5392266115601140 04/20\nCVV: 423\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '12/20'

	fake.credit_card_number(card_type=None)
	# u'3088294193558085'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'KGS'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '20'

	fake.month()
	# '02'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 5, 21, 52)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1999, 9, 19, 16, 9, 28)

	fake.time(pattern="%H:%M:%S")
	# '00:55:01'

	fake.year()
	# '1981'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(518, 12, 10, 10, 37, 58)

	fake.day_of_week()
	# 'Thursday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 14, 30, 20)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 5, 31, 1, 49)

	fake.unix_time()
	# 1393517522

	fake.month_name()
	# 'April'

	fake.timezone()
	# u'Indian/Maldives'

	fake.time_delta()
	# datetime.timedelta(2833, 25122)

	fake.century()
	# u'XX'

	fake.date(pattern="%Y-%m-%d")
	# '2007-06-29'

	fake.iso8601(tzinfo=None)
	# '1977-11-13T06:06:54'

	fake.date_time(tzinfo=None)
	# datetime(1977, 6, 19, 20, 23, 33)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 6, 29, 22, 32, 45)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'image/tiff'

	fake.file_name(category=None, extension=None)
	# u'quaerat.png'

	fake.file_extension(category=None)
	# u'tiff'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'132.155.211.254'

	fake.url()
	# u'http://mikkelsen.com/'

	fake.company_email()
	# u'kirstenklausen@skov-lund.com'

	fake.uri()
	# u'http://www.kristoffersen-gregersen.com/blog/explore/category/category.htm'

	fake.domain_word(*args, **kwargs)
	# u'n\xf8rgaard-schou'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/404x514'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'emmafriis@gmail.com'

	fake.slug(*args, **kwargs)
	# u'quos-quis-dolorem'

	fake.free_email_domain()
	# u'hotmail.com'

	fake.domain_name()
	# u'holst.info'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'd8aa:0b8a:2c57:6165:a0ca:71db:cce6:a452'

	fake.safe_email()
	# u'rmathiesen@example.net'

	fake.user_name(*args, **kwargs)
	# u'carina35'

	fake.uri_path(deep=None)
	# u'tag/main/categories'

	fake.email()
	# u'michelle21@hotmail.com'

	fake.uri_page()
	# u'main'

	fake.mac_address()
	# u'b2:73:7c:c3:8d:7c'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Environmental manager'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Totam repudiandae et recusandae odit sunt doloremque aliquam natus. Assumenda iusto praesentium a eos. Consectetur quis voluptas reprehenderit reprehenderit sit.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Repellendus esse cum ipsum voluptas.'

	fake.word()
	# u'voluptatum'

	fake.paragraphs(nb=3)
	# [   u'Distinctio est rerum consequatur. Iure cumque modi nostrum numquam.',
	#     u'Et error qui qui voluptatibus facilis. Ducimus vitae consectetur omnis dolorem natus numquam aliquid quo. Quia quo omnis et odit in omnis iste.',
	#     u'Corporis est non nihil ratione adipisci iusto atque animi. Ullam odio vero voluptas fugit dolores asperiores. Quis perferendis quia voluptas aut.']

	fake.words(nb=3)
	# [u'quas', u'dicta', u'et']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Ratione sed officiis ut doloribus blanditiis velit. Expedita earum illo eaque aut. Dolorem impedit magnam possimus eos. Non voluptatum totam amet in omnis quam aut nostrum. Ut voluptatem similique voluptas ea.'

	fake.sentences(nb=3)
	# [   u'Est harum consequatur dolore necessitatibus quas sed.',
	#     u'Quis ut voluptatem corrupti tempore est.',
	#     u'Sint rerum quos accusamus rerum atque nihil.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'aa4NJnnh&0'

	fake.locale()
	# u'ru_BN'

	fake.md5(raw_output=False)
	# '1ccfac991f039dfd3a9211a248d338cf'

	fake.sha1(raw_output=False)
	# '8e6a0f243d3dc3581b882490dac02811940248c3'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '38b45f55bb8203147b6f692a2f4c87d2a7c72012496bece1ef75b13967b367f4'

	fake.uuid4()
	# '6d6ddd2e-402e-4ed0-9de0-823aee37e3e4'

	fake.language_code()
	# u'cn'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Steffensen'

	fake.name_female()
	# u'Fru Mette  Thomsen'

	fake.prefix_male()
	# u'Univ.Prof.'

	fake.prefix()
	# u'Univ.Prof.'

	fake.name()
	# u'Katcha Eriksen'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Irma Schmidt'

	fake.first_name()
	# u'Mathias'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Bo'

	fake.first_name_female()
	# u'Anne'

	fake.last_name_female()
	# u'Krogh'

	fake.last_name()
	# u'Paulsen'

	fake.prefix_female()
	# u'Dr.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'+45(0)2947 66499'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Unit 7713 Box 3780\nDPO AE 76819-5689',
	#     'birthdate': '2011-03-31',
	#     'mail': u'ove82@yahoo.com',
	#     'name': u'Univ.Prof. Clara S\xf8ndergaard',
	#     'sex': 'F',
	#     'username': u'marianne31'}

	fake.profile(fields=None)
	# {   'address': u'832 Gorm Park Suite 077\nKlarabury, LA 02594-4410',
	#     'birthdate': '1976-11-01',
	#     'blood_group': 'A+',
	#     'company': u'Laursen-Jensen',
	#     'current_location': (Decimal('-48.1210035'), Decimal('-124.129027')),
	#     'job': 'Horticulturist, commercial',
	#     'mail': u'overgaardmathias@gmail.com',
	#     'name': u'Kristian Lassen',
	#     'residence': u'734 Bobby Wells\nNew Carsten, FL 13080',
	#     'sex': 'M',
	#     'ssn': u'065-46-7926',
	#     'username': u'toftbirthe',
	#     'website': [   u'http://www.thomsen.com/',
	#                    u'http://thomsen-frederiksen.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'mathiesenchristoffer@gmail.com',
	#     -8572.8706016,
	#     1284,
	#     datetime(2011, 3, 4, 0, 41, 30),
	#     Decimal('88838.9'),
	#     3978,
	#     u'Et nemo ut.',
	#     u'Molestiae.',
	#     702512630507218.0,
	#     u'http://kj\xe6r-kristensen.com/login/',
	#     u'aandersen@gmail.com',
	#     3802,
	#     datetime(1979, 12, 26, 8, 24, 8))

	fake.pystr(max_chars=20)
	# u'At blanditiis.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 337117556195929.0

	fake.pystruct(count=10, *value_types)
	# (   [   u'Sunt et omnis omnis.',
	#         u'merete53@friis.com',
	#         Decimal('-107.4'),
	#         u'http://\xf8stergaard.com/category/',
	#         9396,
	#         u'Natus voluptas.',
	#         u'Officia et in aut.',
	#         u'Quo aut quis.',
	#         u'Voluptas at.',
	#         u'stina56@hotmail.com'],
	#     {   u'ipsum': Decimal('3.24378202485E+14'),
	#         u'iste': Decimal('444.0'),
	#         u'quas': 3563,
	#         u'quia': u'Et repudiandae ea.',
	#         u'repellendus': u'Sint vel cum quo ex.',
	#         u'reprehenderit': u'http://www.schmidt-jepsen.com/post/',
	#         u'similique': u'Tempora sunt.',
	#         u'vel': Decimal('8606893809.4'),
	#         u'veniam': u'Dignissimos in.',
	#         u'vitae': u'Sit quia quo.'},
	#     {   u'est': {   6: Decimal('-5.5596477023'),
	#                     7: [   u'Illo sint soluta.',
	#                            datetime(1984, 3, 29, 20, 42, 55),
	#                            1940],
	#                     8: {   6: u'Officia suscipit.',
	#                            7: u'Sit doloremque et.',
	#                            8: [u'In nihil omnis.', 1849]}},
	#         u'fugiat': {   4: u'Quidem quas aut.',
	#                        5: [u'Consequatur atque.', Decimal('-57.244'), 8378],
	#                        6: {   4: 5808,
	#                               5: 2927,
	#                               6: [u'Iusto ipsa hic qui.', 5287]}},
	#         u'ipsam': {   7: u'Veritatis esse.',
	#                       8: [3613, 1184655999360.9, u'Neque cupiditate.'],
	#                       9: {   7: datetime(1977, 7, 12, 7, 26, 28),
	#                              8: 208,
	#                              9: [   u'Eligendi tempora.',
	#                                     u'Non perspiciatis.']}},
	#         u'nisi': {   1: Decimal('66822.2126'),
	#                      2: [   u'http://www.johansen.com/about/',
	#                             u'http://pedersen-kristensen.net/faq/',
	#                             u'antonovergaard@gmail.com'],
	#                      3: {   1: u'Voluptatem et.',
	#                             2: 2414,
	#                             3: [   u'Ab non qui ullam.',
	#                                    datetime(2002, 11, 17, 16, 7, 51)]}},
	#         u'omnis': {   3: u'Excepturi fugiat.',
	#                       4: [   Decimal('-780535168.6'),
	#                              8216,
	#                              u'http://nissen.com/'],
	#                       5: {   3: u'odelinejessen@pedersen.com',
	#                              4: u'Cum veritatis.',
	#                              5: [   u'http://www.henriksen.com/explore/category/blog/home/',
	#                                     datetime(1982, 7, 5, 10, 33, 28)]}},
	#         u'quia': {   2: 8302638351.0,
	#                      3: [   datetime(2002, 5, 30, 6, 51, 29),
	#                             datetime(1977, 7, 10, 22, 58, 2),
	#                             u'Velit qui iusto.'],
	#                      4: {   2: 6895,
	#                             3: Decimal('-47775.364'),
	#                             4: [u'hansenrita@lund-lauritsen.info', 1254]}},
	#         u'reiciendis': {   8: 9838,
	#                            9: [   u'Qui ipsum magnam.',
	#                                   Decimal('2211432000.23'),
	#                                   Decimal('71996934027.6')],
	#                            10: {   8: 218171288.958,
	#                                    9: 1674,
	#                                    10: [   u'Est dolor.',
	#                                            u'Sunt eum voluptatem.']}},
	#         u'sint': {   5: 6672,
	#                      6: [   Decimal('-99956293.8531'),
	#                             Decimal('-60.708'),
	#                             1623],
	#                      7: {   5: Decimal('-1.8482834257E+11'),
	#                             6: Decimal('-8.56618825958E+12'),
	#                             7: [u'Libero amet et est.', 132]}},
	#         u'tenetur': {   9: datetime(1984, 10, 20, 4, 10, 26),
	#                         10: [   u'http://mikkelsen.biz/categories/category/about.htm',
	#                                 Decimal('2.12567703195E+14'),
	#                                 8713],
	#                         11: {   9: Decimal('-6270.56483521'),
	#                                 10: datetime(1978, 4, 8, 8, 55, 22),
	#                                 11: [u'Maxime quis.', u'Et laudantium.']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('809.428688162')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   datetime(1989, 3, 7, 13, 13, 18),
	#     7323,
	#     u'Cumque saepe et.',
	#     datetime(1999, 5, 29, 0, 29, 47),
	#     Decimal('-46071.5539704'),
	#     7998,
	#     9718,
	#     u'Autem aut et atque.',
	#     datetime(2001, 3, 26, 7, 56, 38),
	#     u'Error et hic.',
	#     datetime(1990, 4, 18, 1, 48, 9)]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Laudantium quo et.',
	#     u'Maiores aut et.',
	#     Decimal('9713466.87561'),
	#     Decimal('6.68657498298E+14'),
	#     datetime(1973, 11, 23, 0, 38, 8),
	#     u'Ratione labore.',
	#     Decimal('-113780360.21'))

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([9409, u'Sequi quod quis.', Decimal('-8931.3839'), u'Exercitationem.', 9169, 7315, u'Qui magnam debitis.', Decimal('3.66288748926E+13'), datetime(1971, 11, 30, 0, 47, 57)])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'consequatur': u'Odio consectetur.',
	#     u'exercitationem': u'Sed non voluptas ut.',
	#     u'incidunt': u'Corporis in soluta.',
	#     u'maxime': u'http://www.kristoffersen-olesen.com/homepage.asp',
	#     u'molestiae': Decimal('138854.2349'),
	#     u'omnis': -17321.61596,
	#     u'quis': u'Et optio vero ipsum.',
	#     u'recusandae': u'Hic non earum culpa.',
	#     u'sunt': Decimal('-2.98658438112E+14'),
	#     u'voluptates': u'Deleniti.'}

	fake.pyint()
	# 5967

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'508-46-7977'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_2; rv:1.9.4.20) Gecko/2012-09-26 07:12:09 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.92.(X11; Linux i686; sl-SI) Presto/2.9.169 Version/10.00'

	fake.windows_platform_token()
	# u'Windows 98; Win 9x 4.90'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 4.0; Trident/4.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.01; Trident/3.0)'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5350 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/5350'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_6_8'

	fake.safari()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_8 rv:4.0; it-IT) AppleWebKit/533.43.1 (KHTML, like Gecko) Version/5.1 Safari/533.43.1'
