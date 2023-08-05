
Language en_CA
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('82.7693915')

	fake.street_name()
	# u'Kautzer Underpass'

	fake.address()
	# u'550 Hilma Hollow\nDurganborough, NB M6N 9H2'

	fake.street_address()
	# u'721 Lebsack Trafficway Suite 834'

	fake.postcode()
	# u'57194'

	fake.longitude()
	# Decimal('-146.644524')

	fake.country()
	# u'Germany'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('114.337663')

	fake.postal_code_letter()
	# u'M'

	fake.province()
	# u'Northwest Territories'

	fake.city_prefix()
	# u'West'

	fake.street_suffix()
	# u'Trace'

	fake.city_suffix()
	# u'burgh'

	fake.building_number()
	# u'273'

	fake.country_code()
	# u'RO'

	fake.secondary_address()
	# u'Suite 506'

	fake.city()
	# u'East Taylor'

	fake.province_abbr()
	# u'NL'

	fake.postalcode()
	# u'B4G 2A9'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'6652169239322'

	fake.ean13()
	# u'0123677943200'

	fake.ean8()
	# u'76312724'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(252,96,197)'

	fake.color_name()
	# u'DarkOrchid'

	fake.rgb_color_list()
	# (250, 162, 228)

	fake.rgb_color()
	# u'116,16,184'

	fake.safe_hex_color()
	# u'#ccff00'

	fake.safe_color_name()
	# u'lime'

	fake.hex_color()
	# u'#a577ca'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Hermiston LLC'

	fake.company_suffix()
	# u'Group'

	fake.catch_phrase()
	# u'Re-engineered foreground protocol'

	fake.bs()
	# u'orchestrate value-added paradigms'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'910'

	fake.credit_card_provider(card_type=None)
	# u'Voyager'

	fake.credit_card_full(card_type=None)
	# u'VISA 13 digit\nMamie Yundt\n4493918479174 08/17\nCVC: 478\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '10/24'

	fake.credit_card_number(card_type=None)
	# u'5530741106378414'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'SCR'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '16'

	fake.month()
	# '08'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 5, 56, 3)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1987, 4, 28, 21, 4, 58)

	fake.time(pattern="%H:%M:%S")
	# '05:02:51'

	fake.year()
	# '2002'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1610, 1, 17, 22, 6, 15)

	fake.day_of_week()
	# 'Friday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 1, 57, 58)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2014, 3, 20, 15, 35, 45)

	fake.unix_time()
	# 650896539

	fake.month_name()
	# 'June'

	fake.timezone()
	# u'Africa/Casablanca'

	fake.time_delta()
	# datetime.timedelta(953, 10539)

	fake.century()
	# u'I'

	fake.date(pattern="%Y-%m-%d")
	# '1975-07-04'

	fake.iso8601(tzinfo=None)
	# '2007-12-27T08:55:39'

	fake.date_time(tzinfo=None)
	# datetime(2014, 3, 1, 19, 58, 35)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 12, 23, 9, 53, 53)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'model/iges'

	fake.file_name(category=None, extension=None)
	# u'porro.mp4'

	fake.file_extension(category=None)
	# u'webm'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'13.94.117.27'

	fake.url()
	# u'http://www.wolff.com/'

	fake.company_email()
	# u'josef08@cruickshank-adams.com'

	fake.uri()
	# u'http://blick.net/app/terms/'

	fake.domain_word(*args, **kwargs)
	# u'morissette'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/546/81'

	fake.tld()
	# u'net'

	fake.free_email()
	# u'fern71@gmail.com'

	fake.slug(*args, **kwargs)
	# u'molestiae-odit-est'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'gerlach.com'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'c839:011a:ec4d:a84c:cf10:dd53:8226:d48c'

	fake.safe_email()
	# u'joretta39@example.org'

	fake.user_name(*args, **kwargs)
	# u'hermanrihanna'

	fake.uri_path(deep=None)
	# u'category/tags/category'

	fake.email()
	# u'bharvey@hotmail.com'

	fake.uri_page()
	# u'about'

	fake.mac_address()
	# u'61:55:a7:19:42:34'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Industrial/product designer'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Voluptatibus non laborum adipisci et sed aut ducimus. Qui nam sapiente odio. Deserunt et eos aut eos repudiandae quia molestiae. Architecto est velit fuga veniam.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Nesciunt beatae et quis.'

	fake.word()
	# u'quidem'

	fake.paragraphs(nb=3)
	# [   u'Veritatis fuga pariatur consequatur est velit molestiae consequuntur. Enim maxime corrupti sit amet aut. Eveniet enim quasi nemo. Ullam modi magnam minima.',
	#     u'Sunt mollitia et delectus in. Id laudantium et minima. Reprehenderit modi dolores nostrum quis hic voluptates.',
	#     u'Iure rerum perspiciatis numquam nemo. Quas possimus quasi optio in qui. Ea alias debitis dolorem corrupti id maxime quibusdam.']

	fake.words(nb=3)
	# [u'quas', u'nostrum', u'temporibus']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Dolores aut culpa ratione cupiditate in. Natus et corrupti et dolore. Ad odit minus eum sed consequatur voluptatem consequatur ad. Fugiat corrupti magnam quam est.'

	fake.sentences(nb=3)
	# [   u'Voluptas animi sed accusamus id.',
	#     u'Explicabo doloribus culpa enim est maxime optio.',
	#     u'In quos minima ut commodi.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u')7qWVAw*Oq'

	fake.locale()
	# u'es_OM'

	fake.md5(raw_output=False)
	# '3f586333530bebd0a6eb6a9b1bd82230'

	fake.sha1(raw_output=False)
	# '8ee37fd69cccc3ecaad977f886aaa674e91e88aa'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# '79615cdb05336a0a8336721f6846a1d0de5c9a46e08804b0dceacef13e4cc106'

	fake.uuid4()
	# '1f332dc7-5e0e-41f9-bd98-8d66514c730f'

	fake.language_code()
	# u'el'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Dietrich'

	fake.name_female()
	# u'Evelynn Miller'

	fake.prefix_male()
	# u'Dr.'

	fake.prefix()
	# u'Ms.'

	fake.name()
	# u'Dr. Coley Shanahan'

	fake.suffix_female()
	# u'DVM'

	fake.name_male()
	# u'Burk Schamberger'

	fake.first_name()
	# u'Chelsy'

	fake.suffix_male()
	# u'Sr.'

	fake.suffix()
	# u'DDS'

	fake.first_name_male()
	# u'Devaughn'

	fake.first_name_female()
	# u'Nakisha'

	fake.last_name_female()
	# u'Hegmann'

	fake.last_name()
	# u'Schaefer'

	fake.prefix_female()
	# u'Ms.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'599 460 6300'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'09056 Samira View\nLake Lester, BC V6C9L3',
	#     'birthdate': '2009-11-27',
	#     'mail': u'clemens40@yahoo.com',
	#     'name': u'Kyle Block I',
	#     'sex': 'M',
	#     'username': u'lkris'}

	fake.profile(fields=None)
	# {   'address': u'87895 Kimball Vista Apt. 153\nMonicamouth, AB J4X 6Y3',
	#     'birthdate': '2001-04-06',
	#     'blood_group': 'B-',
	#     'company': u'Kris, Predovic and Murphy',
	#     'current_location': (Decimal('-68.834179'), Decimal('64.223471')),
	#     'job': 'Education officer, environmental',
	#     'mail': u'elza43@gmail.com',
	#     'name': u'Mills Kunde',
	#     'residence': u'30930 Lannie Court Suite 580\nBruenville, YT C9J2X9',
	#     'sex': 'M',
	#     'ssn': u'205 846 835 ',
	#     'username': u'steuberstephan',
	#     'website': [u'http://marquardt.com/', u'http://www.durgan-homenick.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   4453,
	#     u'Exercitationem.',
	#     7935,
	#     Decimal('7.02827504708E+13'),
	#     u'Autem quo.',
	#     Decimal('-4.22795571871E+12'),
	#     datetime(1971, 5, 11, 21, 29, 12),
	#     3582,
	#     1003712.2187137,
	#     7151,
	#     2177,
	#     u'Omnis ratione.',
	#     u'Fuga eligendi.']

	fake.pystr(max_chars=20)
	# u'Molestias quos.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 35.187967903541

	fake.pystruct(count=10, *value_types)
	# (   [   u'Facilis ad nisi.',
	#         Decimal('-78530168569.8'),
	#         u'Asperiores possimus.',
	#         -78174359819761.0,
	#         u'http://www.stokes.info/tags/main/search/',
	#         386200.55,
	#         u'Reprehenderit et.',
	#         u'Aut veritatis omnis.',
	#         u'Ratione officiis.',
	#         u'Cum ut dolor aut ea.'],
	#     {   u'architecto': u'Culpa nihil.',
	#         u'debitis': u'http://stracke-murazik.com/category/author/',
	#         u'natus': u'derichayes@schaden.com',
	#         u'odio': Decimal('-93.7855144'),
	#         u'quam': u'http://www.mann.com/homepage.html',
	#         u'quibusdam': u'Vel et sequi.',
	#         u'quod': u'vara20@powlowski.com',
	#         u'totam': u'glynis40@steuber.com',
	#         u'voluptas': u'Non id voluptatem.',
	#         u'voluptatibus': u'Aut voluptatem esse.'},
	#     {   u'alias': {   4: u'Nam tenetur non.',
	#                       5: [   u'Molestias est est.',
	#                              Decimal('-1.91187'),
	#                              u'http://mayert.com/privacy/'],
	#                       6: {   4: -628336933155198.0,
	#                              5: u'lavelle91@hotmail.com',
	#                              6: [5443, u'http://www.collins-batz.info/']}},
	#         u'architecto': {   2: u'Dolorem qui.',
	#                            3: [u'Beatae sed odio.', -94960075.2155, 6649],
	#                            4: {   2: u'Recusandae.',
	#                                   3: u'Cupiditate.',
	#                                   4: [   u'Nam pariatur vero.',
	#                                          u'Maxime omnis beatae.']}},
	#         u'delectus': {   6: u'Nam minima totam.',
	#                          7: [   -3313280.59519402,
	#                                 Decimal('18178.84676'),
	#                                 13805242.1935431],
	#                          8: {   6: u'Quia corrupti eius.',
	#                                 7: u'http://www.terry.info/wp-content/main/search/',
	#                                 8: [   u'http://www.ullrich-bogisich.com/',
	#                                        u'Omnis aut ratione.']}},
	#         u'dolores': {   7: u'Dolorem sed sint.',
	#                         8: [   u'Quas quis nobis.',
	#                                u'Quae aut et dolorem.',
	#                                u'Aspernatur.'],
	#                         9: {   7: Decimal('622521238673'),
	#                                8: u'http://effertz-botsford.com/category/',
	#                                9: [9452, datetime(1996, 6, 1, 5, 33, 24)]}},
	#         u'enim': {   0: u'Rerum accusantium.',
	#                      1: [   u'alethawaters@ullrich.org',
	#                             u'Sit blanditiis sed.',
	#                             u'rkuvalis@gmail.com'],
	#                      2: {   0: u'Delectus eum.',
	#                             1: u'Odit ut explicabo.',
	#                             2: [   u'http://schumm.net/search.htm',
	#                                    u'Neque nihil.']}},
	#         u'itaque': {   8: -7896904123464.7,
	#                        9: [   u'Molestiae iusto et.',
	#                               u'http://ernser.com/main/posts/about.jsp',
	#                               datetime(1994, 11, 27, 4, 38, 51)],
	#                        10: {   8: 6744,
	#                                9: u'Ad officiis ratione.',
	#                                10: [   u'kathrynlueilwitz@gmail.com',
	#                                        -5094289.99]}},
	#         u'quas': {   5: Decimal('-52894.7676507'),
	#                      6: [   u'Consequatur eaque.',
	#                             -7298884.6,
	#                             66119.1472541742],
	#                      7: {   5: u'Tempora a dolor et.',
	#                             6: u'Maxime qui qui.',
	#                             7: [   u'krodriguez@considine-brakus.net',
	#                                    u'Explicabo molestiae.']}},
	#         u'qui': {   3: u'Deserunt omnis.',
	#                     4: [888, Decimal('445736598.741'), 845183053093.4],
	#                     5: {   3: Decimal('7.27706611356E+12'),
	#                            4: u'Veniam omnis.',
	#                            5: [   datetime(1974, 8, 1, 5, 15, 1),
	#                                   Decimal('0.906033250208')]}},
	#         u'sapiente': {   1: u'Nemo consequatur.',
	#                          2: [6138, 3294, datetime(2004, 12, 28, 1, 9, 44)],
	#                          3: {   1: u'Debitis explicabo.',
	#                                 2: u'Libero a excepturi.',
	#                                 3: [9206, u'Et ut corporis.']}},
	#         u'ut': {   9: Decimal('-5.16131685133E+13'),
	#                    10: [5388, datetime(1972, 6, 15, 12, 20, 35), 7254],
	#                    11: {   9: Decimal('-20.0'),
	#                            10: u'Et voluptas et.',
	#                            11: [u'Ut blanditiis.', 13.22]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('68.88736')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'Nostrum quis.',
	#     u'Ut nostrum et est.',
	#     datetime(1974, 7, 1, 1, 48, 13),
	#     u'http://botsford.com/blog/author.html',
	#     u'http://www.auer-beahan.biz/privacy/',
	#     Decimal('-2.20361849939E+14'),
	#     u'Eos ea nam dolorem.',
	#     4674,
	#     u'In incidunt vitae.',
	#     Decimal('81472.969169'),
	#     u'denver26@davis.com']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'debra75@bosco.com',
	#     u'jaydengreen@gmail.com',
	#     datetime(1990, 9, 5, 15, 1, 59),
	#     Decimal('-11.9921514565'),
	#     u'Deleniti iure qui.',
	#     u'bayeretter@haley.com',
	#     u'Ducimus.')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('2.918'), Decimal('1171758.37'), 6738498.768, 2855, u'http://parker.info/', u'Sed veniam natus.', u'auerconway@deckow.com', u'Commodi qui ut cum.', u'Et beatae qui.', Decimal('-284.602869606')])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'adipisci': 5230,
	#     u'est': Decimal('-421.92397'),
	#     u'mollitia': u'Quos ipsa molestiae.',
	#     u'nisi': u'kalvin64@durgan-collins.org',
	#     u'numquam': 873,
	#     u'qui': -9021649175.1846,
	#     u'sequi': u'Aspernatur nihil.'}

	fake.pyint()
	# 3065

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'319 582 078 '

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_9; rv:1.9.4.20) Gecko/2012-04-02 21:52:02 Firefox/12.0'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.67.(X11; Linux i686; it-IT) Presto/2.9.176 Version/12.00'

	fake.windows_platform_token()
	# u'Windows 98'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.2; Trident/5.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/532.43.3 (KHTML, like Gecko) Version/4.0.4 Safari/532.43.3'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5332 (KHTML, like Gecko) Chrome/13.0.822.0 Safari/5332'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_5_0'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_3 like Mac OS X; en-US) AppleWebKit/531.20.3 (KHTML, like Gecko) Version/4.0.5 Mobile/8B114 Safari/6531.20.3'
