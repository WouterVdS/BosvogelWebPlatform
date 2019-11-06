import html

from django.test import TestCase, Client
from django.urls import reverse

from apps.home.constants import Takken


class TakOverviewGeneralTestCase(TestCase):

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

    def test_tak_views_for_all_takken_should_have_tak_in_content(self):
        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = str(response.content)

            # Check
            self.assertTrue(f'<h1>Pagina van de {tak.lower()}!</h1>' in content,
                            f'The name of the tak ({tak.lower()}) should be displayed in the page, '
                            f'but the content is: \n\n{content}')

    def test_tak_views_for_all_takken_should_have_age_in_content(self):
        # Build
        takinfos = [Takken.TAKINFO_KAP, Takken.TAKINFO_WEL, Takken.TAKINFO_KAB, Takken.TAKINFO_JV, Takken.TAKINFO_JG,
                    Takken.TAKINFO_V, Takken.TAKINFO_G, Takken.TAKINFO_JIN, Takken.TAKINFO_L, Takken.TAKINFO_GRL]

        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = str(response.content)

            age = ''
            for takinfo in takinfos:
                if takinfo['abbrev'] == abbreviation:
                    age = takinfo['age']

            # Check
            self.assertTrue(f'Leeftijd ({age} jaar)' in content,
                            f'The age for the tak ({age}) should be displayed in the page,'
                            f' but the content is: \n\n{content}')

    def test_tak_views_for_all_takken_should_have_the_logo_displayed(self):
        # Build
        takinfos = [Takken.TAKINFO_KAP, Takken.TAKINFO_WEL, Takken.TAKINFO_KAB, Takken.TAKINFO_JV, Takken.TAKINFO_JG,
                    Takken.TAKINFO_V, Takken.TAKINFO_G, Takken.TAKINFO_JIN, Takken.TAKINFO_L, Takken.TAKINFO_GRL]

        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = str(response.content)

            tak_logo = ''
            for takinfo in takinfos:
                if takinfo['abbrev'] == abbreviation:
                    tak_logo = takinfo['takteken'].split('/')[-1]

            # Check
            self.assertTrue(tak_logo in content,
                            f'The logo for the tak ({tak_logo}) should be displayed in the page,'
                            f' but the content is: \n\n{content}')

    def test_tak_views_for_all_takken_should_have_description_in_content(self):
        # Build
        takinfos = [Takken.TAKINFO_KAP, Takken.TAKINFO_WEL, Takken.TAKINFO_KAB, Takken.TAKINFO_JV, Takken.TAKINFO_JG,
                    Takken.TAKINFO_V, Takken.TAKINFO_G, Takken.TAKINFO_JIN, Takken.TAKINFO_L, Takken.TAKINFO_GRL]

        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = html.unescape(str(response.content))

            description = ''
            for takinfo in takinfos:
                if takinfo['abbrev'] == abbreviation:
                    description = str(takinfo['description'].encode('utf-8'))[2:][:-1]

            # Check
            self.assertTrue(description in content,
                            f'The description for the tak ({description}) should be displayed in the page,'
                            f' but the content is: \n\n{content}')

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

    def test_it_should_contain_a_link_to_all_vergaderingen(self):
        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))
        content = str(response.content)

        # Check
        self.assertTrue('kapoenen/alle-vergaderingen' in content,
                        'The agenda page should contain the link to view all (passed) vergaderingen')
