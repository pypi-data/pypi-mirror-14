
Language fr_FR
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('46.8441685')

	fake.department_number()
	# u'45'

	fake.street_name()
	# u'chemin Barbier'

	fake.address()
	# u'boulevard Pruvost\n04301 Labbe-sur-Bertrand'

	fake.department_name()
	# u'Dr\xf4me'

	fake.street_address()
	# u'avenue de Carlier'

	fake.postcode()
	# u'38 921'

	fake.longitude()
	# Decimal('-96.711774')

	fake.country()
	# u'Finlande'

	fake.street_prefix()
	# u'avenue'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('153.303289')

	fake.city_suffix()
	# u'-la-For\xeat'

	fake.building_number()
	# u'8'

	fake.country_code()
	# u'MK'

	fake.region()
	# u'Champagne-Ardenne'

	fake.city()
	# u'CousinVille'

	fake.department()
	# (u'29', u'Finist\xe8re')

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'0595228438402'

	fake.ean13()
	# u'8271558530345'

	fake.ean8()
	# u'36743421'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(23,110,249)'

	fake.color_name()
	# u'GreenYellow'

	fake.rgb_color_list()
	# (239, 114, 112)

	fake.rgb_color()
	# u'250,73,237'

	fake.safe_hex_color()
	# u'#000000'

	fake.safe_color_name()
	# u'blue'

	fake.hex_color()
	# u'#480945'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Boutin'

	fake.company_suffix()
	# u'et Fils'

	fake.catch_phrase_verb()
	# u'de rouler'

	fake.catch_phrase()
	# u"L'assurance de concr\xe9tiser vos projets avant-tout"

	fake.catch_phrase_noun()
	# u'la simplicit\xe9'

	fake.siren()
	# u'014 463 050'

	fake.siret(max_sequential_digits=2)
	# u'407 643 817 00835'

	fake.catch_phrase_attribute()
	# u'sans soucis'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'490'

	fake.credit_card_provider(card_type=None)
	# u'VISA 16 digit'

	fake.credit_card_full(card_type=None)
	# u'American Express\nLaurent Alexandre\n372524088004857 03/24\nCID: 6794\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '08/25'

	fake.credit_card_number(card_type=None)
	# u'5392762734918725'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'UZS'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '12'

	fake.month()
	# '01'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 10, 54, 37)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2002, 11, 15, 15, 42, 44)

	fake.time(pattern="%H:%M:%S")
	# '06:10:04'

	fake.year()
	# '2008'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1391, 7, 21, 21, 12, 4)

	fake.day_of_week()
	# 'Friday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 22, 5, 37)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 4, 16, 2, 57, 26)

	fake.unix_time()
	# 29434562

	fake.month_name()
	# 'April'

	fake.timezone()
	# u'Africa/Bissau'

	fake.time_delta()
	# datetime.timedelta(874, 69031)

	fake.century()
	# u'XX'

	fake.date(pattern="%Y-%m-%d")
	# '2007-10-28'

	fake.iso8601(tzinfo=None)
	# '1987-07-19T12:40:58'

	fake.date_time(tzinfo=None)
	# datetime(1998, 6, 12, 14, 47, 47)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 5, 2, 0, 5, 24)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'multipart/alternative'

	fake.file_name(category=None, extension=None)
	# u'nihil.flac'

	fake.file_extension(category=None)
	# u'wav'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'226.61.129.77'

	fake.url()
	# u'http://meyer.fr/'

	fake.company_email()
	# u'verdierclaude@adam.fr'

	fake.uri()
	# u'http://payet.fr/privacy.php'

	fake.domain_word(*args, **kwargs)
	# u'gonzalez'

	fake.image_url(width=None, height=None)
	# u'https://placeholdit.imgix.net/~text?txtsize=55&txt=0\xd7130&w=0&h=130'

	fake.tld()
	# u'net'

	fake.free_email()
	# u'josephst\xe9phanie@bouygtel.fr'

	fake.slug(*args, **kwargs)
	# u'repellendus-et'

	fake.free_email_domain()
	# u'orange.fr'

	fake.domain_name()
	# u'lefevre.net'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'fad5:0331:00a9:7310:2c5a:1b64:ca56:976a'

	fake.safe_email()
	# u'st\xe9phanebodin@example.fr'

	fake.user_name(*args, **kwargs)
	# u'colettegrenier'

	fake.uri_path(deep=None)
	# u'main/posts/posts'

	fake.email()
	# u'uboulanger@laposte.net'

	fake.uri_page()
	# u'category'

	fake.mac_address()
	# u'6a:9d:cc:36:c0:70'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Restaurant manager, fast food'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Aliquam quis molestias sunt eveniet enim quis dolor amet. Aut nam et dolorum et ut et incidunt architecto. Minus sequi explicabo ea. Cum recusandae ipsam aut rerum dignissimos.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Numquam velit harum et autem.'

	fake.word()
	# u'atque'

	fake.paragraphs(nb=3)
	# [   u'Ea eos earum ut dolor et sapiente. Repudiandae ab et quos sit dolor rerum. Architecto reprehenderit aut non neque. Eveniet omnis ut sit nemo magni ut rem.',
	#     u'Qui voluptatum excepturi magni soluta. Consectetur consequuntur fuga et cupiditate. Harum autem dolorem voluptatem voluptatem officia doloribus. Facilis quia est earum dignissimos praesentium non dolor.',
	#     u'Aut accusantium quod repellat aspernatur laborum. Tenetur numquam enim ex et non quisquam maxime beatae. Odit accusamus et at ratione.']

	fake.words(nb=3)
	# [u'similique', u'illum', u'et']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Aut voluptatem minima nisi voluptates voluptas. Ullam maiores quos et odit est ullam quis. In et numquam animi. Quia ipsa quia quos dolor nisi quia possimus.'

	fake.sentences(nb=3)
	# [   u'Beatae laudantium cupiditate eos voluptas sint.',
	#     u'Et suscipit velit ipsa porro qui maxime.',
	#     u'Expedita fuga quis tempore itaque non odit quaerat.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'(s7!JpS8B%'

	fake.locale()
	# u'ru_DM'

	fake.md5(raw_output=False)
	# '321e151170a4fe8245aae7dfc5925b1f'

	fake.sha1(raw_output=False)
	# '139e2d580a706d0d3978c416cc88560e1cdc972a'

	fake.null_boolean()
	# None

	fake.sha256(raw_output=False)
	# 'e7aa2fcc2c632a33b9bc032db28a6bf1271ee8bc1a7162c79c8b6365670e6e8d'

	fake.uuid4()
	# '650e76f2-1c17-4846-b80a-8d65505fa0bc'

	fake.language_code()
	# u'ru'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Techer'

	fake.name_female()
	# u'Oc\xe9ane Potier'

	fake.prefix_male()
	# u'du'

	fake.prefix()
	# u'de'

	fake.name()
	# u'Thibaut Leclercq'

	fake.suffix_female()
	# ''

	fake.name_male()
	# u'Joseph Baron de Bourgeois'

	fake.first_name()
	# u'Christiane'

	fake.suffix_male()
	# ''

	fake.suffix()
	# ''

	fake.first_name_male()
	# u'Arthur'

	fake.first_name_female()
	# u'Diane'

	fake.last_name_female()
	# u'Barre'

	fake.last_name()
	# u'Breton'

	fake.prefix_female()
	# u'Le'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'08 12 13 86 68'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'743, boulevard \xc9mile Blondel\n06 330 Jourdan-sur-Gautier',
	#     'birthdate': '1993-06-11',
	#     'mail': u'menardsuzanne@ifrance.com',
	#     'name': u'Mich\xe8le Buisson',
	#     'sex': 'F',
	#     'username': u'shernandez'}

	fake.profile(fields=None)
	# {   'address': u'38, avenue Ledoux\n31962 Foucher',
	#     'birthdate': '1992-08-15',
	#     'blood_group': 'A+',
	#     'company': u'Boulay',
	#     'current_location': (Decimal('11.559848'), Decimal('-63.269621')),
	#     'job': 'Mudlogger',
	#     'mail': u'lacombephilippe@wanadoo.fr',
	#     'name': u'Sabine-Hortense Carre',
	#     'residence': u'8, rue Joubert\n62 539 Techer',
	#     'sex': 'F',
	#     'ssn': u'105-96-1007',
	#     'username': u'xvallee',
	#     'website': [   u'http://nicolas.fr/',
	#                    u'http://www.verdier.org/',
	#                    u'http://charles.fr/',
	#                    u'http://www.toussaint.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'da-silvadoroth\xe9e@yahoo.fr',
	#     u'Repudiandae ipsam.',
	#     -95755892.2954,
	#     1368,
	#     u'Nostrum omnis ut.',
	#     u'Animi reiciendis.',
	#     u'Odio accusantium.',
	#     u'http://maillet.net/privacy/']

	fake.pystr(max_chars=20)
	# u'Sit eveniet facilis.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 2647.300885

	fake.pystruct(count=10, *value_types)
	# (   [   datetime(1992, 7, 26, 13, 37, 35),
	#         u'Illum sit iusto.',
	#         u'Velit minima.',
	#         5225,
	#         u'Voluptate doloribus.',
	#         datetime(2002, 5, 12, 4, 3, 2),
	#         u'http://fournier.org/tag/search/register.htm',
	#         8834,
	#         2068,
	#         6352],
	#     {   u'at': 8810,
	#         u'eaque': 3012,
	#         u'est': u'Itaque et autem.',
	#         u'excepturi': u'pagesmaryse@tele2.fr',
	#         u'explicabo': u'http://www.leduc.org/',
	#         u'impedit': u'http://www.pascal.com/list/search.html',
	#         u'molestias': 6217,
	#         u'praesentium': datetime(1981, 7, 19, 12, 22, 4),
	#         u'quisquam': u'Esse ex facilis et.',
	#         u'totam': 6312},
	#     {   u'cupiditate': {   6: 1768,
	#                            7: [   u'allardbrigitte@orange.fr',
	#                                   u'Odit tenetur.',
	#                                   u'Consequatur et et.'],
	#                            8: {   6: u'Culpa pariatur.',
	#                                   7: Decimal('-1.65070388245'),
	#                                   8: [u'Alias est aut et.', 4793]}},
	#         u'dolorem': {   8: 3371,
	#                         9: [   u'http://www.vaillant.fr/app/search/tags/author.asp',
	#                                -75097370.87163,
	#                                u'Tempore voluptas ut.'],
	#                         10: {   8: 7957,
	#                                 9: 69684751.96,
	#                                 10: [1963, 804.632185515]}},
	#         u'ea': {   3: datetime(2001, 3, 9, 8, 31, 37),
	#                    4: [   u'Vitae laborum nihil.',
	#                           Decimal('8.5126932045E+12'),
	#                           2657],
	#                    5: {   3: 301,
	#                           4: 4504,
	#                           5: [   u'http://www.bonneau.fr/wp-content/explore/post.html',
	#                                  728106583.65]}},
	#         u'eaque': {   2: 4636,
	#                       3: [   u'Eaque vel est neque.',
	#                              4729,
	#                              Decimal('-75.64531')],
	#                       4: {   2: 3235327.76751,
	#                              3: Decimal('765328281447'),
	#                              4: [   datetime(2001, 7, 6, 5, 27, 46),
	#                                     u'Sed minus.']}},
	#         u'id': {   9: u'Et deleniti et.',
	#                    10: [   u'http://www.de.org/explore/tags/category.html',
	#                            datetime(1985, 4, 6, 15, 4, 12),
	#                            3685],
	#                    11: {   9: u'http://noel.fr/',
	#                            10: u'Rerum tempora quia.',
	#                            11: [2354, 428.7234]}},
	#         u'nihil': {   7: 2655,
	#                       8: [u'Veritatis quo.', 1399, -3.0],
	#                       9: {   7: u'Aut error.',
	#                              8: u'Deserunt occaecati.',
	#                              9: [2448, u'http://gosselin.net/post.php']}},
	#         u'omnis': {   0: Decimal('1587023.77'),
	#                       1: [5007, Decimal('2718.97'), 6431],
	#                       2: {   0: 9554,
	#                              1: 8794,
	#                              2: [-54434829.0, u'Necessitatibus.']}},
	#         u'sed': {   4: datetime(1987, 10, 25, 6, 3, 19),
	#                     5: [   u'Ut excepturi iste.',
	#                            4929,
	#                            Decimal('57013653.8755')],
	#                     6: {   4: Decimal('-30225654187.3'),
	#                            5: 4843,
	#                            6: [u'Et voluptatem rem.', 4409]}},
	#         u'sequi': {   1: u'http://www.da.fr/',
	#                       2: [   u'http://www.gauthier.net/app/wp-content/homepage.htm',
	#                              1877,
	#                              977],
	#                       3: {   1: u'Ut consequuntur.',
	#                              2: u'Molestiae culpa.',
	#                              3: [5298, u'Eos in harum et.']}},
	#         u'sit': {   5: 8309440.3836,
	#                     6: [   2490,
	#                            Decimal('-59330762.66'),
	#                            u'Rerum debitis qui.'],
	#                     7: {   5: u'Nihil commodi nam.',
	#                            6: u'Earum velit.',
	#                            7: [u'http://martins.fr/about/', 663]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('299004.58')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   datetime(1976, 2, 6, 15, 18, 32),
	#     datetime(1981, 9, 23, 1, 47, 7),
	#     u'Necessitatibus id.',
	#     u'Voluptates sed.',
	#     u'Quia aperiam ad.',
	#     u'moulingr\xe9goire@descamps.org',
	#     5075,
	#     u'kleroy@dbmail.com',
	#     5529,
	#     datetime(1971, 4, 4, 21, 6, 35)]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Dolor omnis ab et.',
	#     9145330545.43,
	#     u'Qui ullam eius sed.',
	#     datetime(1974, 7, 30, 14, 14, 6),
	#     u'http://pons.com/main/',
	#     u'Laboriosam.',
	#     u'Qui id sunt sit.',
	#     u'http://arnaud.org/author.htm')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'Nesciunt sequi.', u'alicenormand@boulay.org', datetime(1998, 9, 29, 11, 52, 5), u'http://www.antoine.com/wp-content/category.asp', u'Et sed ut possimus.', u'Dolor eos.', datetime(1971, 9, 15, 20, 56, 34), 8281, u'grocher@laposte.net'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'asperiores': datetime(1992, 4, 26, 10, 16, 3),
	#     u'est': u'Et maiores maxime.',
	#     u'ex': 9124,
	#     u'in': u'Ut incidunt illo.',
	#     u'mollitia': Decimal('-9.8480486372E+12'),
	#     u'porro': datetime(2005, 3, 25, 18, 52, 37),
	#     u'veritatis': u'Voluptate magnam.'}

	fake.pyint()
	# 4550

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'044-09-5424'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Windows NT 5.01; it-IT; rv:1.9.1.20) Gecko/2012-06-27 09:05:29 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.37.(Windows NT 6.1; it-IT) Presto/2.9.179 Version/10.00'

	fake.windows_platform_token()
	# u'Windows NT 5.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 9.0; Windows 98; Trident/5.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5340 (KHTML, like Gecko) Chrome/14.0.874.0 Safari/5340'

	fake.chrome()
	# u'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_8_3) AppleWebKit/5321 (KHTML, like Gecko) Chrome/14.0.839.0 Safari/5321'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; Intel Mac OS X 10_8_5'

	fake.safari()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7 rv:2.0; sl-SI) AppleWebKit/534.43.4 (KHTML, like Gecko) Version/4.0.3 Safari/534.43.4'
