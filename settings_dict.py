from buttons import pervichka, garant, holod, artem, clean_money, non_profile, class_a, class_b

month_dict = {
    'january': "январь", 'february': "февраль", 'march': 'март', 'april': "апрель", 'may': "май", 'june': "июнь",
    'july': 'июль', 'august': 'август', 'september': "сентябрь", 'october': "октябрь", 'november': "ноябрь",
    'december': "декабрь"
}

percent_rates = {
    class_a: {
        pervichka: {
            "column_name": "s_" + pervichka,
            "rate": {2500: 25, 4500: 30, 7500: 35, 10500: 40, 17000: 45, 17001: 50},
        },
        garant: {
            "column_name": "s_" + garant,
            "rate": {10500: 50, 17000: 45, 17001: 50},
        },
        holod: {
            "column_name": "s_" + holod,
            "rate": {10500: 50, 17000: 45, 17001: 50},
        },
        artem: {
            "column_name": "s_" + artem,
            "rate": {0: 45},
        },
        clean_money: {
            "column_name": "s_" + clean_money,
            "rate": {0: 100},
        },
        non_profile: {
            "column_name": "s_" + non_profile,
            "rate": {10500: 40, 17000: 45, 17001: 50},
        },
    },
    class_b: {
        pervichka: {
            "column_name": "s_" + pervichka,
            "rate": {2500: 20, 4500: 25, 7500: 30, 10500: 35, 17000: 40, 17001: 45},
        },
        garant: {
            "column_name": "s_" + garant,
            "rate": {10500: 50, 17000: 40, 17001: 45},
        },
        holod: {
            "column_name": "s_" + holod,
            "rate": {10500: 50, 17000: 40, 17001: 45},
        },
        artem: {
            "column_name": "s_" + artem,
            "rate": {0: 45},
        },
        clean_money: {
            "column_name": "s_" + clean_money,
            "rate": {0: 100},
        },
        non_profile: {
            "column_name": "s_" + non_profile,
            "rate": {10500: 40, 17000: 40, 17001: 45},
        },
    },
}