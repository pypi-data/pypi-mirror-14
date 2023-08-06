# -*- coding: utf-8 -*-

#  Copyright 2014-2016 Jean-Francois Paris
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, absolute_import, print_function, division
import random
import requests
from lxml import html, etree
from re import sub
import time
from collections import namedtuple
from .log import logger
import pandas as pd


__all__ = ['RateSetterClient']


markets_list = (("monthly", "Rolling"),
                ("bond_1year", "1 Year"),
                ("income_3year", "3 Year Income"),
                ("income_5year", "5 Year Income"))

account_keys = (("deposited", "Deposited"),
                ("balance", "Balance (Available to lend)"),
                ("promotions", "Promotions"),
                ("on_loan", "Money On Loan"),
                ("interest_earned", "Interest earned"),
                ("on_market", "Money On Market"),
                ("fees", "Fees paid to RateSetter"),
                ("withdrawals", "Withdrawals"),
                ("total", "Total"))


Markets = namedtuple('Markets', ','.join([key for key, _ in markets_list]))

home_page_url = "https://www.ratesetter.com/"
provision_fund_url = "https://www.ratesetter.com/Lend/ProvisionFund"
market_view_url = "https://members.ratesetter.com/your_lending/lend_money/choose_term.aspx"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0"


def convert_to_float(num):
    """ convert strings to float, taking into account ratesetter formatting
    conventions

    :param num: a number as per formatted by rate setter website
    :return: float representation of num
    """
    val = sub(r'[^\d\(\)\-km.]', '', num.strip('£ \n\r'))
    multiplier = 1

    if val[0] == '(' and val[-1] == ')':
        val = "-" + val.rstrip(')').lstrip('(')

    if val[-1] == 'm':
        multiplier *= 1000000
        val = val.rstrip('m')

    if val[-1] == 'k':
        multiplier *= 1000
        val = val.rstrip('k')

    return float(val) * multiplier


def multiple_iterator(iterator, nb):

    return zip(*[iterator] * nb)


class RateSetterException(Exception):
    pass


