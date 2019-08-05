from django.test import Client, TestCase
from django.urls import reverse

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile


class IndexViewTestCase(TestCase):

    def test_index_response_code(self):
        # Operate
        response = Client().get(reverse('takken:index'))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')

    def test_tak_views_for_all_takken_response_code(self):
        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = str(response.content)

            # Check
            self.assertEqual(response.status_code, 200,
                             'Takview for ' + tak.lower() + ' should have a HTTP OK response')
            self.assertTrue('<title>De Bosvogels -  ' + tak + '</title>' in content,
                            'The right page should be displayed for ' + tak)

    def test_redirect_on_wrong_takname_in_url(self):
        # Operate
        response = Client().get(reverse('takken:tak', args=['gibberish']))

        # Check
        self.assertEqual(response.status_code, 302,
                         'When going to a faulty tak link, it should be redirected')
        self.assertEqual(response.url, '/takken/',
                         'The page redirected to should be the takken index')

    def test_after_leader_view_response_code(self):
        # Operate
        response = Client().get(reverse('takken:afterleader'))

        # Check
        self.assertEqual(response.status_code, 200, 'Afterleader view should have a HTTP OK response')

    def test_leaders_should_be_displayed_on_the_takpage(self):
        # Build
        """
            Creating:
                * two leaders for kapoenen this year
                * a leader for welpen this year
                * a member for kapoenen this year
                * a leader for kapoenen last year
        """
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

    def test_only_nescessary_info_on_leaders_should_be_displayed(self):
        # todo
        print('test')
        # geen achternaam, enkel het publieke email adres, ...

    def test_the_taknickname_should_be_displayed_if_it_exists(self):
        # todo
        print('test')
        # bvb akela bij de welpen
