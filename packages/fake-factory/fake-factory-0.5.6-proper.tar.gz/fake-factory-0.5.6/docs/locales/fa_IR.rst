
Language fa_IR
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('74.0483345')

	fake.street_name()
	# u'\u067e\u0631\u06cc\u0627 \u0645\u06cc\u062f\u0627\u0646'

	fake.address()
	# u'7890 \u0631\u0647\u0627 \u062f\u0631\u0647\ne, \u0627\u0631\u062f\u0628\u06cc\u0644 2052381236'

	fake.street_address()
	# u'58494 \u062f\u0627\u062f\u0641\u0631 \u0628\u0644\u0648\u0627\u0631'

	fake.postcode()
	# u'087884'

	fake.longitude()
	# Decimal('-106.962199')

	fake.country()
	# u'\u0633\u0646 \u0645\u0627\u0631\u06cc\u0646\u0648'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-125.754129')

	fake.secondary_address()
	# u'\u0648\u0627\u062d\u062f 793'

	fake.street_suffix()
	# u'\u06a9\u0648\u0686\u0647'

	fake.city_prefix()
	# u'\u0634\u0645\u0627\u0644'

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'0879'

	fake.country_code()
	# u'BI'

	fake.city()
	# u'{'

	fake.state()
	# u'\u06a9\u0647\u06af\u06cc\u0644\u0648\u06cc\u0647 \u0648 \u0628\u0648\u06cc\u0631\u0627\u062d\u0645\u062f'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'1619875298680'

	fake.ean13()
	# u'5814282775748'

	fake.ean8()
	# u'78786516'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(133,165,158)'

	fake.color_name()
	# u'MistyRose'

	fake.rgb_color_list()
	# (41, 105, 175)

	fake.rgb_color()
	# u'74,87,219'

	fake.safe_hex_color()
	# u'#ccdd00'

	fake.safe_color_name()
	# u'green'

	fake.hex_color()
	# u'#cbc0f3'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\u0633\u06cc\u0645\u0627\u0646 \u0628\u0648\u0647\u0631\u0648\u06a9 \u06cc\u0632\u062f'

	fake.company_suffix()
	# u'Ltd'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'405'

	fake.credit_card_provider(card_type=None)
	# u'JCB 15 digit'

	fake.credit_card_full(card_type=None)
	# u'Maestro\n\u0646\u0631\u06af\u0633 \u0646\u0648\u0628\u062e\u062a\u06cc\n503827197180 04/16\nCVV: 589\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '07/21'

	fake.credit_card_number(card_type=None)
	# u'4663525985835'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'GEL'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '24'

	fake.month()
	# '08'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 1, 18, 36, 43)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1992, 1, 12, 8, 35, 2)

	fake.time(pattern="%H:%M:%S")
	# '09:21:19'

	fake.year()
	# '1983'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1202, 10, 21, 5, 2, 53)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 4, 20, 7, 15)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2014, 1, 5, 17, 58, 55)

	fake.unix_time()
	# 555973971

	fake.month_name()
	# 'November'

	fake.timezone()
	# u'Pacific/Ponape'

	fake.time_delta()
	# datetime.timedelta(13370, 58791)

	fake.century()
	# u'XXI'

	fake.date(pattern="%Y-%m-%d")
	# '1996-07-13'

	fake.iso8601(tzinfo=None)
	# '2010-03-18T01:35:41'

	fake.date_time(tzinfo=None)
	# datetime(1982, 10, 13, 20, 27, 19)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 7, 20, 0, 3, 41)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'video/ogg'

	fake.file_name(category=None, extension=None)
	# u'aliquid.mov'

	fake.file_extension(category=None)
	# u'xls'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'48.194.123.183'

	fake.url()
	# u'http://\u067e\u062f\u064a\u062f\u0647.net/'

	fake.company_email()
	# u'\u0632\u0646\u062c\u0627\u0646\u06cc\u0622\u0631\u06cc\u0646@\u0632\u0631\u06cc\u0646.ir'

	fake.uri()
	# u'http://www.\u0633\u0631\u0645\u0627\u064a\u0647.org/privacy/'

	fake.domain_word(*args, **kwargs)
	# u'\u06a9\u0634\u0627\u0648\u0631\u0632\u06cc'

	fake.image_url(width=None, height=None)
	# u'http://www.lorempixel.com/738/472'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'\u0622\u062a\u0646\u0627\u0645\u0639\u06cc\u0646@gmail.com'

	fake.slug(*args, **kwargs)
	# u'aut-quisquam-totam'

	fake.free_email_domain()
	# u'yahoo.com'

	fake.domain_name()
	# u'\u062a\u0648\u0644\u064a\u062f\u064a.org'

	fake.uri_extension()
	# u'.php'

	fake.ipv6()
	# u'9856:c88d:784d:9286:9f37:a328:7cae:5269'

	fake.safe_email()
	# u'\u0633\u062c\u0627\u062f57@example.ir'

	fake.user_name(*args, **kwargs)
	# u'\u0631\u06cc\u062d\u0627\u0646\u064729'

	fake.uri_path(deep=None)
	# u'tags'

	fake.email()
	# u'a\u0632\u0627\u0631\u0639\u06cc@\u0645\u06af\u0633\u0627\u0644.net'

	fake.uri_page()
	# u'home'

	fake.mac_address()
	# u'e3:1c:38:19:6d:7e'

