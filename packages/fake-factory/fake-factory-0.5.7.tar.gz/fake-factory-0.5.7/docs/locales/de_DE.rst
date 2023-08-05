
Language de_DE
===============

``faker.providers.address``
---------------------------

::

	fake.latitude()
	# Decimal('60.4808485')

	fake.street_name()
	# u'Uwe-Bolzmann-Gasse'

	fake.address()
	# u'Gerlachgasse 9/7\n74866 B\xfcsingenm Hochrhein'

	fake.street_address()
	# u'Jacobi J\xe4ckelring 2'

	fake.postcode()
	# u'81463'

	fake.longitude()
	# Decimal('-107.810040')

	fake.country()
	# u'Kiribati'

	fake.city_name()
	# u'Mittweida'

	fake.street_suffix_long()
	# u'Ring'

	fake.street_suffix()
	# u'Street'

	fake.geo_coordinate(center=None, radius=0.001)
	# Decimal('-169.529336')

	fake.city_suffix()
	# u'Ville'

	fake.building_number()
	# u'88'

	fake.country_code()
	# u'GA'

	fake.street_suffix_short()
	# u'ring'

	fake.city()
	# u'Bernburg'

	fake.state()
	# u'Th\xfcringen'

``faker.providers.barcode``
---------------------------

::

	fake.ean(length=13)
	# u'2441921241659'

	fake.ean13()
	# u'4640883422429'

	fake.ean8()
	# u'84994776'

``faker.providers.color``
-------------------------

::

	fake.rgb_css_color()
	# u'rgb(52,62,194)'

	fake.color_name()
	# u'DodgerBlue'

	fake.rgb_color_list()
	# (93, 109, 128)

	fake.rgb_color()
	# u'69,35,80'

	fake.safe_hex_color()
	# u'#aa9900'

	fake.safe_color_name()
	# u'maroon'

	fake.hex_color()
	# u'#3fcb44'

``faker.providers.company``
---------------------------

::

	fake.company()
	# u'Ernst S\xf6lzer KGaA'

	fake.company_suffix()
	# u'e.G.'

``faker.providers.credit_card``
-------------------------------

::

	fake.credit_card_security_code(card_type=None)
	# u'221'

	fake.credit_card_provider(card_type=None)
	# u'Mastercard'

	fake.credit_card_full(card_type=None)
	# u'JCB 16 digit\nRalf-Peter Stolze\n3088957219533197 02/17\nCVC: 509\n'

	fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
	# '12/25'

	fake.credit_card_number(card_type=None)
	# u'342367373882125'

``faker.providers.currency``
----------------------------

::

	fake.currency_code()
	# 'PHP'

``faker.providers.date_time``
-----------------------------

::

	fake.day_of_month()
	# '25'

	fake.month()
	# '04'

	fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 2, 15, 17, 8)

	fake.am_pm()
	# 'AM'

	fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
	# datetime(2016, 1, 7, 12, 58, 37)

	fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None)
	# datetime(1990, 5, 16, 2, 28, 55)

	fake.time(pattern="%H:%M:%S")
	# '04:44:57'

	fake.year()
	# '1985'

	fake.date_time_ad(tzinfo=None)
	# datetime.datetime(183, 12, 28, 4, 30, 52)

	fake.day_of_week()
	# 'Tuesday'

	fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
	# datetime(2016, 1, 6, 19, 51, 50)

	fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)
	# datetime(2012, 11, 6, 17, 9, 30)

	fake.unix_time()
	# 936748248

	fake.month_name()
	# 'November'

	fake.timezone()
	# u'America/Dominica'

	fake.time_delta()
	# datetime.timedelta(9346, 66686)

	fake.century()
	# u'XII'

	fake.date(pattern="%Y-%m-%d")
	# '1978-03-29'

	fake.iso8601(tzinfo=None)
	# '2012-01-20T08:34:07'

	fake.date_time(tzinfo=None)
	# datetime(2010, 12, 21, 14, 5, 11)

	fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
	# datetime(2011, 9, 28, 6, 36, 19)

