
Language hi_IN
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('52.438914')

	fake.street_name()
	# u'\u091c\u092e\u093e\u0928\u0924'

	fake.address()
	# u'34 \u0930\u0936\u094d\u092e\u0940 \u092e\u0902\u0917\u0924\n\u0905\u0928\u0902\u0924\u0928\u093e\u0917 535514'

	fake.street_address()
	# u'9189 \u0935\u093f\u0915\u093e\u0935\u093f'

	fake.postcode()
	# u'676989'

	fake.longitude()
	# Decimal('7.106314')

	fake.country()
	# u'\u091c\u092e\u0948\u0915\u093e'

	fake.city_name()
	# u'\u091f\u093f\u0938\u0942\u091c'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-21.177343')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'74'

	fake.country_code()
	# u'IS'

	fake.city()
	# u'\u0907\u0932\u093e\u0939\u093e\u092c\u093e\u0926'

	fake.state()
	# u'\u092a\u0902\u091c\u093e\u092c'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'6219534215451'

	fake.ean13()
	# u'5484746033761'

	fake.ean8()
	# u'38120060'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(70,140,238)'

	fake.color_name()
	# u'GreenYellow'

	fake.rgb_color_list()
	# (58, 42, 249)

	fake.rgb_color()
	# u'121,60,247'

	fake.safe_hex_color()
	# u'#eeee00'

	fake.safe_color_name()
	# u'gray'

	fake.hex_color()
	# u'#587f1b'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\u0932\u094b\u0926\u0940-\u0906\u091a\u093e\u0930\u094d\u092f'

	fake.company_suffix()
	# u'Ltd'

	fake.catch_phrase()
	# u'User-friendly high-level open architecture'

	fake.bs()
	# u'orchestrate customized e-services'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'639'

	fake.credit_card_provider(card_type=None)
	# u'JCB 16 digit'

	fake.credit_card_full(card_type=None)
	# u'JCB 16 digit\n\u0910\u0936\u094d\u0935\u0930\u094d\u092f\u093e \u0922\u0940\u0902\u0917\u0930\u093e\n3088641029323870 11/24\nCVC: 730\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '10/25'

	fake.credit_card_number(card_type=None)
	# u'503809368072'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'TOP'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '13'

	fake.month()
	# '11'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 11, 53, 40)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1999, 11, 12, 6, 21, 46)

	fake.time(pattern="%H:%M:%S")
	# '22:49:20'

	fake.year()
	# '1982'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(560, 5, 11, 22, 29, 42)

	fake.day_of_week()
	# 'Friday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 5, 3, 40, 8)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 8, 12, 6, 57, 13)

	fake.unix_time()
	# 657322490

	fake.month_name()
	# 'October'

	fake.timezone()
	# u'Europe/Istanbul'

	fake.time_delta()
	# datetime.timedelta(14818, 14957)

	fake.century()
	# u'XV'

	fake.date(pattern="%Y-%m-%d")
	# '1993-09-24'

	fake.iso8601(tzinfo=None)
	# '1987-07-06T11:40:09'

	fake.date_time(tzinfo=None)
	# datetime(2014, 10, 10, 19, 41, 42)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 2, 2, 3, 36, 39)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'text/vcard'

	fake.file_name(category=None, extension=None)
	# u'totam.mp4'

	fake.file_extension(category=None)
	# u'jpg'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'179.39.109.68'

	fake.url()
	# u'http://www.\u0932\u0915\u0928\u091f\u092f.com/'

	fake.company_email()
	# u'\u0935\u0937\u0923\u091c\u0936@\u0935\u0915\u0935.com'

	fake.uri()
	# u'http://www.\u0932\u0915\u0928\u091f\u092f.com/search/main.php'

	fake.domain_word(*args, **kwargs)
	# u'\u0906\u0939\u091c-\u091b\u092c\u0930'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/382/33'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'\u0938\u0928\u0927\u0936\u092a\u0930\u0923\u0935@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'earum-nobis'

	fake.free_email_domain()
	# u'yahoo.com'

	fake.domain_name()
	# u'\u092e\u0923.com'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'0cd0:85ab:f2a2:9130:0d01:b09e:4edf:1940'

	fake.safe_email()
	# u'\u0906\u0936\u092e\u0921\u0932@example.org'

	fake.user_name(*args, **kwargs)
	# u'x\u0936\u0930\u0933'

	fake.uri_path(deep=None)
	# u'categories'

	fake.email()
	# u'\u091c\u0917\u0928\u0928\u0925\u0936\u0930\u0933@\u0917\u092a\u0924-\u0935\u0932.com'

	fake.uri_page()
	# u'privacy'

	fake.mac_address()
	# u'93:71:55:14:fe:ae'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Designer, interior/spatial'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Dicta quia ut mollitia quas tempore. Eos non perferendis temporibus quas vel. Laudantium quaerat quis at eveniet. Velit magni labore libero quod voluptatem omnis facilis.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Sit consequuntur aut sint quia fugiat.'

	fake.word()
	# u'ab'

	fake.paragraphs(nb=3)
	# [   u'Tenetur exercitationem quam incidunt ratione voluptatum et consequuntur. Aliquam inventore et aut. Aut possimus distinctio at ut.',
	#     u'Cum molestiae maiores repellendus enim est ea. Aut esse enim vel nesciunt. Autem qui vel incidunt qui sed alias animi. Reiciendis rem mollitia ea perferendis dolorem est. Et molestiae dolores incidunt illo provident.',
	#     u'Voluptatum iusto fugit vero voluptatem. Eligendi nihil fugiat odio et omnis iste. Ipsa recusandae numquam minima quam quo provident ab.']

	fake.words(nb=3)
	# [u'alias', u'pariatur', u'illo']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Corporis saepe similique cumque autem veritatis. Et dolor fugiat et labore sed. Ipsa sed voluptatem animi neque cumque. Et deserunt maxime quod rem cumque voluptatem laborum.'

	fake.sentences(nb=3)
	# [   u'Deleniti fuga et et a id magni aperiam.',
	#     u'Quia iure amet dicta eligendi illum autem atque.',
	#     u'Sequi ut culpa aperiam ratione non.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'&8Arv@u3VS'

	fake.locale()
	# u'en_EE'

	fake.md5(raw_output=False)
	# '9b739b1a05cf936359e8a72d395af498'

	fake.sha1(raw_output=False)
	# 'a4c9177ccd4f4f63b40e74269c82e546d489361e'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# 'a31af73bfcb0ba4f769c157d64c2276bf904d2d005a73307a878fc88e70653d6'

	fake.uuid4()
	# 'f27d5ddd-cdba-47e0-b8af-2b862adfe714'

	fake.language_code()
	# u'ru'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u0930\u093e\u092e\u0936\u0930\u094d\u092e\u093e'

	fake.name_female()
	# u'\u090f\u0937\u093e \u0921\u093e\u0930'

	fake.prefix_male()
	# ''

	fake.prefix()
	# ''

	fake.name()
	# u'\u0926\u0924\u094d\u0924\u093e, \u0917\u0923\u0947\u0936'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'\u092e\u0902\u0917\u0932, \u0935\u093f\u091c\u092f\u093e'

	fake.first_name()
	# u'\u0936\u094d\u092f\u093e\u092e\u093e'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'\u0915\u0948\u0932\u093e\u0936'

	fake.first_name_female()
	# u'\u0908\u0936'

	fake.last_name_female()
	# u'\u0926\u0941\u0906'

	fake.last_name()
	# u'\u0938\u0947\u0928\u093e\u0927\u0940\u0936'

	fake.prefix_female()
	# ''

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'05169 118948'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'390 \u092e\u0939\u093e\u0930\u093e\u091c\n\u0926\u0947\u0935\u0917\u095d 715155',
	#     'birthdate': '1975-01-17',
	#     'mail': u'\u0930\u092f\u092d\u0930\u0924@gmail.com',
	#     'name': u'\u0936\u0915\u094d\u0924\u093f \u0921\u093e\u0930',
	#     'sex': 'M',
	#     'username': u'\u0905\u0915\u093073'}

	fake.profile(fields=None)
	# {   'address': u'79 \u0926\u0941\u0906\n\u091a\u093f\u0930\u093e\u0932\u093e-103902',
	#     'birthdate': '2003-08-21',
	#     'blood_group': 'AB-',
	#     'company': u'\u0915\u0941\u092e\u093e\u0930 Inc',
	#     'current_location': (Decimal('6.9653915'), Decimal('-50.682794')),
	#     'job': 'Telecommunications researcher',
	#     'mail': u'n\u0905\u0917\u0930\u0935\u0932@gmail.com',
	#     'name': u'\u0935\u093f\u0926\u094d\u092f\u093e \u092a\u0941\u0937\u094d\u0915\u0930',
	#     'residence': u'20/964 \u091c\u092e\u093e\u0928\u0924\n\u091a\u093f\u0924\u094d\u0930\u0926\u0941\u0930\u094d\u0917-332982',
	#     'sex': 'F',
	#     'ssn': u'003-33-4069',
	#     'username': u'\u0932\u0932\u092452',
	#     'website': [u'http://\u092a\u0937\u0915\u0930.net/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Qui sint voluptatem.',
	#     8099,
	#     datetime(1978, 11, 8, 1, 38, 37),
	#     u'Tempora hic.',
	#     u'Ut accusamus.',
	#     u'z\u092e\u091c\u092e\u0926\u0930@yahoo.com',
	#     3893,
	#     u'Tenetur iure sunt.',
	#     3642)

	fake.pystr(max_chars=20)
	# u'Quaerat voluptate.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -852409937766599.0

	fake.pystruct(count=10, *value_types)
	# (   [   u'\u092e\u0917\u0924\u0932\u0932@\u092e\u0928.com',
	#         Decimal('5600015.364'),
	#         9638,
	#         1887,
	#         2884,
	#         u'http://\u0917\u0917\u0932.com/',
	#         u'Placeat quod.',
	#         u'Consectetur.',
	#         u'Aut tempore.',
	#         u'Praesentium vero.'],
	#     {   u'aperiam': u'Consequuntur quas.',
	#         u'consequuntur': 6752,
	#         u'fuga': u'Sequi repellat quia.',
	#         u'id': 5065,
	#         u'ipsa': Decimal('1.09840679219E+14'),
	#         u'nostrum': 6595,
	#         u'sint': Decimal('61723.8'),
	#         u'soluta': u'Qui est explicabo.',
	#         u'temporibus': u'Eum natus.',
	#         u'voluptatem': u'\u0938\u0930\u0938\u0935\u092424@yahoo.com'},
	#     {   u'aliquam': {   6: u'Pariatur non eum.',
	#                         7: [   Decimal('-5.67388735388E+12'),
	#                                datetime(1981, 12, 1, 15, 56, 18),
	#                                9906],
	#                         8: {   6: u'Nihil amet ut.',
	#                                7: 2531,
	#                                8: [2811, u'Et autem velit.']}},
	#         u'est': {   2: 8356,
	#                     3: [-928.976, -76819332308.8923, u'Aliquid nihil.'],
	#                     4: {   2: u'A repudiandae.',
	#                            3: Decimal('4560446.5581'),
	#                            4: [   u'\u092e\u0932\u0924\u092c\u0932\u0938\u092c\u0930\u092e\u0923\u092f\u092e@\u091a\u0939\u0928-\u0905\u0917\u0930\u0935\u0932.com',
	#                                   u'Quas dolores aut.']}},
	#         u'et': {   5: 3432,
	#                    6: [   u'Voluptatum quo.',
	#                           25.97524956,
	#                           u'Doloribus nobis sit.'],
	#                    7: {   5: u'http://\u0915\u0932\u0915\u0930\u0923-\u0938\u0928\u0927\u0936.com/explore/main/',
	#                           6: u'Officia velit totam.',
	#                           7: [   u'http://\u0926\u0935.com/explore/explore/search.html',
	#                                  u'Cum error officiis.']}},
	#         u'non': {   4: datetime(2004, 5, 12, 11, 31, 21),
	#                     5: [   1139,
	#                            -33367485212166.0,
	#                            u'http://www.\u0915\u092e\u0930-\u092a\u091f\u0932.com/index.html'],
	#                     6: {   4: Decimal('7096.79949'),
	#                            5: u'Porro velit beatae.',
	#                            6: [   u'Aliquid quam veniam.',
	#                                   u'Sunt ratione amet.']}},
	#         u'quasi': {   7: Decimal('69963.55709'),
	#                       8: [   Decimal('-56.1736334882'),
	#                              datetime(2009, 4, 10, 17, 52, 6),
	#                              u'Nisi illum minima.'],
	#                       9: {   7: u'http://www.\u091c\u0936-\u0917\u092f\u0915\u0935\u0921.com/main/post.html',
	#                              8: u'Molestiae possimus.',
	#                              9: [   u'http://www.\u092d\u0930\u0924-\u0936\u0930\u0933.org/',
	#                                     -1725032.0]}},
	#         u'repellat': {   9: 8208,
	#                          10: [   u'\u091c\u0924\u0928\u0926\u0930\u0917\u092f\u0915\u0935\u0921@gmail.com',
	#                                  u'Dolorum vero ea.',
	#                                  u'Facilis.'],
	#                          11: {   9: 6748, 10: 8085, 11: [u'Aspernatur.', 5247]}},
	#         u'repellendus': {   0: Decimal('-9031.63'),
	#                             1: [-9948.543, 7813, u'Autem impedit quia.'],
	#                             2: {   0: Decimal('9570006576.4'),
	#                                    1: u'\u0928\u0930\u092f\u092347@hotmail.com',
	#                                    2: [u'Culpa illo expedita.', 7459]}},
	#         u'rerum': {   1: 3169192344886.72,
	#                       2: [   Decimal('-92429393.2148'),
	#                              datetime(1986, 12, 10, 6, 9, 14),
	#                              u'\u0935\u091c\u092f53@gmail.com'],
	#                       3: {   1: 7582,
	#                              2: u'Quo perspiciatis.',
	#                              3: [u'Voluptates fuga.', 7628]}},
	#         u'voluptas': {   3: u'Officiis aut earum.',
	#                          4: [   Decimal('-7.95402564784E+14'),
	#                                 Decimal('82373964176.0'),
	#                                 u'Vel porro deleniti.'],
	#                          5: {   3: Decimal('1596539.3278'),
	#                                 4: Decimal('1.27738281035E+12'),
	#                                 5: [   datetime(1977, 6, 8, 8, 51, 38),
	#                                        u'http://\u0915\u0937\u0923\u0928.com/homepage.htm']}},
	#         u'voluptatem': {   8: 5736,
	#                            9: [   datetime(1973, 12, 30, 16, 21, 43),
	#                                   u'http://\u0932\u0915\u0928\u091f\u092f.com/',
	#                                   3784],
	#                            10: {   8: u'Consequatur laborum.',
	#                                    9: u'\u0910\u0936\u0935\u0930\u092f\u0915\u0932@gmail.com',
	#                                    10: [   Decimal('9.12712724281'),
	#                                            u'http://www.\u0927\u0932\u0935\u0932.biz/']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-34455686.2087')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   -553782292251.9,
	#     u'Adipisci eos a quas.',
	#     u'Illo eos molestiae.',
	#     u'Vitae aut ex est.',
	#     u'\u0915\u0932\u093666@\u091c\u0936.com',
	#     4865,
	#     u'Qui et labore enim.',
	#     Decimal('-1271.0'),
	#     u'Perspiciatis.',
	#     datetime(1988, 10, 10, 20, 38, 3),
	#     u'http://www.\u0926\u0926-\u092c\u092c.com/list/author.htm',
	#     u'\u0915\u0930\u092335@\u092c\u0926\u092e.com',
	#     4003,
	#     u'Repellendus cumque.',
	#     u'http://www.\u0917\u092a\u0924-\u0922\u0917\u0930.com/login/']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'\u0905\u0915\u092454@gmail.com',
	#     58.31,
	#     u'Quam ut maiores vel.',
	#     u'Sequi non.',
	#     u'\u0930\u091a\u0928\u0917\u0923\u0936@\u0926\u092f\u0932-\u0917\u0923\u0936.com',
	#     u'http://\u0926\u0926.com/category.htm',
	#     Decimal('-8.37513065098E+14'),
	#     u'Harum cum excepturi.',
	#     u'p\u092c\u0928@\u091c\u0936-\u092e\u0939\u0935\u0930.com',
	#     -746.7013,
	#     9237,
	#     u'Voluptatem beatae.',
	#     u's\u0926\u0906@gmail.com',
	#     u'Sit ut laudantium.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'Dolores explicabo.', u'y\u091a\u0927\u0930@\u091a\u0927\u0930.com', 21808041.5829, -32.6399, u'In pariatur.', datetime(1986, 6, 21, 8, 25, 43), u'\u092a\u091f\u0932\u0908\u0936@hotmail.com', 1747, datetime(1986, 10, 21, 3, 50, 9), u'http://\u0930\u092e\u0936\u0930\u092e-\u0935\u0932.com/', u'\u0926\u0935\u0928\u0916\u0932@\u092e\u0923.com'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'alias': u'Officia ut.',
	#     u'aut': u'Error nihil.',
	#     u'cum': 4423,
	#     u'deleniti': 2466,
	#     u'dicta': u'Quaerat ut.',
	#     u'et': u'Est alias nihil.',
	#     u'laudantium': u'Enim vitae ea.',
	#     u'qui': -337760.39,
	#     u'quia': u'Dignissimos.',
	#     u'sit': u'Velit rerum eum qui.',
	#     u'vero': u'http://\u092e\u091c\u092e\u0926\u0930.com/'}

	fake.pyint()
	# 9748

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'507-59-4768'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (X11; Linux i686; rv:1.9.6.20) Gecko/2014-11-17 16:50:12 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/8.22.(X11; Linux i686; en-US) Presto/2.9.165 Version/11.00'

	fake.windows_platform_token()
	# u'Windows 98'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/3.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5351 (KHTML, like Gecko) Chrome/13.0.823.0 Safari/5351'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_8) AppleWebKit/5362 (KHTML, like Gecko) Chrome/13.0.889.0 Safari/5362'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; PPC Mac OS X 10_7_8'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows 98; Win 9x 4.90) AppleWebKit/532.9.7 (KHTML, like Gecko) Version/5.0 Safari/532.9.7'
