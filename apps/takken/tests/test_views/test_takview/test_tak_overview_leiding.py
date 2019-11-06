from django.test import TestCase, Client
from django.urls import reverse

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.tests.test_models.test_profile import ProfileTestCase


class TakOverviewLeidingTestCase(TestCase):

    def test_every_takpage_should_show_leaders(self):
        this_year = Werkjaar.objects.current_year()
        errors = []
        for tak in Takken.TAKKEN:
            # Build
            profile = Profile.objects.create(
                first_name=f'Loewieke{tak[1]}'
            )
            Membership.objects.create(
                profile=profile,
                is_leader=True,
                tak=tak[0],
                werkjaar=this_year
            )

            # Operate
            response = Client().get(reverse('takken:tak', args=[tak[1]]))
            content = str(response.content)

            # Check
            if f'Loewieke{tak[1]}' not in content:  # pragma: no cover
                errors.append(tak[1])

        self.assertEqual(0, len(errors), 'Leaders should be displayed for ' + ', '.join(x for x in errors))

    def test_every_takpage_should_show_the_takemail(self):
        errors = []
        for tak in Takken.TAKKEN:
            if tak[1] == 'Leiding':
                break
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak[1]]))
            content = str(response.content)

            # Check
            if f'{tak[1].lower()}@bosvogels.be' not in content:  # pragma: no cover
                errors.append(tak[1])

        self.assertEqual(0, len(errors), 'Takmail should be displayed for ' + ', '.join(x for x in errors))

    def test_leiding_page_should_not_display_takmail(self):
        # Build
        errors = []

        # Operate
        response = Client().get(reverse('takken:tak', args=['leiding']))
        content = str(response.content)

        # Check
        if 'leiding@bosvogels.be' in content:  # pragma: no cover
            errors.append('Leiding email is displayed')
        if 'mail' in content:  # pragma: no cover
            errors.append('Mail is displayed')

        self.assertEqual(0, len(errors), 'Mail to all leaders should not be displayed, but the word(s) '
                         + ', '.join(x for x in errors) + ' are displayed')

    def test_leaders_should_be_displayed_on_the_takpage(self):
        # Build
        #   Creating:
        #       * two leaders for kapoenen this year
        #       * a leader for welpen this year
        #       * a member for kapoenen this year
        #       * a leader for kapoenen last year

        this_year = Werkjaar.objects.current_year()
        last_year = this_year.previous_year()

        Membership.objects.create(werkjaar=this_year,
                                  is_leader=True,
                                  tak=Takken.KAPOENEN,
                                  profile=Profile.objects.create(
                                      first_name='Jos'
                                  ))
        Membership.objects.create(werkjaar=this_year,
                                  is_leader=True,
                                  tak=Takken.KAPOENEN,
                                  profile=Profile.objects.create(
                                      first_name='Jef'
                                  ))
        Membership.objects.create(werkjaar=this_year,
                                  is_leader=True,
                                  tak=Takken.WELPEN,
                                  profile=Profile.objects.create(
                                      first_name='Joostwelp'
                                  ))
        Membership.objects.create(werkjaar=this_year,
                                  is_leader=False,
                                  tak=Takken.WELPEN,
                                  profile=Profile.objects.create(
                                      first_name='Jenslid'
                                  ))
        Membership.objects.create(werkjaar=last_year,
                                  is_leader=True,
                                  tak=Takken.KAPOENEN,
                                  profile=Profile.objects.create(
                                      first_name='Jeroenni'
                                  ))
        # Operate
        response = Client().get(reverse('takken:tak', args=['kapoenen']))
        content = str(response.content)

        # Check
        self.assertTrue('Jef' in content,
                        'The correct leaders should be displayed')
        self.assertTrue('Jos' in content,
                        'The correct leaders should be displayed')
        self.assertTrue('Jeroenni' not in content,
                        'No leaders of last year same tak should be displayed')
        self.assertTrue('Joostwelp' not in content,
                        'No leaders of this year but another tak should be displayed')
        self.assertTrue('Jenslid' not in content,
                        'No members should be displayed')

    def test_the_word_None_should_never_be_displayed(self):
        # Build
        this_year = Werkjaar.objects.current_year()
        Membership.objects.create(werkjaar=this_year,
                                  is_leader=True,
                                  tak=Takken.KAPOENEN,
                                  profile=Profile.objects.create())

        # Operate
        response = Client().get(reverse('takken:tak', args=['kapoenen']))
        content = str(response.content)

        # Check
        self.assertFalse('None' in content,
                         'The word "None" should never be displayed')

    def test_only_necessary_info_on_leaders_should_be_displayed(self):
        # Build
        this_year = Werkjaar.objects.current_year()
        profile = ProfileTestCase.generate_profile()
        profile.save()

        Membership.objects.create(
            profile=profile,
            werkjaar=this_year,
            is_leader=True,
            tak=Takken.JINS
        )

        self.assertIsNotNone(Membership.objects.first())

        # Operate
        response = Client().get(reverse('takken:tak', args=['jins']))
        content = str(response.content)
        # Check
        self.assertTrue(profile.first_name in content,
                        'The first name should be displayed')
        self.assertTrue(profile.nickname in content,
                        'The last name should be displayed')
        self.assertTrue(profile.last_name in content,
                        'The nickname should be displayed')
        self.assertTrue(profile.public_email in content,
                        'The public email should be displayed')
        self.assertFalse(profile.email in content,
                         'The personal email should not be publicly displayed')
        self.assertFalse(str(profile.birthday) in content,
                         'The birthday should not be publicly displayed')
        self.assertFalse(profile.totem.totem in content,
                         'The totem should not be publicly displayed')
        self.assertFalse(profile.phone_number in content,
                         'The phone number should not be publicly displayed')
        self.assertFalse(profile.bank_account_number in content,
                         'The bank account number should not be publicly displayed')

    def test_the_taknickname_should_be_displayed_if_it_exists(self):
        # Build
        this_year = Werkjaar.objects.current_year()
        profile = ProfileTestCase.generate_profile()
        profile.save()

        Membership.objects.create(
            profile=profile,
            werkjaar=this_year,
            is_leader=True,
            tak=Takken.KAPOENEN,
            tak_leader_name='Akela'
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=['kapoenen']))
        content = str(response.content)

        # Check
        self.assertTrue('Akela' in content,
                        'The given tak name should be displayed')
        self.assertFalse(profile.first_name in content,
                         'The first name should not be displayed if the person has a tak specific name')
        self.assertFalse(profile.last_name in content,
                         'The last name should not be displayed if the person has a tak specific name')
        self.assertFalse(profile.nickname in content,
                         'The nickname should not be displayed if the person has a tak specific name')
