
Language cs_CZ
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('37.0161615')

	fake.street_name()
	# u'Sliveneck\xe1'

	fake.address()
	# u'Mezilesn\xed 1/9\n062 55 Kostelec nad Labem'

	fake.street_address()
	# u'Weilova 973'

	fake.postcode()
	# u'290 92'

	fake.longitude()
	# Decimal('-73.922540')

	fake.country()
	# u'Kyrgyzst\xe1n'

	fake.city_name()
	# u'Nov\xe9 Hrady'

	fake.street_suffix_long()
	# u'n\xe1m\u011bst\xed'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('169.075706')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'641'

	fake.country_code()
	# u'CI'

	fake.street_suffix_short()
	# u'n\xe1m.'

	fake.city()
	# u'Jistebnice'

	fake.state()
	# u'Olomouck\xfd kraj'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'5979309480552'

	fake.ean13()
	# u'3054486004714'

	fake.ean8()
	# u'56778632'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(198,89,86)'

	fake.color_name()
	# u'GoldenRod'

	fake.rgb_color_list()
	# (232, 125, 44)

	fake.rgb_color()
	# u'61,35,49'

	fake.safe_hex_color()
	# u'#ff4400'

	fake.safe_color_name()
	# u'white'

	fake.hex_color()
	# u'#88aa08'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'\u010cerm\xe1k'

	fake.company_suffix()
	# u'o.s.'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'102'

	fake.credit_card_provider(card_type=None)
	# u'Maestro'

	fake.credit_card_full(card_type=None)
	# u'Voyager\nNikola Dvo\u0159\xe1k\n869914490931922 10/18\nCVC: 318\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '05/19'

	fake.credit_card_number(card_type=None)
	# u'5420505887267861'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'SAR'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '20'

	fake.month()
	# '10'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 9, 24, 35)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1995, 8, 13, 23, 53, 28)

	fake.time(pattern="%H:%M:%S")
	# '11:24:42'

	fake.year()
	# '1973'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1017, 4, 12, 18, 3, 37)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 6, 30, 3)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 7, 18, 1, 59, 22)

	fake.unix_time()
	# 1048076158

	fake.month_name()
	# 'October'

	fake.timezone()
	# u'America/Montevideo'

	fake.time_delta()
	# datetime.timedelta(14072, 76805)

	fake.century()
	# u'XVI'

	fake.date(pattern="%Y-%m-%d")
	# '2011-07-15'

	fake.iso8601(tzinfo=None)
	# '1972-09-26T07:59:34'

	fake.date_time(tzinfo=None)
	# datetime(1984, 6, 27, 12, 18, 1)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 1, 27, 0, 45, 24)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'model/mesh'

	fake.file_name(category=None, extension=None)
	# u'cum.avi'

	fake.file_extension(category=None)
	# u'flac'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'175.226.195.3'

	fake.url()
	# u'http://mal\xe1.com/'

	fake.company_email()
	# u'iveta93@\u0161imkov\xe1.cz'

	fake.uri()
	# u'http://kol\xe1\u0159ov\xe1.cz/login/'

	fake.domain_word(*args, **kwargs)
	# u'barto\u0161ov\xe1'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/48x90'

	fake.tld()
	# u'cz'

	fake.free_email()
	# u'dvo\u0159\xe1kov\xe1vladim\xedra@volny.cz'

	fake.slug(*args, **kwargs)
	# u'unde-qui'

	fake.free_email_domain()
	# u'chello.cz'

	fake.domain_name()
	# u'pol\xe1kov\xe1.com'

	fake.uri_extension()
	# u'.asp'

	fake.ipv6()
	# u'ac5e:b3bc:2dfd:a33b:61bc:9f3d:fe5e:7a8b'

	fake.safe_email()
	# u'martinsedl\xe1\u010dek@example.org'

	fake.user_name(*args, **kwargs)
	# u'iveta38'

	fake.uri_path(deep=None)
	# u'search/tags/list'

	fake.email()
	# u'kopeck\xfdmilan@centrum.cz'

	fake.uri_page()
	# u'main'

	fake.mac_address()
	# u'8a:dd:44:b0:3b:84'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Naval architect'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Aut exercitationem officiis beatae eius. Est doloremque vitae doloribus. Quia sit nihil optio nesciunt blanditiis.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Animi id eius tenetur.'

	fake.word()
	# u'sed'

	fake.paragraphs(nb=3)
	# [   u'Inventore voluptatem voluptatem qui itaque atque. Eaque fugit consequatur vel totam reprehenderit vel. Odit non voluptatem ut saepe.',
	#     u'Illo odit tempora exercitationem facere rem quisquam consequatur. Incidunt alias ipsa in.',
	#     u'Nemo non sed incidunt ut qui harum sint. Rerum similique provident eligendi minima. Porro illum sed qui corrupti facilis eveniet.']

	fake.words(nb=3)
	# [u'cupiditate', u'quibusdam', u'id']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Qui quibusdam excepturi veritatis. In omnis quis aut error aut. Deleniti optio voluptatem ut molestias necessitatibus.'

	fake.sentences(nb=3)
	# [   u'Quaerat reprehenderit velit quidem ad labore qui vitae.',
	#     u'Ipsum quisquam dolores quae velit.',
	#     u'Suscipit ratione quisquam qui magnam hic.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u')kAw59Qr(3'

	fake.locale()
	# u'en_MY'

	fake.md5(raw_output=False)
	# '0e6b4ce30093b0f6ff2813a77b74a18e'

	fake.sha1(raw_output=False)
	# '241d42e318bc93b9f7650150c20cbc2081d50691'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# '84614d4677a4d33d07f995d0a1c24d9a32d526011b07a21b2512fb63c6926fa4'

	fake.uuid4()
	# '188e7007-a967-4ffa-9f5a-0ea96d81b6a2'

	fake.language_code()
	# u'pt'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'\u0160t\u011bp\xe1nek'

	fake.name_female()
	# u'Marie Dvo\u0159\xe1kov\xe1'

	fake.prefix_male()
	# u'Ing.'

	fake.prefix()
	# u'JUDr.'

	fake.name()
	# u'Anton\xedn Soukup'

	fake.suffix_female()
	# u'Th.D.'

	fake.name_male()
	# u'Alois K\u0159\xed\u017e'

	fake.first_name()
	# u'Kamil'

	fake.suffix_male()
	# u'Ph.D.'

	fake.suffix()
	# u'CSc.'

	fake.first_name_male()
	# u'Maty\xe1\u0161'

	fake.first_name_female()
	# u'Viktorie'

	fake.last_name_female()
	# u'Mal\xe1'

	fake.last_name()
	# u'Moravec'

	fake.prefix_female()
	# u'MUDr.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'737 452 730'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Pod Velk\xfdm H\xe1jem 8\n093 15 \u017dd\xe1nice',
	#     'birthdate': '2006-08-12',
	#     'mail': u'hkadlecov\xe1@email.cz',
	#     'name': u'\u0160t\u011bp\xe1n Vesel\xfd',
	#     'sex': 'M',
	#     'username': u'posp\xed\u0161ilov\xe1marta'}

	fake.profile(fields=None)
	# {   'address': u'Lod\u011bnick\xe1 2\n974 78 Kosmonosy',
	#     'birthdate': '1978-06-11',
	#     'blood_group': 'A+',
	#     'company': u'\u0158\xedha s.r.o.',
	#     'current_location': (Decimal('62.365484'), Decimal('69.281694')),
	#     'job': 'Scientist, audiological',
	#     'mail': u'ahor\xe1kov\xe1@gmail.com',
	#     'name': u'Lenka Sedl\xe1\u010dkov\xe1',
	#     'residence': u'U Vlachovky 7\n390 13 Horn\xed B\u0159\xedza',
	#     'sex': 'M',
	#     'ssn': u'688-51-3859',
	#     'username': u'wma\u0161kov\xe1',
	#     'website': [u'http://www.\u0161\u0165astn\xe1.cz/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'http://www.kopeck\xfd.com/categories/app/main/faq/',
	#     u'Totam ducimus.',
	#     805,
	#     u'http://www.\u0159\xedha.com/app/categories/explore/search/',
	#     Decimal('-785185908212'),
	#     u'Id veniam excepturi.',
	#     Decimal('70524.8'),
	#     948115937369.0]

	fake.pystr(max_chars=20)
	# u'Doloremque animi.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 832458301.2707

	fake.pystruct(count=10, *value_types)
	# (   [   -3790999047.0,
	#         u'Et omnis.',
	#         Decimal('8763.3233841'),
	#         773821266717.835,
	#         9745,
	#         u'http://www.vl\u010dek.cz/posts/main/categories/main.php',
	#         u'z\u0159\xedha@email.cz',
	#         u'Eius dolorem beatae.',
	#         -53833657.827,
	#         1378],
	#     {   u'dolorem': Decimal('-3755587.0'),
	#         u'eveniet': u'Aspernatur est sint.',
	#         u'fugiat': u'Numquam molestias.',
	#         u'ipsa': u'Dolores facere.',
	#         u'iste': u'Et est placeat in.',
	#         u'placeat': u'http://www.holub.cz/',
	#         u'quia': u'Facilis maiores.',
	#         u'ratione': u'Aut architecto.',
	#         u'rerum': u'Cupiditate est.',
	#         u'ut': datetime(1992, 7, 20, 23, 32, 9)},
	#     {   u'dolorem': {   3: Decimal('730975.659673'),
	#                         4: [   u'Dolores qui ipsa.',
	#                                u'Assumenda odit.',
	#                                u'Est necessitatibus.'],
	#                         5: {   3: datetime(2007, 5, 2, 15, 18, 44),
	#                                4: u'Vitae voluptatem.',
	#                                5: [23.931034, Decimal('9560242.7864')]}},
	#         u'facere': {   8: u'Eum repellat non.',
	#                        9: [   u'http://vl\u010dkov\xe1.cz/posts/tags/category/main/',
	#                               u'Omnis non veritatis.',
	#                               datetime(1974, 11, 13, 11, 3, 26)],
	#                        10: {   8: u'Quibusdam inventore.',
	#                                9: datetime(1973, 8, 1, 18, 51, 54),
	#                                10: [u'Et est dolores ea.', u'Temporibus.']}},
	#         u'fugit': {   1: 8412,
	#                       2: [   1977,
	#                              9288,
	#                              u'http://www.\u010dern\xe1.com/wp-content/tag/blog/privacy/'],
	#                       3: {   1: Decimal('442843776748'),
	#                              2: 837,
	#                              3: [   4335,
	#                                     u'http://du\u0161kov\xe1.cz/privacy.asp']}},
	#         u'incidunt': {   6: Decimal('2.21026438776E+14'),
	#                          7: [   -833482670022.231,
	#                                 u'Facilis ut.',
	#                                 u'http://www.\u0161t\u011bp\xe1nek.cz/main.html'],
	#                          8: {   6: u'Praesentium impedit.',
	#                                 7: u'Eos veritatis sit.',
	#                                 8: [6559, 8660]}},
	#         u'omnis': {   9: u'http://posp\xed\u0161il.cz/wp-content/app/search/index.html',
	#                       10: [   u'Quo veniam esse.',
	#                               u'Amet et itaque.',
	#                               -517222.98683806],
	#                       11: {   9: u'Voluptas placeat.',
	#                               10: u'http://kr\xe1lov\xe1.cz/app/terms/',
	#                               11: [8072, 2369]}},
	#         u'rerum': {   0: u'Aliquid inventore.',
	#                       1: [   datetime(2007, 9, 9, 20, 27, 51),
	#                              u'Ut quas modi.',
	#                              u'http://www.kol\xe1\u0159.com/register/'],
	#                       2: {   0: -60970893977818.0,
	#                              1: u'http://bl\xe1ha.cz/main/main/main.htm',
	#                              2: [   u'Tenetur nihil.',
	#                                     datetime(1979, 1, 26, 12, 18, 58)]}},
	#         u'sit': {   5: Decimal('18213.85'),
	#                     6: [3190, u'Est voluptates qui.', -770.72865397],
	#                     7: {   5: Decimal('585784.764'),
	#                            6: u'Voluptatem enim eum.',
	#                            7: [908, 1704]}},
	#         u'totam': {   4: u'Rerum sit eum.',
	#                       5: [   Decimal('7514.11431409'),
	#                              9899,
	#                              Decimal('6.03217153532E+14')],
	#                       6: {   4: 6993,
	#                              5: 7326,
	#                              6: [   u'Temporibus et odit.',
	#                                     u'Veritatis maiores.']}},
	#         u'vero': {   7: u'http://www.van\u011bk.cz/homepage/',
	#                      8: [   u'http://www.du\u0161ek.com/login/',
	#                             u'Et maxime.',
	#                             7137],
	#                      9: {   7: u'Maiores consequatur.',
	#                             8: Decimal('63.23'),
	#                             9: [5428, datetime(2001, 11, 25, 10, 36, 21)]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-1.06027999194E+13')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'jaroslavnov\xe1k@centrum.cz',
	#     Decimal('-58631305161.2'),
	#     u'Eius est fuga.',
	#     u'svobodalud\u011bk@chello.cz',
	#     u'http://www.mare\u0161.cz/home/',
	#     u'Dolores alias est.',
	#     4905483.619,
	#     u'Voluptas distinctio.',
	#     u'\u010derm\xe1kov\xe1eli\u0161ka@centrum.cz',
	#     u'Sequi itaque soluta.',
	#     u'Error esse fuga.',
	#     4101,
	#     u'Nisi dolorum.']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   datetime(1978, 6, 1, 18, 13, 26),
	#     4869,
	#     u'Debitis dolor qui.',
	#     u'\u0161t\u011bp\xe1nkov\xe1milada@post.cz',
	#     u'Id natus placeat.',
	#     u'Asperiores velit id.',
	#     u'Et iusto sit.',
	#     -64211.667199352)

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([7777, u'In corrupti quia.', u'Amet dolor aut ea.', u'pol\xe1keduard@seznam.cz', 1391, 6678, u'http://kol\xe1\u0159ov\xe1.com/category/', 8444982523495.43, -6395698793702.0, u'Quia quisquam eum.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'aliquid': u'http://www.\u010dern\xfd.com/search.php',
	#     u'commodi': u'Magni consequatur.',
	#     u'corrupti': datetime(1979, 7, 5, 23, 59, 19),
	#     u'dolores': u'andrea32@gmail.com',
	#     u'ipsum': datetime(2014, 4, 28, 16, 22, 31),
	#     u'occaecati': u'Ad qui reiciendis.',
	#     u'odio': u'Consectetur dolore.',
	#     u'perferendis': Decimal('623058.3'),
	#     u'placeat': u'Libero voluptatem.',
	#     u'reprehenderit': 6577,
	#     u'sapiente': datetime(2005, 9, 21, 21, 32, 44),
	#     u'voluptatem': u'Commodi soluta.',
	#     u'voluptatibus': datetime(1982, 3, 7, 21, 7, 2)}

	fake.pyint()
	# 6026

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'306-44-5921'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_6; rv:1.9.3.20) Gecko/2015-03-19 22:50:24 Firefox/3.6.15'

	fake.linux_platform_token()
	# u'X11; Linux i686'

	fake.opera()
	# u'Opera/8.45.(Windows NT 6.1; it-IT) Presto/2.9.171 Version/11.00'

	fake.windows_platform_token()
	# u'Windows NT 4.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows 95; Trident/5.1)'

	fake.user_agent()
	# u'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2014-11-22 12:29:24 Firefox/3.8'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5362 (KHTML, like Gecko) Chrome/13.0.860.0 Safari/5362'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; U; PPC Mac OS X 10_8_9'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/532.43.1 (KHTML, like Gecko) Version/4.0.2 Safari/532.43.1'
