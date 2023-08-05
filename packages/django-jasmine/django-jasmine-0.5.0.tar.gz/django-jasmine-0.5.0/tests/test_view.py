from django.test import TestCase
from django.core.urlresolvers import reverse

from django_jasmine import settings as dj_jas_settings

example_specs = ['PlayerSpec.js', 'SpecHelper.js']

class TestView(TestCase):

    def setUp(self):
        self.rsp = self.client.get(reverse('jasmine_default'))

    def test_view_success(self):
        self.assertEqual(self.rsp.status_code, 200)

    def test_spec_files_served(self):
        for spec in example_specs:
            self.assertTrue(spec in str(self.rsp.content), '%s not in %s' % (spec, self.rsp.content))

    def test_jasmine_version(self):
        self.assertEqual(self.rsp.context['version'], dj_jas_settings.DEFAULT_JASMINE_VERSION)
        not_default_ver = 'v2.0.1'
        r = self.client.get(reverse('jasmine_version', args=[not_default_ver]))
        # import pdb; pdb.set_trace()
        self.assertEqual(r.context['version'], not_default_ver)