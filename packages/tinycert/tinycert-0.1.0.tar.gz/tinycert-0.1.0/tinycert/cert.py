"""TinyCert Certificate APIs"""

from enum import Enum


class State(Enum):
    """Certificate state enum used for list filtering."""
    expired = 1
    good = 2
    revoked = 4
    hold = 8


class CertificateApi(object):
    """TinyCert Certificate management."""
    def __init__(self, session):
        self._session = session

    def list(self, ca_id, states=(State.expired.value | State.good.value | State.revoked.value | State.hold.value)):
        """List all certificates under the given CA in the given states.

        :param ca_id: the certificate authority id
        :param states: bitwise OR of the states to return certificates for
        :type states: int
        """
        return self._session.request('cert/list', {'ca_id': ca_id, 'what': states})

    def details(self, cert_id):
        """Retrieve details for the given certificate.

        :param cert_id: id of the certificate
        """
        return self._session.request('cert/details', {'cert_id': cert_id})

    def get(self, cert_id, data_type):
        """Download certificate data.

        :param cert_id: id of the certificate
        :param data_type: - 'cert'
                          - 'chain'
                          - 'csr'
                          - 'key.dec'
                          - 'key.enc'
        :type data_type: str or unicode
        """
        params = {'cert_id': cert_id, 'what': data_type}
        return self._session.request('cert/get', params)

    def reissue(self, cert_id):
        """Reissue the given certificate.

        :param cert_id: id of the certificate
        """
        return self._session.request('cert/reissue', {'cert_id': cert_id})

    def set_status(self, cert_id, status):
        """Change the status of the given certificate

        :param cert_id: id of the certificate
        :param status: - 'good'
                       - 'hold'
                       - 'revoked'
        :type status: str or unicode
        """
        return self._session.request('cert/status', {'cert_id': cert_id, 'status': status})

    def create(self, ca_id, cert_detail):
        """Create a new certificate signed by the given CA.

        :param ca_id: id of the CA which will sign this certificate
        :param cert_detail: dict of named values

            - 'C': [required; string] ISO 3166-1 alpha-2 country code; e.g., 'US'
            - 'CN': [required; string] Common Name on the certificate; e.g., '*.example.com'
            - 'L': [optional; string] Locality (city or town); e.g., 'Chicago'
            - 'O': [required; string] Organization name; e.g., 'ACME, Inc.'
            - 'OU': [optional; string] Organizational Unit name; e.g., 'IT Department'
            - 'ST': [optional; string] State or province name; e.g. 'Illinois'
            - 'SANs': [optional; array[dict{type,value}]] Array of Subject Alternative Name key/value pairs.

                Supported SAN types are

                - 'DNS'
                - 'IP'
                - 'email'
                - 'URI'.

              Example values

              Two DNS Names:
              [
                {'DNS': 'www.example.com'},
                {'DNS': 'example.com'},
              ]

              or an email address:
              [
                {'email': 'demo@example.com'}
              ]

              or a combination of an IP address and some DNS names:
              [
                {'IP': '127.0.0.1'},
                {'IP': '::1'},
                {'DNS': 'localhost'}
              ]
        }
        """
        params = dict(cert_detail)
        params['ca_id'] = ca_id
        return self._session.request('cert/new', params)