class RateSetterClient(object):
    """ A HTML scrapping client for the ratesetter website

    """

    def __init__(self, email, password, natural=True):
        """ Initialise the Rate Setter client

        :param str email: email address for the account
        :param str password: password for the account
        :param boolean natural: when True, the client tro to emulate a human behavior and pauses between requests
        """

        self._email = email
        self._password = password
        self._natural = natural
        self._connected = False

        # if in natural mode, we initiate the random number generator
        if self._natural:
            random.seed()

        self._session = requests.Session()
        self._session.headers = {'User-agent': user_agent}
        self._session.verify = True

        self.markets = Markets(*[key for key, _ in markets_list])
        """Named tuple that holding the name of the different markets

        * monthly: Monthly Access
        * bond_1year: 1 Year Bond
        * income_3year: 3 Year Income
        * income_5year: 5 Year Income
        """

        logger.debug("Created client for ratesetter")

    def _get_http_helper(self):
        """Returns a helper function that allows lxml form processor to post using requests"""

        def helper(method, url, value):
            if not url:
                logger.error("Cannot submit request. No URL provided")
                raise ValueError("cannot submit, no URL provided")
            if method == 'GET':
                logger.debug("GET request URL: %s, Value: %s", url, value)
                return self._session.get(url, value)
            else:
                logger.debug("POST request URL: %s, Value: %s", url, value)
                return self._session.post(url, value)

        return helper

    def _sleep_if_needed(self):
        """Sleep for a random amount of time between 2 and 10 seconds

        This method is used to make our behaviour look more human and avoid overloading Zopa's server
        """
        if self._natural:
            # if in natural mode we sleep for some time
            time.sleep(random.randint(2, 10))

    def _extract_url(self, tree):
        """Extract and save the main urls

        This method shall be called once after connection in order to
        avoid having to seek for the URL at a later stage

        :param tree: lxml tree of the account home page
        """
        self._sign_out_url = tree.xpath('.//a[contains(text(),"Sign Out")]')[0].get('href')

        # invert the market list
        inv_markets = {v: k for k, v in markets_list}

        self._lending_url = {}
        lending_menu = tree.xpath('.//a[contains(text(),"Lend Money")]/parent::li//following::li[position()<5]/a')
        for each in lending_menu:
            self._lending_url[inv_markets[each.text]] = each.get("href").replace("market_view_new", "market_view")

    def connect(self):
        """Connect the client to RateSetter
        """
        logger.debug("Authenticating ratesetter client")
        logger.debug("GET request URL: %s", home_page_url)
        page = self._session.get(home_page_url)
        tree = html.fromstring(page.text, base_url=page.url)
        self._sleep_if_needed()

        a = tree.xpath('.//a[contains(text(),"Login")]')

        page = self._session.get(a[0].attrib['href'])
        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]

        # asp.net form require the button that was clicked ..
        form.fields["__EVENTTARGET"] = "ctl00$cphContentArea$cphForm$btnLogin"
        form.fields["ctl00$cphContentArea$cphForm$txtEmail"] = self._email
        form.fields["ctl00$cphContentArea$cphForm$txtPassword"] = self._password

        logger.debug("Submit form")
        page = html.submit_form(form, open_http=self._get_http_helper())

        if "login.aspx" in page.url:
            raise RateSetterException("Failed to connect")
        if "your_lending/summary" not in page.url:
            raise RateSetterException("Site has changed")

        self._dashboard_url = page.url
        tree = html.fromstring(page.text, base_url=page.url)
        self._extract_url(tree)

        self._connected = True

    def disconnect(self):
        """ Disconnect the client from RateSetter
        """
        if not self._connected:
            return

        logger.debug("GET request URL: %s", self._sign_out_url)
        page = self._session.get(self._sign_out_url)

        if "login.aspx" not in page.url:
            raise RateSetterException("Failed to sign out")

        self._connected = False

    def get_account_summary(self):
        """Get a summary of the account

        :return: a dataframe containing one record with the following series

        * deposited: total amount deposited since the opening of the account
        * balance: Balance (Available to lend)
        * promotions: amount received for promotions
        * on_loan: Money On Loan
        * interest_earned: Interest earned
        * on_market: Money offered on market
        * fees: fees paid to RateSetter
        * withdrawals: total Withdrawals since the opening of the account
        * total: Grand total

        """
        logger.debug("GET request URL: %s", self._dashboard_url)
        page = self._session.get(self._dashboard_url)
        self._sleep_if_needed()
        tree = html.fromstring(page.text, base_url=page.url)

        response = {}
        labels = []
        for key, label in account_keys:
            labels.append(key)
            td = tree.xpath('.//h3/span[contains(text(),"Your Balance Sheet")]/following::td[contains(text(),"{}")]/following-sibling::td[contains(text(),"£")]'.format(label))
            response[key] = convert_to_float(td[0].text)

        return pd.DataFrame(response, index=[0])

    def get_portfolio_summary(self):
        """Get a summary of the connected user portfolio

        :return: a dataframe with four record

        * monthly: user portfolio on the Monthly Access market
        * bond_1year: user portfolio on the 1 Year Bond market
        * income_3year: user portfolio on the 3 Year Income market
        * income_5year: user portfolio on the 5 Year Income market

        Each record has the following series
        * amount: Money on loan in that particular market
        * average_rate: Average lending rate
        * on_market: Money currently on offer on the market
        """
        portfolio_items = []

        logger.debug("GET request URL: %s", self._dashboard_url)
        page = self._session.get(self._dashboard_url)
        self._sleep_if_needed()
        tree = html.fromstring(page.text, base_url=page.url)

        for key, label in markets_list:
            td = tree.xpath('.//h3/span[contains(text(),"Your Portfolio")]/following::td[contains(text(),"{}")]/parent::tr/descendant::td[contains(@style,"align")]'.format(label))

            amount = convert_to_float(td[1].text + td[2].text)
            if "-" not in td[3].text:
                average_rate = convert_to_float(td[3].text.rstrip("%")) / 100
            else:
                average_rate = 0.0
            on_market = convert_to_float(td[4].text + td[5].text)
            portfolio_items.append({'amount': amount, 'average_rate': average_rate, 'on_market': on_market})

        # build result as dataframe
        dfindex = [market for market, _ in markets_list]
        return pd.DataFrame(portfolio_items, index=dfindex)

    def get_market(self, market):
        """Get the money on offer on a given market

        :param market: one of the name held in self.markets
        :return: a dataframe with the following series

        * rate: the offered rate
        * lend_amount: the total amount on offer at that rate
        * lend_offers: the number of offers
        * lend_cum_amount: cumulative amount on offer at that rate and below
        * borrow_amount: the total amount on request at that rate
        * borrow_offers: the number of request
        * borrow_cum_amount: cumulative amount on request at that rate and below
        """
        url = self._lending_url[market]
        url = url.replace("market_view", "market_full").replace("?pid=", "?ID=")

        logger.debug("GET request URL: %s", url)
        page = self._session.get(url)
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)

        # extract the lending offers
        lending_menu = tree.xpath('.//form/div[@class="rsTableContainer"]/table[@class="rsTable"]/tr/td')

        iterator = iter(multiple_iterator(iter(lending_menu), 4))
        _ = next(iterator)
        market = {}

        for rate, amount, nb_offer, cum_amount in iterator:
            rate = convert_to_float(rate.text.strip()) / 100
            amount = convert_to_float(amount.text.strip())
            nb_offers = convert_to_float(nb_offer.text.strip())
            cum_amount = convert_to_float(cum_amount.text.strip())

            market[rate] = {'rate': rate, 'lend_amount': amount, 'lend_offers': nb_offers, 'lend_cum_amount': cum_amount,
                            'borrow_amount': 0, 'borrow_offers': 0, 'borrow_cum_amount': 0}

        # extract the borrowing offers
        borrowing_menu = tree.xpath('.//form/div[@id="pnlBorrow"]/div[@class="rsTableContainer"]/table[@class="rsTable"]/tr/td')

        if len(borrowing_menu) > 0:
            iterator = iter(multiple_iterator(iter(borrowing_menu), 4))
            _ = next(iterator)

            for rate, amount, nb_offer, cum_amount in iterator:
                rate = convert_to_float(rate.text.strip()) / 100
                amount = convert_to_float(amount.text.strip())
                nb_offers = convert_to_float(nb_offer.text.strip())
                cum_amount = convert_to_float(cum_amount.text.strip())

                if rate in market.keys():
                    item = market[rate]
                    item['borrow_amount'] = amount
                    item['borrow_offers'] = nb_offers
                    item['borrow_cum_amount'] = cum_amount
                else:
                    market[rate] = {'rate': rate, 'lend_amount': 0, 'lend_offers': 0, 'lend_cum_amount': 0,
                                    'borrow_amount': amount, 'borrow_offers': nb_offers, 'borrow_cum_amount': cum_amount}

        df = pd.DataFrame.from_dict(market, orient='index')
        return df[['rate', 'lend_amount', 'lend_offers', 'lend_cum_amount', 'borrow_amount', 'borrow_offers',
                   'borrow_cum_amount']]

    def place_order(self, market, amount, rate):
        """ Place an order to lend money on the market

        :param market: one of the name held in self.markets
        :param amount: Amount to lend in GBP
        :param rate: Offered rate in percentage
        """
        url = self._lending_url[market]
        logger.debug("GET request URL: %s", url)
        page = self._session.get(url)
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]

        # asp.net form require the button that was clicked ..
        form.fields["__EVENTTARGET"] = "ctl00$cphContentArea$btnSetRate"
        form.fields["ctl00$cphContentArea$tbAmount"] = str(amount)
        form.fields["ctl00$cphContentArea$tbRate"] = str(rate*100)

        logger.debug("Submit form")
        page = html.submit_form(form, open_http=self._get_http_helper())
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)
        form = tree.forms[0]

        # Check if we have arrived on the confirmation page
        confirm_tag = tree.xpath('.//div[@class="singleContainer"]/descendant::h3')
        if len(confirm_tag) > 0 and confirm_tag[0].text.strip(' \n\r') == "Confirm your order":
            logger.debug("Request was accepted. Need to confirm")
        else:
            error_tag = tree.xpath('.//div[@class="contextError"]')
            message = error_tag[0].text.strip('- \n\r')
            logger.debug("Request refused: %s", message)
            raise RateSetterException(message)

        # asp.net form require the button that was clicked ..
        form.fields["__EVENTTARGET"] = "ctl00$cphContentArea$btnOrder"

        page = html.submit_form(form, open_http=self._get_http_helper())
        tree = html.fromstring(page.text, base_url=page.url)

        # Check if the order has been confirmed
        confirm_tag = tree.xpath('.//div[@class="singleContainer"]/descendant::h3')
        if len(confirm_tag) > 0 and confirm_tag[0].text.strip(' \n\r') == "Your order has been placed":
            logger.debug("Request was confirmed")
        else:
            logger.debug("Cannot confirm order")
            raise RateSetterException('Cannot confirm order')

    def get_market_rates(self):
        """Get the rates of the latest matches on the different markets

        :return: a dataframe with four record and a rate for each

        * monthly: user portfolio on the Monthly Access market
        * bond_1year: user portfolio on the 1 Year Bond market
        * income_3year: user portfolio on the 3 Year Income market
        * income_5year: user portfolio on the 5 Year Income market
        """
        rates = []
        logger.debug("GET request URL: %s", self._dashboard_url)
        page = self._session.get(self._dashboard_url)
        tree = html.fromstring(page.text, base_url=page.url)

        for key, html_label in markets_list:

            span = tree.xpath('.//td[contains(text(),"{}")]/parent::tr/following-sibling::tr/td/h3/a'.format(html_label))
            rates.append(convert_to_float(span[0].text) / 100)

        # build result as dataframe
        dfindex = [market for market, _ in markets_list]
        return pd.DataFrame(rates, index=dfindex, columns=['rate'])

    def list_orders(self, market):
        """List orders in a given market

        :param market: one of the name held in self.markets
        :return: a dataframe with the following series

        * date: date the offer was place
        * id: the offer id
        * amount: the amount on offer
        * rate: the rate
        * queue: the amount on offer that stands below in the pecking order
        * cancel_url: the url to cancel the offer
        """
        # load the lending page
        url = self._lending_url[market]
        logger.debug("GET request URL: %s", url)
        page = self._session.get(url)
        self._sleep_if_needed()

        tree = html.fromstring(page.text, base_url=page.url)
        tree.make_links_absolute(page.url)

        # Check if there is there is unmatched money
        span = tree.xpath('.//div[@class="expander"]/h3/span[contains(text(),"Unmatched Money")]')

        # if the span is empty then there is no orders on that market
        if len(span) == 0:
            return ()

        lending_menu = tree.xpath('.//div[@id="ctl00_cphContentArea_expUnmatched_pnlLenderUnMatchedOrders"]/table[@class="rsTable"]/tr/td')

        iterator = multiple_iterator(iter(lending_menu), 6)
        orders = []

        for ldate, lorderid, lamount, lrate, lqueue, lactions in iterator:
            stringify = etree.XPath("string()")

            ldate = stringify(ldate).strip()
            ldate = time.strptime(ldate, "%d/%m/%Y")
            lorderid = lorderid.text.strip()
            lamount = convert_to_float(stringify(lamount).strip())
            lrate = convert_to_float(lrate.text.strip()) / 100
            lqueue = convert_to_float(stringify(lqueue).strip())
            lanchor = lactions.xpath('./a[contains(text(),"Cancel")]')

            orders.append({"date": ldate, "id": lorderid, "amount": lamount, "rate": lrate, "queue": lqueue,
                           "cancel_url": lanchor[0].attrib['href']})

        return pd.DataFrame(orders)

    def cancel_order(self, order):
        """Cancel an order placed previously

        :param order: a DataFrame with one record. Must contain a cancel_url series
        :return:
        """
        logger.debug("Cancelling order %s", order.id)
        logger.debug("GET request URL: %s", order.cancel_url)
        page = self._session.get(order.cancel_url)
        tree = html.fromstring(page.text, base_url=page.url)

        # Check if we have arrived on the confirmation page
        confirm_tag = tree.xpath('.//form/descendant::h1')
        if len(confirm_tag) > 0 and confirm_tag[0].text.strip(' \n\r') == "Cancel Order":
            logger.debug("Request was accepted. Need to confirm")
            form = tree.forms[0]
            form.fields["__EVENTTARGET"] = "ctl00$cphContentArea$cphForm$btnConfirm"

            logger.debug("Submit form")
            page = html.submit_form(form, open_http=self._get_http_helper())
            self._sleep_if_needed()

            tree = html.fromstring(page.text, base_url=page.url)
            form = tree.forms[0]

        else:
            raise RateSetterException('Cannot cancel order')

    def get_provision_fund(self):
        """Get the status of the provision fund

        :return: A pandas dataframe with two series:

        * amount: the amount in the fund in GBP
        * coverage: the coverage ratio of the fund
        """
        logger.debug("GET request URL: %s", provision_fund_url)
        page = self._session.get(provision_fund_url)
        tree = html.fromstring(page.text, base_url=page.url)

        response = {}

        span = tree.xpath('.//span[@class="pf-balance"]')
        response['amount'] = convert_to_float(span[0].text)

        span = tree.xpath('.//div[@class="col-xs-12 coverage-box"]/descendant::span[@class="value"]')  #
        response['coverage'] = convert_to_float(span[0].text) / 100

        return pd.DataFrame(response, index=[0])
