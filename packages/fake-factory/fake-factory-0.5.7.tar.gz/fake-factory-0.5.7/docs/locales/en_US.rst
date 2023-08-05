
Language en_US
===============

``faker.providers.address``
---------------------------

::

	fake.longitude()
	# Decimal('36.862011')

	fake.building_number()
	# u'755'

	fake.street_address()
	# u'306 Mueller Common'

	fake.postalcode_plus4()
	# u'80610-9835'

	fake.city_prefix()
	# u'North'

	fake.military_ship()
	# u'USS'

	fake.country_code()
	# u'SZ'

	fake.city()
	# u'Marvinbury'

	fake.zipcode_plus4()
	# u'96976-7873'

	fake.state_abbr()
	# u'OH'

	fake.latitude()
	# Decimal('68.9052065')

	fake.street_suffix()
	# u'Crescent'

	fake.city_suffix()
	# u'berg'

	fake.military_dpo()
	# u'Unit 2627 Box 0041'

	fake.country()
	# u'Liechtenstein'

	fake.secondary_address()
	# u'Suite 766'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-166.142712')

	fake.postalcode()
	# u'84712'

	fake.address()
	# u'227 Shiloh Drives Suite 126\nChadwickchester, NV 75494-7587'

	fake.state()
	# u'Kansas'

	fake.military_state()
	# u'AE'

	fake.street_name()
	# u'Romaguera Bridge'

	fake.zipcode()
	# u'32068'

	fake.postcode()
	# u'95095'

	fake.military_apo()
	# u'PSC 6955, Box 2642'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'9250512662864'

	fake.ean13()
	# u'7243510891970'

	fake.ean8()
	# u'43843503'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(47,151,104)'

	fake.color_name()
	# u'Cornsilk'

	fake.rgb_color_list()
	# (164, 39, 185)

	fake.rgb_color()
	# u'182,105,208'

	fake.safe_hex_color()
	# u'#aaee00'

	fake.safe_color_name()
	# u'maroon'

	fake.hex_color()
	# u'#bb0b13'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Kohler-Nader'

	fake.company_suffix()
	# u'Inc'

	fake.catch_phrase()
	# u'User-friendly 5thgeneration knowledgebase'

	fake.bs()
	# u'optimize distributed applications'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'191'

	fake.credit_card_provider(card_type=None)
	# u'Voyager'

	fake.credit_card_full(card_type=None)
	# u'JCB 16 digit\nEthel Conroy\n3112681022273573 12/19\nCVC: 162\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '02/24'

	fake.credit_card_number(card_type=None)
	# u'4657878197551614'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'EUR'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '18'

	fake.month()
	# '10'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 4, 10, 28, 31)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1992, 6, 6, 2, 5, 55)

	fake.time(pattern="%H:%M:%S")
	# '12:01:57'

	fake.year()
	# '1982'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(1080, 7, 14, 20, 43, 33)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 5, 18, 18, 25)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2015, 9, 15, 4, 22)

	fake.unix_time()
	# 221553181

	fake.month_name()
	# 'October'

	fake.timezone()
	# u'Europe/Copenhagen'

	fake.time_delta()
	# datetime.timedelta(11598, 22021)

	fake.century()
	# u'XII'

	fake.date(pattern="%Y-%m-%d")
	# '1995-10-18'

	fake.iso8601(tzinfo=None)
	# '2004-06-05T11:54:07'

	fake.date_time(tzinfo=None)
	# datetime(2004, 6, 12, 19, 4, 8)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2013, 1, 24, 3, 22, 37)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'image/pjpeg'

	fake.file_name(category=None, extension=None)
	# u'et.jpg'

	fake.file_extension(category=None)
	# u'css'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'210.250.161.229'

	fake.url()
	# u'http://www.lesch.com/'

	fake.company_email()
	# u'gigibalistreri@wunsch.org'

	fake.uri()
	# u'http://www.ward-hermiston.info/search.html'

	fake.domain_word(*args, **kwargs)
	# u'haag-ebert'

	fake.image_url(width=None, height=None)
	# u'http://dummyimage.com/837x630'

	fake.tld()
	# u'com'

	fake.free_email()
	# u'cronadarcie@hotmail.com'

	fake.slug(*args, **kwargs)
	# u'ullam-ut-beatae'

	fake.free_email_domain()
	# u'gmail.com'

	fake.domain_name()
	# u'kshlerin-grady.com'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'bc8f:afe3:0f7e:a89d:dcd5:c84c:125a:864d'

	fake.safe_email()
	# u'nelsoncarroll@example.com'

	fake.user_name(*args, **kwargs)
	# u'cristinawill'

	fake.uri_path(deep=None)
	# u'app/search/tags'

	fake.email()
	# u'kimballchristiansen@gmail.com'

	fake.uri_page()
	# u'about'

	fake.mac_address()
	# u'dd:3d:3b:8e:68:04'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Town planner'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Qui itaque aliquam vitae est explicabo. Quis dolorum facere eius neque. Quia est ea quae et ut quod id ullam. Illo sapiente explicabo tenetur ut voluptas excepturi.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Velit aut facilis sunt in vero.'

	fake.word()
	# u'omnis'

	fake.paragraphs(nb=3)
	# [   u'Officiis consequatur officiis nulla ex maiores facere. Qui est voluptatem vel. Ullam explicabo aut voluptatem atque tempora.',
	#     u'Ex tempore quasi recusandae aut rerum in atque nihil. Sed totam sed ut alias. Quia nemo voluptas aut non. Impedit ipsa quis suscipit vel.',
	#     u'Laboriosam odio architecto eos rerum et exercitationem qui odio. Vitae sint eveniet rerum porro harum. Qui sunt ab nemo exercitationem magni laboriosam.']

	fake.words(nb=3)
	# [u'voluptas', u'officia', u'pariatur']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Necessitatibus pariatur dolorem adipisci. Impedit sint ut dolorem ut voluptates eos sunt. Facilis ratione totam repellendus quo at.'

	fake.sentences(nb=3)
	# [   u'Sequi minima et quo nemo.',
	#     u'Odit dolor laborum accusamus nobis delectus rerum sunt.',
	#     u'Eum aut sapiente fuga.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'@MR%OJfeY5'

	fake.locale()
	# u'en_KZ'

	fake.md5(raw_output=False)
	# '5f10b6c92cbf6fe55573c7da4e37930d'

	fake.sha1(raw_output=False)
	# '90676fdb4f9670c284d2ef7fd6daa95f0ade6e71'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# 'f66a28870c5dd9f4282cfde38885bd8792b6b878a8a6978bf937e844d009d659'

	fake.uuid4()
	# '449a74c3-bd44-48a8-9c31-0f00e1189ed4'

	fake.language_code()
	# u'de'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Kuvalis'

	fake.name_female()
	# u'Dr. Faith Shanahan DDS'

	fake.prefix_male()
	# u'Dr.'

	fake.prefix()
	# u'Mrs.'

	fake.name()
	# u'Nikolas Feil'

	fake.suffix_female()
	# u'MD'

	fake.name_male()
	# u'Rexford Kub I'

	fake.first_name()
	# u'Euna'

	fake.suffix_male()
	# u'DDS'

	fake.suffix()
	# u'Jr.'

	fake.first_name_male()
	# u'Agustus'

	fake.first_name_female()
	# u'Launa'

	fake.last_name_female()
	# u'Bergstrom'

	fake.last_name()
	# u'Gutkowski'

	fake.prefix_female()
	# u'Ms.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'1-601-997-2748x5248'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'5693 Hane Crossroad Suite 944\nWest Bess, ID 91579-3109',
	#     'birthdate': '2001-08-24',
	#     'mail': u'robinparker@hotmail.com',
	#     'name': u'Sister Schuppe',
	#     'sex': 'F',
	#     'username': u'veronicamacejkovic'}

	fake.profile(fields=None)
	# {   'address': u'4787 Melody Underpass Suite 641\nPurdychester, CT 93942-9159',
	#     'birthdate': '2012-10-18',
	#     'blood_group': '0+',
	#     'company': u'Deckow, Hickle and Dare',
	#     'current_location': (Decimal('11.682034'), Decimal('129.854568')),
	#     'job': 'Psychologist, forensic',
	#     'mail': u'katherinreilly@yahoo.com',
	#     'name': u'Lucious Wilderman',
	#     'residence': u'499 Metz Overpass\nNorth Trystanburgh, KS 26675',
	#     'sex': 'M',
	#     'ssn': u'335-72-9137',
	#     'username': u'strosinartie',
	#     'website': [   u'http://howell.info/',
	#                    u'http://www.hettinger-ohara.net/',
	#                    u'http://www.funk.biz/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'Consequuntur ea.',
	#     u'Mollitia sed.',
	#     u'http://www.braun.com/',
	#     u'Hic perspiciatis.',
	#     u'Eveniet tempora ab.',
	#     8565,
	#     u'Ea voluptas est.',
	#     u'http://www.bins.com/blog/tag/post/')

	fake.pystr(max_chars=20)
	# u'Qui accusamus ut.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 6593768134619.0

	fake.pystruct(count=10, *value_types)
	# (   [   u'Est itaque veniam.',
	#         u'Voluptatem dolore.',
	#         u'Voluptatem aut.',
	#         u'Aliquam quae.',
	#         2375,
	#         u'Minus sit.',
	#         u'hquitzon@hotmail.com',
	#         u'Reprehenderit atque.',
	#         u'Autem quos iusto.',
	#         u'carson88@gmail.com'],
	#     {   u'beatae': datetime(1994, 7, 25, 6, 57, 12),
	#         u'excepturi': 7793,
	#         u'molestiae': 5124,
	#         u'non': u'Nihil ut eaque unde.',
	#         u'occaecati': Decimal('8676789948.3'),
	#         u'quis': 6572,
	#         u'soluta': u'Facilis aperiam vel.',
	#         u'tempora': u'Id corporis neque.',
	#         u'ut': 5105,
	#         u'voluptatem': -15.15},
	#     {   u'consequatur': {   5: Decimal('-2.93791'),
	#                             6: [   47990300401.7,
	#                                    250797532.3,
	#                                    datetime(1995, 2, 25, 6, 34, 34)],
	#                             7: {   5: 6330,
	#                                    6: u'Deleniti natus aut.',
	#                                    7: [   -33.2128416849,
	#                                           u'labadietara@yahoo.com']}},
	#         u'enim': {   6: u'Nobis eius earum.',
	#                      7: [   u'Quibusdam voluptas.',
	#                             u'ukirlin@yahoo.com',
	#                             u'http://www.stamm-feest.com/post.htm'],
	#                      8: {   6: u'lindgrenaddie@baumbach.org',
	#                             7: Decimal('9262149370.5'),
	#                             8: [u'Voluptatem nihil.', 2724]}},
	#         u'in': {   7: u'Aut eius doloremque.',
	#                    8: [   u'Temporibus.',
	#                           u'http://www.osinski-considine.com/',
	#                           u'Voluptatem.'],
	#                    9: {   7: Decimal('-1671883.0'),
	#                           8: 137,
	#                           9: [u'qjacobson@gmail.com', 3539]}},
	#         u'iure': {   1: u'Magnam omnis quae.',
	#                      2: [   838706.200826,
	#                             datetime(2013, 12, 31, 3, 31, 12),
	#                             Decimal('-5574068.14735')],
	#                      3: {   1: 9662,
	#                             2: Decimal('436971915444'),
	#                             3: [   u'Reprehenderit cum.',
	#                                    u'louannjerde@gmail.com']}},
	#         u'iusto': {   9: u'Voluptate velit.',
	#                       10: [   u'Cupiditate porro.',
	#                               u'Magnam et.',
	#                               u'Quae voluptatum.'],
	#                       11: {   9: u'Dolor aut.', 10: 50, 11: [40, 8057]}},
	#         u'minima': {   8: u'Eligendi et.',
	#                        9: [   u'Veniam quibusdam.',
	#                               u'Praesentium.',
	#                               u'Provident et quam.'],
	#                        10: {   8: 7348,
	#                                9: -255530379217723.0,
	#                                10: [u'Dolores.', 470]}},
	#         u'necessitatibus': {   4: u'Voluptatibus porro.',
	#                                5: [   u'Amet doloribus sint.',
	#                                       u'Architecto hic.',
	#                                       u'http://koelpin-pfannerstill.com/login.htm'],
	#                                6: {   4: u'http://www.hartmann-rau.org/wp-content/search/app/terms/',
	#                                       5: u'Dolorem libero.',
	#                                       6: [   u'koberobel@flatley-damore.com',
	#                                              5089]}},
	#         u'nobis': {   0: datetime(1999, 1, 5, 11, 14, 36),
	#                       1: [   datetime(2000, 11, 2, 4, 57, 51),
	#                              u'bashiriansalena@gmail.com',
	#                              1189],
	#                       2: {   0: -843587.3622,
	#                              1: u'Ipsam ad et.',
	#                              2: [   u'Placeat consequatur.',
	#                                     datetime(2004, 8, 10, 12, 12, 5)]}},
	#         u'rerum': {   2: Decimal('-347701.5'),
	#                       3: [   Decimal('11439999405.3'),
	#                              u'Alias nemo itaque.',
	#                              u'Fugit dolore.'],
	#                       4: {   2: 9189,
	#                              3: u'javon03@hintz.biz',
	#                              4: [u'Dicta et ut.', u'Quis aliquam aut.']}},
	#         u'sapiente': {   3: datetime(2000, 4, 18, 9, 1, 2),
	#                          4: [7646792048022.3, u'Ipsum sint magni.', 3678],
	#                          5: {   3: u'Dolorum qui.',
	#                                 4: datetime(1971, 11, 3, 7, 45, 56),
	#                                 5: [   u'tmraz@predovic.com',
	#                                        -963140.91265324]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('428022.895017')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   Decimal('7326.0'),
	#     u'http://ritchie.com/',
	#     datetime(2000, 9, 20, 2, 14, 28),
	#     u'lesdonnelly@gmail.com',
	#     datetime(1990, 7, 6, 8, 54, 18),
	#     u'Nesciunt autem.',
	#     33.73735978196,
	#     4657297690447.1,
	#     u'Quia qui ex impedit.',
	#     -352382.75611,
	#     u'ukulas@mayert.info',
	#     4021052278.356,
	#     3761,
	#     u'lelar96@trantow-heathcote.com']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   u'rgreenholt@yahoo.com',
	#     u'tdubuque@hotmail.com',
	#     u'Nemo autem natus.',
	#     7023,
	#     u'green72@gmail.com',
	#     u'Est dolorem.',
	#     u'Consequuntur quia.',
	#     datetime(1972, 1, 7, 19, 26, 1),
	#     Decimal('-3514480.511'),
	#     u'zeke42@schiller.org',
	#     datetime(2010, 7, 16, 6, 56, 27))

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([-5694747538812.0, u'Eligendi harum.', u'Aut omnis occaecati.', 1803, u'Iste est dolorem.', u'Maiores deleniti.', 9490, Decimal('-2.41354494919E+12'), 5339])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'aut': u'Fugit vitae minima.',
	#     u'autem': u'shanahanottie@parker-gorczany.info',
	#     u'consequuntur': 1378,
	#     u'eos': datetime(1999, 2, 2, 19, 58, 45),
	#     u'ex': 2317,
	#     u'fuga': u'Illo dolor fuga at.',
	#     u'nihil': 84.1,
	#     u'nisi': u'http://daniel.com/category/',
	#     u'reiciendis': u'Vero voluptates aut.',
	#     u'rerum': 8628,
	#     u'ut': u'larae12@bayer.com'}

	fake.pyint()
	# 3405

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'628-67-2793'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0; rv:1.9.6.20) Gecko/2014-08-17 05:50:27 Firefox/3.6.19'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/8.75.(X11; Linux x86_64; it-IT) Presto/2.9.177 Version/12.00'

	fake.windows_platform_token()
	# u'Windows NT 5.0'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 4.0; Trident/3.0)'

	fake.user_agent()
	# u'Opera/8.92.(X11; Linux x86_64; sl-SI) Presto/2.9.190 Version/12.00'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5330 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/5330'

	fake.linux_processor()
	# u'x86_64'

	fake.mac_platform_token()
	# u'Macintosh; PPC Mac OS X 10_5_5'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/533.7.7 (KHTML, like Gecko) Version/4.1 Safari/533.7.7'
