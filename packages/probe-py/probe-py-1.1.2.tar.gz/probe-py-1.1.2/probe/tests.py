import unittest
from probe import SearchApi, CompanyApi


class TestProbeAPI(unittest.TestCase):

    def test_search_company_loanzen(self):
        api = SearchApi()
        companies = api.companies_get('1.1', filters='{"nameStartsWith": "loanzen"}')
        #print type(companies.data), companies.data.companies
        self.assertFalse(len(companies.data.companies) == 0)

    def test_search_authorized_signatory(self):
        api = SearchApi()
        directors = api.authorized_signatories_get('1.1', filters='{"pan": "ANQPK6045G"}')
        #print directors.data.authorized_signatories
        self.assertFalse(len(directors.data.authorized_signatories) == 0)

    def test_get_company_details_empty(self):
        api = CompanyApi()
        company = api.companies_cin_get('1.1', 'U24239DL2002PTC114413')
        #print company.data.company
        self.assertEquals(company.data.company.cin, 'U24239DL2002PTC114413')

    def test_get_company_authorized_signatories(self):
        api = CompanyApi()
        signatories = api.companies_cin_authorized_signatories_get('1.1', 'U24239DL2002PTC114413')
        #print signatories.data.authorized_signatories
        self.assertFalse(len(signatories.data.authorized_signatories) == 0)

    def test_get_company_charges(self):
        api = CompanyApi()
        charges = api.companies_cin_charges_get('1.1', 'U24239DL2002PTC114413')
        #print charges.data.charges
        self.assertFalse(len(charges.data.charges) == 0)

    def test_get_company_financials(self):
        api = CompanyApi()
        financials = api.companies_cin_financials_get('1.1', 'U24239DL2002PTC114413')
        print financials.data.financials

if __name__ == '__main__':
    unittest.main()