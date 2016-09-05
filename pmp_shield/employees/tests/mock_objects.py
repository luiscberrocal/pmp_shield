from openpyxl import load_workbook


class MockLDAPTool(object):
    def __init__(self, source_file=None, append=False):
        self.ldap_data = {'jhuertas': [{'company_id': '8980986',
                                        'first_name': 'Jacobo',
                                        'last_name': 'Huertas',
                                        'username': 'jhuertas',
                                        'email': 'jhuertas@micanal.com',
                                        'office': 'IAIT-TOP',
                                        'phone': None}],
                          'cont-vmurillo': [{'company_id': '',
                                             'first_name': 'Victor',
                                             'last_name': 'Murillo',
                                             'username': 'cont-vmurillo',
                                             'email': 'cont-vmurillo@micanal.com',
                                             'office': None,
                                             'phone': '200-4147'}],
                          'lberrocal': [{'company_id': '1865325',
                                         'first_name': 'Luis',
                                         'last_name': 'Berrocal Cordoba',
                                         'username': 'lberrocal',
                                         'email': 'lberrocal@pancanal.com',
                                         'office': 'TINO-NS',
                                         'phone': '272-4149'}],
                          'pparker': [{'company_id': '1234567',
                                       'first_name': 'Peter',
                                       'last_name': 'Parker',
                                       'username': 'pparker',
                                       'email': 'pparker@marvel.com',
                                       'office': 'TINO-NS',
                                       'phone': '244-4444'}],
                          }
        USERNANME = 0
        FIRST_NAME = 1
        LAST_NAME = 2
        EMAIL = 3
        COMPANY_ID = 4
        OFFICE = 5
        PHONE = 6
        if source_file:
            if not append:
                self.ldap_data = dict()
            workbook = load_workbook(source_file)
            sheet = workbook.active
            row_num = 0
            for row in sheet.rows:
                if row_num != 0:
                    self.ldap_data[row[USERNANME].value] = [{'company_id': row[COMPANY_ID].value,
                                                             'first_name': row[FIRST_NAME].value,
                                                             'last_name': row[LAST_NAME].value,
                                                             'username': row[USERNANME].value,
                                                             'email': row[EMAIL].value,
                                                             'office': row[OFFICE].value,
                                                             'phone': row[PHONE].value}]

                row_num += 1

    def search_by_username(self, username):
        result = self.ldap_data.get(username)
        if result is None:
            result = []
        return result
