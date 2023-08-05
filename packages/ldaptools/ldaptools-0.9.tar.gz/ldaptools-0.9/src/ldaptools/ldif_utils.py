import ldap
import ldif
from ldap.dn import dn2str

from ldaptools.utils import idict, str2dn


class ListLDIFParser(ldif.LDIFParser):
    def __init__(self, *args, **kwargs):
        self.entries = []
        ldif.LDIFParser.__init__(self, *args, **kwargs)

    def handle(self, dn, entry):
        dn = str2dn(dn)
        dn = [[(part[0].lower(),) + part[1:] for part in rdn] for rdn in dn]
        dn = dn2str(dn)
        self.entries.append((dn, entry))

    def add(self, conn):
        for dn, entry in self.entries:
            conn.add_s(dn, ldap.modlist.addModlist(entry))

    def __iter__(self):
        for dn, attributes in self.entries:
            yield dn, idict(attributes)
