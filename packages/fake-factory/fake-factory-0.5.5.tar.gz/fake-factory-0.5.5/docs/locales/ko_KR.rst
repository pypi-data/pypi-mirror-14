
Language ko_KR
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('-88.160928')

	fake.street_name()
	# u'\uc6a9\ud601\uc0b0\ub9c8\uc744'

	fake.address()
	# u'\ub300\uc804\uad11\uc5ed\uc2dc \uc5ec\uc6b1\uae30\uad70 \n \ud654\uc548\uac70\ub9ac 6 183\ub3d9 597\ud638 531-895'

	fake.street_address()
	# u'\ud615\uadfc\uc7ac\uac70\ub9ac 8975'

	fake.postcode()
	# u'110-816'

	fake.longitude()
	# Decimal('-131.414563')

	fake.country()
	# u'\ud30c\ud478\uc544 \ub274\uae30\ub2c8'

	fake.secondary_address()
	# u'077'

	fake.street_suffix()
	# u'\uac70\ub9ac'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-97.852746')

	fake.city_suffix()
	# u'\uc2dc'

	fake.building_number()
	# u'099'

	fake.country_code()
	# u'EG'

	fake.city()
	# u'\uac74\uc11d\uc2dc'

	fake.state()
	# u'\ubd80\uc0b0\uad11\uc5ed\uc2dc'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'0134431433318'

	fake.ean13()
	# u'6070094082873'

	fake.ean8()
	# u'12715527'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(55,40,100)'

	fake.color_name()
	# u'SaddleBrown'

	fake.rgb_color_list()
	# (74, 221, 254)

	fake.rgb_color()
	# u'115,215,147'

	fake.safe_hex_color()
	# u'#224400'

	fake.safe_color_name()
	# u'silver'

	fake.hex_color()
	# u'#c1f384'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\uc720\ud55c\ud68c\uc0ac \ubb34\ub300\uc775'

	fake.company_suffix()
	# u'\uc8fc\uc2dd\ud68c\uc0ac'

	fake.catch_phrase()
	# u'\uc124\uc815 \uac00\ub2a5\ud55c \ubc29\ud5a5 \ud658\uacbd'

	fake.bs()
	# u'\uc2e0\uc18d\ud55c \uc804\uc790 \ube44\uc988\ub2c8\uc2a4 \uc804\uc790 \uc11c\ube44\uc2a4'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'064'

	fake.credit_card_provider(card_type=None)
	# u'American Express'

	fake.credit_card_full(card_type=None)
	# u'Diners Club / Carte Blanche\n\ub2e8 \uc5fd\n30516556604048 10/19\nCVC: 836\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '12/21'

	fake.credit_card_number(card_type=None)
	# u'180002902986973'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'IDR'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '14'

	fake.month()
	# '05'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 4, 1, 50, 42)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 38)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1995, 5, 19, 15, 51)

	fake.time(pattern="%H:%M:%S")
	# '23:26:26'

	fake.year()
	# '2000'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1898, 6, 1, 3, 42, 31)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 6, 29, 5)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 10, 20, 2, 50, 42)

	fake.unix_time()
	# 57687165

	fake.month_name()
	# 'September'

	fake.timezone()
	# u'Africa/Gaborone'

	fake.time_delta()
	# datetime.timedelta(2021, 44261)

	fake.century()
	# u'IV'

	fake.date(pattern="%Y-%m-%d")
	# '1999-04-13'

	fake.iso8601(tzinfo=None)
	# '2004-09-17T03:58:47'

	fake.date_time(tzinfo=None)
	# datetime(1996, 9, 26, 22, 8, 3)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 5, 26, 17, 1, 46)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'multipart/alternative'

	fake.file_name(category=None, extension=None)
	# u'ex.js'

	fake.file_extension(category=None)
	# u'jpeg'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'159.46.125.151'

	fake.url()
	# u'http://www.\uc720.kr/'

	fake.company_email()
	# u'\ubb1847@\ud6a8\ub3d9.org'

	fake.uri()
	# u'http://\uc720.kr/categories/tag/main/category/'

	fake.domain_word(*args, **kwargs)
	# u'\uc8fc\uc2dd\ud68c\uc0ac'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/716x273'

	fake.tld()
	# u'org'

	fake.free_email()
	# u'\ub2e810@gmail.com'

	fake.slug(*args, **kwargs)
	# u'cupiditate-labore'

	fake.free_email_domain()
	# u'dreamwiz.com'

	fake.domain_name()
	# u'\uc720.org'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'd5d9:58f1:62e6:dc42:1ce5:b0a2:e58f:3bfa'

	fake.safe_email()
	# u'x\ud558@example.net'

	fake.user_name(*args, **kwargs)
	# u'\uba85\ud798'

	fake.uri_path(deep=None)
	# u'tag/category/wp-content'

	fake.email()
	# u'\ud574\ud64d@\uc8fc.kr'

	fake.uri_page()
	# u'post'

	fake.mac_address()
	# u'c1:2f:f4:a7:94:39'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Secretary/administrator'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Quia labore illo alias quod ut illo. Ullam numquam cum culpa veniam non voluptas. Inventore eum et eius beatae neque in.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Cupiditate perferendis aut deserunt sed veritatis quibusdam.'

	fake.word()
	# u'eos'

	fake.paragraphs(nb=3)
	# [   u'Earum distinctio officia laboriosam a. Tempora recusandae a voluptas et porro autem quis. Quidem qui qui similique dolorem consequatur deleniti fugit quidem.',
	#     u'Reiciendis unde voluptatem et. Sequi molestias saepe a. Quas non aspernatur commodi vel laboriosam inventore voluptatibus. Assumenda nulla aut vel corrupti.',
	#     u'Ea molestias sed veniam laudantium et. Molestiae nam non quis et molestiae. Sit dolores velit quia natus. Id animi omnis nisi quia ipsam.']

	fake.words(nb=3)
	# [u'voluptatem', u'esse', u'natus']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Ex aut dignissimos ea laboriosam sapiente. Eos eum corporis et id officiis aut aut. Dolor quaerat et mollitia unde incidunt voluptas. Error ut commodi debitis molestias ad consequuntur.'

	fake.sentences(nb=3)
	# [   u'Sapiente optio officiis eum suscipit.',
	#     u'Non neque dignissimos modi excepturi autem facilis perferendis.',
	#     u'Cumque rerum ducimus ut veniam.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'0Q4Da(0x+*'

	fake.locale()
	# u'it_BI'

	fake.md5(raw_output=False)
	# 'b45b577bb6e1969f1e0544ff2a7c1731'

	fake.sha1(raw_output=False)
	# '1eb07fe4a2e855f874850f6281b0742206437d8b'

	fake.null_boolean()
	# False

	fake.sha256(raw_output=False)
	# 'ecfea8ed44b4a571d4e14035afab9e561e1c65940aa4851817486ae59371cf9b'

	fake.uuid4()
	# 'da1d0221-2099-4a20-a069-4ee36a30ac39'

	fake.language_code()
	# u'pt'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\ud6c8'

	fake.name_female()
	# u'\uc131\uc138'

	fake.prefix_male()
	# ''

	fake.prefix()
	# ''

	fake.name()
	# u'\uc999\uc775'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'\uc0ac\uacf5\uad6c\uc0c1'

	fake.first_name()
	# u'\uc694'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'\ubbfc'

	fake.first_name_female()
	# u'\ud669'

	fake.last_name_female()
	# u'\uc6d0'

	fake.last_name()
	# u'\ubbf8'

	fake.prefix_female()
	# ''

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'051-431-7413'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'\uc804\ub77c\ub0a8\ub3c4 \ub1cc\uc18c\ud6c8\uad70 \uc628\ubbf8\ub3d9 554 (788-799)',
	#     'birthdate': '1971-03-20',
	#     'mail': u'\uc5b5\ub9cc@hotmail.com',
	#     'name': u'\uc218\ud611\uad8c',
	#     'sex': 'F',
	#     'username': u'f\ud76c'}

	fake.profile(fields=None)
	# {   'address': u'\ucda9\uccad\ub0a8\ub3c4 \uae38\uc7ac\ud1b5\uad6c \n \uc8fc\ube48\uac70\ub9ac 7239 176-740',
	#     'birthdate': '1985-06-20',
	#     'blood_group': 'B+',
	#     'company': u'\uadfc\uae30\uad6c',
	#     'current_location': (Decimal('-60.9813035'), Decimal('-122.924476')),
	#     'job': 'Air broker',
	#     'mail': u'\uc9c0\uc6d0@naver.com',
	#     'name': u'\uc190\uc548\ud76c',
	#     'residence': u'\ucda9\uccad\ubd81\ub3c4 \ubc30\ub450\ud638\uad6c \n \uc7ac\ud654\ub3d9 4073 039-564',
	#     'sex': 'M',
	#     'ssn': u'270913-2780818',
	#     'username': u'\uc5c492',
	#     'website': [   u'http://\uc8fc.net/',
	#                    u'http://www.\uc9c0\ube44.com/',
	#                    u'http://\ubb34\ub300.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   3713,
	#     u'Culpa ut enim.',
	#     7499,
	#     u'Ut sint sit aut.',
	#     u'http://www.\ud6c8\uc608.kr/posts/tags/search.htm',
	#     u'\uc81592@gmail.com',
	#     datetime(1978, 7, 27, 19, 41, 13),
	#     u'\ubd80\ucca0@dreamwiz.com',
	#     Decimal('-3556217.653'),
	#     u'Magni incidunt.',
	#     -6642.37)

	fake.pystr(max_chars=20)
	# u'Et sunt ullam.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -442.57076

	fake.pystruct(count=10, *value_types)
	# (   [   4946,
	#         datetime(1999, 3, 26, 11, 23, 40),
	#         8472,
	#         u'Quia voluptatibus.',
	#         u'Perferendis quo nam.',
	#         u'Veritatis est ipsam.',
	#         u'http://\uc720.net/category/register/',
	#         u'Quas molestiae.',
	#         u'i\ub780@daum.net',
	#         1989],
	#     {   u'asperiores': u'http://\uc720.com/blog/posts/categories/post.php',
	#         u'aut': u'd\uc21c@\uc8fc.net',
	#         u'consequatur': 11.666600595,
	#         u'dolor': u'Rerum dolorum ipsam.',
	#         u'earum': 6330,
	#         u'et': u'http://\uc6b0\ubbf8.com/search.html',
	#         u'laudantium': 1633,
	#         u'numquam': u'Suscipit molestiae.',
	#         u'omnis': 3153},
	#     {   u'accusamus': {   3: 812100389.5,
	#                           4: [578, u'Distinctio.', u'Omnis voluptatum.'],
	#                           5: {   3: u'Possimus ipsam.',
	#                                  4: 7809,
	#                                  5: [   Decimal('987.466'),
	#                                         u'Amet amet quidem.']}},
	#         u'autem': {   7: u'Quia dolor fuga est.',
	#                       8: [   datetime(1971, 9, 30, 4, 0, 17),
	#                              datetime(1991, 8, 3, 3, 4, 48),
	#                              u'http://\uc6c5\uba85.net/app/category/index.jsp'],
	#                       9: {   7: -516585549799.0,
	#                              8: datetime(1994, 1, 7, 7, 19, 8),
	#                              9: [2109, u'Aut mollitia quos.']}},
	#         u'neque': {   4: datetime(1975, 9, 7, 22, 19, 9),
	#                       5: [   datetime(1998, 8, 23, 10, 35, 13),
	#                              u'Aliquam tempora.',
	#                              Decimal('7691191.82')],
	#                       6: {   4: u'http://\uc644\uc6b0\uc775.net/',
	#                              5: 16173702986.137,
	#                              6: [u'Alias quos dolores.', u'Suscipit.']}},
	#         u'nobis': {   9: datetime(2000, 4, 24, 12, 47, 21),
	#                       10: [   Decimal('-7.0672940068E+14'),
	#                               u'A non excepturi sit.',
	#                               7747],
	#                       11: {   9: u'Officia maxime.',
	#                               10: u'http://www.\ubcd1\uad6c.net/homepage/',
	#                               11: [   u'\ucd08\uc9c4@\uc8fc\uc2dd\ud68c\uc0ac.com',
	#                                       Decimal('28.0')]}},
	#         u'non': {   0: 5103,
	#                     1: [   3024,
	#                            Decimal('-962891.923502'),
	#                            u'y\ud574@\uc8fc.net'],
	#                     2: {   0: u'Unde officiis ipsum.',
	#                            1: u'Eligendi rerum et.',
	#                            2: [9409, u'Aut vel dolor.']}},
	#         u'odit': {   5: Decimal('-42445427451.0'),
	#                      6: [u'Dolores rem.', 2601, u'Ea quo aperiam sit.'],
	#                      7: {   5: u'Maiores sit totam.',
	#                             6: u'http://www.\uc591\uc724\ud6a8.kr/home.html',
	#                             7: [Decimal('6375128198.0'), u'Explicabo in.']}},
	#         u'quod': {   8: u'Et rem et impedit.',
	#                      9: [   u'\uac00\uc7a5\uace1@\uc8fc.com',
	#                             u'Veniam architecto.',
	#                             u'Non odio nemo.'],
	#                      10: {   8: u'Animi possimus aut.',
	#                              9: u'Ipsam ullam veniam.',
	#                              10: [Decimal('-2.36078025042E+12'), 4199]}},
	#         u'temporibus': {   6: u'Quia id repudiandae.',
	#                            7: [   u'Earum repellendus.',
	#                                   8904,
	#                                   datetime(1992, 7, 30, 17, 0, 57)],
	#                            8: {   6: u'Nulla.',
	#                                   7: u'Molestiae repellat.',
	#                                   8: [   u'http://\uc628\ubcd1\uc5f0.org/home.php',
	#                                          u'Aut quasi velit sed.']}},
	#         u'vel': {   2: u'http://\uc11d\ub3d9\uc5f4.com/homepage/',
	#                     3: [   u'Sit consequuntur.',
	#                            Decimal('-8562999.56101'),
	#                            u'Voluptatem omnis ea.'],
	#                     4: {   2: datetime(2004, 3, 31, 22, 29, 46),
	#                            3: Decimal('-22097.472942'),
	#                            4: [   datetime(2001, 7, 14, 6, 22, 11),
	#                                   u'Nulla magni cum.']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-50027726.26')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   6979147344441.33,
	#     1171,
	#     u'Voluptas est quos.',
	#     u'Dolorem ducimus.',
	#     u'f\uac00@\uaddc\ud718.org',
	#     Decimal('-68907842.3462'),
	#     Decimal('-692817700.545'),
	#     u'Voluptatem enim nam.',
	#     u'Omnis expedita aut.',
	#     442,
	#     Decimal('9216087499.1'),
	#     datetime(2004, 6, 14, 11, 41, 6),
	#     u'http://www.\uc8fc\uc2dd\ud68c\uc0ac.kr/explore/posts/homepage.htm']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'http://www.\uc720.kr/home.php',
	#     u'http://www.\uc8fc.com/categories/explore/search/index.php',
	#     u'p\uc724@\uba85\uc6b0\uc8fc.net',
	#     u'Rerum nesciunt quia.',
	#     u'Error ex nulla at.',
	#     9008,
	#     Decimal('6.1'),
	#     datetime(1992, 2, 21, 15, 59, 48),
	#     2803,
	#     4801635777564.26,
	#     2776,
	#     70575698874969.0,
	#     4315,
	#     u'Qui totam qui vero.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([446279654.9, u'\ucc44\uaddc@dreamwiz.com', u'Maiores non tempora.', u'Quos porro.', 8972, u'\uc720\ubc29@gmail.com', -816209.0, 2997, u'Quia soluta minima.', u'w\uc6a9@\uc9c4\ub824\ub780.com', 44970214211.88, 3003, u'Quia fuga qui.', u'Non qui doloremque.', Decimal('3337.59')])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'dolor': u'\uba85\ud638@\ud669\uc131\uc9c0.kr',
	#     u'eum': 6482,
	#     u'inventore': u'p\uac15@naver.com',
	#     u'laudantium': u'http://www.\ud638\uc21c\ub780.com/tags/tag/search/index.jsp',
	#     u'maiores': u'Excepturi et.',
	#     u'non': u'\ubcf4\uc548@hanmail.net',
	#     u'occaecati': -95129985673768.0,
	#     u'quia': datetime(2009, 7, 27, 21, 59, 42),
	#     u'quis': u'Illo ipsa cumque et.',
	#     u'totam': u'\uc724\uc601@nate.com',
	#     u'voluptatem': 5802}

	fake.pyint()
	# 1030

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'280801-1563121'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Windows NT 6.2; en-US; rv:1.9.1.20) Gecko/2010-12-13 07:01:35 Firefox/3.6.18'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/8.93.(X11; Linux x86_64; it-IT) Presto/2.9.180 Version/10.00'

	fake.windows_platform_token()
	# u'Windows 98'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 4.0; Trident/3.1)'

	fake.user_agent()
	# u'Opera/9.53.(Windows NT 6.2; en-US) Presto/2.9.160 Version/10.00'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5330 (KHTML, like Gecko) Chrome/13.0.808.0 Safari/5330'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; PPC Mac OS X 10_7_1'

	fake.safari()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_8_6 rv:2.0; it-IT) AppleWebKit/535.34.1 (KHTML, like Gecko) Version/4.0 Safari/535.34.1'
