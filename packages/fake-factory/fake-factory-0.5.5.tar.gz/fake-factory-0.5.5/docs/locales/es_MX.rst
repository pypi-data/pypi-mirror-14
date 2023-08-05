
Language es_MX
===============

``faker.providers.address``
---------------------------

::

	fake.state_abbr()
	# u'SON'

	fake.latitude()
	# Decimal('-86.527668')

	fake.street_name()
	# u'Peatonal Hungr\xeda'

	fake.address()
	# u'Avenida Lara 280 Edif. 646 , Depto. 427\nVieja Om\xe1n, GTO 54060-8446'

	fake.street_address()
	# u'Callej\xf3n Campeche 319 Edif. 000 , Depto. 183'

	fake.postcode()
	# u'38750-0973'

	fake.longitude()
	# Decimal('105.262090')

	fake.country()
	# u'Islas Marshall'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('148.295880')

	fake.secondary_address()
	# u'524 Interior 191'

	fake.street_prefix()
	# u'Boulevard'

	fake.street_suffix()
	# u'Street'

	fake.city_prefix()
	# u'Norte'

	fake.city_suffix()
	# u'los bajos'

	fake.building_number()
	# u'975'

	fake.country_code()
	# u'LB'

	fake.city_adjetive()
	# u'Vieja'

	fake.city()
	# u'Nueva Bhut\xe1n'

	fake.state()
	# u'Distrito Federal'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'4226852421619'

	fake.ean13()
	# u'7200085165813'

	fake.ean8()
	# u'35246152'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(62,96,38)'

	fake.color_name()
	# u'Crimson'

	fake.rgb_color_list()
	# (252, 124, 61)

	fake.rgb_color()
	# u'115,180,254'

	fake.safe_hex_color()
	# u'#662200'

	fake.safe_color_name()
	# u'white'

	fake.hex_color()
	# u'#ac4189'

``faker.providers.company``
---------------------------

