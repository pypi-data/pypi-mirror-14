
Language pl_PL
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('79.3957495')

	fake.street_name()
	# u'Broniewskiego'

	fake.address()
	# u'32 Lubelska 73-744 Krosno'

	fake.street_address()
	# u'24 Lawendowa'

	fake.postcode()
	# u'00-322'

	fake.longitude()
	# Decimal('-19.548268')

	fake.country()
	# u'Guinea-Bissau'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-138.303650')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'80'

	fake.country_code()
	# u'CY'

	fake.city()
	# u'Grudzi\u0105dz'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'4294207487245'

	fake.ean13()
	# u'4390257445362'

	fake.ean8()
	# u'10575383'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(225,175,44)'

	fake.color_name()
	# u'Yellow'

	fake.rgb_color_list()
	# (104, 223, 27)

	fake.rgb_color()
	# u'203,255,253'

	fake.safe_hex_color()
	# u'#660000'

	fake.safe_color_name()
	# u'black'

	fake.hex_color()
	# u'#a9c0f6'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Zas\u0119pa Ltd'

	fake.company_suffix()
	# u'Inc'

	fake.catch_phrase()
	# u'Persistent clear-thinking matrices'

	fake.bs()
	# u'e-enable impactful architectures'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'586'

	fake.credit_card_provider(card_type=None)
	# u'VISA 16 digit'

	fake.credit_card_full(card_type=None)
	# u'VISA 16 digit\nAleksander Kr\xf3likiewicz\n4951891788508151 01/17\nCVC: 832\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '10/19'

	fake.credit_card_number(card_type=None)
	# u'3528646791766931'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'INR'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '15'

	fake.month()
	# '08'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 1, 0, 51, 8)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 38)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1994, 11, 18, 19, 31, 12)

	fake.time(pattern="%H:%M:%S")
	# '01:00:13'

	fake.year()
	# '1970'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(127, 8, 31, 15, 17, 57)

	fake.day_of_week()
	# 'Thursday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 10, 41, 39)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 9, 21, 7, 27, 9)

	fake.unix_time()
	# 1362285116

	fake.month_name()
	# 'July'

	fake.timezone()
	# u'Africa/Brazzaville'

	fake.time_delta()
	# datetime.timedelta(233, 85798)

	fake.century()
	# u'XII'

	fake.date(pattern="%Y-%m-%d")
	# '1983-11-19'

	fake.iso8601(tzinfo=None)
	# '2008-10-21T10:17:02'

	fake.date_time(tzinfo=None)
	# datetime(2012, 9, 12, 18, 53, 12)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 7, 19, 14, 20, 58)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'text/html'

	fake.file_name(category=None, extension=None)
	# u'delectus.json'

	fake.file_extension(category=None)
	# u'csv'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'14.203.33.197'

	fake.url()
	# u'http://drej.com/'

	fake.company_email()
	# u'kgorol@zander.biz'

	fake.uri()
	# u'http://www.sajda.info/'

	fake.domain_word(*args, **kwargs)
	# u'pi\u0105tkiewicz'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/571x588'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'maksymkamil@yahoo.com'

	fake.slug(*args, **kwargs)
	# u'ut-eum-facere'

	fake.free_email_domain()
	# u'hotmail.com'

	fake.domain_name()
	# u'durma-dankiewicz.com'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'3153:0abd:554e:a1ec:395e:cc40:b450:85b7'

	fake.safe_email()
	# u'kornel25@example.org'

	fake.user_name(*args, **kwargs)
	# u'bieszkeaurelia'

	fake.uri_path(deep=None)
	# u'wp-content'

	fake.email()
	# u'\u0142ukasz61@hotmail.com'

	fake.uri_page()
	# u'author'

	fake.mac_address()
	# u'05:d5:b3:fb:b1:44'

``faker.providers.job``
-----------------------

