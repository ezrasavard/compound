import getpass
import lastpass
from lastpass.exceptions import (
    LastPassIncorrectGoogleAuthenticatorCodeError,
    LastPassIncorrectYubikeyPasswordError
)


class CredentialGetter(object):

    def open_vault(self, username, password):
        try:
            self.vault = lastpass.Vault.open_remote(username, password)
        except (LastPassIncorrectGoogleAuthenticatorCodeError,
                LastPassIncorrectYubikeyPasswordError):
            auth = input('Enter your 2-factor authentication code: ')
            self.vault = lastpass.Vault.open_remote(username, password, auth)

    def __init__(self, username=None, password=None):
        """Create a DataFetcher with Lastpass logins stored."""
        if not (username and password):
            username = input('Enter your LastPass username: ')
            password = getpass.getpass('Enter your LastPass password: ')
        self.open_vault(username, password)

    def get_logins(self, site):
        """Finds the login info for a website from the Lastpass vault.

        A Lastpass account entry is considered to match the site if either the
        account name or account URL contains the site name supplied.

        The returned list will consist of tuples containing the username
        and password as unicode strings.

        Args:
            site (bytestring): the website.

        Returns:
            A list containing all the matching logins for the site.
        """
        return [(str(x.username, 'utf-8'), str(x.password, 'utf-8'))
                for x in self.vault.accounts
                if site in x.name or (x.url and site in x.url)]
