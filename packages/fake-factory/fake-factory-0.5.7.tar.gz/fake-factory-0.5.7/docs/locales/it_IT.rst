
Language it_IT
===============

``faker.providers.address``
---------------------------

::

	fake.state_abbr()
	# u'LT'

	fake.latitude()
	# Decimal('7.123200')

	fake.street_name()
	# u'Stretto Montanari'

	fake.address()
	# u'Via Isabel 80 Appartamento 66\nBarbieri ligure, 38682 Como (CN)'

	fake.street_address()
	# u'Incrocio Bianchi 488'

	fake.postcode()
	# u'04418'

	fake.longitude()
	# Decimal('52.560962')

	fake.country()
	# u'Samoa'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-84.833347')

	fake.secondary_address()
	# u'Piano 4'

	fake.street_suffix()
	# u'Stretto'

	fake.city_prefix()
	# u'San'

	fake.city_suffix()
	# u'calabro'

	fake.building_number()
	# u'56'

	fake.country_code()
	# u'GH'

	fake.city()
	# u'Settimo Joshua calabro'

	fake.state()
	# u'Pavia'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'8360268373400'

	fake.ean13()
	# u'3418443838482'

	fake.ean8()
	# u'22444783'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(64,32,5)'

	fake.color_name()
	# u'SeaShell'

	fake.rgb_color_list()
	# (72, 61, 207)

	fake.rgb_color()
	# u'242,214,45'

	fake.safe_hex_color()
	# u'#555500'

	fake.safe_color_name()
	# u'maroon'

	fake.hex_color()
	# u'#55f18c'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Ferrari, Fiore e Longo Group'

	fake.company_suffix()
	# u'e figli'

	fake.catch_phrase()
	# u'Matrice ridotta sistemica'

	fake.bs()
	# u'e-commerce exploit dinamiche'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'924'

	fake.credit_card_provider(card_type=None)
	# u'Maestro'

	fake.credit_card_full(card_type=None)
	# u'Maestro\nTristano Vitale\n503806718956 01/22\nCVV: 205\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '03/16'

	fake.credit_card_number(card_type=None)
	# u'4948588610082092'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'GBP'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '23'

	fake.month()
	# '10'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 0, 52, 50)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1994, 10, 30, 14, 25, 30)

	fake.time(pattern="%H:%M:%S")
	# '08:22:09'

	fake.year()
	# '2013'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1223, 11, 18, 6, 18, 48)

	fake.day_of_week()
	# 'Thursday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 12, 12, 25)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 7, 9, 20, 15)

	fake.unix_time()
	# 584087513

	fake.month_name()
	# 'January'

	fake.timezone()
	# u'Indian/Mahe'

	fake.time_delta()
	# datetime.timedelta(7409, 36441)

	fake.century()
	# u'XVI'

	fake.date(pattern="%Y-%m-%d")
	# '1992-09-04'

	fake.iso8601(tzinfo=None)
	# '1993-05-16T23:48:58'

	fake.date_time(tzinfo=None)
	# datetime(1992, 7, 11, 12, 17, 30)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 11, 3, 3, 13, 56)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'application/ogg'

	fake.file_name(category=None, extension=None)
	# u'repellendus.jpg'

	fake.file_extension(category=None)
	# u'html'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'244.108.157.66'

	fake.url()
	# u'http://ferraro.net/'

	fake.company_email()
	# u'ibruno@damico.com'

	fake.uri()
	# u'http://martino.biz/tags/explore/category.html'

	fake.domain_word(*args, **kwargs)
	# u'de'

	fake.image_url(width=None, height=None)
	# u'https://placeholdit.imgix.net/~text?txtsize=55&txt=827\xd7248&w=827&h=248'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'vnegri@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'sed-libero-ut-quis'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'mariani-serra.org'

	fake.uri_extension()
	# u'.asp'

	fake.ipv6()
	# u'f90b:99b0:2e2e:fba6:478a:a3dc:2821:8139'

	fake.safe_email()
	# u'zmorelli@example.com'

	fake.user_name(*args, **kwargs)
	# u'ferrarimirko'

	fake.uri_path(deep=None)
	# u'wp-content'

	fake.email()
	# u'mirco96@gmail.com'

	fake.uri_page()
	# u'login'

	fake.mac_address()
	# u'd3:97:16:9b:76:d9'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Soil scientist'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Ad aliquid modi eos fugiat et. Ut illo molestias voluptatem error veniam. Quia corrupti accusantium quisquam et.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Est maxime et enim vero.'

	fake.word()
	# u'sint'

	fake.paragraphs(nb=3)
	# [   u'Accusantium vel cupiditate ipsam in quia eum. Quod adipisci explicabo nihil aut enim ratione id dolorem. Blanditiis minus ea laborum incidunt ut. Repudiandae id quod quis ipsum corporis.',
	#     u'Nisi sint et vel sit repudiandae earum. Et ab quibusdam id et non aut odit. Ut distinctio ipsam et ad quia ea non. Nemo blanditiis quis eos et itaque est.',
	#     u'Aliquam possimus molestias est voluptas voluptatibus. Incidunt unde fugiat assumenda tempora omnis impedit quidem. Nisi nihil et vero ipsum incidunt dolor. Vero quos asperiores quia repudiandae dolore accusamus.']

	fake.words(nb=3)
	# [u'voluptatem', u'et', u'provident']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Commodi sit natus rem vel et. Repudiandae reiciendis rem eum suscipit voluptas expedita. Voluptatem natus est et dolorum. Quo occaecati tempora voluptatem repudiandae et dolore.'

	fake.sentences(nb=3)
	# [   u'Minus est molestiae velit ut esse.',
	#     u'Cupiditate et doloremque et doloremque aut et odit pariatur.',
	#     u'Perferendis quia quia rerum quia magni maiores magni.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'(&5Wf!19Vz'

	fake.locale()
	# u'it_NZ'

	fake.md5(raw_output=False)
	# 'a6ebfc80d53cee250dc7c852ff03b479'

	fake.sha1(raw_output=False)
	# '257d7a76d52b68661e34df8235e28338d768fb9d'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '1273d1d1205d7fc5ab18418d0b2004d8eea995ed05ac4b7656cc56cd81486597'

	fake.uuid4()
	# 'aef9170d-c7d1-4f87-bc2d-f86f30a3ac0d'

	fake.language_code()
	# u'de'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Palumbo'

	fake.name_female()
	# u'Michael Moretti'

	fake.prefix_male()
	# u'Sig.'

	fake.prefix()
	# u'Dott.'

	fake.name()
	# u'Dott. Maria Rossi'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Sig. Liborio Bianco'

	fake.first_name()
	# u'Trevis'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Hector'

	fake.first_name_female()
	# u'Irene'

	fake.last_name_female()
	# u'Barbieri'

	fake.last_name()
	# u'Pellegrini'

	fake.prefix_female()
	# u'Sig.ra'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'+39 066 69 13 6430'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Canale Neri 30\nSan Gastone del friuli, 82050 Siena (LI)',
	#     'birthdate': '2013-04-06',
	#     'mail': u'martinizelida@yahoo.com',
	#     'name': u'Dott. Gioacchino Costantini',
	#     'sex': 'F',
	#     'username': u'ferrarabettino'}

	fake.profile(fields=None)
	# {   'address': u'Via Michael 468 Appartamento 45\nRossi veneto, 01490 Avellino (KR)',
	#     'birthdate': '1982-07-19',
	#     'blood_group': 'AB-',
	#     'company': u'Sanna e figli',
	#     'current_location': (Decimal('-9.7519985'), Decimal('175.490890')),
	#     'job': 'Investment banker, operational',
	#     'mail': u'antoninogreco@gmail.com',
	#     'name': u'Concetta Ferrara',
	#     'residence': u'Rotonda Vitali 38 Piano 6\nGallo laziale, 56831 Novara (BI)',
	#     'sex': 'F',
	#     'ssn': u'EHJHHI42N05K644V',
	#     'username': u'flavio55',
	#     'website': [u'http://www.esposito.com/', u'http://marini-montanari.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Perspiciatis dicta.',
	#     -6814874029723.0,
	#     u'Aliquid sint ipsam.',
	#     u'Nobis delectus.',
	#     102337.754453,
	#     u'Sunt est asperiores.',
	#     6669,
	#     1838,
	#     8847,
	#     u'demis29@barbieri.com',
	#     u'Voluptatem magni.',
	#     u'priscaferraro@yahoo.com')

	fake.pystr(max_chars=20)
	# u'Voluptas sit.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 488922650.3

	fake.pystruct(count=10, *value_types)
	# (   [   u'http://longo.com/wp-content/category/register/',
	#         datetime(1997, 4, 13, 1, 32, 13),
	#         5.84816507,
	#         u'Ex illum nam.',
	#         u'Accusamus sunt.',
	#         u'Molestiae non porro.',
	#         u'Asperiores cumque.',
	#         u'feliciacaruso@mancini.com',
	#         u'Tenetur non nihil.',
	#         38539908390141.8],
	#     {   u'delectus': datetime(1996, 2, 24, 4, 23, 24),
	#         u'molestias': Decimal('-6.70992970511E+13'),
	#         u'numquam': u'http://www.sartori.com/list/main/list/home/',
	#         u'omnis': datetime(1982, 7, 31, 21, 51, 38),
	#         u'quia': u'Voluptas rerum.',
	#         u'quis': Decimal('-2.37372111919E+13'),
	#         u'sapiente': datetime(2006, 5, 1, 0, 49, 17),
	#         u'sunt': u'Quas aut inventore.'},
	#     {   u'alias': {   3: u'http://www.vitali-pellegrini.biz/',
	#                       4: [   u'isira36@yahoo.com',
	#                              u'Consequuntur sit.',
	#                              datetime(2007, 11, 28, 16, 58, 35)],
	#                       5: {   3: -70761775503.6,
	#                              4: u'Officiis illo culpa.',
	#                              5: [   u'Vel nemo libero ab.',
	#                                     u'Sint sed omnis.']}},
	#         u'aut': {   7: u'Omnis iusto.',
	#                     8: [   u'http://www.morelli.com/search/app/privacy/',
	#                            u'Soluta quasi quo.',
	#                            u'Non quas.'],
	#                     9: {   7: u'Quibusdam.',
	#                            8: u'Amet eligendi.',
	#                            9: [u'Voluptas vel ut.', u'Est et nam.']}},
	#         u'ex': {   2: u'Cupiditate et ut.',
	#                    3: [u'Occaecati a sit.', 8234, 6137],
	#                    4: {   2: 6237,
	#                           3: u'Officiis id ipsa.',
	#                           4: [u'http://de.org/about/', -562808248923.0]}},
	#         u'nemo': {   9: u'sorrentinovitalba@yahoo.com',
	#                      10: [   Decimal('5.52552663421E+12'),
	#                              48054.8567,
	#                              u'barbierisarita@gmail.com'],
	#                      11: {   9: 8608,
	#                              10: Decimal('-4966.8252668'),
	#                              11: [   u'Quo minima.',
	#                                      Decimal('-368546.262091')]}},
	#         u'odit': {   8: 2521,
	#                      9: [   u'http://bellini.info/',
	#                             u'Aut nihil ut totam.',
	#                             u'morelligianmarco@conte.com'],
	#                      10: {   8: 6035,
	#                              9: u'serracaio@yahoo.com',
	#                              10: [u'Veniam sunt.', 2168]}},
	#         u'rerum': {   4: u'Aliquam corrupti.',
	#                       5: [   u'Sed quam assumenda.',
	#                              u'Sunt sequi quia et.',
	#                              642],
	#                       6: {   4: datetime(1979, 9, 7, 3, 44),
	#                              5: u'Et quibusdam.',
	#                              6: [u'Qui eum ducimus.', u'Quae tempore et.']}},
	#         u'tempore': {   5: 5074381401.777,
	#                         6: [u'Esse vel pariatur.', 1910, -95866.8],
	#                         7: {   5: u'Aut ut doloremque.',
	#                                6: u'http://russo-romano.biz/faq.htm',
	#                                7: [9499, u'Et assumenda harum.']}},
	#         u'voluptas': {   0: u'http://villa.com/app/search/explore/home.asp',
	#                          1: [   -75033959710928.0,
	#                                 u'Fugit ut nihil qui.',
	#                                 u'Dignissimos.'],
	#                          2: {   0: u'umberto60@vitali.com',
	#                                 1: 2220,
	#                                 2: [   u'Ex eos occaecati.',
	#                                        u'http://www.villa.com/']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('3021085.2')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'vaniavilla@hotmail.com',
	#     3112,
	#     924,
	#     u'Corrupti animi sed.',
	#     u'Ad voluptatibus.',
	#     7242,
	#     u'Minima sed nobis.',
	#     u'harrymazza@gmail.com',
	#     datetime(1997, 8, 21, 8, 17, 19),
	#     8016,
	#     Decimal('-47673537162.3')]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Eos eum autem nihil.',
	#     57615479677078.5,
	#     -49288360643.7642,
	#     -7666.71944221,
	#     461,
	#     u'Voluptas earum.',
	#     u'Earum ut debitis.',
	#     u'Qui sunt qui.')

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'Expedita laboriosam.', Decimal('8.992'), -6660.354848, 452, Decimal('115104831365'), datetime(2004, 12, 25, 10, 14, 51), u'Aperiam eum nulla.', 5900, Decimal('-742994410094'), datetime(1991, 11, 19, 6, 38, 37), u'Nemo similique.', u'ivanomariani@barone-battaglia.org'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'alias': u'contetazio@martinelli.info',
	#     u'consequatur': -8737.19,
	#     u'corporis': u'Nesciunt corporis.',
	#     u'ipsam': u'Dolor qui omnis.',
	#     u'qui': u'Optio accusamus.',
	#     u'quod': -5514181712609.51,
	#     u'velit': datetime(1983, 2, 15, 4, 0, 24)}

	fake.pyint()
	# 7409

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'RWSZHQ89H49N521Q'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_1; rv:1.9.4.20) Gecko/2015-09-03 18:31:41 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/8.20.(X11; Linux i686; sl-SI) Presto/2.9.162 Version/11.00'

	fake.windows_platform_token()
	# u'Windows NT 5.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows 98; Trident/4.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/5341 (KHTML, like Gecko) Chrome/15.0.840.0 Safari/5341'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_6) AppleWebKit/5322 (KHTML, like Gecko) Chrome/14.0.833.0 Safari/5322'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_8_1'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; en-US) AppleWebKit/533.3.1 (KHTML, like Gecko) Version/4.0.5 Mobile/8B115 Safari/6533.3.1'
