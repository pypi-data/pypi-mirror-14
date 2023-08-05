
Language pt_BR
===============

``faker.providers.address``
---------------------------

::

	fake.estado_nome()
	# u'Santa Catarina'

	fake.latitude()
	# Decimal('-1.3038005')

	fake.street_name()
	# u'Rua Ana L\xedvia Costela'

	fake.street_prefix()
	# u'Vale'

	fake.address()
	# u'Fazenda de Dias, 519\nS\xe3o Francisco\n02202-204 Carvalho Verde / CE'

	fake.street_address()
	# u'Vale Emilly Souza, 44'

	fake.bairro()
	# u'Nova Gameleira'

	fake.longitude()
	# Decimal('-176.121906')

	fake.country()
	# u'Suriname'

	fake.estado_sigla()
	# u'PR'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('173.813884')

	fake.estado()
	# (u'SE', u'Sergipe')

	fake.city_suffix()
	# u'Verde'

	fake.building_number()
	# u'17'

	fake.country_code()
	# u'LI'

	fake.city()
	# u'Cunha de Souza'

	fake.postcode()
	# u'12253-451'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'2483326673215'

	fake.ean13()
	# u'0214912118740'

	fake.ean8()
	# u'21209840'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(201,12,115)'

	fake.color_name()
	# u'LavenderBlush'

	fake.rgb_color_list()
	# (143, 209, 40)

	fake.rgb_color()
	# u'188,7,235'

	fake.safe_hex_color()
	# u'#665500'

	fake.safe_color_name()
	# u'purple'

	fake.hex_color()
	# u'#ee21aa'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Santos'

	fake.company_suffix()
	# u'Ltda.'

	fake.catch_phrase_verb()
	# u'de realizar seus sonhos'

	fake.catch_phrase()
	# u'A arte de avan\xe7ar com for\xe7a total'

	fake.catch_phrase_noun()
	# u'a arte'

	fake.catch_phrase_attribute()
	# u'direto da fonte'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'715'

	fake.credit_card_provider(card_type=None)
	# u'VISA 16 digit'

	fake.credit_card_full(card_type=None)
	# u'Discover\nDavi Lucca Melo\n6011904764140056 01/20\nCVC: 941\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '01/19'

	fake.credit_card_number(card_type=None)
	# u'210056606062600'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'SPL'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '25'

	fake.month()
	# '05'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 5, 17, 57, 4)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 38)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2010, 6, 28, 3, 55, 8)

	fake.time(pattern="%H:%M:%S")
	# '23:02:48'

	fake.year()
	# '1995'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1062, 1, 18, 2, 25, 40)

	fake.day_of_week()
	# 'Friday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 1, 12, 28)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 5, 14, 7, 28, 21)

	fake.unix_time()
	# 1389814081

	fake.month_name()
	# 'November'

	fake.timezone()
	# u'Asia/Hovd'

	fake.time_delta()
	# datetime.timedelta(15856, 52672)

	fake.century()
	# u'XIII'

	fake.date(pattern="%Y-%m-%d")
	# '1998-07-24'

	fake.iso8601(tzinfo=None)
	# '1978-03-04T15:25:54'

	fake.date_time(tzinfo=None)
	# datetime(1992, 1, 7, 9, 22, 30)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 6, 8, 1, 6, 53)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'multipart/mixed'

	fake.file_name(category=None, extension=None)
	# u'et.mp3'

	fake.file_extension(category=None)
	# u'mp3'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'73.145.188.122'

	fake.url()
	# u'http://pinto.br/'

	fake.company_email()
	# u'amanda49@melo.net'

	fake.uri()
	# u'http://www.ribeiro.br/'

	fake.domain_word(*args, **kwargs)
	# u'cunha'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/926x1005'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'vit\xf3ria34@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'officia-aliquam-in'

	fake.free_email_domain()
	# u'yahoo.com.br'

	fake.domain_name()
	# u'correia.net'

	fake.uri_extension()
	# u'.php'

	fake.ipv6()
	# u'2be5:ec6b:b28c:7f8d:cbf7:e0d0:0851:1642'

	fake.safe_email()
	# u'correiaana-sophia@example.br'

	fake.user_name(*args, **kwargs)
	# u'maria-clara88'

	fake.uri_path(deep=None)
	# u'categories'

	fake.email()
	# u'henrique72@uol.com.br'

	fake.uri_page()
	# u'faq'

	fake.mac_address()
	# u'4e:42:f0:af:fb:91'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Surveyor, quantity'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Ea minima aperiam debitis. Quam voluptatibus ut nemo aperiam. Illum ea sed harum autem.\nVeniam molestiae amet et. Velit repudiandae vitae molestiae. Sunt maxime non explicabo libero.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Beatae aliquam et consectetur quasi magnam qui amet.'

	fake.word()
	# u'voluptatibus'

	fake.paragraphs(nb=3)
	# [   u'Totam eos non qui quam fugit nemo. In pariatur voluptate similique optio. Recusandae ea autem ipsa sit. Id sed consequuntur ut.',
	#     u'Rerum quo repellendus dolorum et earum in. Laboriosam nobis sit assumenda numquam maxime deleniti. Et ipsa pariatur cumque assumenda cum pariatur ex. Blanditiis id nisi vitae et hic saepe.',
	#     u'Magnam placeat eligendi qui non sit. Odio voluptatem rem sunt corporis. Aspernatur sed maxime tenetur et nobis. Optio et quo maiores quo atque voluptatem et.']

	fake.words(nb=3)
	# [u'harum', u'totam', u'veniam']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Beatae odit alias ea minus inventore. Aliquid saepe esse blanditiis deleniti vero exercitationem. Aliquid quis dolorem facilis et.'

	fake.sentences(nb=3)
	# [   u'Ut voluptatem quam numquam.',
	#     u'Nobis quia sit aperiam recusandae est vero.',
	#     u'Qui dolor eligendi quis et.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'r0xE8N#q_s'

	fake.locale()
	# u'el_FJ'

	fake.md5(raw_output=False)
	# '00ba7fcc1322d74ab21ac09fe5980b9f'

	fake.sha1(raw_output=False)
	# '74c53d57d806f4cac73506b6015c04416bcaefba'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# '4072ce50cd12150ede6a40265ed96fd1dd8d23464eb1c7a6bab08a2c229e58bf'

	fake.uuid4()
	# 'f574802c-e10f-41d3-a7cc-f1b3c3d81351'

	fake.language_code()
	# u'en'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Barbosa'

	fake.name_female()
	# u'Agatha do Cunha'

	fake.prefix_male()
	# u'de'

	fake.prefix()
	# u'do'

	fake.name()
	# u'Luiz Gustavo Cunha'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Kaique Ferreira'

	fake.first_name()
	# u'Calebe'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Lorena'

	fake.first_name_female()
	# u'Leonardo'

	fake.last_name_female()
	# u'Ara\xfajo'

	fake.last_name()
	# u'Oliveira'

	fake.prefix_female()
	# u'do'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'41 9675 8443'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Estrada Isabelly Oliveira, 2\nMariano De Abreu\n53501426 Alves da Mata / AP',
	#     'birthdate': '2008-12-08',
	#     'mail': u'rodriguesjo\xe3o-miguel@bol.com.br',
	#     'name': u'Gabriel Melo',
	#     'sex': 'F',
	#     'username': u'la\xedsribeiro'}

	fake.profile(fields=None)
	# {   'address': u'Quadra Pereira, 73\nSanta Helena\n94253-178 Castro das Pedras / MG',
	#     'birthdate': '1973-06-17',
	#     'blood_group': '0+',
	#     'company': u'Correia',
	#     'current_location': (Decimal('46.153381'), Decimal('-17.174284')),
	#     'job': 'Insurance broker',
	#     'mail': u'alvesraul@bol.com.br',
	#     'name': u'Vitor Azevedo',
	#     'residence': u'Aeroporto Catarina Cunha\nCalafate\n68161195 Lima / TO',
	#     'sex': 'M',
	#     'ssn': u'37918260511',
	#     'username': u'ucunha',
	#     'website': [u'http://cunha.com/', u'http://silva.net/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('-3751594061.76'), u'fbarros@costela.net', -6315881368026.0, 3399, u'Nesciunt excepturi.', u'Nobis ipsa expedita.', Decimal('-329940845.0'), -29.143185650012, u'Veniam aliquam sunt.'])

	fake.pystr(max_chars=20)
	# u'Nostrum ipsam est.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -227614378.352

	fake.pystruct(count=10, *value_types)
	# (   [   Decimal('5028965530.48'),
	#         u'la\xeds36@hotmail.com',
	#         Decimal('9.15838040712E+14'),
	#         Decimal('-7.76133683'),
	#         38451307.1435105,
	#         u'Similique omnis aut.',
	#         -91467654.3321,
	#         u'Porro soluta.',
	#         datetime(1979, 2, 1, 19, 59, 3),
	#         -117.7570148363],
	#     {   u'animi': u'tcorreia@cardoso.net',
	#         u'at': datetime(2001, 2, 14, 12, 13, 55),
	#         u'dolor': datetime(1970, 1, 10, 14, 13, 57),
	#         u'eius': Decimal('600996780.182'),
	#         u'labore': u'Nostrum nemo dolore.',
	#         u'non': u'Consectetur laborum.',
	#         u'ratione': 8890,
	#         u'sit': u'bferreira@hotmail.com',
	#         u'veniam': u'Praesentium ut nisi.'},
	#     {   u'aliquam': {   8: datetime(1995, 12, 7, 2, 15, 45),
	#                         9: [   u'Beatae enim animi.',
	#                                405,
	#                                u'Sint et enim sed.'],
	#                         10: {   8: u'Quas consequuntur.',
	#                                 9: 7781,
	#                                 10: [   Decimal('-64687721.7934'),
	#                                         datetime(2000, 10, 4, 3, 2, 38)]}},
	#         u'atque': {   5: u'Eos explicabo.',
	#                       6: [   u'Eligendi sed quis.',
	#                              u'Ab ea esse tempora.',
	#                              u'Itaque qui mollitia.'],
	#                       7: {   5: u'castroigor@gomes.com',
	#                              6: u'Repellendus est.',
	#                              7: [9881766.729871, u'Omnis nulla maxime.']}},
	#         u'eaque': {   0: 9833,
	#                       1: [   u'Veritatis ad cum.',
	#                              Decimal('30.72885683'),
	#                              3233],
	#                       2: {   0: u'ara\xfajopedro-miguel@fernandes.br',
	#                              1: 97647924.24,
	#                              2: [   Decimal('787.760756705'),
	#                                     u'Veritatis sequi.']}},
	#         u'earum': {   2: u'Odio repellendus et.',
	#                       3: [   u'Et iusto nulla.',
	#                              2665,
	#                              datetime(1982, 9, 28, 7, 50, 58)],
	#                       4: {   2: Decimal('-39466.0'),
	#                              3: u'Est et quia soluta.',
	#                              4: [   datetime(1987, 6, 28, 15, 39, 26),
	#                                     -13219586553074.2]}},
	#         u'et': {   6: 3811,
	#                    7: [   u'Provident.',
	#                           u'http://santos.com/main/tags/homepage/',
	#                           8922],
	#                    8: {   6: -89314447506975.0,
	#                           7: 1759,
	#                           8: [u'Delectus corrupti.', 501]}},
	#         u'exercitationem': {   9: u'Ut fuga at maiores.',
	#                                10: [   datetime(2008, 8, 3, 17, 0, 25),
	#                                        553603569488015.0,
	#                                        u'Neque eos aut iste.'],
	#                                11: {   9: u'http://correia.br/homepage.asp',
	#                                        10: u'Et officia.',
	#                                        11: [   u'jo\xe3o-lucas22@oliveira.org',
	#                                                u'Sit molestias.']}},
	#         u'quia': {   3: 7679,
	#                      4: [   datetime(2015, 1, 17, 7, 1, 57),
	#                             7644811845.98,
	#                             u'Minima animi.'],
	#                      5: {   3: Decimal('-8.9439'),
	#                             4: u'Qui quos voluptas.',
	#                             5: [u'Saepe magnam.', u'Eos itaque et.']}},
	#         u'repellat': {   4: 7030.65736994,
	#                          5: [   u'http://www.cunha.net/index.php',
	#                                 u'http://www.santos.net/faq.html',
	#                                 6048],
	#                          6: {   4: 4683,
	#                                 5: -1456.975,
	#                                 6: [   u'Odit aut soluta qui.',
	#                                        u'icastro@ferreira.com']}},
	#         u'reprehenderit': {   1: 2389,
	#                               2: [   u'http://www.oliveira.com/posts/app/category.html',
	#                                      u'A velit provident.',
	#                                      Decimal('47.601176')],
	#                               3: {   1: Decimal('-5.73101931534E+12'),
	#                                      2: 4772,
	#                                      3: [   Decimal('-61882822.2526'),
	#                                             u'Et sunt odio.']}},
	#         u'ut': {   7: Decimal('196685.786'),
	#                    8: [   u'cunhacarolina@azevedo.br',
	#                           u'zgomes@ig.com.br',
	#                           u'http://www.castro.net/explore/categories/search/privacy/'],
	#                    9: {   7: -72758756316418.5,
	#                           8: u'Iste deleniti.',
	#                           9: [2271, Decimal('-23.111')]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-96122.6910692')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'Molestias doloribus.',
	#     u'Rerum nam error est.',
	#     u'Veritatis suscipit.',
	#     3372,
	#     datetime(2007, 1, 23, 5, 36, 43),
	#     u'http://www.cardoso.br/search/main/',
	#     Decimal('-4457053256.59'),
	#     u'http://www.azevedo.com/about/',
	#     u'Facilis quia.',
	#     u'Nulla amet maiores.',
	#     u'Beatae dignissimos.',
	#     datetime(2014, 4, 28, 12, 23, 46),
	#     datetime(1997, 7, 25, 14, 29, 21)]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   Decimal('-2.23265602584E+14'),
	#     u'isilva@costela.net',
	#     4962,
	#     u'http://gomes.br/faq.htm',
	#     u'http://www.alves.net/explore/tag/home.html',
	#     Decimal('1489.725'),
	#     7852,
	#     u'Ea quisquam.',
	#     54,
	#     u'brenosantos@fernandes.net')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('49133040.93'), u'santospedro@uol.com.br', u'gsouza@ig.com.br', 6827, u'pedro-lucas68@ara\xfajo.br', 8060, u'Aut debitis nemo.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'adipisci': u'Repellendus rerum.',
	#     u'aut': 1925,
	#     u'eum': u'Saepe delectus.',
	#     u'in': datetime(2004, 11, 1, 16, 37, 20),
	#     u'minima': u'Deserunt nihil.',
	#     u'mollitia': Decimal('39615152.7565'),
	#     u'nostrum': u'Quos qui aliquid.',
	#     u'officiis': 5164,
	#     u'omnis': u'http://cardoso.br/register.asp',
	#     u'quo': u'Similique dolor.',
	#     u'sunt': 6708,
	#     u'ut': datetime(1990, 7, 24, 0, 11, 30)}

	fake.pyint()
	# 7523

``faker.providers.ssn``
-----------------------

::

	fake.cpf()
	# u'689.017.452-67'

	fake.ssn()
	# u'60724319841'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Windows NT 5.2; sl-SI; rv:1.9.2.20) Gecko/2013-06-06 18:44:47 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/8.64.(Windows NT 5.1; sl-SI) Presto/2.9.169 Version/10.00'

	fake.windows_platform_token()
	# u'Windows NT 5.1'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/3.0)'

	fake.user_agent()
	# u'Opera/9.78.(Windows 98; en-US) Presto/2.9.167 Version/12.00'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7) AppleWebKit/5322 (KHTML, like Gecko) Chrome/15.0.874.0 Safari/5322'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; Intel Mac OS X 10_8_3'

	fake.safari()
	# u'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_7_0 rv:2.0; sl-SI) AppleWebKit/533.45.6 (KHTML, like Gecko) Version/5.0 Safari/533.45.6'
