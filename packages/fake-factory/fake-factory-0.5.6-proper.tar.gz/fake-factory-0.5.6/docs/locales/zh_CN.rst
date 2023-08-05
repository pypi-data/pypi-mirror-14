
Language zh_CN
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('-88.4376535')

	fake.street_name()
	# u'\u72d0\u8def'

	fake.address()
	# u'\u51e4\u82f1\u5e02\u88d8\u8deft\u5ea7 889570'

	fake.street_address()
	# u'\u540e\u8857U\u5ea7'

	fake.postcode()
	# u'809270'

	fake.longitude()
	# Decimal('-82.649545')

	fake.country()
	# u'\u9a6c\u8033\u4ed6'

	fake.city_name()
	# u'\u4e0a\u6d77'

	fake.street_suffix()
	# u'\u8def'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('35.914021')

	fake.city_suffix()
	# u'\u5e02'

	fake.building_number()
	# u'Y\u5ea7'

	fake.country_code()
	# u'KM'

	fake.city()
	# u'\u6960\u5e02'

	fake.state()
	# u'\u82b1\u6eaa\u533a'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'7998825423759'

	fake.ean13()
	# u'5154146303411'

	fake.ean8()
	# u'50272815'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(136,214,48)'

	fake.color_name()
	# u'LightSteelBlue'

	fake.rgb_color_list()
	# (126, 73, 249)

	fake.rgb_color()
	# u'106,132,185'

	fake.safe_hex_color()
	# u'#eecc00'

	fake.safe_color_name()
	# u'black'

	fake.hex_color()
	# u'#e07924'

``faker.providers.company``
---------------------------

