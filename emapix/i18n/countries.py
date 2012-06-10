
"""
ISO 3166 Country Codes
    http://en.wikipedia.org/wiki/ISO_3166-1
    
ISO 4217 Currency Information
    http://www.xe.com/iso4217.php
    http://www.xe.com/symbols.php

"""


COUNTRIES   = {
    "AD": {
        "alpha2": "AD",
        "name": "Andorra",
        "alpha3": "AND",
        "currency": {
            "code": "EUR",
            "symbol": "€",
            "name": "Euro",
            "unicode_hex": 0x20ac,
        }
    },
    "AE": {
        "alpha2": "AE",
        "name": "United Arab Emirates",
        "alpha3": "ARE",
        "currency": {
            "code": "AED",
            "name": "Dirhams",
        }
    },
    "AF": {
        "alpha2": "AF",
        "name": "Afghanistan",
        "alpha3": "AFG",
        "currency": {
            "code": "AFN",
            "symbol": "؋",
            "name": "Afghanis",
            "unicode_hex": 0x60b,
        }
    },
    "AG": {
        "alpha2": "AG",
        "name": "Antigua And Barbuda",
        "alpha3": "ATG",
        "currency": {}
    },
    "AI": {
        "alpha2": "AI",
        "name": "Anguilla",
        "alpha3": "AIA",
        "currency": {
            "code": "XCD",
            "name": "East Caribbean Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "AL": {
        "alpha2": "AL",
        "name": "Albania",
        "alpha3": "ALB",
        "currency": {
            "code": "ALL",
            "symbol": "LEK",
            "name": "Leke",
            "unicode_hex": [0x4c, 0x65, 0x6b],
        }
    },
    "AM": {
        "alpha2": "AM",
        "name": "Armenia",
        "alpha3": "ARM",
        "currency": {
            "code": "AMD",
            "name": "Drams",
        }
    },
    "AN": {
        "alpha2": "AN",
        "name": "Netherlands Antilles",
        "alpha3": "ANT",
        "currency": {
            "code": "ANG",
            "name": "Guilders",
            "symbol": "ƒ",
            "unicode_hex": 0x192,
        }
    },
    "AO": {
        "alpha2": "AO",
        "name": "Angola",
        "alpha3": "AGO",
        "currency": {
            "code": "AOA",
            "name": "Kwanza",
        }
    },
    "AQ": {
        "alpha2": "AQ",
        "name": "Antarctica",
        "alpha3": "ATA",
        "currency": {}
    },
    "AR": {
        "alpha2": "AR",
        "name": "Argentina",
        "alpha3": "ARG",
        "currency": {
            "code": "ARS",
            "symbol": "$",
            "name": "Pesos",
        }
    },
    "AS": {
        "alpha2": "AS",
        "name": "American Samoa",
        "alpha3": "ASM",
        "currency": {}
    },
    "AT": {
        "alpha2": "AT",
        "name": "Austria",
        "alpha3": "AUT",
        "currency": {}
    },
    "AU": {
        "alpha2": "AU",
        "name": "Australia",
        "alpha3": "AUS",
        "currency": {
            "code": "AUD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "AW": {
        "alpha2": "AW",
        "name": "Aruba",
        "alpha3": "ABW",
        "currency": {
            "code": "AWG",
            "name": "Guilders",
            "alt_name": "Florins",
            "symbol": "ƒ",
            "unicode_hex": 0x192,
        }
    },
    "AX": {
        "alpha2": "AX",
        "name": "Aland Islands",
        "alpha3": "ALA",
        "currency": {}
    },
    "AZ": {
        "alpha2": "AZ",
        "name": "Azerbaijan",
        "alpha3": "AZ",
        "currency": {
            "code": "AZN",
            "name": "New Manats",
            "symbol": "ман",
            "unicode_hex": [0x43c, 0x430, 0x43d],
        }
    },
    "BA": {
        "alpha2": "BA",
        "name": "Bosnia and Herzegovina",
        "alpha3": "BIH",
        "currency": {
            "code": "BAM",
            "name": "Convertible Marka",
            "symbol": "KM",
            "unicode_hex": [0x4b, 0x4d],
        }
    },
    "BB": {
        "alpha2": "BB",
        "name": "Barbados",
        "alpha3": "BRB",
        "currency": {
            "code": "BBD",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "BD": {
        "alpha2": "BD",
        "name": "Bangladesh",
        "alpha3": "BGD",
        "currency": {
            "code": "BTD",
            "name": "Taka",
        }
    },
    "BE": {
        "alpha2": "BE",
        "name": "Belgium",
        "alpha3": "BEL",
        "currency": {}
    },
    "BF": {
        "alpha2": "BF",
        "name": "Burkina Faso",
        "alpha3": "BFA",
        "currency": {}
    },
    "BG": {
        "alpha2": "BG",
        "name": "Bulgaria",
        "alpha3": "BGR",
        "currency": {
            "code": "BGN",
            "name": "Leva",
            "symbol": "лв",
            "unicode_hex": [0x52, 0x432],
        }
    },
    "BH": {
        "alpha2": "BH",
        "name": "Bahrain",
        "alpha3": "BHR",
        "currency": {
            "code": "BHD",
            "name": "Dinars",
        }
    },
    "BI": {
        "alpha2": "BI",
        "name": "Burundi",
        "alpha3": "BDI",
        "currency": {
            "code": "BIF",
            "name": "Francs",
        }
    },
    "BJ": {
        "alpha2": "BJ",
        "name": "Benin",
        "alpha3": "BEN",
        "currency": {
            "code": "XOF",
            "name": "Communauté Financière Africaine Francs",
        }
    },
    "BL": {
        "alpha2": "BL",
        "name": "Saint Barthelemy",
        "alpha3": "BLM",
        "currency": {}
    },
    "BM": {
        "alpha2": "BM",
        "name": "Bermuda",
        "alpha3": "BMU",
        "currency": {
            "code": "BMD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "BN": {
        "alpha2": "BN",
        "name": "Brunei Darussalam",
        "alpha3": "BRN",
        "currency": {
            "code": "BND",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "BO": {
        "alpha2": "BO",
        "name": "Bolivia",
        "alpha3": "BOL",
        "currency": {
            "code": "BOB",
            "name": "Bolivianos",
            "symbol": "$b",
            "unicode_hex": [0x24, 0x62],
        }
    },
    "BR": {
        "alpha2": "BR",
        "name": "Brazil",
        "alpha3": "BRA",
        "currency": {
            "code": "BRL",
            "name": "Real",
            "symbol": "R$",
            "unicode_hex": [0x52, 0x24],
        }
    },
    "BS": {
        "alpha2": "BS",
        "name": "Bahamas",
        "alpha3": "BHS",
        "currency": {
            "code": "BSD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "BT": {
        "alpha2": "BT",
        "name": "Bhutan",
        "alpha3": "BTN",
        "currency": {
            "code": "BTN",
            "name": "Ngultrum",
        }
    },
    "BV": {
        "alpha2": "BV",
        "name": "Bouvet Island",
        "alpha3": "BVT",
        "currency": {}
    },
    "BW": {
        "alpha2": "BW",
        "name": "Botswana",
        "alpha3": "BWA",
        "currency": {
            "code": "BWP",
            "name": "Pulas",
            "symbol": "P",
            "unicode_hex": 0x50,
        }
    },
    "BY": {
        "alpha2": "BY",
        "name": "Belarus",
        "alpha3": "BLR",
        "currency": {
            "code": "BYR",
            "name": "Rubles",
            "symbol": "p.",
            "unicode_hex": [0x70, 0x2e],
        }
    },
    "BZ": {
        "alpha2": "BZ",
        "name": "Belize",
        "alpha3": "BLZ",
        "currency": {
            "code": "BZD",
            "name": "Dollars",
            "symbol": "BZ$",
            "unicode_hex": [0x42, 0x5a, 0x24],
        }
    },
    "CA": {
        "alpha2": "CA",
        "name": "Canada",
        "alpha3": "CAN",
        "currency": {
            "code": "CAD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "CC": {
        "alpha2": "CC",
        "name": "Cocos (Keeling) Islands",
        "alpha3": "CCK",
        "currency": {}
    },
    "CD": {
        "alpha2": "CD",
        "name": "Congo, the Democratic Republic of the",
        "alpha3": "COD",
        "currency": {}
    },
    "CF": {
        "alpha2": "CF",
        "name": "Central African Republic",
        "alpha3": "CAF",
        "currency": {}
    },
    "CG": {
        "alpha2": "CG",
        "name": "Congo",
        "alpha3": "COG",
        "currency": {}
    },
    "CH": {
        "alpha2": "CH",
        "name": "Switzerland",
        "alpha3": "CHE",
        "currency": {
            "code": "CHF",
            "name": "Switzerland Francs",
            "symbol": "CHF",
            "unicode_hex": [0x43, 0x48, 0x46],
        }
    },
    "CI": {
        "alpha2": "CI",
        "name": "Côte d'Ivoire",
        "alpha3": "CIV",
        "currency": {}
    },
    "CK": {
        "alpha2": "CK",
        "name": "Cook Islands",
        "alpha3": "COK",
        "currency": {}
    },
    "CL": {
        "alpha2": "CL",
        "name": "Chile",
        "alpha3": "CHL",
        "currency": {
            "code": "CLP",
            "name": "Pesos",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "CM": {
        "alpha2": "CM",
        "name": "Cameroon",
        "alpha3": "CMR",
        "currency": {
            "code": "XAF",
            "name": "Communauté Financière Africaine Francs",
        }
    },
    "CN": {
        "alpha2": "CN",
        "name": "China",
        "alpha3": "CHN",
        "currency": {
            "code": "CNY",
            "name": "Yuan Renminbi",
            "symbol": "¥",
            "unicode_hex": 0xa5,
        }
    },
    "CO": {
        "alpha2": "CO",
        "name": "Colombia",
        "alpha3": "COL",
        "currency": {
            "code": "COP",
            "name": "Pesos",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "CR": {
        "alpha2": "CR",
        "name": "Costa Rica",
        "alpha3": "CRI",
        "currency": {
            "code": "CRC",
            "name": "Colones",
            "symbol": "₡",
            "unicode_hex": 0x20a1,
        }
    },
    "CU": {
        "alpha2": "CU",
        "name": "Cuba",
        "alpha3": "CUB",
        "currency": {
            "code": "CUP",
            "name": "Pesos",
            "symbol": "₱",
            "unicode_hex": 0x20b1,
        }
    },
    "CV": {
        "alpha2": "CV",
        "name": "Cape Verde",
        "alpha3": "CPV",
        "currency": {
            "code": "CVE",
            "name": "Escudos",
        }
    },
    "CX": {
        "alpha2": "CX",
        "name": "Christmas Island",
        "alpha3": "CXR",
        "currency": {}
    },
    "CY": {
        "alpha2": "CY",
        "name": "Cyprus",
        "alpha3": "CYP",
        "currency": {}
    },
    "CZ": {
        "alpha2": "CZ",
        "name": "Czech Republic",
        "alpha3": "CZE",
        "currency": {
            "code": "CZK",
            "name": "Koruny",
            "symbol": "Kč",
            "unicode_hex": [0x4b, 0x10d],
        }
    },
    "DE": {
        "alpha2": "DE",
        "name": "Germany",
        "alpha3": "DEU",
        "currency": {}
    },
    "DJ": {
        "alpha2": "DJ",
        "name": "Djibouti",
        "alpha3": "DJI",
        "currency": {
            "code": "DJF",
            "name": "Francs",
        }
    },
    "DK": {
        "alpha2": "DK",
        "name": "Denmark",
        "alpha3": "DNK",
        "currency": {
            "code": "DKK",
            "name": "Kroner",
            "symbol": "kr",
            "unicode_hex": [0x6b, 0x72],
        }
    },
    "DM": {
        "alpha2": "DM",
        "name": "Dominica",
        "alpha3": "DMA",
        "currency": {}
    },
    "DO": {
        "alpha2": "DO",
        "name": "Dominican Republic",
        "alpha3": "DOM",
        "currency": {
            "code": "DOP",
            "name": "Pesos",
            "symbol": "RD$",
            "unicode_hex": [0x52, 0x44, 0x24],
        }
    },
    "DZ": {
        "alpha2": "DZ",
        "name": "Algeria",
        "alpha3": "DZA",
        "currency": {
            "code": "DZD",
            "name": "Dinars",
        }
    },
    "EC": {
        "alpha2": "EC",
        "name": "Ecuador",
        "alpha3": "ECU",
        "currency": {}
    },
    "EE": {
        "alpha2": "EE",
        "name": "Estonia",
        "alpha3": "EST",
        "currency": {
            "code": "EEK",
            "name": "Krooni",
            "symbol": "kr",
            "unicode_hex": [0x6b, 0x72],
        }
    },
    "EG": {
        "alpha2": "EG",
        "name": "Egypt",
        "alpha3": "EGY",
        "currency": {
            "code": "EGP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "EH": {
        "alpha2": "EH",
        "name": "Western Sahara",
        "alpha3": "ESH",
        "currency": {}
    },
    "ER": {
        "alpha2": "ER",
        "name": "Eritrea",
        "alpha3": "ERI",
        "currency": {
            "code": "ETB",
            "name": "Ethopia Birr",
        }
    },
    "ES": {
        "alpha2": "ES",
        "name": "Spain",
        "alpha3": "ESP",
        "currency": {}
    },
    "ET": {
        "alpha2": "ET",
        "name": "Ethiopia",
        "alpha3": "ETH",
        "currency": {}
    },
    "FI": {
        "alpha2": "FI",
        "name": "Finland",
        "alpha3": "FIN",
        "currency": {}
    },
    "FJ": {
        "alpha2": "FJ",
        "name": "Fiji",
        "alpha3": "FJI",
        "currency": {}
    },
    "FK": {
        "alpha2": "FK",
        "name": "Falkland Islands (Malvinas)",
        "alpha3": "FLK",
        "currency": {
            "code": "FKP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "FM": {
        "alpha2": "FM",
        "name": "Micronesia, Federated States of",
        "alpha3": "FSM",
        "currency": {}
    },
    "FO": {
        "alpha2": "FO",
        "name": "Faroe Islands",
        "alpha3": "FRO",
        "currency": {}
    },
    "FR": {
        "alpha2": "FR",
        "name": "France",
        "alpha3": "FRA",
        "currency": {}
    },
    "GA": {
        "alpha2": "GA",
        "name": "Gabon",
        "alpha3": "GAB",
        "currency": {}
    },
    "GB": {
        "alpha2": "GB",
        "name": "United Kingdom",
        "alpha3": "GBR",
        "currency": {
            "code": "GBP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "GD": {
        "alpha2": "GD",
        "name": "Grenada",
        "alpha3": "GRD",
        "currency": {}
    },
    "GE": {
        "alpha2": "GE",
        "name": "Georgia",
        "alpha3": "GEO",
        "currency": {
            "code": "GEL",
            "name": "Lari",
        }
    },
    "GF": {
        "alpha2": "GF",
        "name": "French Guiana",
        "alpha3": "GUF",
        "currency": {}
    },
    "GG": {
        "alpha2": "GG",
        "name": "Guernsey",
        "alpha3": "GGY",
        "currency": {
            "code": "GGP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "GH": {
        "alpha2": "GH",
        "name": "Ghana",
        "alpha3": "GHA",
        "currency": {
            "code": "GHS",
            "name": "Cedis",
            "symbol": "¢",
            "unicode_hex": 0xa2,
        }
    },
    "GI": {
        "alpha2": "GI",
        "name": "Gibraltar",
        "alpha3": "GIB",
        "currency": {
            "code": "GIP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "GL": {
        "alpha2": "GL",
        "name": "Greenland",
        "alpha3": "GRL",
        "currency": {}
    },
    "GM": {
        "alpha2": "GM",
        "name": "Gambia",
        "alpha3": "GMB",
        "currency": {
            "code": "GMD",
            "name": "Lari",
        }
    },
    "GN": {
        "alpha2": "GN",
        "name": "Guinea",
        "alpha3": "GIN",
        "currency": {
            "code": "GNF",
            "name": "Francs",
        }
    },
    "GP": {
        "alpha2": "GP",
        "name": "Guadeloupe",
        "alpha3": "GLP",
        "currency": {}
    },
    "GQ": {
        "alpha2": "GQ",
        "name": "Equatorial Guinea",
        "alpha3": "GNQ",
        "currency": {}
    },
    "GR": {
        "alpha2": "GR",
        "name": "Greece",
        "alpha3": "GRC",
        "currency": {}
    },
    "GS": {
        "alpha2": "GS",
        "name": "South Georgia and the South Sandwich Islands",
        "alpha3": "SGS",
        "currency": {}
    },
    "GT": {
        "alpha2": "GT",
        "name": "Guatemala",
        "alpha3": "GTM",
        "currency": {
            "code": "GTQ",
            "name": "Quetzales",
            "symbol": "Q",
            "unicode_hex": 0x51,
        }
    },
    "GU": {
        "alpha2": "GU",
        "name": "Guam",
        "alpha3": "GUM",
        "currency": {}
    },
    "GW": {
        "alpha2": "GW",
        "name": "Guinea-Bissau",
        "alpha3": "GNB",
        "currency": {}
    },
    "GY": {
        "alpha2": "GY",
        "name": "Guyana",
        "alpha3": "GUY",
        "currency": {
            "code": "GYD",
            "name": "Dollars",
        }
    },
    "HK": {
        "alpha2": "HK",
        "name": "Hong Kong",
        "alpha3": "HKG",
        "currency": {
            "code": "HKD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "HM": {
        "alpha2": "HM",
        "name": "Heard and McDonald Islands",
        "alpha3": "HMD",
        "currency": {}
    },
    "HN": {
        "alpha2": "HN",
        "name": "Honduras",
        "alpha3": "HND",
        "currency": {
            "code": "HNL",
            "name": "Lempiras",
            "symbol": "L",
            "unicode_hex": 0x4c,
        }
    },
    "HR": {
        "alpha2": "HR",
        "name": "Croatia",
        "alpha3": "HRV",
        "currency": {
            "code": "HRK",
            "name": "Kuna",
            "symbol": "kn",
            "unicode_hex": [0x6b, 0x6e],
        }
    },
    "HT": {
        "alpha2": "HT",
        "name": "Haiti",
        "alpha3": "HTI",
        "currency": {}
    },
    "HU": {
        "alpha2": "HU",
        "name": "Hungary",
        "alpha3": "HUN",
        "currency": {
            "code": "HUF",
            "name": "Forint",
            "symbol": "Ft",
            "unicode_hex": [0x46, 0x74],
        }
    },
    "ID": {
        "alpha2": "ID",
        "name": "Indonesia",
        "alpha3": "IDN",
        "currency": {
            "code": "IDR",
            "name": "Indonesian Rupiahs",
            "symbol": "Rp",
            "unicode_hex": [0x52, 0x70],
        }
    },
    "IE": {
        "alpha2": "IE",
        "name": "Ireland",
        "alpha3": "IRL",
        "currency": {}
    },
    "IL": {
        "alpha2": "IL",
        "name": "Israel",
        "alpha3": "ISR",
        "currency": {
            "code": "ILS",
            "name": "New Shekels",
            "symbol": "₪",
            "unicode_hex": 0x20aa,
        }
    },
    "IM": {
        "alpha2": "IM",
        "name": "Isle of Man",
        "alpha3": "IMN",
        "currency": {
            "code": "IMP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "IN": {
        "alpha2": "IN",
        "name": "India",
        "alpha3": "IND",
        "currency": {
            "code": "INR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "IO": {
        "alpha2": "IO",
        "name": "British Indian Ocean Territory",
        "alpha3": "IOT",
        "currency": {}
    },
    "IQ": {
        "alpha2": "IQ",
        "name": "Iraq",
        "alpha3": "IRQ",
        "currency": {
            "code": "IQD",
            "name": "Dinars",
        }
    },
    "IR": {
        "alpha2": "IR",
        "name": "Iran, Islamic Republic of",
        "alpha3": "IRN",
        "currency": {
            "code": "IRR",
            "name": "Riais",
            "symbol": "﷼",
            "unicode_hex": 0xfdfc,
        }
    },
    "IS": {
        "alpha2": "IS",
        "name": "Iceland",
        "alpha3": "ISL",
        "currency": {
            "code": "ISK",
            "name": "Kronur",
            "symbol": "kr",
            "unicode_hex": [0x6b, 0x72],
        }
    },
    "IT": {
        "alpha2": "IT",
        "name": "Italy",
        "alpha3": "ITA",
        "currency": {}
    },
    "JE": {
        "alpha2": "JE",
        "name": "Jersey",
        "alpha3": "JEY",
        "currency": {
            "code": "JEP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "JM": {
        "alpha2": "JM",
        "name": "Jamaica",
        "alpha3": "JAM",
        "currency": {
            "code": "JMD",
            "name": "Dollars",
        }
    },
    "JO": {
        "alpha2": "JO",
        "name": "Jordan",
        "alpha3": "JOR",
        "currency": {
            "code": "JOD",
            "name": "Dinars",
        }
    },
    "JP": {
        "alpha2": "JP",
        "name": "Japan",
        "alpha3": "JPN",
        "currency": {
            "code": "JPY",
            "name": "Yen",
            "symbol": "¥",
            "unicode_hex": 0xa5,
        }
    },
    "KE": {
        "alpha2": "KE",
        "name": "Kenya",
        "alpha3": "KEN",
        "currency": {
            "code": "KES",
            "name": "Shillings",
        }
    },
    "KG": {
        "alpha2": "KG",
        "name": "Kyrgyzstan",
        "alpha3": "KGZ",
        "currency": {
            "code": "KGS",
            "name": "Soms",
            "symbol": "лв",
            "unicode_hex": [0x43b, 0x432],
        }
    },
    "KH": {
        "alpha2": "KH",
        "name": "Cambodia",
        "alpha3": "KHM",
        "currency": {
            "code": "KHR",
            "name": "Rieis",
        }
    },
    "KI": {
        "alpha2": "KI",
        "name": "Kiribati",
        "alpha3": "KIR",
        "currency": {}
    },
    "KM": {
        "alpha2": "KM",
        "name": "Comoros",
        "alpha3": "COM",
        "currency": {
            "code": "KMF",
            "name": "Francs",
        }
    },
    "KN": {
        "alpha2": "KN",
        "name": "Saint Kitts and Nevis",
        "alpha3": "KNA",
        "currency": {}
    },
    "KP": {
        "alpha2": "KP",
        "name": "Korea, Democratic People's Republic of",
        "alpha3": "PRK",
        "currency": {
            "code": "KPW",
            "name": "Won",
            "symbol": "₩",
            "unicode_hex": 0x20a9,
        }
    },
    "KR": {
        "alpha2": "KR",
        "name": "Korea, Republic of",
        "alpha3": "KOR",
        "currency": {
            "code": "KRW",
            "name": "Won",
            "symbol": "₩",
            "unicode_hex": 0x20a9,
        }
    },
    "KW": {
        "alpha2": "KW",
        "name": "Kuwait",
        "alpha3": "KWT",
        "currency": {
            "code": "KWD",
            "name": "Dinars",
        }
    },
    "KY": {
        "alpha2": "KY",
        "name": "Cayman Islands",
        "alpha3": "CYM",
        "currency": {
            "code": "KYD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "KZ": {
        "alpha2": "KZ",
        "name": "Kazakhstan",
        "alpha3": "KAZ",
        "currency": {
            "code": "KZT",
            "name": "Tenege",
            "symbol": "лв",
            "unicode_hex": [0x43b, 0x432],
        }
    },
    "LA": {
        "alpha2": "LA",
        "name": "Lao People's Democratic Republic",
        "alpha3": "LAO",
        "currency": {
            "code": "LAK",
            "name": "Kips",
            "symbol": "₭",
            "unicode_hex": 0x20ad,
        }
    },
    "LB": {
        "alpha2": "LB",
        "name": "Lebanon",
        "alpha3": "LBN",
        "currency": {
            "code": "LBP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "LC": {
        "alpha2": "LC",
        "name": "Saint Lucia",
        "alpha3": "LCA",
        "currency": {}
    },
    "LI": {
        "alpha2": "LI",
        "name": "Liechtenstein",
        "alpha3": "LIE",
        "currency": {}
    },
    "LK": {
        "alpha2": "LK",
        "name": "Sri Lanka",
        "alpha3": "LKA",
        "currency": {
            "code": "LKR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "LR": {
        "alpha2": "LR",
        "name": "Liberia",
        "alpha3": "LBR",
        "currency": {
            "code": "LRD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "LS": {
        "alpha2": "LS",
        "name": "Lesotho",
        "alpha3": "LSO",
        "currency": {
            "code": "LSL",
            "name": "Maloti",
            "alt_currency": "*zar",
        }
    },
    "LT": {
        "alpha2": "LT",
        "name": "Lithuania",
        "alpha3": "LTU",
        "currency": {
            "code": "LTL",
            "name": "Litai",
            "symbol": "Lt",
            "unicode_hex": [0x4c, 0x74],
        }
    },
    "LU": {
        "alpha2": "LU",
        "name": "Luxembourg",
        "alpha3": "LUX",
        "currency": {}
    },
    "LV": {
        "alpha2": "LV",
        "name": "Latvia",
        "alpha3": "LVA",
        "currency": {
            "code": "LVL",
            "name": "Lati",
            "symbol": "Ls",
            "unicode_hex": [0x4c, 0x73],
        }
    },
    "LY": {
        "alpha2": "LY",
        "name": "Libyan Arab Jamahiriya",
        "alpha3": "LBY",
        "currency": {
            "code": "LYD",
            "name": "Dinars",
        }
    },
    "MA": {
        "alpha2": "MA",
        "name": "Morocco",
        "alpha3": "MAR",
        "currency": {
            "code": "MAD",
            "name": "Dirhams",
        }
    },
    "MC": {
        "alpha2": "MC",
        "name": "Monaco",
        "alpha3": "MCO",
        "currency": {}
    },
    "MD": {
        "alpha2": "MD",
        "name": "Moldova, Republic of",
        "alpha3": "MDA",
        "currency": {
            "code": "MDL",
            "name": "Lei",
        }
    },
    "ME": {
        "alpha2": "ME",
        "name": "Montenegro",
        "alpha3": "MNE",
        "currency": {}
    },
    "MF": {
        "alpha2": "MF",
        "name": "Saint Martin",
        "alpha3": "MAF",
        "currency": {}
    },
    "MG": {
        "alpha2": "MG",
        "name": "Madagascar",
        "alpha3": "MDG",
        "currency": {}
    },
    "MH": {
        "alpha2": "MH",
        "name": "Marshall Islands",
        "alpha3": "MHL",
        "currency": {}
    },
    "MK": {
        "alpha2": "MK",
        "name": "Macedonia",
        "alpha3": "MKD",
        "currency": {
            "code": "MKD",
            "name": "Denars",
            "symbol": "ден",
            "unicode_hex": [0x434, 0x435, 0x43d],
        }
    },
    "ML": {
        "alpha2": "ML",
        "name": "Mali",
        "alpha3": "MLI",
        "currency": {}
    },
    "MM": {
        "alpha2": "MM",
        "name": "Myanmar",
        "alpha3": "MMR",
        "currency": {
            "code": "MNK",
            "name": "Kyats",
        }
    },
    "MN": {
        "alpha2": "MN",
        "name": "Mongolia",
        "alpha3": "MNG",
        "currency": {
            "code": "MNT",
            "name": "Tugriks",
            "symbol": "₮",
            "unicode_hex": 0x20ae,
        }
    },
    "MO": {
        "alpha2": "MO",
        "name": "Macao",
        "alpha3": "MAC",
        "currency": {}
    },
    "MP": {
        "alpha2": "MP",
        "name": "Northern Mariana Islands",
        "alpha3": "MNP",
        "currency": {}
    },
    "MQ": {
        "alpha2": "MQ",
        "name": "Martinique",
        "alpha3": "MTQ",
        "currency": {}
    },
    "MR": {
        "alpha2": "MR",
        "name": "Mauritania",
        "alpha3": "MRT",
        "currency": {
            "code": "MRO",
            "name": "Ouguiyas",
        }
    },
    "MS": {
        "alpha2": "MS",
        "name": "Montserrat",
        "alpha3": "MSR",
        "currency": {}
    },
    "MT": {
        "alpha2": "MT",
        "name": "Malta",
        "alpha3": "MLT",
        "currency": {}
    },
    "MU": {
        "alpha2": "MU",
        "name": "Mauritius",
        "alpha3": "MUS",
        "currency": {
            "code": "MUR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "MV": {
        "alpha2": "MV",
        "name": "Maldives",
        "alpha3": "MDV",
        "currency": {
            "code": "MVR",
            "name": "Rufiyaa",
        }
    },
    "MW": {
        "alpha2": "MW",
        "name": "Malawi",
        "alpha3": "MWI",
        "currency": {
            "code": "MWK",
            "name": "Kwachas",
        }
    },
    "MX": {
        "alpha2": "MX",
        "name": "Mexico",
        "alpha3": "MEX",
        "currency": {
            "code": "MXN",
            "name": "Pesos",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "MY": {
        "alpha2": "MY",
        "name": "Malaysia",
        "alpha3": "MYS",
        "currency": {
            "code": "MYR",
            "name": "Ringgits",
            "symbol": "RM",
            "unicode_hex": [0x52, 0x4d],
        }
    },
    "MZ": {
        "alpha2": "MZ",
        "name": "Mozambique",
        "alpha3": "MOZ",
        "currency": {
            "code": "MZN",
            "name": "Meticals",
            "symbol": "MT",
            "unicode_hex": [0x4d, 0x54],
        }
    },
    "NA": {
        "alpha2": "NA",
        "name": "Namibia",
        "alpha3": "NAM",
        "currency": {
            "code": "NAD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
            "alt_currency": "*zar",
        }
    },
    "NC": {
        "alpha2": "NC",
        "name": "New Caledonia",
        "alpha3": "NCL",
        "currency": {
            "code": "XPF",
            "name": "Comptoirs Français du Pacifique Francs",
        }
    },
    "NE": {
        "alpha2": "NE",
        "name": "Niger",
        "alpha3": "NER",
        "currency": {}
    },
    "NF": {
        "alpha2": "NF",
        "name": "Norfolk Island",
        "alpha3": "NFK",
        "currency": {}
    },
    "NG": {
        "alpha2": "NG",
        "name": "Nigeria",
        "alpha3": "NGA",
        "currency": {
            "code": "NGN",
            "name": "Nairas",
            "symbol": "₦",
            "unicode_hex": 0x20a6,
        }
    },
    "NI": {
        "alpha2": "NI",
        "name": "Nicaragua",
        "alpha3": "NIC",
        "currency": {
            "code": "NIO",
            "name": "Cordobas",
            "symbol": "C$",
            "unicode_hex": [0x43, 0x24],
        }
    },
    "NL": {
        "alpha2": "NL",
        "name": "Netherlands",
        "alpha3": "NLD",
        "currency": {}
    },
    "NO": {
        "alpha2": "NO",
        "name": "Norway",
        "alpha3": "NOR",
        "currency": {
            "code": "NOK",
            "name": "Kroner",
            "symbol": "kr",
            "unicode_hex": [0x7b, 0x72],
        }
    },
    "NP": {
        "alpha2": "NP",
        "name": "Nepal",
        "alpha3": "NPL",
        "currency": {
            "code": "NPR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "NR": {
        "alpha2": "NR",
        "name": "Nauru",
        "alpha3": "NRU",
        "currency": {}
    },
    "NU": {
        "alpha2": "NU",
        "name": "Niue",
        "alpha3": "NIU",
        "currency": {}
    },
    "NZ": {
        "alpha2": "NZ",
        "name": "New Zealand",
        "alpha3": "NZL",
        "currency": {
            "code": "NZD",
            "name": "New Zealand Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "OM": {
        "alpha2": "OM",
        "name": "Oman",
        "alpha3": "OMN",
        "currency": {
            "code": "OMR",
            "name": "Riais",
            "symbol": "﷼",
            "unicode_hex": 0xfdfc,
        }
    },
    "PA": {
        "alpha2": "PA",
        "name": "Panama",
        "alpha3": "PAN",
        "currency": {
            "code": "PAB",
            "name": "Balboa",
            "symbol": "B/.",
            "unicode_hex": [0x42, 0x2f, 0x2e],
            "alt_currency": "*usd",
        }
    },
    "PE": {
        "alpha2": "PE",
        "name": "Peru",
        "alpha3": "PER",
        "currency": {
            "code": "PEN",
            "name": "Nuevos Soles",
            "symbol": "S/.",
            "unicode_hex": [0x50,0x2f,0x2e],
        }
    },
    "PF": {
        "alpha2": "PF",
        "name": "French Polynesia",
        "alpha3": "PYF",
        "currency": {
            "code": "XPF",
            "name": "Comptoirs Français du Pacifique Francs",
        }
    },
    "PG": {
        "alpha2": "PG",
        "name": "Papua New Guinea",
        "alpha3": "PNG",
        "currency": {
            "code": "PGK",
            "name": "Kina",
        }
    },
    "PH": {
        "alpha2": "PH",
        "name": "Philippines",
        "alpha3": "PHL",
        "currency": {
            "code": "PHP",
            "name": "Pesos",
            "symbol": "Php",
            "unicode_hex": [0x50, 0x68, 0x70],
        }
    },
    "PK": {
        "alpha2": "PK",
        "name": "Pakistan",
        "alpha3": "PAK",
        "currency": {
            "code": "PKR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "PL": {
        "alpha2": "PL",
        "name": "Poland",
        "alpha3": "POL",
        "currency": {
            "code": "PLN",
            "name": "Zlotych",
            "symbol": "zł",
            "unicode_hex": [0x7a, 0x142],
        }
    },
    "PM": {
        "alpha2": "PM",
        "name": "Saint Pierre and Miquelon",
        "alpha3": "SPM",
        "currency": {}
    },
    "PN": {
        "alpha2": "PN",
        "name": "Pitcairn",
        "alpha3": "PCN",
        "currency": {}
    },
    "PR": {
        "alpha2": "PR",
        "name": "Puerto Rico",
        "alpha3": "PRI",
        "currency": {}
    },
    "PS": {
        "alpha2": "PS",
        "name": "Palestinian Territory, Occupied",
        "alpha3": "PSE",
        "currency": {}
    },
    "PT": {
        "alpha2": "PT",
        "name": "Portugal",
        "alpha3": "PRT",
        "currency": {}
    },
    "PW": {
        "alpha2": "PW",
        "name": "Palau",
        "alpha3": "PLW",
        "currency": {}
    },
    "PY": {
        "alpha2": "PY",
        "name": "Paraguay",
        "alpha3": "PRY",
        "currency": {
            "code": "PYG",
            "name": "Guarani",
            "symbol": "Gs",
            "unicode_hex": [0x47, 0x73],
        }
    },
    "QA": {
        "alpha2": "QA",
        "name": "Qatar",
        "alpha3": "QAT",
        "currency": {
            "code": "QAR",
            "name": "Rials",
            "symbol": "﷼",
            "unicode_hex": 0xfdfc,
        }
    },
    "RE": {
        "alpha2": "RE",
        "name": "Réunion",
        "alpha3": "REU",
        "currency": {}
    },
    "RO": {
        "alpha2": "RO",
        "name": "Romania",
        "alpha3": "ROU",
        "currency": {
            "code": "RON",
            "name": "New Lei",
            "symbol": "lei",
            "unicode_hex": [0x6c, 0x65, 0x69],
        }
    },
    "RS": {
        "alpha2": "RS",
        "name": "Serbia",
        "alpha3": "SRB",
        "currency": {
            "code": "RSD",
            "name": "Dinars",
            "symbol": "Дин.",
            "unicode_hex": [0x414, 0x438, 0x43d, 0x2e],
        }
    },
    "RU": {
        "alpha2": "RU",
        "name": "Russian Federation",
        "alpha3": "RUS",
        "currency": {
            "code": "RUB",
            "name": "Rubles",
            "symbol": "руб",
            "unicode_hex": [0x440, 0x443, 0x431],
        }
    },
    "RW": {
        "alpha2": "RW",
        "name": "Rwanda",
        "alpha3": "RWA",
        "currency": {
            "code": "RWF",
            "name": "Francs",
        }
    },
    "SA": {
        "alpha2": "SA",
        "name": "Saudi Arabia",
        "alpha3": "SAU",
        "currency": {
            "code": "SAR",
            "name": "Riyals",
            "symbol": "﷼",
            "unicode_hex": 0xfdfc,
        }
    },
    "SB": {
        "alpha2": "SB",
        "name": "Solomon Islands",
        "alpha3": "SLB",
        "currency": {
            "code": "SBD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "SC": {
        "alpha2": "SC",
        "name": "Seychelles",
        "alpha3": "SYC",
        "currency": {
            "code": "SCR",
            "name": "Rupees",
            "symbol": "₨",
            "unicode_hex": 0x20a8,
        }
    },
    "SD": {
        "alpha2": "SD",
        "name": "Sudan",
        "alpha3": "SDN",
        "currency": {
            "code": "SDG",
            "name": "Pounds",
        }
    },
    "SE": {
        "alpha2": "SE",
        "name": "Sweden",
        "alpha3": "SWE",
        "currency": {
            "code": "SEK",
            "name": "Kronor",
            "symbol": "kr",
            "unicode_hex": [0x6b, 0x72],
        }
    },
    "SG": {
        "alpha2": "SG",
        "name": "Singapore",
        "alpha3": "SGP",
        "currency": {
            "code": "SGD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "SH": {
        "alpha2": "SH",
        "name": "Saint Helena",
        "alpha3": "SHN",
        "currency": {
            "code": "SHP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "SI": {
        "alpha2": "SI",
        "name": "Slovenia",
        "alpha3": "SVN",
        "currency": {}
    },
    "SJ": {
        "alpha2": "SJ",
        "name": "Svalbard and Jan Mayen",
        "alpha3": "SJM",
        "currency": {}
    },
    "SK": {
        "alpha2": "SK",
        "name": "Slovakia",
        "alpha3": "SVK",
        "currency": {}
    },
    "SL": {
        "alpha2": "SL",
        "name": "Sierra Leone",
        "alpha3": "SLE",
        "currency": {
            "code": "SLL",
            "name": "Leones",
        }
    },
    "SM": {
        "alpha2": "SM",
        "name": "San Marino",
        "alpha3": "SMR",
        "currency": {}
    },
    "SN": {
        "alpha2": "SN",
        "name": "Senegal",
        "alpha3": "SEN",
        "currency": {}
    },
    "SO": {
        "alpha2": "SO",
        "name": "Somalia",
        "alpha3": "SOM",
        "currency": {
            "code": "SOS",
            "name": "Shillings",
            "symbol": "S",
            "unicode_hex": 0x53,
        }
    },
    "SR": {
        "alpha2": "SR",
        "name": "Suriname",
        "alpha3": "SUR",
        "currency": {
            "code": "SRD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "ST": {
        "alpha2": "ST",
        "name": "São Tome and Principe",
        "alpha3": "STP",
        "currency": {
            "code": "STD",
            "name": "Dobras",
        }
    },
    "SV": {
        "alpha2": "SV",
        "name": "El Salvador",
        "alpha3": "SLV",
        "currency": {}
    },
    "SY": {
        "alpha2": "SY",
        "name": "Syrian Arab Republic",
        "alpha3": "SYR",
        "currency": {
            "code": "SYP",
            "name": "Pounds",
            "symbol": "£",
            "unicode_hex": 0xa3,
        }
    },
    "SZ": {
        "alpha2": "SZ",
        "name": "Swaziland",
        "alpha3": "SWZ",
        "currency": {
            "code": "SZL",
            "name": "Emalangeni",
        }
    },
    "TC": {
        "alpha2": "TC",
        "name": "Turks and Caicos Islands",
        "alpha3": "TCA",
        "currency": {}
    },
    "TD": {
        "alpha2": "TD",
        "name": "Chad",
        "alpha3": "TCD",
        "currency": {}
    },
    "TF": {
        "alpha2": "TF",
        "name": "French Southern Territories",
        "alpha3": "ATF",
        "currency": {}
    },
    "TG": {
        "alpha2": "TG",
        "name": "Togo",
        "alpha3": "TGO",
        "currency": {}
    },
    "TH": {
        "alpha2": "TH",
        "name": "Thailand",
        "alpha3": "THA",
        "currency": {
            "code": "THB",
            "name": "Baht",
            "symbol": "฿",
            "unicode_hex": 0xe3f,
        }
    },
    "TJ": {
        "alpha2": "TJ",
        "name": "Tajikistan",
        "alpha3": "TJK",
        "currency": {
            "code": "TJS",
            "name": "Somoni",
            "alt_currency": "*rub",
        }
    },
    "TK": {
        "alpha2": "TK",
        "name": "Tokelau",
        "alpha3": "TKL",
        "currency": {}
    },
    "TL": {
        "alpha2": "TL",
        "name": "Timor-Leste",
        "alpha3": "TLS",
        "currency": {}
    },
    "TM": {
        "alpha2": "TM",
        "name": "Turkmenistan",
        "alpha3": "TKM",
        "currency": {}
    },
    "TN": {
        "alpha2": "TN",
        "name": "Tunisia",
        "alpha3": "TUN",
        "currency": {
            "code": "TND",
            "name": "Dollars",
        }
    },
    "TO": {
        "alpha2": "TO",
        "name": "Tonga",
        "alpha3": "TON",
        "currency": {
            "code": "TOP",
            "name": "Pa'anga",
        }
    },
    "TR": {
        "alpha2": "TR",
        "name": "Turkey",
        "alpha3": "TUR",
        "currency": {
            "code": "TRY",
            "name": "Lira",
            "symbol": "TL",
            "unicode_hex": [0x54, 0x4c],
        }
    },
    "TT": {
        "alpha2": "TT",
        "name": "Trinidad and Tobago",
        "alpha3": "TTO",
        "currency": {
            "code": "TTD",
            "name": "Dollars",
            "symbol": "$",
            "unicode_hex": 0x24,
        }
    },
    "TV": {
        "alpha2": "TV",
        "name": "Tuvalu",
        "alpha3": "TUV",
        "currency": {
            "code": "TVD",
            "name": "Tuvalu Dollars",
        }
    },
    "TW": {
        "alpha2": "TW",
        "name": "Taiwan, Province of China",
        "alpha3": "TWN",
        "currency": {
            "code": "TWD",
            "name": "New Dollars",
            "symbol": "NT$",
            "unicode_hex": [0x4e, 0x54, 0x24],
        }
    },
    "TZ": {
        "alpha2": "TZ",
        "name": "Tanzania, United Republic of",
        "alpha3": "TZA",
        "currency": {
            "code": "TZS",
            "name": "Shillings",
        }
    },
    "UA": {
        "alpha2": "UA",
        "name": "Ukraine",
        "alpha3": "UKR",
        "currency": {
            "code": "UAH",
            "name": "Hryvnia",
            "symbol": "₴",
            "unicode_hex": 0x20b4,
        }
    },
    "UG": {
        "alpha2": "UG",
        "name": "Uganda",
        "alpha3": "UGA",
        "currency": {
            "code": "UGX",
            "name": "Shillings",
        }
    },
    "UM": {
        "alpha2": "UM",
        "name": "United States Minor Outlying Islands",
        "alpha3": "UMI",
        "currency": {}
    },
    "US": {
        "alpha2": "US",
        "name": "United States",
        "alpha3": "USA",
        "currency": {
            "code": "USD",
            "symbol": "$",
            "name": "Dollars",
            "unicode_hex": 0x24,
        }
    },
    "UY": {
        "alpha2": "UY",
        "name": "Uruguay",
        "alpha3": "URY",
        "currency": {
            "code": "UYU",
            "name": "Pesos",
            "symbol": "$U",
            "unicode_hex": [0x24, 0x55],
        }
    },
    "UZ": {
        "alpha2": "UZ",
        "name": "Uzbekistan",
        "alpha3": "UZB",
        "currency": {
            "code": "UZS",
            "name": "Sums",
            "symbol": "лв",
            "unicode_hex": [0x43b, 0x432],
        }
    },
    "VA": {
        "alpha2": "VA",
        "name": "Holy See (Vatican City State)",
        "alpha3": "VAT",
        "currency": {}
    },
    "VC": {
        "alpha2": "VC",
        "name": "Saint Vincent and the Grenadines",
        "alpha3": "VCT",
        "currency": {}
    },
    "VE": {
        "alpha2": "VE",
        "name": "Venezuela",
        "alpha3": "VEN",
        "currency": {
            "code": "VEF",
            "name": "Bolivares Fuertes",
            "symbol": "Bs",
            "unicode_hex": [0x43b, 0x432],
        }
    },
    "VG": {
        "alpha2": "VG",
        "name": "Virgin Islands, British",
        "alpha3": "VGB",
        "currency": {}
    },
    "VI": {
        "alpha2": "VI",
        "name": "Virgin Islands, U.S.",
        "alpha3": "VIR",
        "currency": {}
    },
    "VN": {
        "alpha2": "VN",
        "name": "Viet Nam",
        "alpha3": "VNM",
        "currency": {
            "code": "VND",
            "name": "Dong",
            "symbol": "₫",
            "unicode_hex": 0x20ab,
        }
    },
    "VU": {
        "alpha2": "VU",
        "name": "Vanuatu",
        "alpha3": "VUT",
        "currency": {}
    },
    "WF": {
        "alpha2": "WF",
        "name": "Wallis and Futuna",
        "alpha3": "WLF",
        "currency": {}
    },
    "WS": {
        "alpha2": "WS",
        "name": "Samoa",
        "alpha3": "WSM",
        "currency": {}
    },
    "YE": {
        "alpha2": "YE",
        "name": "Yemen",
        "alpha3": "YEM",
        "currency": {
            "code": "YER",
            "name": "Rials",
            "symbol": "﷼",
            "unicode_hex": 0xfdfc,
        }
    },
    "YT": {
        "alpha2": "YT",
        "name": "Mayotte",
        "alpha3": "MYT",
        "currency": {}
    },
    "ZA": {
        "alpha2": "ZA",
        "name": "South Africa",
        "alpha3": "ZAF",
        "currency": {
            "code": "ZAR",
            "name": "Rand",
            "symbol": "R",
            "unicode_hex": 0x52,
        }
    },
    "ZM": {
        "alpha2": "ZM",
        "name": "Zambia",
        "alpha3": "ZMB",
        "currency": {
            "code": "ZMK",
            "name": "Kwacha",
        }
    },
    "ZW": {
        "alpha2": "ZW",
        "name": "Zimbabwe",
        "alpha3": "ZWE",
        "currency": {
            "code": "ZWD",
            "name": "Zimbabwe Dollars",
            "symbol": "Z$",
            "unicode_hex": [0x5a, 0x24],
        }
    },
}
