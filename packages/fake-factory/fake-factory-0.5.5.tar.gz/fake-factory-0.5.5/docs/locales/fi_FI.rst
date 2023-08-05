
Language fi_FI
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('-89.409040')

	fake.street_name()
	# u'Taatelibulevardi'

	fake.address()
	# u'Sweetiepolku 836\n59718 Nivala'

	fake.street_address()
	# u'Granaattiomenatie 798'

	fake.postcode()
	# u'60699'

	fake.longitude()
	# Decimal('-2.959033')

	fake.country()
	# u'Thaimaa'

	fake.city_name()
	# u'Somero'

	fake.fruit()
	# u'Tamarillo'

	fake.street_suffix()
	# u'tie'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-58.926847')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'7'

	fake.country_code()
	# u'GQ'

	fake.city()
	# u'Sein\xe4joki'

	fake.state()
	# u'It\xe4-Suomen l\xe4\xe4ni'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'6075055625717'

	fake.ean13()
	# u'6370275088909'

	fake.ean8()
	# u'92074125'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(192,96,225)'

	fake.color_name()
	# u'Cornsilk'

	fake.rgb_color_list()
	# (193, 21, 215)

	fake.rgb_color()
	# u'225,50,211'

	fake.safe_hex_color()
	# u'#884400'

	fake.safe_color_name()
	# u'white'

	fake.hex_color()
	# u'#44596b'

``faker.providers.company``
---------------------------

