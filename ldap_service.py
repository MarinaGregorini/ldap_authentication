from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
import os

class LDAPAuthService:
    def __init__(self):
        self.ldap_server = '<>'
        self.ldap_port = 3268
        self.bind_dn = 'CN=<>,CN=<>,DC=<>,DC=<>,DC=<>,DC=<>'
        self.bind_password = os.getenv('LDAP_ADMIN_PASSWORD')
        self.search_base = 'DC=<>,DC=<>,DC=<>,DC=<>'
        self.user_search_filter = '(sAMAccountName={})'

    def authenticate(self, username, password):

        try:
            # 1. Conexão como admin para buscar o usuário
            server = Server(self.ldap_server, port=self.ldap_port, get_info=ALL)
            with Connection(server, user=self.bind_dn, password=self.bind_password) as admin_conn:
                if not admin_conn.bind():
                    return False, {"message": "Admin authentication failed"}
                
                admin_conn.search(
                    search_base=self.search_base,
                    search_filter=self.user_search_filter.format(username),
                    search_scope=SUBTREE,
                    attributes=['displayName', 'mail', 'department']
                )
                
                if not admin_conn.entries:
                    return False, {"message": "User not found"}
                
                user_dn = admin_conn.entries[0].entry_dn
                
            with Connection(server, user=user_dn, password=password) as user_conn:
                if user_conn.bind():
                    user_data = admin_conn.entries[0]
                    return True, {
                        'username': username,
                        'display_name': user_data.displayName.value if hasattr(user_data, 'displayName') else None,
                        'email': user_data.mail.value if hasattr(user_data, 'mail') else None
                    }
                return False, {"message": "Invalid credentials"}
                
        except LDAPException as e:
            return False, {"message": f"LDAP error: {str(e)}"}
        except Exception as e:
            return False, {"message": f"Unexpected error: {str(e)}"}