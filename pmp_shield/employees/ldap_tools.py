import logging
from django.conf import settings
from ldap3 import Server, ServerPool, Connection, FIRST, SYNC, SIMPLE
from django.core.exceptions import ImproperlyConfigured
from ldap3.core.exceptions import LDAPInvalidCredentialsResult

logger = logging.getLogger(__name__)


class LDAPTool(object):
    # server pool
    pool = None
    _ldap_conn = None

    # do we use LDAP Groups?
    use_groups = False

    def __init__(self, distinguised_name=None, password=None, uri=None):
        self._ldap_conn = self.init_ldap_server()

    def search_by_username(self, username):
        return self._search_ldap_by('cn', username)

    def search_by_ip(self, ip_number):
        return self._search_ldap_by('employeeID', ip_number)

    def _convert_dictionary(self, result_data):
        str_dictionary = dict()
        ldap_dictionary = result_data[0][1]
        for key in ldap_dictionary.keys():
            new_key = self.model_attributes.get(key, key)
            str_dictionary[new_key] = ldap_dictionary[key][0].decode(encoding='UTF-8')

        return str_dictionary

    def _search_ldap_by(self, attribute, value):
        # TODO validate, raise exceptions
        user_attribs = dict()
        logger.debug("search filter formatted =" + "(&(%s=%s)(objectClass=%s))" % (attribute, value,
                                                                                  settings.LDAP_USER_OBJECT_CLASS))
        self._ldap_conn.search(settings.LDAP_SEARCH_BASE,
                               "(&(%s=%s)(objectClass=%s))" % (attribute, value,settings.LDAP_USER_OBJECT_CLASS, ),
                               attributes=list(settings.LDAP_ATTRIBUTES_MAP.values()))
        logger.debug("_ldap_conn.response =" + str(self._ldap_conn.response))
        if self._ldap_conn.result['result'] == 0 and len(self._ldap_conn.response) > 0 and 'dn' in \
            self._ldap_conn.response[
                0].keys():
            user_attribs = self.create_user_dictionary(self._ldap_conn.response,
                                                       settings.LDAP_ATTRIBUTES_MAP)

        return user_attribs

    @staticmethod
    def create_user_dictionary(response_items: map, user_map):
        users = []
        counter = 0
        for item in response_items:
            user = {}
            logger.debug("user_map=" + str(user_map))
            for key, value in user_map.items():
                logger.debug("key, value, item:" + str(key) + ', ' + str(value) + ', '+str(item))
                if value in item['attributes']:
                    user[key] = item['attributes'][value][0]
            logger.debug("user=" + str(user))
            users.append(user)
            counter += 1

        logger.debug("users[]=" + str(users))

        return users

    def init_ldap_server(self):
        assert hasattr(settings, 'LDAP_SERVERS'), 'No ldap servers configured check LDAP_SERVERS variable'

        # and hasattr(settings, 'LDAP_BIND_USER') and
        #             hasattr(settings, 'LDAP_BIND_PWD') and hasattr(settings, 'LDAP_SEARCH_BASE') and
        #             hasattr(settings, 'LDAP_USER_SEARCH_FILTER') and hasattr(settings, 'LDAP_ATTRIBUTES_MAP')):
        #     raise ImproperlyConfigured()
        logger.debug("LDAP_SERVERS=" + str(settings.LDAP_SERVERS))
        logger.debug("LDAP_BIND_USER=" + str(settings.LDAP_BIND_USER))
        logger.debug("LDAP_BIND_PWD=" + str(settings.LDAP_BIND_PWD))
        logger.debug("LDAP_USER_SEARCH_FILTER=" + str(settings.LDAP_USER_SEARCH_FILTER))
        logger.debug("LDAP_ATTRIBUTES_MAP=" + str(settings.LDAP_ATTRIBUTES_MAP))
        logger.debug("LDAP_SEARCH_BASE=" + str(settings.LDAP_SEARCH_BASE))
        logger.debug("LDAP_USE_LDAP_GROUPS=" + str(settings.LDAP_USE_LDAP_GROUPS))
        # as first release of the module does not have this parameter, default is to set it true to keep the same
        # comportment after updates.
        if hasattr(settings, 'LDAP_USE_LDAP_GROUPS') and isinstance(settings.LDAP_USE_LDAP_GROUPS, bool):

            LDAPTool.use_groups = settings.LDAP_USE_LDAP_GROUPS
        else:
            LDAPTool.use_groups = True
        if LDAPTool.use_groups and not (hasattr(settings, 'LDAP_GROUPS_SEARCH_FILTER') and
                                            hasattr(settings, 'LDAP_GROUP_MEMBER_ATTRIBUTE') and
                                            hasattr(settings, 'LDAP_GROUPS_MAP')):
            raise ImproperlyConfigured()

        # inspired from
        # https://github.com/Lucterios2/django_auth_ldap3_ad/commit/ce24d4687f85ed12a0c4c796022ae7dcb3ff38e3
        # by jobec
        # all_ldap_groups = []
        # for group in settings.LDAP_SUPERUSER_GROUPS + settings.LDAP_STAFF_GROUPS + list(
        #     settings.LDAP_GROUPS_MAP.values()):
        #     # all_ldap_groups.append("(distinguishedName={0})".format(group))
        #     all_ldap_groups.append("(distinguishedName={0})".format(group))
        # if len(all_ldap_groups) > 0:
        #     settings.LDAP_GROUPS_SEARCH_FILTER = "(&{0}(|{1}))".format(settings.LDAP_GROUPS_SEARCH_FILTER,
        #                                                                "".join(all_ldap_groups))
        # end
        # first: build server pool from settings
        if LDAPTool.pool is None:
            LDAPTool.pool = ServerPool(None, pool_strategy=FIRST, active=True, exhaust=True)
            for srv in settings.LDAP_SERVERS:
                server = Server(srv['host'], srv['port'], srv['use_ssl'])
                logger.debug("port added to pool:" + srv['host'])
                LDAPTool.pool.add(server)

        # then, try to connect with user/pass from settings
        con = self.connect_to_ldap_server()
        self._ldap_conn = con
        return con

    def connect_to_ldap_server(self):
        try:
            con = Connection(LDAPTool.pool, auto_bind=True, client_strategy=SYNC, user=settings.LDAP_BIND_USER,
                             password=settings.LDAP_BIND_PWD, authentication=SIMPLE, check_names=True,
                             raise_exceptions=True, lazy=True)
            logger.debug("connection.result:" + str(con.result))
        except LDAPInvalidCredentialsResult as e:
            logger.error('%s %s ' % (str(e), settings.LDAP_BIND_USER))
            raise e
        return con