::

	fake.job()
	# u'Zarz\u0105dca nieruchomo\u015bci'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Minus doloribus amet qui illo. Fugit a eum iste sint laudantium. Culpa illum dicta neque voluptatum. Delectus nostrum dolor praesentium beatae.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Commodi suscipit ipsa cum vel distinctio quia.'

	fake.word()
	# u'in'

	fake.paragraphs(nb=3)
	# [   u'Repellendus est iure impedit blanditiis quis. Eos quaerat dicta sit dolorem aspernatur tempora. Maxime dicta quam et id nam laudantium.',
	#     u'Amet consequatur rerum ullam quasi commodi voluptatem molestias. Saepe veritatis et exercitationem fugiat autem odit. Eos itaque et occaecati laborum aut. Sed repellendus aut est quia corrupti soluta.',
	#     u'Quia sint qui a et fugit ut. Vel vero veniam consequuntur minima veniam nihil. Quisquam nam aut illum tempore perspiciatis.']

	fake.words(nb=3)
	# [u'laborum', u'libero', u'repellat']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Qui ut impedit in velit ullam laudantium qui. Officiis aut sequi et. Ab expedita fugiat quam atque. Eligendi facilis velit eligendi sint.'

	fake.sentences(nb=3)
	# [   u'Ad laboriosam aut blanditiis corrupti ipsa doloremque.',
	#     u'Et praesentium quia cumque molestiae veritatis autem.',
	#     u'Cum mollitia magnam est et molestiae dicta.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'%1i#Wt4L^x'

	fake.locale()
	# u'fr_SL'

	fake.md5(raw_output=False)
	# '4049d6d9e2dacb2eeacc925351daa443'

	fake.sha1(raw_output=False)
	# '91bb4aa219cbdcf481a43c807f0e067e0f7127a4'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '2b7982e200b306ec56d18299f2b5cbe9c705391996964a1508708482a9c19506'

	fake.uuid4()
	# '10598c48-0b14-4965-86c8-6ebe0ff43b3d'

	fake.language_code()
	# u'de'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Kulisz'

	fake.name_female()
	# u'Maks Bylina'

	fake.prefix_male()
	# u'pani'

	fake.prefix()
	# u'pani'

	fake.name()
	# u'Marcin Nurek'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Gabriel Detka'

	fake.first_name()
	# u'Ada'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Artur'

	fake.first_name_female()
	# u'Ewelina'

	fake.last_name_female()
	# u'\u015awierkot'

	fake.last_name()
	# u'Pindor'

	fake.prefix_female()
	# u'pani'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'662 111 289'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'85 Kwiatowa 31-242 Pabianice',
	#     'birthdate': '2014-06-15',
	#     'mail': u'nkozdr\xf3j@gmail.com',
	#     'name': u'pani Kaja Siemion',
	#     'sex': 'M',
	#     'username': u'udargacz'}

	fake.profile(fields=None)
	# {   'address': u'88 Dzialkowa 10-231 Kielce',
	#     'birthdate': '1973-07-07',
	#     'blood_group': 'A+',
	#     'company': u'M\u0105drzyk-Stachelek',
	#     'current_location': (Decimal('0.488644'), Decimal('102.570400')),
	#     'job': u'Barista',
	#     'mail': u'u\u0142osiewicz@hotmail.com',
	#     'name': u'Kornel Gramza',
	#     'residence': u'08 Rynek 07-474 Rybnik',
	#     'sex': 'M',
	#     'ssn': u'364-82-6772',
	#     'username': u'j\xf3zef14',
	#     'website': [   u'http://szymanik.biz/',
	#                    u'http://oleszko-zawal.org/',
	#                    u'http://www.machowicz.org/',
	#                    u'http://www.cieniuch-kontny.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   datetime(2006, 4, 13, 20, 4, 22),
	#     5792,
	#     u'Vel eum sed et enim.',
	#     -126.66036,
	#     datetime(1973, 1, 15, 1, 4, 38),
	#     u'http://katana-gortat.info/explore/categories/main/about/',
	#     u'Sunt est rerum.']

	fake.pystr(max_chars=20)
	# u'Esse fugiat quo.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -847918326.0

	fake.pystruct(count=10, *value_types)
	# (   [   6294,
	#         u'Et enim rem dolore.',
	#         22284889982.48,
	#         -45703547073.667,
	#         60364.568532,
	#         datetime(2010, 11, 21, 20, 42, 52),
	#         u'Reprehenderit et.',
	#         -111396844.7,
	#         u'Dolores voluptas.',
	#         u'Pariatur dolore.'],
	#     {   u'aut': u'http://www.ga\u0142aj-majzner.info/search.htm',
	#         u'ducimus': Decimal('914956597266'),
	#         u'et': u'Fuga ut mollitia.',
	#         u'excepturi': u'http://matejuk-ryczko.com/tags/app/homepage/',
	#         u'molestiae': 162952.1,
	#         u'nihil': 7369,
	#         u'occaecati': u'Quibusdam.',
	#         u'officiis': 2481,
	#         u'qui': u'http://sinkiewicz-tywoniuk.com/post/'},
	#     {   u'architecto': {   0: 2015,
	#                            1: [   u'http://pa\u015bnik.com/category/',
	#                                   u'Debitis veritatis.',
	#                                   u'Repudiandae aperiam.'],
	#                            2: {   0: u'Dolores assumenda.',
	#                                   1: datetime(1981, 6, 20, 6, 34),
	#                                   2: [   u'Perferendis enim ut.',
	#                                          u'Voluptatem aut enim.']}},
	#         u'est': {   5: 7211,
	#                     6: [   9044,
	#                            Decimal('-6.05849931698E+14'),
	#                            Decimal('-35904863.15')],
	#                     7: {   5: -7363080311.194,
	#                            6: u'Minus sed esse.',
	#                            7: [Decimal('-3787284.12372'), 3839]}},
	#         u'iste': {   8: 7804,
	#                      9: [   74381010349.249,
	#                             u'Eum assumenda ipsam.',
	#                             u'http://www.pik-gronostaj.com/list/app/privacy/'],
	#                      10: {   8: Decimal('-4957.4494956'),
	#                              9: u'ryszardkubowicz@\u0142achacz-augustynek.org',
	#                              10: [u'Ea unde aliquam.', u'Ut corrupti.']}},
	#         u'minima': {   6: u'http://www.le\u015bna.com/main/app/list/terms/',
	#                        7: [   u'Quos quos nihil.',
	#                               u'stanis\u0142awmzyk@chmara.com',
	#                               Decimal('-6817360943.8')],
	#                        8: {   6: Decimal('-9.04071256037E+14'),
	#                               7: u'In vel repellat.',
	#                               8: [6207, 8497]}},
	#         u'non': {   7: 7275,
	#                     8: [   datetime(1982, 8, 3, 14, 52, 29),
	#                            u'http://uryga.net/',
	#                            u'http://gogola.net/login/'],
	#                     9: {   7: 1292,
	#                            8: u'Illum repudiandae.',
	#                            9: [   Decimal('-44.856'),
	#                                   datetime(1984, 2, 4, 1, 1, 28)]}},
	#         u'porro': {   4: 9336,
	#                       5: [   datetime(1993, 10, 8, 20, 19, 50),
	#                              Decimal('135.0'),
	#                              u'Ut voluptatem cum.'],
	#                       6: {   4: u'Rerum inventore.',
	#                              5: 9400,
	#                              6: [   Decimal('6483005.785'),
	#                                     u'Et nesciunt eaque.']}},
	#         u'sapiente': {   2: 4370,
	#                          3: [   u'http://www.ciapa.com/category/categories/author.asp',
	#                                 u'http://szymanik-wons.com/',
	#                                 u'Aut voluptatem.'],
	#                          4: {   2: u'Tempora ea sed.',
	#                                 3: u'Nobis voluptatem.',
	#                                 4: [   u'http://imio\u0142czyk-herbut.com/tag/list/about/',
	#                                        u'Qui qui quae.']}},
	#         u'sint': {   9: u'Aspernatur odit.',
	#                      10: [   u'daniel62@hotmail.com',
	#                              Decimal('30782.3321453'),
	#                              7367],
	#                      11: {   9: 4943,
	#                              10: u'Illo quibusdam.',
	#                              11: [   37.3687735919691,
	#                                      u'http://www.ostapiuk.com/']}},
	#         u'vel': {   3: u'http://www.gapys.biz/tags/wp-content/tag/author/',
	#                     4: [   u'vochnik@dyczko.info',
	#                            u'http://www.dro\u015b.com/categories/tags/categories/privacy.jsp',
	#                            u'py\u0107dawid@yahoo.com'],
	#                     5: {   3: 7009160.3987846,
	#                            4: datetime(1982, 5, 9, 18, 15, 28),
	#                            5: [   datetime(1991, 6, 6, 10, 16, 43),
	#                                   u'http://www.potoczna.com/author.php']}},
	#         u'voluptas': {   1: datetime(2001, 7, 14, 13, 32, 51),
	#                          2: [   u'Error explicabo.',
	#                                 datetime(1971, 3, 11, 0, 46, 33),
	#                                 5671],
	#                          3: {   1: 1614,
	#                                 2: Decimal('184.6983'),
	#                                 3: [u'Vel voluptas.', 5396]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-6375694223.1')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'zmajerczyk@karwan-dokt\xf3r.biz',
	#     u'nkiciak@gmail.com',
	#     6645794.368542,
	#     u'Officiis nihil illo.',
	#     u'http://pietrasiak.org/author/',
	#     u'Provident.',
	#     u'http://labocha-tyniec.com/faq/',
	#     u'http://www.dzienis.info/tag/category/tag/index/',
	#     u'Sit corporis.']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'http://www.kurc.info/about.asp',
	#     u'Explicabo sed vero.',
	#     Decimal('530876.848'),
	#     u'Optio est excepturi.',
	#     u'Omnis consequatur.',
	#     u'roksanaosman@hotmail.com',
	#     -77105016.388,
	#     u'Eligendi quia.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([datetime(1986, 2, 1, 12, 0, 46), u'Eaque blanditiis.', datetime(1989, 9, 2, 17, 11, 8), u'Ut nisi tempore.', u'Ab debitis sit.', -55753.578704884, u'Autem est dicta.', u'At consequuntur.', 3422, u'melkarozalia@gmail.com'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'aut': u'Minus velit sit.',
	#     u'distinctio': u'Nesciunt alias.',
	#     u'dolor': u'juliuszstosik@kiliszek.com',
	#     u'incidunt': 3749,
	#     u'itaque': datetime(1971, 2, 4, 22, 26, 15),
	#     u'maxime': u'Accusantium impedit.',
	#     u'quia': u'http://baszak.biz/explore/categories/tags/author.html',
	#     u'quisquam': u'http://www.stanis\u0142awek.com/terms.asp'}

	fake.pyint()
	# 6855

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'270-36-1041'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'PPC'

	fake.firefox()
	# u'Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-10-22 17:40:54 Firefox/3.6.19'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/9.62.(Windows NT 6.1; sl-SI) Presto/2.9.178 Version/10.00'

	fake.windows_platform_token()
	# u'Windows NT 6.2'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.1)'

	fake.user_agent()
	# u'Opera/9.66.(X11; Linux x86_64; en-US) Presto/2.9.189 Version/12.00'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5360 (KHTML, like Gecko) Chrome/13.0.803.0 Safari/5360'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; PPC Mac OS X 10_7_8'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows NT 5.0) AppleWebKit/535.18.3 (KHTML, like Gecko) Version/5.0.3 Safari/535.18.3'