``faker.providers.file``
------------------------

::

	fake.mime_type(category=None)
	# u'model/iges'

	fake.file_name(category=None, extension=None)
	# u'cupiditate.pptx'

	fake.file_extension(category=None)
	# u'flac'

``faker.providers.internet``
----------------------------

::

	fake.ipv4()
	# u'178.132.90.245'

	fake.url()
	# u'http://gorlitz.com/'

	fake.company_email()
	# u'boucseindina@stumpf.de'

	fake.uri()
	# u'http://www.loewer.de/search/'

	fake.domain_word(*args, **kwargs)
	# u'gutknecht'

	fake.image_url(width=None, height=None)
	# u'https://placeholdit.imgix.net/~text?txtsize=55&txt=417\xd7520&w=417&h=520'

	fake.tld()
	# u'org'

	fake.free_email()
	# u'xheinz@hotmail.de'

	fake.slug(*args, **kwargs)
	# u'illum-earum-quas'

	fake.free_email_domain()
	# u'yahoo.de'

	fake.domain_name()
	# u'krebs.com'

	fake.uri_extension()
	# u'.jsp'

	fake.ipv6()
	# u'e0c5:1f0c:1625:3293:63b5:3e91:1ed9:5c64'

	fake.safe_email()
	# u'vhornich@example.com'

	fake.user_name(*args, **kwargs)
	# u'kreuselkaroline'

	fake.uri_path(deep=None)
	# u'tags/blog/wp-content'

	fake.email()
	# u'fweihmann@scholl.de'

	fake.uri_page()
	# u'category'

	fake.mac_address()
	# u'5c:c6:dc:b2:c0:75'

``faker.providers.job``
-----------------------

::

	fake.job()
	# 'Broadcast journalist'

``faker.providers.lorem``
-------------------------

::

	fake.text(max_nb_chars=200)
	# u'Maiores repellat cumque non debitis illo eos. Ea quia voluptatem repudiandae voluptatem modi quas veniam. Culpa qui consequatur quis qui.'

	fake.sentence(nb_words=6, variable_nb_words=True)
	# u'Ad voluptatem laboriosam dolorem magni aliquid et et.'

	fake.word()
	# u'vitae'

	fake.paragraphs(nb=3)
	# [   u'Eum magni non aut sint. Alias fuga quos quis maiores delectus. Eaque quos dolorum fugit molestiae aliquid impedit eum.',
	#     u'Eos voluptates asperiores ipsa voluptas accusantium porro exercitationem. Ea impedit quis minima soluta assumenda corrupti debitis. Quisquam error sed maiores voluptatum sequi.',
	#     u'Eius recusandae modi similique earum eligendi tempora natus quaerat. Est magni est ut et dolores. Deserunt blanditiis animi fugit quibusdam nostrum officiis tempora.']

	fake.words(nb=3)
	# [u'dolorum', u'accusantium', u'voluptas']

	fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
	# u'Nulla necessitatibus aut blanditiis dolores exercitationem. Cupiditate vel fuga quidem omnis voluptatum rerum. Et quia doloribus maxime quisquam incidunt vel inventore animi. Aliquam quia excepturi excepturi magni eos perferendis nam et. At veritatis earum ea libero architecto.'

	fake.sentences(nb=3)
	# [   u'Adipisci nesciunt impedit provident.',
	#     u'Consequatur ab ut veritatis nisi id perferendis iusto.',
	#     u'Error vitae error et sint quis.']

``faker.providers.misc``
------------------------

