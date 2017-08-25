import processor

import getpass, requests, csv
from decimal import Decimal
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Fetcher():
    """Generic bank transaction fetcher.

    Requires concrete implementations for _login(...) and _parse(...)
    """
    driver = webdriver.PhantomJS(service_args=["--webdriver-loglevel=ERROR"])

    def __init__(self, credentials):
        """Create a Fetcher with a list of possible logins to try.

        Args:
            credentials (list(tuple)): list of tuples, where the first element
                is the username and the second element is the password
        """
        self.credentials = credentials

    def fetch(self):
        """Fetch a list of transactions.

        Requires that the _login and _fetch methods be implemented.
        """
        for username, password in self.credentials:
            if self._login(username, password):
                return self._fetch()
        return []

    def _login(self, username, password):
        """Attempt to login using the supplied credentials.

        If login success, expect that the webdriver instance will be
        authenticated and can be used to retrieve data.

        Args:
            username (str)
            password (str)

        Returns:
            True if login was successful, False otherwise.
        """
        raise NotImplementedException("Implement me.")

    def _fetch(self):
        """Fetch the transactions."""
        raise NotImplementedException("Implement me.")


class ChaseFetcher(Fetcher):

    _url_root = 'https://online.chasecanada.ca/ChaseCanada_Consumer/'

    LOGIN_URL = _url_root + 'Login.do'
    DOWNLOAD_URL = _url_root + 'DownLoadTransaction.do'

    def _login(self, username, password):
        driver = self.driver
        driver.get(self.LOGIN_URL)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_name('password').send_keys(password)
        if not self._submit('Sign On'):
            raise NoSuchElementException('Error: No "Sign On" button on login page')

        if driver.current_url.endswith('Login.do'):  # bad credentials
            return False

        # sometimes a security question is needed
        while driver.current_url.endswith('SecondaryAuth.do'):
            question = driver.find_element_by_css_selector('td.normaltext_SIDE').text
            print('Secondary authorization required:', question)
            answer = getpass.getpass('Answer: ')

            driver.find_element_by_css_selector('input[type=password]').send_keys(answer)
            if not self._submit('Next'):
                raise NoSuchElementException('Error: No "Next" button on ' +
                    'secondary authorization page')

        if driver.current_url.endswith('TransHistory.do'):
            return True

        # probably failed the security check, I guess?
        return False

    def _submit(self, text):
        """Helper to find and click the submit button on the Chase web site.

        Args:
            text (str): submit button text string

        Returns:
            True if button was found and clicked, False otherwise.
        """
        for btn in self.driver.find_elements_by_css_selector('input[type=submit]'):
            if text in btn.get_attribute('value'):
                btn.click()
                return True
        return False

    def _download(self):
        download_form = self.driver.find_element_by_name('downLoadTransactionForm')
        hidden = download_form.find_elements_by_xpath('//input[@type="hidden"]')
        params = {x.get_attribute('name'): x.get_attribute('value') for x in hidden}
        params['downloadType'] = 'csv'
        with requests.Session() as s:
            for cookie in self.driver.get_cookies():
                s.cookies.set(cookie['name'], cookie['value'])
            response = s.post(self.DOWNLOAD_URL, data=params)
            return response.content.decode('utf-8').strip()

    def _fetch(self):
        reader = csv.reader(self._download().split('\r\n'), delimiter=',')
        next(reader)  # skip header
        transactions = []
        for row in reader:
            try:
                amount = Decimal(row[2].strip('()$'))
                if row[-1] == 'D':
                    amount = amount * -1
                transactions.append({
                    processor.TRANSACTION_DATE: row[0],
                    processor.TRANSACTION_AMOUNT: amount,
                    processor.MERCHANT_NAME: row[3],
                    processor.REFERENCE_NUMBER: int(row[7].strip('" '))
                })
            except:
                print("Failed to process row:", row)
                raise
        return transactions