::

	fake.company_vat()
	# u'FI89903045'

	fake.company_suffix()
	# u'Oy'

	fake.company()
	# u'Varala R\xe4ikk\xf6nen Osk'

	fake.company_business_id()
	# u'9160600-7'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'616'

	fake.credit_card_provider(card_type=None)
	# u'American Express'

	fake.credit_card_full(card_type=None)
	# u'American Express\nIines Varvikko\n348554650767111 07/24\nCID: 0491\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '01/25'

	fake.credit_card_number(card_type=None)
	# u'4036894067663787'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'IMP'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '19'

	fake.month()
	# '01'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 7, 8, 7, 32)

	fake.am_pm()
	# 'PM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(2008, 3, 26, 23, 20, 8)

	fake.time(pattern="%H:%M:%S")
	# '18:17:11'

	fake.year()
	# '1973'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(646, 7, 8, 23, 47, 22)

	fake.day_of_week()
	# 'Wednesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 5, 19, 46, 12)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 9, 24, 13, 25, 18)

	fake.unix_time()
	# 616223513

	fake.month_name()
	# 'July'

	fake.timezone()
	# u'Asia/Pyongyang'

	fake.time_delta()
	# datetime.timedelta(5393, 54053)

	fake.century()
	# u'XVI'

	fake.date(pattern="%Y-%m-%d")
	# '2005-02-23'

	fake.iso8601(tzinfo=None)
	# '1981-06-07T22:43:27'

	fake.date_time(tzinfo=None)
	# datetime(2015, 2, 3, 23, 43, 20)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2010, 4, 3, 3, 11, 44)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'model/vrml'

	fake.file_name(category=None, extension=None)
	# u'voluptas.txt'

	fake.file_extension(category=None)
	# u'avi'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'16.191.82.20'

	fake.url()
	# u'http://www.korhonen.fi/'

	fake.company_email()
	# u'smakkonen@ollikainen.fi'

	fake.uri()
	# u'http://www.oranen.org/list/tags/register.html'

	fake.domain_word(*args, **kwargs)
	# u'harjula'

	fake.image_url(width=None, height=None)
	# u'https://placeholdit.imgix.net/~text?txtsize=55&txt=618\xd7667&w=618&h=667'

	fake.tld()
	# u'fi'

	fake.free_email()
	# u'alli44@googlemail.com'

	fake.slug(*args, **kwargs)
	# u'dolor-dignissimos'

	fake.free_email_domain()
	# u'kolumbus.fi'

	fake.domain_name()
	# u'asunmaa.org'

	fake.uri_extension()
	# u'.html'

	fake.ipv6()
	# u'd884:4552:7135:d16b:f54a:7753:d1e0:0891'

	fake.safe_email()
	# u'haanp\xe4\xe4reino@example.org'

	fake.user_name(*args, **kwargs)
	# u'mirja65'

	fake.uri_path(deep=None)
	# u'tags/tag/blog'

	fake.email()
	# u'paavo77@hotmail.com'

	fake.uri_page()
	# u'register'

	fake.mac_address()
	# u'25:51:63:02:bb:bb'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Wellsite geologist'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Soluta ut quam commodi debitis qui non consequatur. Asperiores possimus nihil est ipsa. Ex aut est ut.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Nulla voluptates eius accusamus recusandae nostrum.'

	fake.word()
	# u'at'

	fake.paragraphs(nb=3)
	# [   u'Ut enim tempora voluptates assumenda quaerat alias. Eaque adipisci laboriosam non animi. Atque excepturi ipsum dolorem aut possimus.',
	#     u'Aut reiciendis cumque rerum tempore deleniti minima. Rem quae a ipsum rerum rerum ea accusamus quis. Nihil vel tenetur quo et cumque.',
	#     u'Voluptatem vel quia atque autem inventore. Et et aspernatur nostrum ab corrupti.']

	fake.words(nb=3)
	# [u'voluptatem', u'porro', u'voluptas']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Ut molestias voluptatum et inventore voluptatem et eos quibusdam. Consequatur deserunt molestias enim. Molestiae mollitia quos harum doloremque soluta. Ipsa commodi corporis beatae aperiam provident.'

	fake.sentences(nb=3)
	# [   u'Eum qui consequuntur quia accusamus sunt qui at quaerat.',
	#     u'Et eum perspiciatis qui facilis.',
	#     u'Omnis fuga aspernatur facilis quia recusandae consequuntur sequi.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'o79Qj+pL#&'

	fake.locale()
	# u'de_US'

	fake.md5(raw_output=False)
	# '1bd8726df14341b5cac1495926860bbf'

	fake.sha1(raw_output=False)
	# '85ac562abc23dc5da25090190d89b0f126f713f5'

	fake.null_boolean()
	# True

	fake.sha256(raw_output=False)
	# '6e1695af78b76b6fbc36a46cd25efb753a49d1c7e6c98c4e476f1dec2c493476'

	fake.uuid4()
	# 'b8532305-cbc2-4334-a9e3-4b196737e971'

	fake.language_code()
	# u'de'

	fake.boolean(chance_of_getting_true=50)
	# True

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Ahtisaari'

	fake.name_female()
	# u'Hilla Suntila'

	fake.prefix_male()
	# u'prof.'

	fake.prefix()
	# u'arkkit.'

	fake.name()
	# u'Senni Nurminen'

	fake.suffix_female()
	# u'DI'

	fake.name_male()
	# u'Helin\xe4 Peltosaari'

	fake.first_name()
	# u'Alisa'

	fake.suffix_male()
	# u'MSc'

	fake.suffix()
	# u'DI'

	fake.first_name_male()
	# u'Viivi'

	fake.first_name_female()
	# u'Talvikki'

	fake.last_name_female()
	# u'H\xe4nninen'

	fake.last_name()
	# u'Purho'

	fake.prefix_female()
	# u'rva'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'073 274 7974'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Kaktusviikunatie 274\n15758 Laitila',
	#     'birthdate': '1971-06-17',
	#     'mail': u'zjussila@gmail.com',
	#     'name': u'Verneri Lepist\xf6',
	#     'sex': 'M',
	#     'username': u'erno92'}

	fake.profile(fields=None)
	# {   'address': u'Limettikuja 5\n23500 J\xe4ms\xe4',
	#     'birthdate': '1988-09-02',
	#     'blood_group': 'B+',
	#     'company': u'Iivonen ry',
	#     'current_location': (Decimal('-83.2884705'), Decimal('-176.150142')),
	#     'job': 'Warden/ranger',
	#     'mail': u'susantirkkonen@kolumbus.fi',
	#     'name': u'Fanni Itkonen',
	#     'residence': u'Nashipolku 369\n12625 Raisio',
	#     'sex': 'M',
	#     'ssn': u'190977-320P',
	#     'username': u'eevakorhonen',
	#     'website': [   u'http://vuolle.com/',
	#                    u'http://www.salmi.net/',
	#                    u'http://lehtonen.fi/',
	#                    u'http://www.utriainen.com/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([Decimal('-8740874.91058'), 4662695847611.0, datetime(1976, 11, 21, 8, 17, 29), u'Nobis culpa.', u'http://www.supinen.fi/faq/', u'http://pitk\xe4nen.org/', Decimal('-517316410.316'), u'http://www.iivonen.com/explore/explore/list/terms.html', u'http://www.porkka.com/faq.jsp', u'bnikkinen@suomi24.fi', u'myl\xe4m\xe4ki@savolainen.fi'])

	fake.pystr(max_chars=20)
	# u'Enim mollitia quis.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# -668.396054

	fake.pystruct(count=10, *value_types)
	# (   [   7084,
	#         2549,
	#         Decimal('-34845646995.0'),
	#         datetime(1985, 8, 18, 15, 33, 45),
	#         u'Libero nam id.',
	#         u'zhintikka@karppanen.fi',
	#         u'Et fuga.',
	#         u'Aspernatur.',
	#         u'Maxime eligendi.',
	#         u'http://virolainen.com/'],
	#     {   u'eaque': u'Aspernatur suscipit.',
	#         u'error': 5921,
	#         u'et': 7744,
	#         u'facilis': Decimal('-435931692.0'),
	#         u'inventore': 645,
	#         u'itaque': u'km\xe4enp\xe4\xe4@saisio.fi',
	#         u'iusto': Decimal('-3.90752852859E+14'),
	#         u'quia': u'http://yrj\xe4l\xe4.com/home.php',
	#         u'quo': -993501.6322801,
	#         u'repudiandae': u'Quis inventore in.'},
	#     {   u'beatae': {   1: u'Distinctio qui.',
	#                        2: [-907954377540662.0, 325, u'Laborum ut.'],
	#                        3: {   1: u'Autem perspiciatis.',
	#                               2: datetime(2008, 11, 8, 4, 39, 55),
	#                               3: [   u'keskinenhannele@hotmail.com',
	#                                      u'Et vel minima.']}},
	#         u'consectetur': {   8: 2789,
	#                             9: [3213, 1080, u'vieno58@lehtinen.com'],
	#                             10: {   8: u'Similique sequi aut.',
	#                                     9: u'Enim magni.',
	#                                     10: [u'Expedita rerum quis.', 2254]}},
	#         u'distinctio': {   4: 502,
	#                            5: [   u'Doloremque.',
	#                                   Decimal('-8.10847615761'),
	#                                   u'Officiis odio omnis.'],
	#                            6: {   4: u'http://jalonen.com/home.php',
	#                                   5: u'helkam\xe4kil\xe4@luukku.com',
	#                                   6: [   u'Qui beatae ipsum.',
	#                                          292944816571.11]}},
	#         u'ea': {   0: Decimal('9.1858094929'),
	#                    1: [   84.4,
	#                           Decimal('462503499524'),
	#                           u'bharjula@heikkil\xe4.com'],
	#                    2: {   0: u'Vel nemo quod.',
	#                           1: 752,
	#                           2: [u'Deleniti harum non.', 5740]}},
	#         u'expedita': {   9: -43829249599929.0,
	#                          10: [   2371,
	#                                  u'Officia consectetur.',
	#                                  u'Tenetur est sequi.'],
	#                          11: {   9: Decimal('9.69144365401E+12'),
	#                                  10: u'Ut non earum at aut.',
	#                                  11: [   9888,
	#                                          datetime(1981, 9, 10, 5, 2, 43)]}},
	#         u'illo': {   6: 9826,
	#                      7: [u'Optio modi sit.', u'Ullam modi at rem.', 1606],
	#                      8: {   6: u'Totam velit aut.',
	#                             7: Decimal('-6764.592'),
	#                             8: [   datetime(1970, 3, 30, 8, 29, 46),
	#                                    u'tpoutanen@suomi24.fi']}},
	#         u'nobis': {   5: 9832,
	#                       6: [5284, u'Illo modi qui vel.', 8534],
	#                       7: {   5: 4972,
	#                              6: u'Et accusamus.',
	#                              7: [   datetime(2013, 1, 3, 22, 34, 24),
	#                                     u'Molestiae voluptas.']}},
	#         u'qui': {   3: -213559.389342829,
	#                     4: [   u'Quo tenetur quam.',
	#                            datetime(1995, 3, 5, 2, 37, 13),
	#                            u'Unde neque.'],
	#                     5: {   3: u'olivia64@suomi24.fi',
	#                            4: u'Eligendi nobis.',
	#                            5: [327580.5063, u'Voluptate.']}},
	#         u'voluptatibus': {   7: 3649090424.49651,
	#                              8: [   3.77150051373,
	#                                     u'Quibusdam in sunt.',
	#                                     datetime(2014, 5, 14, 14, 51, 52)],
	#                              9: {   7: u'http://www.aaltonen.org/list/explore/index.html',
	#                                     8: u'Qui consequatur eos.',
	#                                     9: [u'Nulla voluptatum.', 6306]}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('-18382053081.0')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'kokkonenmaija@lehtinen.com',
	#     u'Incidunt pariatur.',
	#     8757,
	#     u'Eius consectetur.',
	#     u'marianne75@viitala.com',
	#     Decimal('4427919278.51'),
	#     u'Labore laudantium.',
	#     Decimal('56.3631896185'),
	#     Decimal('21.1603903446'),
	#     9268,
	#     u'kaleva95@suomi24.fi',
	#     Decimal('-7.88591498412E+14'),
	#     8435,
	#     9382]

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   3584,
	#     u'Veritatis beatae.',
	#     u'Fugit dolorem vero.',
	#     datetime(1971, 9, 14, 11, 17, 46),
	#     Decimal('1218737384.16'),
	#     u'Dolor temporibus.',
	#     -8877247746311.44,
	#     u'Qui quisquam.',
	#     u'Deleniti.',
	#     8052,
	#     8478,
	#     u'Dolorum enim.',
	#     u'Officia consequatur.',
	#     u'Qui quibusdam et.')

	fake.pybool()
	# False

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'teemu30@tuuri.com', 2627, u'Velit vel vero.', 541275047991850.0, 4284409410893.0, u'Perspiciatis ipsam.', Decimal('2.07603338346E+14'), u'Culpa autem soluta.', u'http://www.sulkanen.com/terms/', 5783, u'Ut dolor corrupti.', u'Voluptatibus ipsa.', u'Ipsum est maxime.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'asperiores': u'raisa48@hotmail.com',
	#     u'corrupti': 2008,
	#     u'dolorem': u'rahopalo@googlemail.com',
	#     u'neque': 323245074.96517,
	#     u'possimus': u'Velit est dolor.',
	#     u'praesentium': u'Repellendus velit.',
	#     u'qui': 1838.65,
	#     u'sed': 2904,
	#     u'voluptas': u'Ratione voluptatem.'}

	fake.pyint()
	# 5745

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'260866-1259'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'Intel'

	fake.firefox()
	# u'Mozilla/5.0 (Windows 95; sl-SI; rv:1.9.0.20) Gecko/2015-08-28 01:09:45 Firefox/3.8'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.34.(Windows NT 6.2; it-IT) Presto/2.9.186 Version/12.00'

	fake.windows_platform_token()
	# u'Windows NT 5.2'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; Trident/3.0)'

	fake.user_agent()
	# u'Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.0; Trident/5.0)'

	fake.chrome()
	# u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5362 (KHTML, like Gecko) Chrome/14.0.854.0 Safari/5362'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; Intel Mac OS X 10_6_1'

	fake.safari()
	# u'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; it-IT) AppleWebKit/535.50.4 (KHTML, like Gecko) Version/3.0.5 Mobile/8B115 Safari/6535.50.4'