::

	fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
	# u'm%02nXkl6k'

	fake.locale()
	# u'it_ID'

	fake.md5(raw_output=False)
	# '88ff02153ba8c4b3c0fcb76cc55cb73e'

	fake.sha1(raw_output=False)
	# '4c1264eab0b61216c959061e8ed6fd59f6965299'

	fake.null_boolean()
	# False

	fake.sha256(raw_output=False)
	# '50c0cc7050d89110f80ddc98937d2f7027397744ee685171d16d4f127cba0564'

	fake.uuid4()
	# 'd3794c64-8026-41b5-b00d-a13690b38d85'

	fake.language_code()
	# u'en'

	fake.boolean(chance_of_getting_true=50)
	# False

``faker.providers.person``
--------------------------

::

	fake.last_name_male()
	# u'Wulff'

	fake.name_female()
	# u'Lea Kramer'

	fake.prefix_male()
	# u'Herr'

	fake.prefix()
	# u'Dipl.-Ing.'

	fake.name()
	# u'Hermann Junken-Caspar'

	fake.suffix_female()
	# u'MBA.'

	fake.name_male()
	# u'Stephanie Reichmann'

	fake.first_name()
	# u'Kathi'

	fake.suffix_male()
	# u'B.Sc.'

	fake.suffix()
	# u'B.Sc.'

	fake.first_name_male()
	# u'Harald'

	fake.first_name_female()
	# u'Wilfriede'

	fake.last_name_female()
	# u'Weitzel'

	fake.last_name()
	# u'Hamann'

	fake.prefix_female()
	# u'Univ.Prof.'

``faker.providers.phone_number``
--------------------------------

::

	fake.phone_number()
	# u'(04477) 054342'

``faker.providers.profile``
---------------------------

::

	fake.simple_profile()
	# {   'address': u'Fischerallee 81\n61140 Eichst\xe4tt',
	#     'birthdate': '1985-05-19',
	#     'mail': u'arthur34@gmail.com',
	#     'name': u'Donald Spie\xdf',
	#     'sex': 'F',
	#     'username': u'elizabeth06'}

	fake.profile(fields=None)
	# {   'address': u'Torben-Grein Groth-Gasse 3/4\n05104 Haldensleben',
	#     'birthdate': '1978-03-06',
	#     'blood_group': 'A-',
	#     'company': u'Heidrich',
	#     'current_location': (Decimal('14.5625365'), Decimal('172.726549')),
	#     'job': 'Community pharmacist',
	#     'mail': u'nadinalbers@gmail.com',
	#     'name': u'Gunter Margraf',
	#     'residence': u'Haufferweg 83\n45332 F\xfcrstenfeldbruck',
	#     'sex': 'M',
	#     'ssn': u'406-67-8273',
	#     'username': u'ulrikehenk',
	#     'website': [   u'http://www.schoenland.com/',
	#                    u'http://www.adler.com/',
	#                    u'http://franke.de/']}

``faker.providers.python``
--------------------------

