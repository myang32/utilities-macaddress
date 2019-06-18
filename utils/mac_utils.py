#!/usr/bin/python

"""Mac Utils.

Queries the macaddress.io api for vendor information.

Example:
        ~$ python mac_utils.py --macaddress $MAC_ADDRESS --token $API_TOKEN
Usage:
        ~$ python git_reports.py --help
Todo:

"""

import sys
import argparse

try:
    import requests
    HAS_IMPORTS = True
except ImportError:
    HAS_IMPORTS = False

DEFAULT_ENDPOINT = "api.macaddress.io"
DEFAULT_OUTPUT = 'json'
MAC_ADDR = "?output=%s&search=%s"


class MacAddressIoRestOps(object):
    """MacAddressIoRestOperations
    param :: args
    returns :: requested queries results
    """

    @property
    def session(self):
        return self._session

    @property
    def baseurl(self):
        return self._baseurl

    def __init__(self, args):
        super(MacAddressIoRestOps, self).__init__()
        self.args = args
        self._verify = args.secure
        self._baseurl = self.base_url()
        self._session = self._get_session(self.args.token)

    def _get_session(self, token):
        """ """
        session = requests.Session()
        session.verify = self._verify
        session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Authentication-Token': token
        }
        return session

    def base_url(self):
        """ """
        return "https://%s/v1" % DEFAULT_ENDPOINT

    def do_get(self, url):
        """ """
        response = None
        content = None
        try:
            response = requests.get(
                url,
                headers=self.session.headers,
                verify=self.session.verify
            )
        except requests.exceptions.HTTPError as http_err:
            raise http_err
        except requests.exceptions.RequestException as req_err:
            raise req_err
        except Exception as gen_err:
            raise gen_err

        if response.status_code != 200:
            raise response.status_code
        try:
            content = response.json()
        except ValueError:
            pass
        return response.status_code, content

    def query_mac_address(self, mac_address, output_type=DEFAULT_OUTPUT):
        """ """
        path = MAC_ADDR % (output_type, mac_address)
        url = "%s/%s" % (self.baseurl, path)
        status_code, content = self.do_get(url)
        return content

    def get_mac_company_name(self, query_results):
        """ """
        valid_mac = query_results['macAddressDetails']['isValid']
        company_name = query_results['vendorDetails']['companyName']
        mac_addr = query_results['macAddressDetails']['searchTerm']
        msg = "Companye Name: %s\nMAC Address: %s" % (company_name, mac_addr)

        if valid_mac and not company_name:
            msg = "Valid MAC Address: %s\nCompany Name NOT Found" % mac_addr
        return msg

class MacAddressIoOps(object):
    """MacAddressIoOperations,
    params :: args
    returns :: results
    """

    def __init__(self, args):
        super(MacAddressIoOps, self).__init__()
        self.args = args
        self.rest_ops = MacAddressIoRestOps(self.args)

    def do_request(self):
        """ """
        mac_address_results = self.rest_ops.query_mac_address(
            self.args.macaddress
        )
        mac_address_company_name = self.rest_ops.get_mac_company_name(
            mac_address_results
        )
        return mac_address_company_name


def main():
    """ """
    parser = argparse.ArgumentParser(description='Query macaddress.io api')
    parser.add_argument('-t',
                        '--token',
                        type=str,
                        required=True,
                        help='API Token')
    parser.add_argument('-m',
                        '--macaddress',
                        type=str,
                        required=True,
                        help="MAC address to query")
    parser.add_argument('-s',
                        '--secure',
                        type=bool,
                        required=False,
                        default=False,
                        help="SSL Verify")
    args = parser.parse_args()
    mac_ops = MacAddressIoOps(args)
    results = mac_ops.do_request()

    print "\n--- Results ---\n"
    print results
    print "\n--- End Results ---\n"


if __name__ == '__main__':
    if not HAS_IMPORTS:
        print "Failed to import modules"
        sys.exit(1)
    main()