``faker.providers.job``
-----------------------

::

	fake.job()
	# u'\u062c\u0631\u0627\u062d'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Dolore maxime mollitia qui. Dolor qui et molestiae asperiores.\nPorro omnis id veritatis. Aut vitae dolore quibusdam atque saepe rem.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Deleniti sed nemo omnis.'

	fake.word()
	# u'quam'

	fake.paragraphs(nb=3)
	# [   u'Iure quo quo aut debitis a rem eum. Quis soluta dignissimos ut ipsam praesentium. Enim nesciunt occaecati sit ea. Est id beatae quas rerum quas quos alias.',
	#     u'Occaecati et nulla id corrupti velit quisquam explicabo. Dignissimos tempora maiores est ratione repellat adipisci commodi. Sunt aut nostrum laborum quia explicabo exercitationem omnis sint.',
	#     u'Qui ut perferendis laudantium consequatur laborum possimus quisquam. Magni dolore consequatur sunt qui tempore. Veritatis quasi cupiditate quia rerum sed labore saepe. Mollitia mollitia delectus magnam adipisci eum natus eaque ratione.']

	fake.words(nb=3)
	# [u'architecto', u'placeat', u'aut']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Voluptates rerum vitae porro rerum. Veniam iusto pariatur expedita sequi nobis ea et.'

	fake.sentences(nb=3)
	# [   u'Aut est deleniti autem modi at.',
	#     u'Dolorem soluta ducimus ullam possimus sed qui.',
	#     u'Veritatis illum sint totam voluptatibus esse voluptas.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'tQ65mEztB#'

	fake.locale()
	# u'es_ZW'

	fake.md5(raw_output=False)
	# '62693f699f3815e04fd403c626636be1'

	fake.sha1(raw_output=False)
	# 'ba2748a852b86b1a137964b9bd322cb94ac6b5f8'

	fake.null_boolean()
	# False

	fake.sha256(raw_output=False)
	# '77a7bce7b915fb9610065402dd6f12b5af2d0ae58243c259739ce48c4f4cf32d'

	fake.uuid4()
	# 'dd40811c-7f45-403f-9f7e-9d57d30c2854'

	fake.language_code()
	# u'pt'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u0638\u0641\u0631\u06cc'

	fake.name_female()
	# u'\u0633\u0631\u06a9\u0627\u0631 \u062e\u0627\u0646\u0645 \u062f\u06a9\u062a\u0631 \u0633\u0627\u0631\u06cc\u0646\u0627 \u0631\u0628\u0627\u0646\u06cc '

	fake.prefix_male()
	# u'\u062c\u0646\u0627\u0628 \u0622\u0642\u0627\u06cc'

	fake.prefix()
	# u'\u0633\u0631\u06a9\u0627\u0631 \u062e\u0627\u0646\u0645 \u062f\u06a9\u062a\u0631'

	fake.name()
	# u'\u0633\u0631\u06a9\u0627\u0631 \u062e\u0627\u0646\u0645 \u062f\u06a9\u062a\u0631 \u06cc\u0627\u0633\u0645\u06cc\u0646 \u0644\u0627\u0647\u0648\u062a\u06cc '

	fake.suffix_female()
	# u''

	fake.name_male()
	# u'\u0645\u062d\u0645\u062f\u067e\u0627\u0631\u0633\u0627 \u0639\u0628\u0627\u0633\u06cc '

	fake.first_name()
	# u'\u0622\u0631\u0645\u06cc\u0646'

	fake.suffix_male()
	# u''

	fake.suffix()
	# u''

	fake.first_name_male()
	# u'\u0627\u0645\u06cc\u0631\u0645\u0647\u062f\u06cc'

	fake.first_name_female()
	# u'\u0645\u0647\u0633\u0627'

	fake.last_name_female()
	# u'\u0633\u0639\u06cc\u062f\u06cc'

	fake.last_name()
	# u'\u0631\u0641\u06cc\u0639\u06cc'

	fake.prefix_female()
	# u'\u0633\u0631\u06a9\u0627\u0631 \u062e\u0627\u0646\u0645'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'+98 21 9404 5228'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'2012 \u062a\u0646\u0632\u06cc\u0644\u06cc \u06a9\u0648\u0647\nn, \u0627\u0644\u0628\u0631\u0632 818840',
	#     'birthdate': '1981-12-09',
	#     'mail': u'\u0627\u0634\u0631\u0641\u06cc\u0628\u0646\u06cc\u0627\u0645\u06cc\u0646@gmail.com',
	#     'name': u'\u0645\u0627\u0626\u062f\u0647 \u0633\u0631\u062e\u0648\u0634\u06cc\u0627\u0646',
	#     'sex': 'F',
	#     'username': u'\u0622\u06cc\u062f\u0627\u0645\u0647\u062f\u06cc\u0627\u0646'}

	fake.profile(fields=None)
	# {   'address': u'160 \u0646\u0648\u0631\u06cc \u0628\u0644\u0648\u0627\u0631\ni, \u0642\u0645 4598915691',
	#     'birthdate': '1983-06-24',
	#     'blood_group': '0+',
	#     'company': u'\u062a\u0648\u0644\u064a\u062f\u064a \u0645\u0631\u062a\u0628',
	#     'current_location': (Decimal('43.8167085'), Decimal('44.705914')),
	#     'job': u'\u0622\u0647\u0646\u06af\u0631',
	#     'mail': u'\u0645\u0639\u0635\u0648\u0645\u0647\u067e\u0648\u06cc\u0627\u0646@hotmail.com',
	#     'name': u'\u0646\u0631\u06af\u0633 \u06cc\u0632\u062f\u06cc ',
	#     'residence': u'94493 \u0639\u0631\u0641\u0627\u0646 \u062a\u0648\u0646\u0644\ni, \u0627\u0635\u0641\u0647\u0627\u0646 0872393830',
	#     'sex': 'F',
	#     'ssn': u'177-20-9569',
	#     'username': u'\u062b\u0646\u0627\u067e\u0627\u0631\u0633\u0627',
	#     'website': [   u'http://www.\u0630\u0648\u0628.com/',
	#                    u'http://www.\u0628\u0627\u0646\u06a9.com/',
	#                    u'http://\u062f\u0648\u062f\u0647.ir/',
	#                    u'http://\u0635\u0646\u0639\u062a\u064a.ir/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   7564,
	#     u'Est est sit alias.',
	#     7429,
	#     u'Velit facere.',
	#     4591,
	#     u'Quae quia dolor.',
	#     Decimal('355392883763')]

	fake.pystr(max_chars=20)
	# u'Rem quo voluptas.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -35.5379753699717

	fake.pystruct(count=10, *value_types)
	# (   [   8670,
	#         1019,
	#         7346,
	#         u'\u0645\u062d\u0645\u062f\u0631\u0636\u0627\u0631\u0648\u062f\u06af\u0631@\u062a\u062c\u0647\u064a\u0632.com',
	#         u'Aliquid quaerat.',
	#         6467,
	#         u'\u062c\u0639\u0641\u0631-\u067e\u0648\u0631\u0627\u0645\u06cc\u0631\u062d\u0633\u06cc\u0646@chmail.ir',
	#         4779,
	#         4000,
	#         -2611356081.6],
	#     {   u'enim': -8353783756493.0,
	#         u'et': -851611.7215948,
	#         u'expedita': 2945,
	#         u'nobis': 6872,
	#         u'possimus': -99690525149.6,
	#         u'quas': datetime(1989, 5, 22, 16, 33, 59),
	#         u'quia': u'Laudantium possimus.',
	#         u'tempore': u'http://\u0635\u0646\u0627\u064a\u0639.org/homepage/',
	#         u'ut': u'Laboriosam aut sit.',
	#         u'vitae': u'http://www.\u062c\u0647\u0627\u0646.com/homepage.html'},
	#     {   u'blanditiis': {   4: 9865,
	#                            5: [   u'Necessitatibus.',
	#                                   u'Corporis autem eum.',
	#                                   u'Voluptate et eos.'],
	#                            6: {   4: u'h\u0631\u0636\u0627-\u0632\u0627\u062f\u0647@\u062a\u0648\u0644\u06cc\u062f\u06cc.ir',
	#                                   5: 355553639.5556,
	#                                   6: [   Decimal('-2.02878845405E+13'),
	#                                          Decimal('2.82989713109E+14')]}},
	#         u'et': {   6: u'Nam dolores.',
	#                    7: [   u'Rerum facere quod.',
	#                           u'http://www.\u06af\u0631\u0648\u0647.ir/search/',
	#                           datetime(2015, 6, 23, 11, 57, 31)],
	#                    8: {   6: u'\u0622\u0648\u0627\u0646\u0648\u0631\u06cc@gmail.com',
	#                           7: u'http://www.\u0642\u0646\u062f.ir/homepage.html',
	#                           8: [u'Blanditiis sint.', u'Omnis autem rerum.']}},
	#         u'magni': {   0: u'http://\u0635\u0646\u0639\u062a\u06cc.net/',
	#                       1: [2190, 4651, Decimal('-8.24241692862E+13')],
	#                       2: {   0: u'http://\u062f\u0627\u0631\u0648\u0633\u0627\u0632\u06cc.com/list/categories/blog/author/',
	#                              1: 7375,
	#                              2: [   datetime(1997, 3, 12, 14, 11, 39),
	#                                     datetime(1984, 3, 8, 6, 32, 22)]}},
	#         u'perferendis': {   1: u'Laudantium neque.',
	#                             2: [   u'\u0645\u062d\u0645\u062f\u067e\u0627\u0631\u0633\u062752@\u0622\u062c\u0631.ir',
	#                                    datetime(1983, 12, 6, 12, 57, 39),
	#                                    u'Provident.'],
	#                             3: {   1: u'\u0632\u06cc\u0646\u0628\u0639\u0632\u06cc\u0632\u06cc@\u0633\u0631\u0645\u0627\u064a\u0647.com',
	#                                    2: Decimal('-542327028.9'),
	#                                    3: [   u'Explicabo labore.',
	#                                           u'\u0633\u0645\u0627\u0648\u0627\u062a\u0628\u0646\u06cc\u0627\u0645\u06cc\u0646@\u0646\u0633\u0627\u062c\u06cc.org']}},
	#         u'quas': {   2: u'Dicta similique.',
	#                      3: [   u'Explicabo et.',
	#                             u'Dolor non.',
	#                             u'c\u062f\u0627\u062f\u0641\u0631@\u06af\u0631\u0648\u0647.org'],
	#                      4: {   2: u'http://\u0633\u06cc\u0645\u0627\u0646.org/',
	#                             3: datetime(2004, 1, 24, 9, 33, 52),
	#                             4: [1845555.92, u'Voluptatem ipsa.']}},
	#         u'qui': {   9: datetime(1972, 12, 12, 18, 1, 18),
	#                     10: [   8921,
	#                             u'Libero et facilis.',
	#                             datetime(2007, 9, 3, 14, 59, 41)],
	#                     11: {   9: 518,
	#                             10: u'\u06cc\u06af\u0627\u0646\u0647\u0638\u0641\u0631\u06cc@mailfa.com',
	#                             11: [   u'Autem soluta id aut.',
	#                                     u'http://\u067e\u0627\u0631\u0633.com/category.asp']}},
	#         u'ut': {   5: u'Enim atque hic.',
	#                    6: [   u'Modi error totam.',
	#                           u'\u0645\u062d\u0645\u062f\u062d\u0633\u06cc\u064639@\u06af\u0631\u0648\u0647.com',
	#                           u'\u0645\u06cc\u0631\u062f\u0627\u0645\u0627\u062f\u06cc\u0645\u0644\u06cc\u0643\u0627@\u0628\u0633\u062a\u0647.org'],
	#                    7: {   5: 6641.69944,
	#                           6: Decimal('1.03058545123E+12'),
	#                           7: [u'Eos et aut.', u'Sunt temporibus.']}},
	#         u'vel': {   3: 8588,
	#                     4: [   u'Soluta deserunt et.',
	#                            48728140350210.9,
	#                            datetime(1987, 4, 6, 1, 3, 13)],
	#                     5: {   3: 6580,
	#                            4: datetime(1994, 8, 30, 15, 31, 41),
	#                            5: [   u'Omnis dolor et.',
	#                                   datetime(1970, 1, 7, 4, 16, 57)]}},
	#         u'voluptas': {   7: u'Ab numquam maiores.',
	#                          8: [   u'Ea voluptatem sequi.',
	#                                 u'Omnis voluptas.',
	#                                 2217],
	#                          9: {   7: u'Omnis distinctio.',
	#                                 8: 471838.347161784,
	#                                 9: [Decimal('-593386.119'), 3776]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('4666081.9623')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   datetime(1976, 12, 5, 18, 16, 53),
	#     u'Ut perspiciatis.',
	#     u'Est rem quisquam.',
	#     4018,
	#     u'Perspiciatis fuga.',
	#     7846,
	#     -309363023.648,
	#     Decimal('-504355100015'),
	#     3272]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Ipsam pariatur.',
	#     u'Quis nesciunt dolor.',
	#     2216,
	#     u'Molestiae rem qui.',
	#     u'Sunt veritatis quod.',
	#     8107,
	#     7592,
	#     u'Illo odio aut quia.',
	#     u'Sed voluptates.',
	#     datetime(2003, 9, 11, 17, 4, 34),
	#     -54783.3,
	#     6200732.0,
	#     datetime(2007, 4, 8, 7, 56, 8),
	#     datetime(2007, 8, 7, 21, 39, 46))

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'http://www.\u062a\u0648\u0644\u064a\u062f\u064a.com/faq.html', Decimal('3659120004.75'), datetime(1993, 8, 9, 6, 16, 35), u'Consequuntur.', u'http://\u0633\u06cc\u0645\u0627\u0646.ir/category/category/main.htm', u'Nesciunt incidunt.', u'http://\u0635\u0646\u0627\u064a\u0639.ir/tags/terms/', 1364, u'Occaecati ducimus.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'ad': u'\u0632\u0646\u062c\u0627\u0646\u06cc\u0622\u06cc\u0644\u06cc\u0646@\u062a\u062c\u0627\u0631\u06cc.org',
	#     u'dignissimos': u'http://\u0628\u0627\u0646\u06a9.ir/category/',
	#     u'enim': u'Saepe qui provident.',
	#     u'hic': datetime(2015, 2, 12, 17, 13, 58),
	#     u'inventore': 6726,
	#     u'ipsum': 6961,
	#     u'mollitia': Decimal('-34066548.53'),
	#     u'repellat': Decimal('8963902.27732'),
	#     u'repudiandae': 245395718602.14,
	#     u'soluta': u'http://\u06af\u0631\u0648\u0647.com/categories/list/post/',
	#     u'sunt': u'Possimus voluptatem.'}

	fake.pyint()
	# 8799

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'519-41-7115'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Windows NT 5.1; it-IT; rv:1.9.0.20) Gecko/2011-01-23 08:29:36 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.22.(X11; Linux x86_64; sl-SI) Presto/2.9.184 Version/12.00'

	fake.windows_platform_token()
	# u'Windows NT 5.1'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 6.0; Windows CE; Trident/3.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 6.2; Trident/3.1)'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5320 (KHTML, like Gecko) Chrome/13.0.844.0 Safari/5320'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_6_4'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1 like Mac OS X; it-IT) AppleWebKit/534.40.2 (KHTML, like Gecko) Version/3.0.5 Mobile/8B116 Safari/6534.40.2'
