# Tak a.k.a Age category


class Takken:
    KAPOENEN = 'KAP'
    WELPEN = 'WEL'
    KABOUTERS = 'KAB'
    JONGVERKENNERS = 'JV'
    JONGGIDSEN = 'JG'
    VERKENNERS = 'V'
    GIDSEN = 'G'
    JINS = 'JIN'

    TAKKEN = (
        (KAPOENEN, 'Kapoenen'),
        (WELPEN, 'Welpen'),
        (KABOUTERS, 'Kabouters'),
        (JONGVERKENNERS, 'Jongverkenners'),
        (JONGGIDSEN, 'Jonggidsen'),
        (VERKENNERS, 'Verkenners'),
        (GIDSEN, 'Gidsen'),
        (JINS, 'Jins'),
    )


class Events:
    PUBLIC_ACTIVITY = 'pbla'
    WEEKLY_ACTIVITY = 'vrgd'
    RENTAL = 'rntl'
    WEEKEND = 'wknd'
    CAMP = 'camp'
    JINCAFE = 'jncf'
    LEADER_ACTIVITY = 'ldra'
    WORKDAY = 'wrkd'
    GROUPMEETING = 'grpr'

    EVENT_TYPES = (
        (PUBLIC_ACTIVITY, 'Openbaar event'),
        (WEEKLY_ACTIVITY, 'Vergadering'),
        (RENTAL, 'Verhuur'),
        (WEEKEND, 'Weekend'),
        (CAMP, 'Kamp'),
        (JINCAFE, 'Jincafé'),
        (LEADER_ACTIVITY, 'Leidingsactiviteit'),
        (WORKDAY, 'Werkdag'),
        (GROUPMEETING, 'Groepsraad')
    )
