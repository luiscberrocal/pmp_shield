
from django.test import TestCase


from django.conf import settings
import logging

from ldap3 import LDAPInvalidCredentialsResult

from ..ldap_tools import LDAPTool

logger = logging.getLogger(__name__)

class TestLDAP(TestCase):

    # def test_get_user(self):
    #     user = LDAPBackend().populate_user('OAHerrera')
    #     self.assertIsNotNone(user)
    #     self.assertEqual('Herrera Valdes', user.last_name)
    def test_wrong_credentials(self):
        old_setting = settings.LDAP_BIND_PWD
        settings.LDAP_BIND_PWD = 'WrongPassword'
        try:
            ldap_tool = LDAPTool()
            settings.LDAP_BIND_PWD = old_setting
            ldap_tool.search_by_username('oaherrera')
            self.fail('LDAPInvalidCredentialsResult was not thrown')
        except LDAPInvalidCredentialsResult as e:
            self.assertTrue(str(e).startswith('LDAPInvalidCredentialsResult'))

        settings.LDAP_BIND_PWD = old_setting


    def test_search_by_username(self):
        ldap_tool = LDAPTool()
        results = ldap_tool.search_by_username('oaherrera')
        self.assertEqual(1, len(results))
        self.assertEqual('Herrera Valdes', results[0]['last_name'])
        self.assertEqual('2773538', results[0]['company_id'])
        self.assertEqual('oaherrera@pancanal.com', results[0]['email'].lower())
        self.assertEqual('272-4147', results[0]['phone'])
        self.assertEqual('TINO-NS', results[0]['office'])

    def test_search_by_ip_4_op(self):
        ldap_tool = LDAPTool()
        results = ldap_tool.search_by_ip('2205777')
        self.assertEqual(1, len(results))
        self.assertEqual('GManfredo@pancanal.com', results[0]['email'])
        self.assertEqual('OPT', results[0]['office'])
        self.assertEqual('Permanente', results[0]['tenure'])

    def test_search_by_username_many(self):
        ldap_tool = LDAPTool()
        results = ldap_tool.search_by_username('*berrocal')
        self.assertEqual(3, len(results))

    def test_search_by_ip(self):
        ldap_tool = LDAPTool()
        results = ldap_tool.search_by_ip('1795341')
        self.assertEqual(1, len(results))
        self.assertEqual('Berrocal Cordoba', results[0]['last_name'])

    # def test_search(self):
    #     try:
    #         l = ldap.initialize(getattr(settings, 'AUTH_LDAP_SERVER_URI'))
    #         ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
    #         ## and do a bind as shown in the above example.
    #         # you can also set this to ldap.VERSION2 if you're using a v2 directory
    #         # you should  set the next option to ldap.VERSION2 if you're using a v2 directory
    #         l.simple_bind_s(getattr(settings, 'AUTH_LDAP_BIND_DN'), getattr(settings,'AUTH_LDAP_BIND_PASSWORD'))
    #         #l.protocol_version = ldap.VERSION3
    #     except ldap.LDAPError as e:
    #         print(e)
    #
    #     ## The next lines will also need to be changed to support your search requirements and directory
    #     baseDN = "OU=Corp,DC=canal,DC=acp" # "ou=Customers, ou=Sales, o=anydomain.com"
    #     searchScope = ldap.SCOPE_SUBTREE
    #     ## retrieve all attributes - again adjust to your needs - see documentation for more options
    #     retrieveAttributes = ['cn', 'employeeId', 'givenName', 'sn', 'mail', 'company', 'extensionAttribute8', 'telephoneNumber', 'department']
    #     #searchFilter = "employeeID=179*"
    #     searchFilter = "cn=cont-v*"
    #
    #     try:
    #         ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
    #         result_set = []
    #         while 1:
    #             result_type, result_data = l.result(ldap_result_id, 0)
    #             if (result_data == []):
    #                 break
    #             else:
    #                 ## here you don't have to append to a list
    #                 ## you could do whatever you want with the individual entry
    #                 ## The appending to list is just for illustration.
    #                 if result_type == ldap.RES_SEARCH_ENTRY:
    #                     result_set.append(result_data)
    #         for r in result_set:
    #             logger.debug(r)
    #     except ldap.LDAPError as e:
    #         print(e)
