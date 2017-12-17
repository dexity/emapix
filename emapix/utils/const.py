# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

OK = 'ok'
FAIL = 'fail'

PASSWORD_REGEX = '^[A-Za-z0-9]{6,30}$'  # XXX: Change password regex
USERNAME_REGEX = '^[A-Za-z0-9]{5,}$'
REQ_REGEX = '(\w{16})'
LOC_REGEX = '[^/]{,64}'   # Regex for city or country

IMAGE_CONTENT_TYPES = [
    'image/jpeg',
    'image/png'
]

IMAGE_TYPES = {
    'image/jpeg': 'jpg',
    'image/png': 'png'
}

IMAGE_FORMATS = {
    'jpg': ('image/jpeg', 'JPEG'),
    'png': ('image/png', 'PNG')
}

# See: https://developers.google.com/appengine/docs/python/images/functions
MAX_SERVING_SIZE = 600


GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('n', 'Rather not say')
)

STATUS_CHOICES = (
    ('n', 'Not Active'),
    ('a', 'Active'),
    ('w', 'Waiting'),   # waiting confirmation
    ('p', 'New Password'),
    ('b', 'Banned'),
)

REQ_STATUS_CHOICES = [
    ('o', 'Open'),
    ('c', 'Closed'),
]

SHORT_REQ_STATUS = {
    'open':     'o',
    'close':    'c'
}

PHOTO_CHOICES = [
    ('request', 'Request Photo'),
    ('preview', 'Photo Preview'),
    ('crop', 'Photo Crop'),
    ('profile', 'Profile Photo')
]

IMAGE_SIZES = [
    ('tiny', 'Tiny'),
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
    ('jumbo', 'Jumbo')
]

MONTH_CHOICES = [
    ('', 'Month'),
    ('JAN', 'January'),
    ('FEB', 'February'),
    ('MAR', 'March'),
    ('APR', 'April'),
    ('MAY', 'May'),
    ('JUN', 'June'),
    ('JUL', 'July'),
    ('AUG', 'August'),
    ('SEP', 'September'),
    ('OCT', 'October'),
    ('NOV', 'November'),
    ('DEC', 'December')
]


def month_days(days):
    return [(str(x), str(x)) for x in range(1, days + 1)]


DAY_CHOICES = {
    'JAN':  month_days(31),
    'FEB':  month_days(29),
    'MAR':  month_days(31),
    'APR':  month_days(30),
    'MAY':  month_days(31),
    'JUN':  month_days(30),
    'JUL':  month_days(31),
    'AUG':  month_days(31),
    'SEP':  month_days(30),
    'OCT':  month_days(31),
    'NOV':  month_days(30),
    'DEC':  month_days(31),
}

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

YEAR_CHOICES = [(str(x), str(x)) for x in range(2006, 1899, -1)]

AUTH_ERROR = 'Please <a href="/login">login</a> or <a href="/join">sign up</a>'
AUTH_ERROR_TXT = 'You need to be logged in'
AUTHOR_ERROR = "You don't have permission"
METHOD_ERROR = 'Method is not supported'

COUNTRY_CHOICES = [
    ('AF', 'Afghanistan'),
    ('AX', 'Aland Islands'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua And Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo, the Democratic Republic of the'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('CI', "Côte d'Ivoire"),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GG', 'Guernsey'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HM', 'Heard and McDonald Islands'),
    ('VA', 'Holy See (Vatican City State)'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran, Islamic Republic of'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JE', 'Jersey'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', "Korea, Democratic People's Republic of"),
    ('KR', 'Korea, Republic of'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', "Lao People's Democratic Republic"),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libyan Arab Jamahiriya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macao'),
    ('MK', 'Macedonia'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia, Federated States of'),
    ('MD', 'Moldova, Republic of'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PS', 'Palestinian Territory, Occupied'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('RE', 'Réunion'),
    ('BL', 'Saint Barthelemy'),
    ('SH', 'Saint Helena'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin'),
    ('PM', 'Saint Pierre and Miquelon'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('GS', 'South Georgia and the South Sandwich Islands'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SJ', 'Svalbard and Jan Mayen'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('ST', 'São Tome and Principe'),
    ('TW', 'Taiwan, Province of China'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania, United Republic of'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom'),
    ('US', 'United States'),
    ('UM', 'United States Minor Outlying Islands'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands, British'),
    ('VI', 'Virgin Islands, U.S.'),
    ('WF', 'Wallis and Futuna'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
]
