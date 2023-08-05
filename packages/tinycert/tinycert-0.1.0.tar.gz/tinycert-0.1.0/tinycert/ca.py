"""TinyCert Certificate Authority APIs"""


class CertificateAuthorityApi(object):
    """TinyCert Certificate Authority management."""
    def __init__(self, session):
        self._session = session

    def list(self):
        """List CAs in this account.
        """
        return self._session.request('ca/list')

    def details(self, ca_id):
        """Retrieve details of a particular CA.

        :param ca_id: id of the CA
        """
        return self._session.request('ca/details', {'ca_id': ca_id})

    def get(self, ca_id):
        """Download the CA's certificate.

        :param ca_id: id of the CA
        """
        return self._session.request('ca/get', {'ca_id': ca_id, 'what': 'cert'})

    def delete(self, ca_id):
        """Delete the given CA.

        :param ca_id: id of the CA
        """
        return self._session.request('ca/delete', {'ca_id': ca_id})

    def create(self, ca_detail):
        """Create a new Certificate Authority in this account.

        :param ca_detail: dict of named values

            - 'C': [required; string] ISO 3166-1 alpha-2 country code; e.g., 'US'
            - 'O': [required; string] Organization name; e.g., 'ACME, Inc.'
            - 'L': [optional; string] Locality (city or town); e.g., 'Chicago'
            - 'ST': [optional; string] State or province name; e.g., 'Illinois'
            - 'hash_method': [required; string] Hashing algorithm - one of 'sha1' or 'sha256'(recommended)
        """
        return self._session.request('ca/new', ca_detail)
