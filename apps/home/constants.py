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


class Takken:
    KAPOENEN = 'KAP'
    WELPEN = 'WEL'
    KABOUTERS = 'KAB'
    JONGVERKENNERS = 'JV'
    JONGGIDSEN = 'JG'
    VERKENNERS = 'V'
    GIDSEN = 'G'
    JINS = 'JIN'
    LEIDING = 'L'
    GROEPSLEIDING = 'GRL'

    TAKKEN = (
        (KAPOENEN, 'Kapoenen'),
        (WELPEN, 'Welpen'),
        (KABOUTERS, 'Kabouters'),
        (JONGVERKENNERS, 'Jongverkenners'),
        (JONGGIDSEN, 'Jonggidsen'),
        (VERKENNERS, 'Verkenners'),
        (GIDSEN, 'Gidsen'),
        (JINS, 'Jins'),
        (LEIDING, 'Leiding'),
        (GROEPSLEIDING, 'Groepsleiding')
    )

    TAKINFO_KAP = {
        'fullName': 'Kapoenen',
        'abbrev': 'KAP',
        'age': '6 tot 7',
        'takteken': 'takken/img/taktekens/takteken_kap.png',
        'description': 'Wij zijn in één woord: kapoenen! Iedere week opnieuw ravotten, spelen en springen samen met '
                       'zo\'n 30 andere leeftijdsgenootjes. Samen ontdekken wat het betekent in groep te spelen, samen '
                       'te werken en gewoon merken dat het zooooooveeeeel leuker is dan alleen. Laat je fantasie de '
                       'vrije loop en knutsel eens een teletijdsmachine in elkaar of reis in 2 uur tijd de wereld rond '
                       'in een zeppelin... Bij ons kan het allemaal!'
    }

    TAKINFO_WEL = {
        'fullName': 'Welpen',
        'abbrev': 'WEL',
        'age': '8 tot 10',
        'takteken': 'takken/img/taktekens/takteken_wel_kab.png',
        'description': 'Vanaf de leeftijd van 8 jaar worden meisjes en jongens gesplitst: de meisjes komen terecht '
                       'bij de \'kabouters\' en de jongens bij de \'welpen\'. '
                       'In beide groepen staat uiteraard spelen en ontdekken nog centraal, maar ook komen ze reeds '
                       'in aanraking met de typische scoutsactiviteiten: eenvoudige tochttechnieken, het sjorren ('
                       'op een eenvoudige manier, enkel met een touw, stevige constructies van balken maken) '
                       'Ook wordt bij deze takken al meer aandacht besteed aan samenwerken: de meerwaarde van '
                       'spelen in groep. De werking wordt ingekleed met verhalen en fantasie, met als leidraad '
                       'het Kabouterverhaal en het Jungleboek. De verdeling in \'nesten\' '
                       '(kleinere groepjes onder de hoede van een nestleider) leert de oudere kabouters/welpen, '
                       '11-jarigen, van de groep verantwoordelijkheid te nemen en te zorgen voor de jongere leden.'
    }

    TAKINFO_KAB = {
        'fullName': 'Kabouters',
        'abbrev': 'KAB',
        'age': '8 tot 10',
        'takteken': 'takken/img/taktekens/takteken_wel_kab.png',
        'description': 'Vanaf de leeftijd van 8 jaar worden meisjes en jongens gesplitst: de meisjes komen terecht '
                       'bij de \'kabouters\' en de jongens bij de \'welpen\'. '
                       'In beide groepen staat uiteraard spelen en ontdekken nog centraal, maar ook komen ze reeds '
                       'in aanraking met de typische scoutsactiviteiten: eenvoudige tochttechnieken, het sjorren ('
                       'op een eenvoudige manier, enkel met een touw, stevige constructies van balken maken) '
                       'Ook wordt bij deze takken al meer aandacht besteed aan samenwerken: de meerwaarde van '
                       'spelen in groep. De werking wordt ingekleed met verhalen en fantasie, met als leidraad '
                       'het Kabouterverhaal en het Jungleboek. De verdeling in \'nesten\' '
                       '(kleinere groepjes onder de hoede van een nestleider) leert de oudere kabouters/welpen, '
                       '11-jarigen, van de groep verantwoordelijkheid te nemen en te zorgen voor de jongere leden.'
    }

    TAKINFO_JV = {
        'fullName': 'Jongverkenners',
        'abbrev': 'JV',
        'age': '11 tot 13',
        'takteken': 'takken/img/taktekens/takteken_jv_jg.png',
        'description': 'De jonggivers (jong-gidsen en jong-verkenners) hebben zo hun eigen smaak als het op '
                       'spelen aankomt. Jonggivers spelen graag grote spelen waarbij ze een eigen tactiek kunnen '
                       'kiezen om het spel te winnen. Bosspelen staan bovenaan hun lijstje van favorieten. '
                       'Maar ook avonturentochten nemen ze graag aan. Een rivier oversteken met behulp van een touw, '
                       'of een heus hoogteparcours tussen de bomen kunnen ze altijd wel appreciëren.'
    }

    TAKINFO_JG = {
        'fullName': 'Jonggidsen',
        'abbrev': 'JG',
        'age': '11 tot 13',
        'takteken': 'takken/img/taktekens/takteken_jv_jg.png',
        'description': 'De jonggivers (jong-gidsen en jong-verkenners) hebben zo hun eigen smaak als het op '
                       'spelen aankomt. Jonggivers spelen graag grote spelen waarbij ze een eigen tactiek kunnen '
                       'kiezen om het spel te winnen. Bosspelen staan bovenaan hun lijstje van favorieten. '
                       'Maar ook avonturentochten nemen ze graag aan. Een rivier oversteken met behulp van een touw, '
                       'of een heus hoogteparcours tussen de bomen kunnen ze altijd wel appreciëren.'
    }

    TAKINFO_V = {
        'fullName': 'Verkenners',
        'abbrev': 'V',
        'age': '14 tot 16',
        'takteken': 'takken/img/taktekens/takteken_v_g.png',
        'description': 'Givers (gidsen en verkenners) zijn eigenlijk heel erg vergelijkbaar met jonggivers, '
                       'maar dan een stukje ouder. Ook zij spelen graag grote spelen, gaan graag de avontuurlijke '
                       'toer op en kunnen heel actief zijn. Toch komt ook het kinderlijke terug naar boven. Givers '
                       'zijn er niet bang voor om zichzelf belachelijk te maken. Bij de givers is er meestal een hele '
                       'goede groepssfeer, iedereen is er vriend van iedereen. Givers krijgen ook meer '
                       'verantwoordelijkheden dan jonggivers, waardoor meerdere (vormen van) spelen mogelijk worden.'
    }

    TAKINFO_G = {
        'fullName': 'Gidsen',
        'abbrev': 'G',
        'age': '14 tot 16',
        'takteken': 'takken/img/taktekens/takteken_v_g.png',
        'description': 'Givers (gidsen en verkenners) zijn eigenlijk heel erg vergelijkbaar met jonggivers, '
                       'maar dan een stukje ouder. Ook zij spelen graag grote spelen, gaan graag de avontuurlijke '
                       'toer op en kunnen heel actief zijn. Toch komt ook het kinderlijke terug naar boven. Givers '
                       'zijn er niet bang voor om zichzelf belachelijk te maken. Bij de givers is er meestal een hele '
                       'goede groepssfeer, iedereen is er vriend van iedereen. Givers krijgen ook meer '
                       'verantwoordelijkheden dan jonggivers, waardoor meerdere (vormen van) spelen mogelijk worden.'
    }

    TAKINFO_JIN = {
        'fullName': 'Jins',
        'abbrev': 'J',
        'age': '17 tot 18',
        'takteken': 'takken/img/taktekens/takteken_jin.png',
        'description': 'Jin is de afkorting voor "Jij en Ik: een Noodzaak" In tegenstelling tot de andere takken, '
                       'duurt de loopbaan van de jins maar 2 jaar. De jongens en meisjes zijn ook hier terug samen. '
                       'Het is eigenlijk een soort van voorbereiding op leiding. Je staat in een kleinere groep en '
                       'kiest eigenlijk zelf wanneer je vergadert en wat je wilt doen tijdens je vergaderingen. '
                       'Jins steken de handen uit de mouwen, maar denken ook na over wie ze zijn en wat ze willen, '
                       'binnen en buiten scouts. Ze plannen zelf een weekend organiseren een fuif om zo hun reis in '
                       'het buitenland te kunnen betalen. De jinleiding heeft meer een begeleidende functie. '
                       'Tijdens het jaar gaan de jins ook eens op stage bij een andere tak, om een eerste '
                       'leidingservaring op te doen. Op de vooravond van het in leiding staan, ondervinden we wat '
                       'ploeggeest, zelfstandigheid en inzet betekenen.'
    }

    TAKINFO_L = {
        'fullName': 'Leiding',
        'abbrev': 'L',
        'age': '17+',
        'takteken': 'takken/img/taktekens/takteken_l.png',
        'description': 'Leiders en leidsters zijn jonge mensen die in hun vrije tijd zorgen voor sfeer, '
                       'activiteiten en werking per tak en per groep; ze doen dat door samen met hun leden te '
                       'spelen en met hen onderweg te zijn. Leiding is verantwoordelijk voor de organisatie en '
                       'het toezicht tijdens scouting. De meeste scoutsgroepen hebben maar één jaar jin waar wij er '
                       'twee hebben. Dit heeft als gevolg dat je pas op de leeftijd van 19 in leiding komt. '
                       'Wel krijg je na je eerste jaar jin een brief in de bus met de uitnodiging om dan al '
                       '-volledig vrijblijvend- bij de leiding te komen. '
    }

    TAKINFO_GRL = {
        'fullName': 'Groepsleiding',
        'abbrev': 'GRL',
        'age': '21+',
        'takteken': 'takken/img/taktekens/takteken_grl.png',
        'description': ''
    }
