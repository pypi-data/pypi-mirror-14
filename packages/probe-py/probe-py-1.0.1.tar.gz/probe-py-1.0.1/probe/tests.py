import unittest
from probe import SearchApi, CompanyApi


class TestProbeAPI(unittest.TestCase):

    def test_search_company_loanzen(self):
        api = SearchApi()
        companies = api.companies_get(filters='{"nameStartsWith": "loanzen"}')
        self.assertFalse(len(companies.data) == 0)

    def test_search_authorized_signatory(self):
        api = SearchApi()
        directors = api.authorized_signatories_get(filters='{"pan": "ANQPK6045G"}')
        self.assertFalse(len(directors.data) == 0)

    def test_get_company_details_empty(self):
        api = CompanyApi()
        company = api.companies_cin_get('U24239DL2002PTC114413')
        self.assertEquals(company.cin, 'U24239DL2002PTC114413')

    def test_get_company_authorized_signatories(self):
        api = CompanyApi()
        signatories = api.companies_cin_authorized_signatories_get('U24239DL2002PTC114413')
        self.assertFalse(len(signatories) == 0)

    def test_get_company_charges_empty(self):
        api = CompanyApi()
        charges = api.companies_cin_charges_get('U24239DL2002PTC114413')
        self.assertFalse(len(charges) == 0)


if __name__ == '__main__':
    unittest.main()