::

	fake.company_suffix()
	# u'\u7f51\u7edc\u6709\u9650\u516c\u53f8'

	fake.company()
	# u'\u5929\u5f00\u79d1\u6280\u6709\u9650\u516c\u53f8'

	fake.company_prefix()
	# u'\u946b\u535a\u817e\u98de'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'131'

	fake.credit_card_provider(card_type=None)
	# u'American Express'

	fake.credit_card_full(card_type=None)
	# u'VISA 16 digit\n\u5175 \u52b3\n4288823179719828 01/17\nCVC: 874\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '06/24'

	fake.credit_card_number(card_type=None)
	# u'210066510396507'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'IQD'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '12'

	fake.month()
	# '12'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 5, 22, 54)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 38)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2004, 7, 6, 22, 30, 32)

	fake.time(pattern="%H:%M:%S")
	# '13:31:55'

	fake.year()
	# '2013'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1676, 11, 30, 5, 49, 3)

	fake.day_of_week()
	# 'Sunday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 11, 7, 45)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2011, 12, 15, 22, 25, 3)

	fake.unix_time()
	# 1256364794

	fake.month_name()
	# 'May'

	fake.timezone()
	# u'Asia/Baghdad'

	fake.time_delta()
	# datetime.timedelta(1805, 41312)

	fake.century()
	# u'IX'

	fake.date(pattern="%Y-%m-%d")
	# '1993-06-30'

	fake.iso8601(tzinfo=None)
	# '2007-03-19T01:11:44'

	fake.date_time(tzinfo=None)
	# datetime(1986, 12, 4, 18, 58, 28)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 3, 25, 23, 50, 3)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'video/mp4'

	fake.file_name(category=None, extension=None)
	# u'provident.css'

	fake.file_extension(category=None)
	# u'html'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'241.114.199.53'

	fake.url()
	# u'http://www.\u9e3f\u777f\u601d\u535a\u7f51\u7edc\u6709\u9650\u516c\u53f8.com/'

	fake.company_email()
	# u'e\u5389@\u5170\u91d1\u7535\u5b50\u7f51\u7edc\u6709\u9650\u516c\u53f8.com'

	fake.uri()
	# u'http://www.\u51cc\u4e91\u4f20\u5a92\u6709\u9650\u516c\u53f8.com/category/category.php'

	fake.domain_word(*args, **kwargs)
	# u'\u56db\u901a\u7f51\u7edc\u6709\u9650\u516c\u53f8'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/464x854'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'\u688500@yahoo.com'

	fake.slug(*args, **kwargs)
	# u'accusantium-qui'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'\u601d\u4f18\u4fe1\u606f\u6709\u9650\u516c\u53f8.info'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'e06a:b50c:452d:4720:569e:83a1:fdd0:64b0'

	fake.safe_email()
	# u'r\u5b63@example.com'

	fake.user_name(*args, **kwargs)
	# u'\u9633\u5229'

	fake.uri_path(deep=None)
	# u'categories'

	fake.email()
	# u'\u79c0\u6885\u6a0a@\u4e2d\u5efa\u521b\u4e1a\u4f20\u5a92\u6709\u9650\u516c\u53f8.biz'

	fake.uri_page()
	# u'faq'

	fake.mac_address()
	# u'ec:08:dc:f6:f3:b2'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Media buyer'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Dolores ducimus aliquid qui. Nihil nesciunt cum cumque error sed et autem. Dolores molestiae magni dicta.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Voluptas maiores ea laboriosam.'

	fake.word()
	# u'possimus'

	fake.paragraphs(nb=3)
	# [   u'Ipsum ut esse quidem molestiae ut eum. Ipsum voluptas ad libero autem et adipisci cumque. Voluptas consectetur omnis illum rerum rem a in.',
	#     u'Officia rerum veniam quos. Aut dolor voluptatem enim sit magni quas. Ut vitae blanditiis illum ipsum. Sunt consequuntur facere exercitationem perferendis qui sed inventore.',
	#     u'Ratione dolorem qui quaerat quisquam repellendus cum doloribus. Provident et voluptatem ea. Voluptate nihil voluptatem quia dolorem. Qui dolorem alias necessitatibus exercitationem impedit.']

	fake.words(nb=3)
	# [u'eius', u'numquam', u'commodi']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Consequuntur consequatur quos ex et non ut dolores. Similique sit quo et nostrum est rerum architecto. Quod laboriosam non eum distinctio.'

	fake.sentences(nb=3)
	# [   u'Quia necessitatibus officia neque nostrum.',
	#     u'Hic explicabo impedit corrupti odit amet reiciendis dolore.',
	#     u'Natus et est officiis voluptatum.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'_76XmRcc6_'

	fake.locale()
	# u'pt_IN'

	fake.md5(raw_output=False)
	# '70f47d71b833f053f61100c00a68ffcf'

	fake.sha1(raw_output=False)
	# '208103bde07ab40298391e3ef12a050c1c785436'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '1b995612d5438aa1e579595cad85100d32a14d791e27c6b067d717278ed3257c'

	fake.uuid4()
	# 'aebe1af3-48b5-45ac-807b-4365d36120fa'

	fake.language_code()
	# u'fr'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u79bb'

	fake.name_female()
	# u'\u8fde\u82b3'

	fake.prefix_male()
	# ''

	fake.prefix()
	# ''

	fake.name()
	# u'\u9c7c\u6dd1\u73cd'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'\u5434\u7434'

	fake.first_name()
	# u'\u79c0\u73cd'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'\u71d5'

	fake.first_name_female()
	# u'\u4fca'

	fake.last_name_female()
	# u'\u9c7c'

	fake.last_name()
	# u'\u72c4'

	fake.prefix_female()
	# ''

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'15999229599'

	fake.phonenumber_prefix()
	# 189

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'\u79c0\u82b3\u5e02\u536b\u8857m\u5ea7 305977',
	#     'birthdate': '1992-07-09',
	#     'mail': u'c\u4e8e@yahoo.com',
	#     'name': u'\u76d6\u5efa',
	#     'sex': 'M',
	#     'username': u's\u4e25'}

	fake.profile(fields=None)
	# {   'address': u'\u83b9\u5e02\u8fdf\u8857w\u5ea7 703383',
	#     'birthdate': '1982-04-16',
	#     'blood_group': 'A-',
	#     'company': u'\u51cc\u4e91\u4f20\u5a92\u6709\u9650\u516c\u53f8',
	#     'current_location': (Decimal('-34.1127035'), Decimal('113.465124')),
	#     'job': 'International aid/development worker',
	#     'mail': u'\u5065\u5b59@yahoo.com',
	#     'name': u'\u90ed\u4e91',
	#     'residence': u'\u51e4\u82f1\u5e02\u5353\u8defb\u5ea7 947054',
	#     'sex': 'F',
	#     'ssn': u'420101196605170481',
	#     'username': u'\u5175\u82d7',
	#     'website': [   u'http://www.\u60e0\u6d3e\u56fd\u9645\u516c\u53f8\u4f20\u5a92\u6709\u9650\u516c\u53f8.org/',
	#                    u'http://\u5f69\u8679\u4f20\u5a92\u6709\u9650\u516c\u53f8.org/',
	#                    u'http://www.\u4e07\u8fc5\u7535\u8111\u4f20\u5a92\u6709\u9650\u516c\u53f8.com/',
	#                    u'http://\u5bcc\u7f73\u4f20\u5a92\u6709\u9650\u516c\u53f8.biz/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   5920,
	#     -676233842518044.0,
	#     u'Suscipit totam qui.',
	#     datetime(1970, 2, 1, 8, 27, 23),
	#     u'Culpa asperiores.',
	#     datetime(1980, 11, 2, 1, 45, 7),
	#     u'Commodi sunt totam.',
	#     u'Nobis vel laborum.',
	#     u'Dignissimos debitis.',
	#     u'Quia voluptas dolor.',
	#     5375)

	fake.pystr(max_chars=20)
	# u'Asperiores quasi.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 637030364305122.0

	fake.pystruct(count=10, *value_types)
	# (   [   u'j\u53cc@\u83ca\u98ce\u516c\u53f8\u7f51\u7edc\u6709\u9650\u516c\u53f8.com',
	#         u'Est quo temporibus.',
	#         1313,
	#         1722,
	#         Decimal('0.21644023005'),
	#         -1344.3,
	#         u'http://www.\u601d\u4f18\u4fe1\u606f\u6709\u9650\u516c\u53f8.biz/post.php',
	#         u'\u96ea\u6885\u8f66@\u51cc\u9896\u4fe1\u606f\u79d1\u6280\u6709\u9650\u516c\u53f8.info',
	#         u'Suscipit sequi quo.',
	#         u'\u6167\u67ef@hotmail.com'],
	#     {   u'est': u'Ratione iusto sed.',
	#         u'eveniet': u'Dolore ut.',
	#         u'id': datetime(1992, 12, 18, 16, 42, 49),
	#         u'nemo': -38850076867619.8,
	#         u'neque': 291902.7376,
	#         u'nisi': 75461339731215.5,
	#         u'quam': u'Dolores tempore.',
	#         u'reprehenderit': 2321,
	#         u'tempora': datetime(1982, 6, 29, 21, 1, 14)},
	#     {   u'alias': {   8: 8992,
	#                       9: [   u'Magnam aut.',
	#                              u'http://\u540c\u5174\u4e07\u70b9\u7f51\u7edc\u6709\u9650\u516c\u53f8.biz/tags/main.php',
	#                              u'z\u6fee@gmail.com'],
	#                       10: {   8: Decimal('-86682081.8446'),
	#                               9: u'\u6842\u9999\u5c48@hotmail.com',
	#                               10: [   datetime(1980, 6, 17, 15, 39, 17),
	#                                       u'Autem voluptatem.']}},
	#         u'dolor': {   6: u'Soluta qui in odit.',
	#                       7: [datetime(2011, 11, 26, 7, 13, 9), 9682967.1, 4145],
	#                       8: {   6: u'http://www.\u901a\u9645\u540d\u8054\u4fe1\u606f\u6709\u9650\u516c\u53f8.biz/login/',
	#                              7: u'z\u95e8@\u4e5d\u65b9\u4f20\u5a92\u6709\u9650\u516c\u53f8.com',
	#                              8: [   u'Dolores qui.',
	#                                     datetime(2015, 1, 27, 16, 55, 52)]}},
	#         u'et': {   0: u'Porro et ea sit est.',
	#                    1: [   u'Libero ea et autem.',
	#                           u'Sed iusto iusto.',
	#                           u'Animi eaque hic.'],
	#                    2: {   0: u'http://\u8944\u6a0a\u5730\u7403\u6751\u4f20\u5a92\u6709\u9650\u516c\u53f8.com/',
	#                           1: -4.403974,
	#                           2: [685, u'Natus praesentium.']}},
	#         u'laudantium': {   1: u'Id odit ut.',
	#                            2: [   u'Tenetur ut libero.',
	#                                   Decimal('2761.4081616'),
	#                                   u'http://\u4fe1\u8bda\u81f4\u8fdc\u4fe1\u606f\u6709\u9650\u516c\u53f8.com/author/'],
	#                            3: {   1: datetime(1986, 9, 16, 10, 2),
	#                                   2: datetime(1995, 9, 19, 13, 45, 30),
	#                                   3: [   u'\u679746@\u6613\u52a8\u529b\u79d1\u6280\u6709\u9650\u516c\u53f8.com',
	#                                          u'http://www.\u56fe\u9f99\u4fe1\u606f\u4f20\u5a92\u6709\u9650\u516c\u53f8.com/home/']}},
	#         u'maiores': {   5: u'http://\u83ca\u98ce\u516c\u53f8\u4f20\u5a92\u6709\u9650\u516c\u53f8.com/',
	#                         6: [   Decimal('64761884961.0'),
	#                                u'Minima maiores ut.',
	#                                9994],
	#                         7: {   5: u'Quibusdam est.',
	#                                6: 5571,
	#                                7: [   -2087053638.0,
	#                                       u'http://www.\u6d77\u521b\u4fe1\u606f\u6709\u9650\u516c\u53f8.biz/category/']}},
	#         u'minima': {   4: u'Ullam et iure.',
	#                        5: [   u'Harum at quisquam.',
	#                               6687,
	#                               Decimal('-849228.86258')],
	#                        6: {   4: u'Nostrum.',
	#                               5: u'Quia perferendis.',
	#                               6: [   u'http://\u56db\u901a\u7f51\u7edc\u6709\u9650\u516c\u53f8.com/faq.htm',
	#                                      3801]}},
	#         u'nam': {   3: u'Omnis est.',
	#                     4: [   u'Eum consequuntur et.',
	#                            u'Rerum cumque non.',
	#                            datetime(1993, 1, 18, 18, 47)],
	#                     5: {   3: 3894,
	#                            4: datetime(1985, 10, 16, 15, 9, 57),
	#                            5: [3559, Decimal('-2538441632.82')]}},
	#         u'temporibus': {   7: u'\u963304@yahoo.com',
	#                            8: [   5710,
	#                                   u'\u7389\u5170\u6ee1@yahoo.com',
	#                                   Decimal('0.27456')],
	#                            9: {   7: 8097,
	#                                   8: u'Qui quibusdam qui.',
	#                                   9: [   u'http://\u660a\u5609\u4f20\u5a92\u6709\u9650\u516c\u53f8.net/search/search/category/',
	#                                          u'Voluptatem.']}},
	#         u'velit': {   9: 5796,
	#                       10: [   633051944659446.0,
	#                               u'Consequatur.',
	#                               u'w\u683e@\u4e03\u559c\u79d1\u6280\u6709\u9650\u516c\u53f8.org'],
	#                       11: {   9: 2925,
	#                               10: Decimal('-4.64754831757E+12'),
	#                               11: [   u'Libero non odit non.',
	#                                       u'http://\u826f\u8bfa\u79d1\u6280\u6709\u9650\u516c\u53f8.com/']}},
	#         u'voluptate': {   2: 632004406263340.0,
	#                           3: [   408,
	#                                  u'Placeat vitae hic.',
	#                                  datetime(1977, 2, 19, 3, 51, 24)],
	#                           4: {   2: u'http://\u6d59\u5927\u4e07\u670b\u4fe1\u606f\u6709\u9650\u516c\u53f8.net/',
	#                                  3: u'Aut non porro.',
	#                                  4: [u'\u838918@hotmail.com', 4902]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('28256.8102624')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   -998408324388.293,
	#     datetime(1984, 4, 7, 3, 9, 27),
	#     390391706274728.0,
	#     u'q\u4e50@hotmail.com',
	#     u'Ut molestiae ab.',
	#     u'\u7434\u7434@\u601d\u4f18\u79d1\u6280\u6709\u9650\u516c\u53f8.com',
	#     u'Officiis.',
	#     u'Aut fuga voluptas.',
	#     Decimal('-4.0'),
	#     u'Molestiae omnis.',
	#     datetime(1996, 3, 18, 22, 31, 43),
	#     u'\u946b\u5305@\u5feb\u8baf\u4fe1\u606f\u6709\u9650\u516c\u53f8.com']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Officiis sit.',
	#     7912,
	#     u'http://www.\u56fe\u9f99\u4fe1\u606f\u4f20\u5a92\u6709\u9650\u516c\u53f8.info/main.jsp',
	#     Decimal('-223081167.931'),
	#     145.0,
	#     1202,
	#     u'Provident.',
	#     datetime(2014, 1, 30, 17, 2, 32),
	#     3226,
	#     datetime(1970, 7, 30, 16, 19, 26),
	#     u'Illo temporibus.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('72329.9438'), u'http://\u53cc\u654f\u7535\u5b50\u7f51\u7edc\u6709\u9650\u516c\u53f8.net/list/login.htm', u'Nihil sunt.', u'Debitis et quaerat.', u'Aliquid sed vitae.', 1068, Decimal('14.0'), 20644766.26599, u'Et nulla quia eos.', 921, 3193, Decimal('-5.49642592359E+12'), 5531, u'http://\u6656\u6765\u8ba1\u7b97\u673a\u4fe1\u606f\u6709\u9650\u516c\u53f8.com/category/tags/login/'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'adipisci': u'\u5b98\u745c@yahoo.com',
	#     u'architecto': 242,
	#     u'ducimus': u'Unde voluptas.',
	#     u'exercitationem': u'w\u590f@\u6cf0\u9e92\u9e9f\u4f20\u5a92\u6709\u9650\u516c\u53f8.com',
	#     u'illum': u'Doloribus placeat.',
	#     u'nam': u'Voluptas natus.',
	#     u'qui': datetime(1973, 9, 7, 0, 58, 58)}

	fake.pyint()
	# 9931

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'61032619931101320X'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2015-06-22 13:31:57 Firefox/14.0'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/8.39.(X11; Linux i686; en-US) Presto/2.9.186 Version/12.00'

	fake.windows_platform_token()
	# u'Windows NT 5.1'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Win 9x 4.90; Trident/4.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (Windows NT 5.01; en-US; rv:1.9.2.20) Gecko/2015-08-09 12:54:02 Firefox/3.8'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_1) AppleWebKit/5311 (KHTML, like Gecko) Chrome/14.0.856.0 Safari/5311'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_6_2'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/533.24.2 (KHTML, like Gecko) Version/4.0.3 Safari/533.24.2'