# class LDAPToolOld(object):
#
#     def __init__(self, distinguised_name=None, password=None, uri=None):
#         if distinguised_name is None:
#             distinguised_name = getattr(settings, 'AUTH_LDAP_BIND_DN')
#         if password is None:
#             password = getattr(settings, 'AUTH_LDAP_BIND_PASSWORD')
#         if uri is None:
#             uri = getattr(settings, 'AUTH_LDAP_SERVER_URI')
#
#         self.retrieve_attributes = ['cn', 'employeeID', 'givenName', 'sn', 'mail', 'company', 'extensionAttribute8',
#                                'telephoneNumber', 'department']
#         self.model_attributes = {'cn': 'username',
#                                  'employeeID': 'company_id',
#                                  'givenName': 'first_name',
#                                  'sn': 'last_name',
#                                  'department': 'office',
#                                  'telephoneNumber': 'phone',
#                                  'mail': 'email',
#                                  'extensionAttribute8': 'tenure'}
#
#
#
#         self._ldap_conn = ldap.initialize(uri)
#         ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
#         ## and do a bind as shown in the above example.
#         # you can also set this to ldap.VERSION2 if you're using a v2 directory
#         # you should  set the next option to ldap.VERSION2 if you're using a v2 directory
#         try:
#             self._ldap_conn.simple_bind_s(distinguised_name, password)
#         except ldap.INVALID_CREDENTIALS:
#             msg = 'Cannot connect to the LDAP server with credentials set. Check config variables LDAP_USERNAME and AUTH_LDAP_BIND_PASSWORD'
#             raise ValueError(msg)
#
#     def _search_by(self, attribute, search_value):
#         baseDN = "OU=Corp,DC=canal,DC=acp"  # "ou=Customers, ou=Sales, o=anydomain.com"
#         searchScope = ldap.SCOPE_SUBTREE
#         ## retrieve all attributes - again adjust to your needs - see documentation for more options
#
#         # searchFilter = "employeeID=179*"
#         searchFilter = "%s=%s" % (attribute, search_value)
#
#         try:
#             ldap_result_id = self._ldap_conn.search(baseDN, searchScope, searchFilter, self.retrieve_attributes)
#             result_set = []
#             while 1:
#                 result_type, result_data = self._ldap_conn.result(ldap_result_id, 0)
#                 if (result_data == []):
#                     break
#                 else:
#                     ## here you don't have to append to a list
#                     ## you could do whatever you want with the individual entry
#                     ## The appending to list is just for illustration.
#                     if result_type == ldap.RES_SEARCH_ENTRY:
#                         result_set.append(self._convert_dictionary(result_data))
#             return result_set
#
#         except ldap.LDAPError as e:
#             raise e
#
#     def search_by_username(self, username):
#         return self._search_by('cn', username)
#
#     def search_by_ip(self, ip_number):
#         return self._search_by('employeeId', ip_number)
#
#     def _convert_dictionary(self,result_data):
#         str_dictionary = dict()
#         ldap_dictionary = result_data[0][1]
#         for key in ldap_dictionary.keys():
#             new_key = self.model_attributes.get(key, key)
#             str_dictionary[new_key] = ldap_dictionary[key][0].decode(encoding='UTF-8')
#
#         return str_dictionary
