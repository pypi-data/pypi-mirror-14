TinyCert
========

A wrapper library around TinyCert's v1 rest api.

API details (including your API key) can be found at https://www.tinycert.org/docs/api

## Usage

Preferred method of use is via the provided ContextManager.

```
from tinycert import auto_session

with auto_session(api_key, account, passphrase) as session:
    ca_list = session.ca.list()
    cert_list = session.cert.list(ca_list[0]['id'])
```

Or, connect and disconnect manually.

```
from tinycert import Session

session = Session(api_key)
session.connect(account, passphrase)
ca_list = session.ca.list()
cert_list = session.cert.list(ca_list[0]['id'])
session.disconnect()
```

## Examples

Find examples in the unit tests under the test/ directory.