::

	fake.company_suffix()
	# u'y Asociados'

	fake.company()
	# u'Proyectos Espino-\xc1vila'

	fake.company_prefix()
	# u'Industrias'

	fake.catch_phrase()
	# u'inteligencia artificial incremental visionario'

	fake.bs()
	# u'mejora sistemas inal\xe1mbrica'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'835'

	fake.credit_card_provider(card_type=None)
	# u'JCB 15 digit'

	fake.credit_card_full(card_type=None)
	# u'Voyager\nFelipe de Anda\n869918114535571 09/16\nCVC: 131\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '02/25'

	fake.credit_card_number(card_type=None)
	# u'4783561291770127'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'YER'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '24'

	fake.month()
	# '11'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 3, 22, 13, 15)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1990, 2, 10, 16, 49, 45)

	fake.time(pattern="%H:%M:%S")
	# '03:47:57'

	fake.year()
	# '2008'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(176, 12, 13, 22, 7, 39)

	fake.day_of_week()
	# 'Wednesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 3, 3, 31, 7)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 8, 22, 18, 47, 22)

	fake.unix_time()
	# 896461384

	fake.month_name()
	# 'June'

	fake.timezone()
	# u'Europe/Chisinau'

	fake.time_delta()
	# datetime.timedelta(2535, 66499)

	fake.century()
	# u'VI'

	fake.date(pattern="%Y-%m-%d")
	# '2006-02-20'

	fake.iso8601(tzinfo=None)
	# '1985-09-15T17:24:52'

	fake.date_time(tzinfo=None)
	# datetime(1995, 11, 4, 16, 45, 7)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 8, 23, 20, 52, 42)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'model/iges'

	fake.file_name(category=None, extension=None)
	# u'est.mp4'

	fake.file_extension(category=None)
	# u'flac'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'100.236.87.134'

	fake.url()
	# u'http://www.proyectos.com/'

	fake.company_email()
	# u'celia11@laboy.com'

	fake.uri()
	# u'http://www.molina.com/wp-content/main/'

	fake.domain_word(*args, **kwargs)
	# u'rosales'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/280x497'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'curielyeni@gmail.com'

	fake.slug(*args, **kwargs)
	# u'sequi-est-fugit'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'montoya.net'

	fake.uri_extension()
	# u'.htm'

	fake.ipv6()
	# u'b026:a37f:20c8:7cbb:8a55:37d0:40fe:4063'

	fake.safe_email()
	# u'bpuente@example.com'

	fake.user_name(*args, **kwargs)
	# u'isabel90'

	fake.uri_path(deep=None)
	# u'blog/category/tag'

	fake.email()
	# u'colladocornelio@despacho.net'

	fake.uri_page()
	# u'privacy'

	fake.mac_address()
	# u'd7:c8:ae:7f:43:8f'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Recycling officer'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Rerum voluptas ab non nisi omnis. Placeat doloribus earum iste et. Quia debitis ex occaecati quis. Similique rerum nulla id maxime.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Aut a enim exercitationem aut rerum neque omnis cupiditate.'

	fake.word()
	# u'et'

	fake.paragraphs(nb=3)
	# [   u'Quos praesentium et quod optio veniam porro iste et. Sunt aut voluptatem non nesciunt sit velit. Repellat ut voluptatem ad laborum magni odit. Tenetur praesentium est fuga nihil.',
	#     u'Consequatur laborum omnis porro ea dolorem tempora accusantium. Pariatur impedit nihil autem. Ut non iste enim consequatur fuga. Deleniti repudiandae molestias quam cupiditate et qui aperiam.',
	#     u'Hic corrupti quis voluptas aut. Blanditiis et suscipit voluptas rerum. Facere laborum omnis et nam magnam.']

	fake.words(nb=3)
	# [u'et', u'quis', u'dicta']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Autem ipsam et error vel. Dolorem nostrum asperiores doloremque et eum. Magnam vel voluptatum dolorum adipisci quibusdam voluptas.'

	fake.sentences(nb=3)
	# [   u'Voluptate aut debitis maiores quibusdam nulla placeat magnam nulla.',
	#     u'Placeat qui ipsa odit aut doloribus maiores maxime.',
	#     u'At et aut ducimus sit quam.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'8jXU3iSg5('

	fake.locale()
	# u'de_CA'

	fake.md5(raw_output=False)
	# 'f35725f37c3ec3978ebc2e884c8e743a'

	fake.sha1(raw_output=False)
	# '393e6ab48aacd50a0ed7719e2ed6b44991cc32f0'

	fake.null_boolean()
	# False

	fake.sha256(raw_output=False)
	# '0a60edfb28cd6771068e2439f3d1b5231aa8e2feda9f93439bc6e6045241b17b'

	fake.uuid4()
	# '5533911b-fcb8-41ae-acbe-bba8cb51b5f6'

	fake.language_code()
	# u'fr'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Vera'

	fake.name_female()
	# u'Ing. Gilberto Salgado'

	fake.prefix_male()
	# u'Sr(a).'

	fake.prefix()
	# u'Dr.'

	fake.name()
	# u'Judith Elizondo'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Dr. Flavio Montenegro'

	fake.first_name()
	# u'Alicia'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Celia'

	fake.first_name_female()
	# u'Pascual'

	fake.last_name_female()
	# u'Cepeda'

	fake.last_name()
	# u'Fierro'

	fake.prefix_female()
	# u'Ing.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'05049446181'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Prolongaci\xf3n Guanajuato 427 Edif. 487 , Depto. 966\nNueva Chile, OAX 62332-1283',
	#     'birthdate': '1973-11-09',
	#     'mail': u'tlebr\xf3n@hotmail.com',
	#     'name': u'Miriam Alvarado Fajardo',
	#     'sex': 'M',
	#     'username': u'mgranados'}

	fake.profile(fields=None)
	# {   'address': u'Circuito Sur Baeza 992 987\nNueva Polonia, VER 15963',
	#     'birthdate': '2015-06-19',
	#     'blood_group': 'A+',
	#     'company': u'Club D\xe1vila y Arevalo',
	#     'current_location': (Decimal('52.2607515'), Decimal('-76.885324')),
	#     'job': 'Firefighter',
	#     'mail': u'barbarabueno@gmail.com',
	#     'name': u'Ra\xfal Garay Pedroza',
	#     'residence': u'Andador Quintana Roo 343 Edif. 926 , Depto. 102\nNueva Etiop\xeda, MOR 69699-6021',
	#     'sex': 'M',
	#     'ssn': u'150-85-0973',
	#     'username': u'waponte',
	#     'website': [   u'http://tafoya.info/',
	#                    u'http://laboy.biz/',
	#                    u'http://pab\xf3n.net/',
	#                    u'http://anguiano-valadez.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'Sint quaerat autem.',
	#     -16529601268.31,
	#     u'Sed sed magni.',
	#     68126306.7,
	#     u'Quasi delectus ut.',
	#     u'Consequatur quia.',
	#     u'Distinctio.']

	fake.pystr(max_chars=20)
	# u'Totam laudantium.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 31619233.9

	fake.pystruct(count=10, *value_types)
	# (   [   u'Magnam repudiandae.',
	#         u'Et itaque aut.',
	#         u'Laudantium ducimus.',
	#         0.672034240539,
	#         Decimal('-560324.0'),
	#         u'Sint facilis ut.',
	#         u'http://despacho.com/privacy/',
	#         u'mitzy67@balderas.com',
	#         u'Magnam sit ut vel.',
	#         6386],
	#     {   u'asperiores': -810958428.35,
	#         u'culpa': u'http://olivares.com/category/list/search.html',
	#         u'doloremque': Decimal('-34.2257205203'),
	#         u'dolores': -5.398467798,
	#         u'eius': u'Suscipit tenetur.',
	#         u'facilis': u'Eos quos dolorum.',
	#         u'magni': u'http://garza.com/terms/',
	#         u'minima': Decimal('-72.129'),
	#         u'non': u'Nisi aliquid autem.',
	#         u'vel': u'Natus sit nihil.'},
	#     {   u'at': {   1: u'Veritatis hic quia.',
	#                    2: [   u'Sint facere quod.',
	#                           -749.394704,
	#                           u'Qui ea corrupti.'],
	#                    3: {   1: u'http://becerra-montoya.com/',
	#                           2: u'Sit quia ea illum.',
	#                           3: [u'Quibusdam tempora.', u'Et voluptatem.']}},
	#         u'aut': {   3: u'Sed facere.',
	#                     4: [   u'http://www.alonzo.com/tag/home.php',
	#                            u'Et aliquid odio.',
	#                            -79647.7142439],
	#                     5: {   3: datetime(2013, 11, 19, 10, 42, 9),
	#                            4: 3506,
	#                            5: [   u'jmu\xf1oz@orellana-villanueva.com',
	#                                   u'Nulla velit ut.']}},
	#         u'commodi': {   7: u'Qui commodi culpa.',
	#                         8: [   Decimal('49940964.0'),
	#                                u'Veritatis et qui.',
	#                                u'Alias et nihil.'],
	#                         9: {   7: 1685,
	#                                8: datetime(1997, 6, 29, 14, 11, 24),
	#                                9: [   u'Minima a voluptas.',
	#                                       datetime(1976, 10, 19, 18, 11, 34)]}},
	#         u'consequuntur': {   4: u'http://navarro.com/',
	#                              5: [   u'Ducimus amet beatae.',
	#                                     u'http://www.club.com/home.html',
	#                                     u'Eligendi facilis.'],
	#                              6: {   4: 9518,
	#                                     5: 7840,
	#                                     6: [   datetime(2003, 8, 18, 18, 2, 39),
	#                                            datetime(1986, 8, 10, 6, 49, 22)]}},
	#         u'et': {   8: datetime(2009, 2, 10, 13, 38, 41),
	#                    9: [   u'Sed excepturi quis.',
	#                           Decimal('-3.1334103551E+13'),
	#                           u'Quisquam expedita.'],
	#                    10: {   8: 6157,
	#                            9: 5421,
	#                            10: [datetime(2012, 8, 14, 7, 33, 17), 5698]}},
	#         u'id': {   5: u'http://www.due\xf1as-holgu\xedn.com/list/wp-content/about/',
	#                    6: [   u'http://rico.com/tag/blog/app/register/',
	#                           u'http://grupo.com/login/',
	#                           u'http://www.soto.com/post.php'],
	#                    7: {   5: u'Fuga saepe non quia.',
	#                           6: u'orozcominerva@balderas.com',
	#                           7: [   u'Laudantium tempora.',
	#                                  u'padillaeloy@hotmail.com']}},
	#         u'repudiandae': {   2: u'http://ledesma.com/tags/main/search.html',
	#                             3: [   datetime(1972, 10, 9, 5, 32, 28),
	#                                    u'Delectus voluptates.',
	#                                    Decimal('2409404526.7')],
	#                             4: {   2: u'http://corporativo.com/login/',
	#                                    3: u'http://reyna-espinal.com/category/',
	#                                    4: [   u'Ex dolorem nobis.',
	#                                           u'http://www.curiel.com/category/tags/tag/index.html']}},
	#         u'ut': {   9: 9154,
	#                    10: [   Decimal('768033.704'),
	#                            Decimal('61186480548.8'),
	#                            9812370.9],
	#                    11: {   9: u'Necessitatibus.',
	#                            10: 8481,
	#                            11: [   u'http://lara-rol\xf3n.info/',
	#                                    datetime(1970, 8, 3, 11, 35, 41)]}},
	#         u'vel': {   0: u'Ipsa harum amet qui.',
	#                     1: [   Decimal('71756297.2'),
	#                            datetime(1974, 6, 7, 3, 58, 50),
	#                            5646],
	#                     2: {   0: u'Tempore est.',
	#                            1: u'Voluptates odit.',
	#                            2: [   u'http://industrias.net/about.htm',
	#                                   799217407644.6]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('300447.3088')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   5336,
	#     9283,
	#     u'Aut unde eos dolor.',
	#     Decimal('-4957427454.0'),
	#     -570202.90359,
	#     u'http://n\xfa\xf1ez.com/about.html',
	#     u'Recusandae quo quod.',
	#     u'Veritatis ipsam.',
	#     Decimal('6092238.0'),
	#     datetime(2008, 12, 15, 9, 27, 34),
	#     88]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Sit et in dolore.',
	#     68,
	#     u'Ut et iste dolor.',
	#     1993,
	#     u'http://www.industrias.com/author/',
	#     9633631323694.29,
	#     u'Temporibus.',
	#     u'Ex sed dolorem.',
	#     u'Culpa earum est.',
	#     8309,
	#     Decimal('9.41903126255E+14'),
	#     u'Qui est facere.',
	#     Decimal('83885383.1997'))

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([3940, datetime(2011, 8, 7, 18, 35, 50), u'Et perferendis odit.', u'http://rinc\xf3n-quintana.org/post.php', 1710, u'Atque beatae et.', u'Architecto et nisi.', datetime(2012, 5, 19, 23, 51, 2), u'http://www.corona.net/privacy.php', datetime(2005, 1, 27, 11, 56, 49)])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'aperiam': u'ur\xedasvanesa@hotmail.com',
	#     u'autem': 97608493892.3,
	#     u'dignissimos': 9758,
	#     u'fugiat': u'Quis sint eos enim.',
	#     u'qui': u'Labore esse quasi.',
	#     u'quia': 7219,
	#     u'quo': u'http://www.pantoja-parra.biz/tags/main/category/',
	#     u'reprehenderit': u'Porro aperiam esse.',
	#     u'sint': 5856,
	#     u'sunt': datetime(1973, 10, 6, 13, 48, 7)}

	fake.pyint()
	# 5785

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'789-08-1716'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/2013-09-13 10:58:44 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/8.71.(X11; Linux x86_64; en-US) Presto/2.9.187 Version/10.00'

	fake.windows_platform_token()
	# u'Windows NT 4.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Win 9x 4.90; Trident/4.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (Windows; U; Windows NT 4.0) AppleWebKit/531.13.3 (KHTML, like Gecko) Version/5.0.1 Safari/531.13.3'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5330 (KHTML, like Gecko) Chrome/13.0.883.0 Safari/5330'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; Intel Mac OS X 10_8_1'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_0 like Mac OS X; en-US) AppleWebKit/535.38.1 (KHTML, like Gecko) Version/3.0.5 Mobile/8B118 Safari/6535.38.1'