::

	fake.pyiterable(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   Decimal('-891936965.28'),
	#     u'Beatae molestias.',
	#     6342,
	#     u'anna36@roehricht.com',
	#     u'Sit architecto.',
	#     8495,
	#     datetime(2010, 10, 27, 0, 49, 27),
	#     u'Explicabo debitis.')

	fake.pystr(max_chars=20)
	# u'Autem quibusdam.'

	fake.pyfloat(left_digits=None, right_digits=None, positive=False)
	# 454.0

	fake.pystruct(count=10, *value_types)
	# (   [   u'http://www.buchholz.com/posts/categories/index.php',
	#         u'http://www.lindau.com/index/',
	#         datetime(1988, 11, 4, 4, 55, 33),
	#         Decimal('-7.16533821243E+14'),
	#         u'adlernatascha@huhn.com',
	#         u'Odio voluptates sed.',
	#         6371678480413.89,
	#         Decimal('1016098.9'),
	#         -586936868.607,
	#         datetime(1998, 2, 1, 16, 16, 30)],
	#     {   u'assumenda': u'Exercitationem.',
	#         u'ea': u'Reiciendis qui sit.',
	#         u'eos': u'iboerner@aol.de',
	#         u'est': 2837,
	#         u'eveniet': 5694476144.9,
	#         u'nemo': u'Dignissimos amet.',
	#         u'quis': 9675,
	#         u'quo': 2330,
	#         u'quos': u'Hic ut hic.',
	#         u'sunt': Decimal('4.76523834606E+14')},
	#     {   u'accusantium': {   9: u'gklemm@googlemail.com',
	#                             10: [   u'ojuettner@kallert.de',
	#                                     u'sarinathanel@schleich.com',
	#                                     u'Voluptatem facilis.'],
	#                             11: {   9: datetime(2012, 9, 10, 17, 30, 10),
	#                                     10: 400532.33684,
	#                                     11: [   u'Soluta nihil aut ut.',
	#                                             datetime(2009, 9, 5, 6, 50, 23)]}},
	#         u'dicta': {   7: u'Est ipsam fuga.',
	#                       8: [9018, u'Fugiat repellat.', u'Tempore occaecati.'],
	#                       9: {   7: 7999,
	#                              8: 830,
	#                              9: [   u'karl-hansscholl@yahoo.de',
	#                                     -11026728261.55]}},
	#         u'eos': {   8: u'Atque quo.',
	#                     9: [   datetime(2001, 2, 18, 3, 42, 54),
	#                            u'lreichmann@harloff.de',
	#                            Decimal('-8.17045596015E+13')],
	#                     10: {   8: u'Est non fuga aut.',
	#                             9: -93285254630.95,
	#                             10: [   u'wilmsenthies@web.de',
	#                                     u'wulf01@seifert.com']}},
	#         u'et': {   2: u'Aspernatur illo.',
	#                    3: [   u'http://hauffer.com/list/tags/explore/category/',
	#                           8821,
	#                           5955],
	#                    4: {   2: 4754,
	#                           3: u'http://trapp.net/explore/tags/tag/terms/',
	#                           4: [   Decimal('56017575140.5'),
	#                                  u'Debitis explicabo.']}},
	#         u'laboriosam': {   3: u'Magni quos qui.',
	#                            4: [   u'Blanditiis soluta.',
	#                                   Decimal('-34.8677048801'),
	#                                   91465504751.2099],
	#                            5: {   3: 536,
	#                                   4: datetime(1986, 2, 13, 6, 21, 57),
	#                                   5: [   Decimal('844892.2'),
	#                                          u'http://www.weihmann.de/app/terms/']}},
	#         u'neque': {   1: -8594.9283408516,
	#                       2: [   9889,
	#                              u'http://www.hoefig.de/register/',
	#                              u'Adipisci et quidem.'],
	#                       3: {   1: 2950,
	#                              2: datetime(2011, 5, 24, 21, 48, 38),
	#                              3: [   datetime(1994, 12, 22, 12, 52, 40),
	#                                     u'Ipsum ad tempore.']}},
	#         u'nisi': {   6: 9398,
	#                      7: [   662280537526578.0,
	#                             u'Assumenda et.',
	#                             -27346640293528.1],
	#                      8: {   6: 3190,
	#                             7: u'http://www.cichorius.de/category/',
	#                             8: [   u'anne-kathrin64@klotz.com',
	#                                    u'Blanditiis non.']}},
	#         u'perspiciatis': {   4: Decimal('-370363.8'),
	#                              5: [   u'Officiis dolores.',
	#                                     u'Eum non omnis.',
	#                                     778],
	#                              6: {   4: u'Et ad ratione atque.',
	#                                     5: Decimal('16004559.7902'),
	#                                     6: [   u'Voluptatem deleniti.',
	#                                            u'Reiciendis.']}},
	#         u'quia': {   5: Decimal('160058713002'),
	#                      6: [   datetime(2005, 2, 6, 5, 36, 13),
	#                             1390,
	#                             u'Tempore veritatis.'],
	#                      7: {   5: u'hansjoergpergande@vollbrecht.de',
	#                             6: datetime(1983, 3, 30, 18, 47, 48),
	#                             7: [   u'Aliquid voluptates.',
	#                                    Decimal('-2.61381623138E+13')]}},
	#         u'saepe': {   0: datetime(1976, 11, 29, 0, 25, 27),
	#                       1: [   u'Porro est veritatis.',
	#                              3438,
	#                              datetime(1987, 2, 7, 12, 44, 59)],
	#                       2: {   0: u'Itaque voluptas.',
	#                              1: Decimal('-58.23578849'),
	#                              2: [   datetime(1995, 11, 17, 4, 0, 16),
	#                                     u'geiselgerda@junck.de']}}})

	fake.pydecimal(left_digits=None, right_digits=None, positive=False)
	# Decimal('4.28995065838E+12')

	fake.pylist(nb_elements=10, variable_nb_elements=True, *value_types)
	# [   u'frederik52@hotmail.de',
	#     u'bpaffrath@misicher.de',
	#     2771,
	#     4485,
	#     Decimal('-97396.8967015'),
	#     u'Vitae dolores id.',
	#     u'jopichmarie-theres@gmx.de']

	fake.pytuple(nb_elements=10, variable_nb_elements=True, *value_types)
	# (   392,
	#     datetime(2010, 5, 24, 9, 56, 26),
	#     u'hendriksjosefa@gmail.com',
	#     u'Aut iste hic et.',
	#     7027,
	#     2388,
	#     Decimal('-63291288.0'),
	#     495)

	fake.pybool()
	# True

	fake.pyset(nb_elements=10, variable_nb_elements=True, *value_types)
	# set([u'Velit voluptate.', u'http://ring.de/', Decimal('-90896439920.9'), Decimal('0.76878'), u'Nobis aspernatur.', u'francescahauffer@zimmer.de', u'Facere qui quo et.', u'Modi aspernatur.'])

	fake.pydict(nb_elements=10, variable_nb_elements=True, *value_types)
	# {   u'et': u'Incidunt optio.',
	#     u'eum': u'Perspiciatis quis.',
	#     u'fugiat': Decimal('17.24032925'),
	#     u'in': Decimal('56589.5482713'),
	#     u'minima': u'Veritatis qui et.',
	#     u'molestiae': u'albrechtwagner@pergande.de',
	#     u'nam': u'Similique id modi.',
	#     u'non': 4512,
	#     u'provident': 9436,
	#     u'quis': 349951773916050.0,
	#     u'tempore': datetime(1994, 6, 24, 9, 2, 35)}

	fake.pyint()
	# 412

``faker.providers.ssn``
-----------------------

::

	fake.ssn()
	# u'749-53-0685'

``faker.providers.user_agent``
------------------------------

::

	fake.mac_processor()
	# u'U; PPC'

	fake.firefox()
	# u'Mozilla/5.0 (Windows NT 6.1; sl-SI; rv:1.9.2.20) Gecko/2015-02-17 00:55:57 Firefox/9.0'

	fake.linux_platform_token()
	# u'X11; Linux x86_64'

	fake.opera()
	# u'Opera/9.94.(Windows NT 4.0; en-US) Presto/2.9.188 Version/11.00'

	fake.windows_platform_token()
	# u'Windows NT 5.1'

	fake.internet_explorer()
	# u'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/4.0)'

	fake.user_agent()
	# u'Opera/8.21.(X11; Linux x86_64; it-IT) Presto/2.9.173 Version/12.00'

	fake.chrome()
	# u'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5310 (KHTML, like Gecko) Chrome/14.0.860.0 Safari/5310'

	fake.linux_processor()
	# u'i686'

	fake.mac_platform_token()
	# u'Macintosh; Intel Mac OS X 10_7_2'

	fake.safari()
	# u'Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/533.18.2 (KHTML, like Gecko) Version/4.0.4 Safari/533.18.2'
