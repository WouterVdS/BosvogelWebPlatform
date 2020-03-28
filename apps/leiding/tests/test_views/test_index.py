from django.test import TestCase
from django.urls import reverse

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile


class IndexViewTestCase(TestCase):
    VIEW_NAME = 'leiding:index'
    VIEW_ARGS = None
    TITLE_SUFFIX = 'Leiding'

    def test_index_response_code(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Check
        self.assertEqual(response.status_code, 200, f'The view {self.VIEW_NAME} should have a HTTP OK response')

    def test_using_base_html(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        f'The template for {self.VIEW_NAME} should extend the base template')

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue(f'<title>De Bosvogels - {self.TITLE_SUFFIX}</title>' in content,
                        f'The correct head title should be displayed in {self.VIEW_NAME}')

    def test_all_takken_represented(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME))

        # Operate
        content = str(response.content)

        # Check
        for abbrev, tak in Takken.TAKKEN:
            if abbrev is Takken.LEIDING:
                self.assertFalse(f'<h1>{tak}</h1>' in content,
                                 f'"Leider" is no tak and no header is expected')
            else:
                self.assertTrue(f'<h1>{tak}</h1>' in content,
                                f'A header for {tak} is expected')

    def test_leaders_should_be_presented_for_each_tak(self):
        # Build
        werkjaar = Werkjaar.objects.current_year()
        for abbrev, tak in Takken.TAKKEN:
            profile = Profile.objects.create(
                first_name=f'leader for tak {tak}'
            )
            Membership.objects.create(
                profile=profile,
                werkjaar=werkjaar,
                is_leader=True,
                tak=abbrev,
                tak_leader_name=f'leader for tak {tak}'
            )

        response = self.client.get(reverse(self.VIEW_NAME))

        # Operate
        content = str(response.content)

        # Check
        for abbrev, tak in Takken.TAKKEN:
            if abbrev is Takken.LEIDING:
                self.assertFalse(f'leader for tak {tak}' in content,
                                 f'"Leider" is no tak and no leaders should be shown')
            else:
                self.assertTrue(f'leader for tak {tak}' in content,
                                f'A leader for tak {tak} should be displayed')

    def test_members_should_not_be_shown(self):
        # Build
        werkjaar = Werkjaar.objects.current_year()
        for abbrev, tak in Takken.TAKKEN:
            profile = Profile.objects.create(
                first_name=f'leader for tak {tak}'
            )
            Membership.objects.create(
                profile=profile,
                werkjaar=werkjaar,
                is_leader=False,
                tak=abbrev,
                tak_leader_name=f'leader for tak {tak}'
            )

        response = self.client.get(reverse(self.VIEW_NAME))

        # Operate
        content = str(response.content)

        # Check
        for abbrev, tak in Takken.TAKKEN:
            if abbrev is Takken.LEIDING:
                self.assertFalse(f'leader for tak {tak}' in content,
                                 'Members should not be shown')
            else:
                self.assertFalse(f'leader for tak {tak}' in content,
                                 'Members should not be shown')

    def test_tak_leader_names_should_be_used_if_available(self):
        # Build
        werkjaar = Werkjaar.objects.current_year()
        profile = Profile.objects.create(
            first_name='this should not be shown'
        )
        Membership.objects.create(
            profile=profile,
            werkjaar=werkjaar,
            is_leader=True,
            tak=Takken.WELPEN,
            tak_leader_name='Akela'
        )
        response = self.client.get(reverse(self.VIEW_NAME))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('Akela' in content,
                        'Tak leader name should be used if it exists')
        self.assertTrue('this should not be shown' not in content,
                        'It the leader has a takname, it should not use the real name')
