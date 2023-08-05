
Language en_GB
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('83.6640435')

	fake.street_name()
	# u'Moore land'

	fake.address()
	# u'9 Hollie pass\nSouth Gradyton\nSS93 4LZ'

	fake.street_address()
	# u'2 Corie mountains'

	fake.postcode()
	# u'L6F 4EY'

	fake.longitude()
	# Decimal('149.581660')

	fake.country()
	# u'Turkmenistan'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('58.831446')

	fake.secondary_address()
	# u'Flat 60h'

	fake.street_suffix()
	# u'loop'

	fake.city_prefix()
	# u'South'

	fake.city_suffix()
	# u'ville'

	fake.building_number()
	# u'071'

	fake.country_code()
	# u'RU'

	fake.city()
	# u'Lake Sherie'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'1588427102976'

	fake.ean13()
	# u'1622663707189'

	fake.ean8()
	# u'67967827'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(184,59,41)'

	fake.color_name()
	# u'OrangeRed'

	fake.rgb_color_list()
	# (228, 28, 162)

	fake.rgb_color()
	# u'203,191,189'

	fake.safe_hex_color()
	# u'#44ff00'

	fake.safe_color_name()
	# u'purple'

	fake.hex_color()
	# u'#81d4bf'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Hagenes, Bernier and Kozey'

	fake.company_suffix()
	# u'Inc'

	fake.catch_phrase()
	# u'Optional global customer loyalty'

	fake.bs()
	# u'morph mission-critical web services'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'842'

	fake.credit_card_provider(card_type=None)
	# u'Maestro'

	fake.credit_card_full(card_type=None)
	# u'American Express\nAdele Haley\n343027367859963 01/25\nCID: 8644\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '01/21'

	fake.credit_card_number(card_type=None)
	# u'6011448306159109'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'HUF'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '26'

	fake.month()
	# '08'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 14, 4, 51)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1993, 10, 20, 14, 23, 52)

	fake.time(pattern="%H:%M:%S")
	# '12:59:06'

	fake.year()
	# '2012'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1375, 9, 8, 4, 25, 38)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 4, 7, 21, 33)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 6, 29, 9, 53, 53)

	fake.unix_time()
	# 1408003699

	fake.month_name()
	# 'October'

	fake.timezone()
	# u'Africa/Lubumbashi'

	fake.time_delta()
	# datetime.timedelta(4010, 75386)

	fake.century()
	# u'XII'

	fake.date(pattern="%Y-%m-%d")
	# '1980-06-02'

	fake.iso8601(tzinfo=None)
	# '1984-12-15T01:15:53'

	fake.date_time(tzinfo=None)
	# datetime(1980, 3, 18, 7, 48, 23)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 11, 29, 20, 52, 25)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'text/css'

	fake.file_name(category=None, extension=None)
	# u'recusandae.js'

	fake.file_extension(category=None)
	# u'gif'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'67.151.255.35'

	fake.url()
	# u'http://krajcik.com/'

	fake.company_email()
	# u'deckowclarine@hessel-brekke.com'

	fake.uri()
	# u'http://west.net/register/'

	fake.domain_word(*args, **kwargs)
	# u'will-haley'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/981/152'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'arch61@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'quaerat-et-aut'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'lemke.net'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'89f8:5b3b:1a3c:4343:f85d:0bae:6986:5371'

	fake.safe_email()
	# u'olene74@example.org'

	fake.user_name(*args, **kwargs)
	# u'arlin75'

	fake.uri_path(deep=None)
	# u'explore/search'

	fake.email()
	# u'gladis66@gmail.com'

	fake.uri_page()
	# u'faq'

	fake.mac_address()
	# u'5b:9e:77:5f:17:8b'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Banker'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Ex et et at velit totam. Laborum cupiditate ut ullam nostrum qui.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Velit doloremque ex esse dolor quia.'

	fake.word()
	# u'eum'

	fake.paragraphs(nb=3)
	# [   u'Et facilis hic tempora harum est quos. Voluptatibus quae molestiae velit deleniti quos est.',
	#     u'Accusamus quod vel eius doloremque quia nobis laborum. Repellat omnis consequuntur qui et voluptas vel. Sed nisi molestias ipsum nulla accusamus sint quos. Illum laborum est quia omnis.',
	#     u'Aliquid sed molestias molestias enim tenetur. Distinctio voluptas laboriosam quisquam fugit. Et et nesciunt eum maxime et dolorum voluptatem nostrum.']

	fake.words(nb=3)
	# [u'voluptatum', u'et', u'voluptatum']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Laudantium provident quod eius. Nemo dolore sed quibusdam corrupti ea harum. Quia repellat repellat vel cumque neque magni amet. Laborum eius illo est fugit ipsam quia.'

	fake.sentences(nb=3)
	# [   u'Rerum rerum officia enim tempore dicta.',
	#     u'Aut autem ipsa minus ut.',
	#     u'Necessitatibus qui neque ipsa sit.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'1hL4L_pd&d'

	fake.locale()
	# u'es_GT'

	fake.md5(raw_output=False)
	# '51e2afe998479b1b2ccc7504be09b3e8'

	fake.sha1(raw_output=False)
	# '2d8cbe66828911a0166987207918a819c930dcb1'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# '3684db3d425f16ee2b843c3e4d6b31a181d19c84a223674d3b1520e6343cf062'

	fake.uuid4()
	# '37395c0e-b4e7-449b-9103-c80fd8cd84f8'

	fake.language_code()
	# u'fr'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u"O'Kon"

	fake.name_female()
	# u'Porsha Fahey'

	fake.prefix_male()
	# u'Dr.'

	fake.prefix()
	# u'Dr.'

	fake.name()
	# u'Korey Friesen'

	fake.suffix_female()
	# u'DVM'

	fake.name_male()
	# u'Amos Baumbach'

	fake.first_name()
	# u'Harrie'

	fake.suffix_male()
	# u'V'

	fake.suffix()
	# u'DVM'

	fake.first_name_male()
	# u'Walton'

	fake.first_name_female()
	# u'Dayana'

	fake.last_name_female()
	# u'Cummerata'

	fake.last_name()
	# u'Ryan'

	fake.prefix_female()
	# u'Mrs.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'(03337) 86745'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Flat 94X\nKuvalis burgs\nHarrisport\nTQ1E 6WL',
	#     'birthdate': '2006-08-12',
	#     'mail': u'lucianaspinka@gmail.com',
	#     'name': u'Minta Blick',
	#     'sex': 'F',
	#     'username': u'iveyweimann'}

	fake.profile(fields=None)
	# {   'address': u'Flat 50F\nMaggio plaza\nQuitzonbury\nB8E 8NL',
	#     'birthdate': '1981-02-28',
	#     'blood_group': 'A+',
	#     'company': u'Jaskolski, Franecki and Hahn',
	#     'current_location': (Decimal('-84.542811'), Decimal('62.798612')),
	#     'job': 'Drilling engineer',
	#     'mail': u'rhiannaheidenreich@yahoo.com',
	#     'name': u'Jordin Beier MD',
	#     'residence': u'9 Rishi parkways\nNew Luciusfort\nG7C 3TE',
	#     'sex': 'F',
	#     'ssn': u'648-10-4111',
	#     'username': u'jovanny28',
	#     'website': [   u'http://www.considine-schowalter.com/',
	#                    u'http://little.com/',
	#                    u'http://www.koch-wiza.org/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('-40256.6679975'), u'mrice@yahoo.com', u'Harum numquam ea.', u'http://www.pollich.net/index.html', u'Et beatae soluta.', -116.890948622061, Decimal('-70.6219699682'), Decimal('-4.35211204497E+14'), u'zkuhn@gmail.com'])

	fake.pystr(max_chars=20)
	# u'Rem ut doloremque.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -90807180334656.8

	fake.pystruct(count=10, *value_types)
	# (   [   u'Eum consectetur.',
	#         Decimal('996192.94'),
	#         1511,
	#         4643,
	#         u'Dignissimos et.',
	#         u'esta81@hayes.net',
	#         u'Laboriosam dicta.',
	#         u'wfahey@yahoo.com',
	#         u'http://smitham.info/posts/explore/main/',
	#         6686],
	#     {   u'dolorum': u'http://bergnaum.com/register/',
	#         u'est': u'Pariatur velit quia.',
	#         u'mollitia': 6887,
	#         u'non': Decimal('-80696763583.8'),
	#         u'occaecati': u'jacobidoug@hotmail.com',
	#         u'quia': u'Nisi ut libero.',
	#         u'saepe': Decimal('6191004833.8'),
	#         u'suscipit': u'Consequatur a iusto.',
	#         u'voluptas': 2997},
	#     {   u'aut': {   4: u'Hic laborum.',
	#                     5: [   u'charleymurray@kuhlman.com',
	#                            -91059727.0,
	#                            u'itorphy@rau.com'],
	#                     6: {   4: u'http://rice.com/main/categories/author/',
	#                            5: u'http://spencer.com/main/author.htm',
	#                            6: [   Decimal('-502771724.808'),
	#                                   u'Reprehenderit ea.']}},
	#         u'consequatur': {   8: u'Et dolorum aut.',
	#                             9: [   4331,
	#                                    datetime(1985, 3, 14, 14, 14, 38),
	#                                    u'Modi est est optio.'],
	#                             10: {   8: u'Consequatur dolorum.',
	#                                     9: datetime(1974, 4, 7, 8, 57, 39),
	#                                     10: [   2736702970143.37,
	#                                             u'Omnis id quia.']}},
	#         u'dolorem': {   3: u'Eveniet molestiae.',
	#                         4: [   u'karenflatley@hayes.com',
	#                                u'Iste et numquam.',
	#                                Decimal('6.93259460235E+14')],
	#                         5: {   3: u'kiehnmaximiliano@bogisich.com',
	#                                4: u'Ad praesentium.',
	#                                5: [datetime(1999, 10, 7, 9, 0, 16), 8679]}},
	#         u'eius': {   6: -8853857.0,
	#                      7: [   8932,
	#                             datetime(1997, 8, 30, 6, 40, 59),
	#                             datetime(2000, 8, 10, 7, 8, 10)],
	#                      8: {   6: 4382,
	#                             7: 8477,
	#                             8: [   u'Quia qui quia.',
	#                                    u'http://corkery.com/blog/home/']}},
	#         u'rem': {   5: u'Qui et corporis est.',
	#                     6: [257.662, u'Assumenda quidem.', u'Architecto ipsam.'],
	#                     7: {   5: u'darnellcummerata@sauer.info',
	#                            6: u'Ut voluptas.',
	#                            7: [   datetime(2000, 10, 29, 18, 17, 46),
	#                                   u'Cupiditate non.']}},
	#         u'sapiente': {   2: -61779172370.7372,
	#                          3: [   datetime(2012, 11, 18, 8, 29, 52),
	#                                 Decimal('2020.0'),
	#                                 -51585619902882.4],
	#                          4: {   2: Decimal('9301767.33'),
	#                                 3: u'http://torp.info/login.html',
	#                                 4: [-67808.0, 888]}},
	#         u'sint': {   9: u'Et ullam.',
	#                      10: [   u'Dolor facilis.',
	#                              datetime(1983, 10, 17, 4, 8, 44),
	#                              u'elzyhayes@heller.org'],
	#                      11: {   9: u'A ullam.',
	#                              10: u'Rerum hic sed culpa.',
	#                              11: [   u'art38@grady-konopelski.net',
	#                                      -8454878936.72376]}},
	#         u'sit': {   7: u'tsteuber@yahoo.com',
	#                     8: [   6890,
	#                            u'Et fugit deleniti.',
	#                            u'Debitis repellendus.'],
	#                     9: {   7: -999010983.1,
	#                            8: 9010,
	#                            9: [u'Asperiores ea illum.', 15462527346341.0]}},
	#         u'voluptas': {   1: u'A ab quam quae modi.',
	#                          2: [   8217003.94379182,
	#                                 u'Nemo voluptatibus.',
	#                                 u'Voluptate quam.'],
	#                          3: {   1: 3665,
	#                                 2: 4531,
	#                                 3: [   69340670215.1191,
	#                                        u'bauchquentin@harris.com']}},
	#         u'voluptates': {   0: u'http://www.kemmer.com/',
	#                            1: [   u'Ab iste ipsam quis.',
	#                                   326,
	#                                   u'Commodi perferendis.'],
	#                            2: {   0: u'Placeat ut commodi.',
	#                                   1: u'markitawest@lynch.com',
	#                                   2: [   u'Illo sint eius et.',
	#                                          u'Reprehenderit et.']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('9020006621.88')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   1510,
	#     5882,
	#     5356,
	#     Decimal('-84315296.2'),
	#     u'http://mcclure.info/search/',
	#     u'Sit doloremque quo.',
	#     1619,
	#     u'http://dickens.com/',
	#     datetime(1994, 4, 8, 15, 38, 44),
	#     Decimal('64.6199831505')]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   597282.0,
	#     u'Eos impedit illum.',
	#     datetime(2000, 7, 9, 18, 39, 53),
	#     76,
	#     u'Temporibus ducimus.',
	#     Decimal('-162356.15957'),
	#     datetime(1976, 4, 7, 7, 33, 16),
	#     datetime(1996, 2, 15, 2, 30, 16),
	#     u'Deserunt vero ea.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('-18409605654.9'), u'Quidem aut omnis.', Decimal('-2434845.88743'), Decimal('-8690866.2'), u'Et quo dolores.', u'http://hauck-armstrong.com/tags/tag/search/', 2430])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'ad': u'http://www.hermann-fisher.com/login.htm',
	#     u'aperiam': u'http://jones-heidenreich.net/about.html',
	#     u'et': u'Blanditiis optio.',
	#     u'ipsa': 9857,
	#     u'qui': Decimal('-51814.487'),
	#     u'quia': u'http://volkman.com/main/blog/list/post/',
	#     u'saepe': u'Nemo quia.',
	#     u'sed': u'Vel est debitis.'}

	fake.pyint()
	# 5919

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'704-36-7245'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; rv:1.9.4.20) Gecko/2012-06-13 13:28:19 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.16.(Windows 98; Win 9x 4.90; sl-SI) Presto/2.9.176 Version/12.00'

	fake.windows_platform_token()
	# u'Windows CE'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/3.0)'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5361 (KHTML, like Gecko) Chrome/14.0.838.0 Safari/5361'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; Intel Mac OS X 10_7_2'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/532.38.4 (KHTML, like Gecko) Version/5.0.3 Safari/532.38.4'
