
Language es_ES
===============

``faker.providers.address``
---------------------------

::

	fake.state_name()
	# u'C\xe1ceres'

	fake.latitude()
	# Decimal('-0.865788')

	fake.street_name()
	# u'Pasaje Felipe Ari\xf1o'

	fake.address()
	# u'Rambla Jordi Cabrero 902 Puerta 8 \nAlbacete, 62490'

	fake.street_address()
	# u'Via Magdalena Rueda 63'

	fake.postcode()
	# u'28355'

	fake.longitude()
	# Decimal('46.728158')

	fake.country()
	# u'Kirguist\xe1n'

	fake.secondary_address()
	# u'Piso 3'

	fake.street_prefix()
	# u'Camino'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('91.480587')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'1'

	fake.country_code()
	# u'EC'

	fake.city()
	# u'Le\xf3n'

	fake.state()
	# u'Badajoz'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'7245948622928'

	fake.ean13()
	# u'5311326288771'

	fake.ean8()
	# u'41083819'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(78,241,248)'

	fake.color_name()
	# u'Brown'

	fake.rgb_color_list()
	# (87, 49, 118)

	fake.rgb_color()
	# u'185,213,59'

	fake.safe_hex_color()
	# u'#11ff00'

	fake.safe_color_name()
	# u'fuchsia'

	fake.hex_color()
	# u'#d06f1d'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'R\xedos, Torrijos and Torrents'

	fake.company_suffix()
	# u'Ltd'

	fake.catch_phrase()
	# u'Innovative dedicated monitoring'

	fake.bs()
	# u'whiteboard bricks-and-clicks experiences'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'901'

	fake.credit_card_provider(card_type=None)
	# u'VISA 13 digit'

	fake.credit_card_full(card_type=None)
	# u'Mastercard\nAlejandra Belmonte\n5197271106749566 05/25\nCVV: 906\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '03/18'

	fake.credit_card_number(card_type=None)
	# u'4275482956186'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'EGP'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '17'

	fake.month()
	# '08'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 3, 53, 33)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1999, 5, 17, 2, 52, 5)

	fake.time(pattern="%H:%M:%S")
	# '09:46:05'

	fake.year()
	# '2011'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1188, 11, 14, 19, 54, 24)

	fake.day_of_week()
	# 'Wednesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 7, 7, 28)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2011, 8, 5, 11, 23, 57)

	fake.unix_time()
	# 865092860

	fake.month_name()
	# 'March'

	fake.timezone()
	# u'Europe/Tallinn'

	fake.time_delta()
	# datetime.timedelta(4330, 31794)

	fake.century()
	# u'XXI'

	fake.date(pattern="%Y-%m-%d")
	# '1986-06-24'

	fake.iso8601(tzinfo=None)
	# '2011-10-23T14:19:08'

	fake.date_time(tzinfo=None)
	# datetime(1975, 5, 27, 18, 20, 53)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2014, 8, 14, 16, 3, 25)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'audio/ogg'

	fake.file_name(category=None, extension=None)
	# u'est.mov'

	fake.file_extension(category=None)
	# u'avi'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'110.201.140.154'

	fake.url()
	# u'http://www.aguilar.com/'

	fake.company_email()
	# u'm\xf3nica34@sol\xeds.info'

	fake.uri()
	# u'http://cordero-ramis.net/'

	fake.domain_word(*args, **kwargs)
	# u'garmendia'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/313/319'

	fake.tld()
	# u'biz'

	fake.free_email()
	# u'inmaculada77@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'et-alias-dolor-et'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'carrillo-moraleda.org'

	fake.uri_extension()
	# u'.asp'

	fake.ipv6()
	# u'd954:b373:9029:726e:59df:51c6:3619:4a5b'

	fake.safe_email()
	# u'molesisabel@example.net'

	fake.user_name(*args, **kwargs)
	# u'iterr\xf3n'

	fake.uri_path(deep=None)
	# u'blog/posts/list'

	fake.email()
	# u'arellanoalejandro@vilalta.com'

	fake.uri_page()
	# u'index'

	fake.mac_address()
	# u'9d:18:a0:3d:e6:c4'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Secretary/administrator'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Reiciendis sit nemo asperiores ea iusto autem dolorum. Reprehenderit vel sed et asperiores totam necessitatibus rerum. Quidem enim illum deserunt omnis corporis.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Modi quis sint voluptate illum natus corrupti.'

	fake.word()
	# u'voluptas'

	fake.paragraphs(nb=3)
	# [   u'Aliquam fuga voluptatem enim dolore velit. Officiis quis sint et reprehenderit sapiente soluta qui. Eos inventore sed consequatur est quidem est. Sit laborum ut officiis deserunt tenetur.',
	#     u'Molestiae quasi sapiente distinctio occaecati voluptatem minima. Blanditiis et repellat odio quia. Fugit corrupti eos molestias a possimus enim. Doloremque aut doloremque distinctio rerum quaerat.',
	#     u'Voluptas blanditiis qui pariatur mollitia harum ut rerum. Aspernatur qui quia dolor numquam id fuga maxime. Culpa nemo omnis pariatur id explicabo aut reprehenderit. Eos odit quo omnis.']

	fake.words(nb=3)
	# [u'labore', u'in', u'quae']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Ipsam tempore voluptatem fugit voluptatum. Exercitationem voluptatibus sit et ipsum est et quia. Aperiam qui consectetur ipsum consequatur aut. Vel vel doloribus quo consequuntur voluptatem aspernatur.'

	fake.sentences(nb=3)
	# [   u'Aut aut enim et.',
	#     u'Corrupti alias a nobis est enim.',
	#     u'A sit eius rerum velit optio veritatis autem.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'2tFaxUqt$U'

	fake.locale()
	# u'de_SE'

	fake.md5(raw_output=False)
	# 'a0354f0276824a35aa24198168b3566a'

	fake.sha1(raw_output=False)
	# '6209bee54e393c66f443ab6801db52ac8a6929c6'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '1fd308df35b8883460a6f7ca5e0c2459fc9ad28006506ae3da91c68b241af916'

	fake.uuid4()
	# '9c7156db-e225-4942-9424-d4a4f63ee92e'

	fake.language_code()
	# u'cn'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Rubio'

	fake.name_female()
	# u'Patricia Ba\xf1os Morata'

	fake.prefix_male()
	# u'del'

	fake.prefix()
	# u'del'

	fake.name()
	# u'Elisa Pintor-Navarrete'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Enrique Barba Zabaleta'

	fake.first_name()
	# u'Mar\xeda'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Guillermo'

	fake.first_name_female()
	# u'Natalia'

	fake.last_name_female()
	# u'Ben\xedtez'

	fake.last_name()
	# u'Acevedo'

	fake.prefix_female()
	# u'de'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'+34 502485920'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Callej\xf3n de Albert Ar\xe9valo 3 Piso 5 \nPontevedra, 97005',
	#     'birthdate': '1974-07-07',
	#     'mail': u'emiliagil@hotmail.com',
	#     'name': u'Gonzalo Jose Angel Sastre Nieto',
	#     'sex': 'M',
	#     'username': u'joaquin74'}

	fake.profile(fields=None)
	# {   'address': u'Cuesta de Roberto Rosado 6 Apt. 67 \nAlicante, 13453',
	#     'birthdate': '2004-05-07',
	#     'blood_group': 'B-',
	#     'company': u'Pino LLC',
	#     'current_location': (Decimal('78.1850205'), Decimal('-102.266913')),
	#     'job': 'Magazine features editor',
	#     'mail': u'antoniob\xe1rcena@hotmail.com',
	#     'name': u'Magdalena Navarrete Lopez',
	#     'residence': u'Urbanizaci\xf3n Patricia Gordillo 93 Piso 1 \nVizcaya, 37120',
	#     'sex': 'F',
	#     'ssn': u'044-89-1752',
	#     'username': u'quir\xf3ssonia',
	#     'website': [   u'http://atienza-osuna.com/',
	#                    u'http://calleja.com/',
	#                    u'http://ribas-artigas.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'Omnis vero nobis.', u'Unde est quasi.', u'adriana86@falc\xf3.com', Decimal('48.692155619'), u'qtoledo@catal\xe1-arnaiz.com', u'Repudiandae fuga.', u'Hic culpa quia.', u'http://www.ugarte.info/category/', u'Dolores voluptatem.', Decimal('4.76387498211E+12')])

	fake.pystr(max_chars=20)
	# u'Temporibus dolores.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -3366146683671.0

	fake.pystruct(count=10, *value_types)
	# (   [   datetime(1988, 7, 23, 13, 19, 23),
	#         u'Quia voluptates.',
	#         u'suredajosefa@pareja.info',
	#         u'http://www.garriga.com/',
	#         u'ismael21@guzman.com',
	#         u'Rerum inventore.',
	#         datetime(1992, 10, 28, 21, 41, 50),
	#         u'Esse temporibus.',
	#         244,
	#         u'Et neque ut quia.'],
	#     {   u'ad': u'iayala@jara-laguna.com',
	#         u'dolorem': -2674840127.12,
	#         u'doloribus': 83,
	#         u'et': 7433537225.8522,
	#         u'facilis': -84.7,
	#         u'impedit': datetime(1973, 11, 5, 23, 9, 46),
	#         u'quia': u'Earum sapiente.',
	#         u'quibusdam': u'http://www.cabrera.com/terms.html',
	#         u'similique': 959949.56,
	#         u'ut': u'patriciapizarro@yahoo.com'},
	#     {   u'aperiam': {   4: 8506,
	#                         5: [   datetime(1980, 3, 18, 12, 48, 22),
	#                                8001,
	#                                u'Dolore voluptatum.'],
	#                         6: {   4: u'Totam architecto.',
	#                                5: 7365,
	#                                6: [u'Repudiandae id.', u'Voluptatum.']}},
	#         u'eos': {   5: 63067456388.572,
	#                     6: [   u'Voluptatem.',
	#                            datetime(2014, 6, 24, 21, 23, 3),
	#                            7195],
	#                     7: {   5: 6910, 6: u'Quo optio quis.', 7: [9376, 6285]}},
	#         u'error': {   0: u'Voluptas dolor.',
	#                       1: [   u'http://rico.com/post.htm',
	#                              Decimal('8583561.4'),
	#                              -3088654510971.4],
	#                       2: {   0: u'adri\xe1n25@soto.net',
	#                              1: 1164,
	#                              2: [   u'joaquinbastida@yahoo.com',
	#                                     u'Et molestiae et qui.']}},
	#         u'et': {   2: u'Qui vero debitis.',
	#                    3: [   u'http://www.iglesias.biz/search.html',
	#                           u'Praesentium itaque.',
	#                           datetime(1985, 10, 31, 1, 24, 54)],
	#                    4: {   2: u'Ex sapiente et.',
	#                           3: 7628,
	#                           4: [   Decimal('333145173.283'),
	#                                  datetime(1981, 8, 7, 17, 29, 6)]}},
	#         u'expedita': {   9: 4106,
	#                          10: [   datetime(1992, 8, 30, 5, 48, 2),
	#                                  datetime(1974, 2, 16, 6, 32, 14),
	#                                  u'Consequatur.'],
	#                          11: {   9: datetime(2011, 2, 20, 23, 21, 38),
	#                                  10: Decimal('-6.7645'),
	#                                  11: [800, u'Et asperiores.']}},
	#         u'molestiae': {   3: -94894.0,
	#                           4: [   u'Soluta doloribus.',
	#                                  datetime(1976, 12, 17, 17, 30, 59),
	#                                  u'Eaque ipsa fuga est.'],
	#                           5: {   3: -787380269680393.0,
	#                                  4: u'Molestias non.',
	#                                  5: [1865, 9292]}},
	#         u'occaecati': {   7: datetime(2003, 1, 6, 1, 54, 8),
	#                           8: [   Decimal('-78858606.4419'),
	#                                  2246,
	#                                  datetime(1999, 10, 30, 2, 57, 26)],
	#                           9: {   7: u'lourdesmadrigal@yahoo.com',
	#                                  8: datetime(1991, 1, 19, 20, 18, 47),
	#                                  9: [   u'Eaque unde velit.',
	#                                         u'Ea dolor illo.']}},
	#         u'odio': {   6: datetime(1988, 6, 7, 2, 0, 47),
	#                      7: [   3.242255112,
	#                             u'http://pedraza.com/',
	#                             Decimal('-2087385102.7')],
	#                      8: {   6: u'Culpa iure voluptas.',
	#                             7: 4409,
	#                             8: [   u'Est voluptatem.',
	#                                    u'http://galvez-sobrino.com/post/']}},
	#         u'totam': {   1: 1619,
	#                       2: [   u'Qui quo qui.',
	#                              u'Adipisci qui omnis.',
	#                              u'Autem earum labore.'],
	#                       3: {   1: u'Voluptas ut rerum.',
	#                              2: u'mnicol\xe1s@gaya.net',
	#                              3: [   u'sandrapardo@gmail.com',
	#                                     Decimal('-3.81688495247E+12')]}},
	#         u'voluptas': {   8: u'Impedit debitis ea.',
	#                          9: [   4001,
	#                                 u'nerea49@hotmail.com',
	#                                 u'lbriones@hotmail.com'],
	#                          10: {   8: u'Harum sed excepturi.',
	#                                  9: u'Ut et numquam.',
	#                                  10: [5759, u'Eos in laudantium.']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('4824.92018029')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   4712,
	#     u'Nihil ad optio.',
	#     u'Tempora omnis enim.',
	#     u'Cupiditate quisquam.',
	#     datetime(1970, 3, 29, 8, 19, 43),
	#     u'http://www.mariscal.org/tag/categories/blog/privacy.html',
	#     u'http://alc\xe1zar.com/login.asp',
	#     6647,
	#     u'Molestiae voluptas.',
	#     6285,
	#     u'Sunt eos et facilis.',
	#     u'Possimus qui.',
	#     u'http://www.palmer.com/']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   datetime(1987, 3, 21, 18, 12, 42),
	#     -2241252351.55253,
	#     u'Cum delectus omnis.',
	#     5190,
	#     datetime(2005, 6, 21, 0, 11, 11),
	#     u'Consectetur eaque.',
	#     u'http://quintana.com/login/',
	#     Decimal('-600488682931'),
	#     u'Nesciunt non.',
	#     -3283819.0,
	#     u'Doloribus dolor et.',
	#     860,
	#     8703)

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([7611, -75369696885.283, 8.0, u'Molestiae maiores.', Decimal('-8.9897'), u'Voluptatem incidunt.', u'Tenetur molestias.', u'Dolor sint omnis.', 6464915.438911, 3278, 399])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'accusamus': u'http://www.sanjuan.com/category/main/categories/privacy.html',
	#     u'animi': datetime(1984, 11, 20, 14, 16, 26),
	#     u'consequuntur': 2637,
	#     u'deserunt': 40998180421.0,
	#     u'excepturi': 8160,
	#     u'in': datetime(2013, 3, 15, 22, 29, 36),
	#     u'iste': u'http://gimenez.info/search/posts/list/index.php',
	#     u'itaque': -9329691.7618,
	#     u'minus': Decimal('-1139333.92'),
	#     u'optio': datetime(1998, 11, 4, 21, 53, 59),
	#     u'quaerat': datetime(1982, 2, 7, 8, 27, 58),
	#     u'quo': 1902,
	#     u'sit': u'torrentmarina@arag\xf3n-garcia.com',
	#     u'voluptatibus': -99724300.826}

	fake.pyint()
	# 2451

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'486-52-2229'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:1.9.2.20) Gecko/2015-11-26 20:28:28 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/8.25.(Windows 98; Win 9x 4.90; it-IT) Presto/2.9.184 Version/11.00'

	fake.windows_platform_token()
	# u'Windows 95'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90; Trident/3.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_6; rv:1.9.4.20) Gecko/2011-10-17 18:32:52 Firefox/3.6.13'

	fake.chrome()
	# u'Mozilla/5.0 (Windows 98) AppleWebKit/5312 (KHTML, like Gecko) Chrome/15.0.828.0 Safari/5312'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_5_1'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; it-IT) AppleWebKit/533.39.2 (KHTML, like Gecko) Version/3.0.5 Mobile/8B112 Safari/6533.39.2'
