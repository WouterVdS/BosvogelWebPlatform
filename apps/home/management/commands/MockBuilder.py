from datetime import date, timedelta, time

from django.db import IntegrityError

from apps.agenda.models import Event
from apps.home.constants import Takken, Sex, Events
from apps.home.models import Werkjaar

from random import randint, choice
from faker import Faker
from faker.providers import person, bank, color, date_time, internet, job, lorem, phone_number, address

from apps.place.models import Place
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.models.totem import Totem

from apps.rent.models import Pricing, Reservation, get_prices
# todo add public events en jincafes, they are shown on /agenda


class MockBuilder:
    def __init__(self):
        self.years = None
        self.current_year = None

        self.fake = Faker('nl_NL')
        self.fake.add_provider(person)
        self.fake.add_provider(bank)
        self.fake.add_provider(color)
        self.fake.add_provider(date_time)
        self.fake.add_provider(internet)
        self.fake.add_provider(job)
        self.fake.add_provider(lorem)
        self.fake.add_provider(address)
        self.fake.add_provider(phone_number)

    def fill_database_with_objects(self, years):
        print(f'Generating data to simulate {years} years...')

        self.current_year = Werkjaar.objects.current_year()
        current_year = self.current_year.year
        self.years = [x for x in range(current_year, current_year-years, -1)]

        self.create_werkjaren()
        self.create_leaders()
        self.create_weekly_meetings_vergaderingen()
        self.add_rental_prices()
        self.create_rental_reservations()
        print('\nDone!')

    def create_werkjaren(self):
        self.current_year.yearTheme = 'Jaarthema van dit jaar'
        self.current_year.yearThemeSong = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        # todo logo toevoegen
        self.current_year.save()

        if Werkjaar.objects.count() >= len(self.years):
            print(f'Not creating extra werkjaren, there already exist {Werkjaar.objects.count()}')
            return
        print('Creating werkjaren...')
        for year in self.years:
            try:
                # todo logo's toevoegen voor elk jaar
                Werkjaar.objects.create(
                    year=year,
                    yearTheme=f'Jaarthema van werkjaar {year}',
                    yearThemeSong='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                )
            except IntegrityError:
                # skip years that already exist
                continue

    def create_leaders(self):
        if Membership.objects.filter(werkjaar__year=self.years[-1]).exists():
            print('Not creating extra leaders, leaders already exist for the existing workyears')
            return
        print('Creating leaders... (this may take a while, go grab a coffee)')
        for year in self.years:
            for tak in Takken.TAKKEN:
                current_leader_count = Membership.objects.filter(werkjaar=year, tak=tak[0], is_leader=True).count()
                if current_leader_count > 5:
                    # if a tak already has 5 leaders, stop creating new ones
                    continue
                max_extra_leaders = 5 - current_leader_count
                for x in range(randint(1, max_extra_leaders)):
                    self.create_a_leader_with_history(tak=tak[0], year=year)

    def create_a_leader_with_history(self, tak, year):
        totem = Totem.objects.create(
            kleurentotem=self.fake.color_name(),
            kleurentotem_text=self.fake.text(max_nb_chars=200),
            voortotem=self.fake.job(),
            voortotem_text=self.fake.text(max_nb_chars=200),
            totem=self.fake.job(),
            totem_text=self.fake.text(max_nb_chars=200)
        )

        leader = None
        while leader is None:
            try:
                leader = Profile.objects.create(
                    last_name=self.fake.last_name(),
                    email=self.fake.email(),
                    public_email=self.fake.company_email(),
                    birthday=self.fake.date_between(start_date='-25y', end_date='-17y'),
                    totem=totem,
                    phone_number=self.fake.phone_number(),
                    bank_account_number=self.fake.iban()
                )
            except IntegrityError:
                pass

        if randint(0, 1) == 0:
            leader.sex = Sex.MALE
            leader.first_name = self.fake.first_name_male()
        else:
            leader.sex = Sex.FEMALE
            leader.first_name = self.fake.first_name_female()

        if randint(0, 1) == 0:
            leader.nickname = self.fake.first_name()

        leader.save()

        # create a history for the leader
        werkjaar = Werkjaar.objects.get(year=year)
        earliest_year = self.years[-1]
        for x in range(randint(1, 5)):
            membership = Membership.objects.create(
                profile=leader,
                werkjaar=werkjaar,
                is_leader=True,
                tak=tak,
            )

            if tak in ['KAP', 'WEL', 'KAB']:
                membership.tak_leader_name = self.fake.first_name()
                membership.save()

            if werkjaar.year == earliest_year:
                return

            werkjaar = werkjaar.previous_year()
            tak = choice(Takken.TAKKEN)[0]

    def create_weekly_meetings_vergaderingen(self):
        print('Creating vergaderingen for each tak... (this wil take a while)')
        # todo bulk add event objects for speed
        place = Place.objects.create(
            name='Locatie van het lokaal',
            country=self.fake.country(),
            zipcode=self.fake.postcode(),
            city=self.fake.city(),
            street_and_number=f'{self.fake.street_name()} {self.fake.random_digit()}'
        )
        for year in self.years:
            if Event.objects.filter(type=Events.WEEKLY_ACTIVITY,
                                    startDate__gt=date(year=year, month=9, day=1),
                                    startDate__lt=date(year=year, month=12, day=31)).exists():
                continue
            for tak in Takken.TAKKEN:
                next_date = date(year=year, month=9, day=14)
                while next_date.weekday() not in [5, 6]:  # 5 is saturday, 6 is sunday
                    next_date = next_date + timedelta(days=1)
                while not (next_date.year > year and next_date.month > 6):
                    Event.objects.create(
                        name='Vergadering naam',
                        place=place,
                        startDate=next_date,
                        startTime=time(14, 0, 0),
                        endTime=time(16, 30, 0),
                        description=self.fake.text(max_nb_chars=200),
                        type=Events.WEEKLY_ACTIVITY,
                        tak=tak[0]
                    )

                    next_date = next_date + timedelta(days=7)



    @staticmethod
    def add_rental_prices():
        if get_prices().perPersonPerDay != 0:
            print('Not creating rental pricing, there is already rental pricing')
            return
        print('Creating rental pricing')

        Pricing.objects.create(
            perPersonPerDay=2.5,
            dailyMinimum=90,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=20,
            deposit=500,
            pricesSetOn=date.today()
        )

    def create_rental_reservations(self):
        print('Creating rental reservations')
        for year in self.years:
            if Reservation.objects.filter(period__startDate__gt=date(year=year, month=1, day=1),
                                          period__startDate__lt=date(year=year, month=12, day=31)).exists():
                continue

            next_summer_year = year
            if date.today().month > 8:
                next_summer_year += 1

            start_dates = [
                date(year=next_summer_year, month=7, day=1),
                date(year=next_summer_year, month=7, day=15),
                date(year=next_summer_year, month=8, day=1),
                date(year=next_summer_year, month=8, day=11),
            ]

            pricing = Pricing.objects.first()

            for start_date in start_dates:
                period = Event.objects.create(
                    startDate=start_date,
                    endDate=start_date + timedelta(days=10),
                    type=Events.RENTAL
                )
                # Not all fields used: contract, status, depositStatusn checklist, finalBill
                Reservation.objects.create(
                    groupName=self.fake.word(),
                    town=self.fake.city(),
                    email=self.fake.email(),
                    phoneNr=self.fake.phone_number(),
                    period=period,
                    pricing=pricing,
                    bankAccountNumber=self.fake.iban(),
                    depositAmount=200,
                    numberOfPeople=50,
                    comments=self.fake.text(max_nb_chars=50)
                )
