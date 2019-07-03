from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from operator import itemgetter
from typing import Union, Any, List, Dict, Generator

import logging
import attr
import json

from .exceptions import NotConnectedError, NotConfiguredError, NotAuthenticatedError
from .contacts import Contacts, Contact
from .organizations import Organizations, Organization
from .invoices import Invoices, Invoice

JSONType = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
logger = logging.getLogger(__name__)

class Dinero(object):
    '''Entry point for the Dinero API module

    :param oauth_url:     Dinero OAUTH authentication endpoint
    :param client:        Requests session client
    :param token:         OAuth token for client session
    :param organization:  Organization id to use in queries
    '''

    api_endpoint: str = 'https://api.dinero.dk/v1'
    authentication_endpoint: str = 'https://authz.dinero.dk/dineroapi/oauth/token'
    client: OAuth2Session = None
    token = None
    organization: Organization

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        organization_key: str = None,
        organization_name: str = None,
        organization_id: int = None,
    ):
        '''Create an oauth connection

        :param client_id:         ID of client developing the service integrating with Dinero
        :param client_secret:     Secrect of client developing the servuce integrating with Dinero
        :param organization_key:  Unique key from the company using the service
        :param organization_name: Name of the company using the service
        :param organization_id:   Numeric ID of company using the service
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))

        if organization_key:
            self.authenticate(organization_key)

        self.organizations = Organizations(self)
        self.contacts = Contacts(self)
        self.invoices = Invoices(self)

        # set default organization if only one is found, or name/id is passed
        if len(self.organizations.list()) == 1 or organization_name or organization_id:
            self.set_organization(organization_name, organization_id)

    def is_connected(self) -> None:
        '''Check if instance is connected'''
        if self.client is None:
            raise NotConnectedError('Instance not connected')

    def is_authenticated(self) -> None:
        '''Check if instance is authenticated'''
        self.is_connected()

        if self.token is None:
            raise NotAuthenticatedError('Instance not authenticated')

    def is_configured(self) -> None:
        '''Check if instance is configured'''
        self.is_authenticated()

        if not self.organization:
            raise NotConfiguredError('Instance not configured')

    def set_authentication_endpoint(self, authentication_endpoint: str) -> None:
        '''Override default OAUTH authentication endpoint url

        :param authentication_endpoint: New endpoint url to use
        '''
        self.authentication_endpoint = authentication_endpoint

    def set_api_endpoint(self, api_endpoint: str):
        '''Override default Dinero API endpoint url

        :param api_endpoint: New enpoint url to use
        '''

        self.api_endpoint = api_endpoint.rstrip('/')

    def authenticate(self, organization_key: str) -> None:
        '''Get authentication token from OAUTH endpoint

        :param organization_key: Unique key for company using the service
        '''
        self.is_connected()

        self.token = self.client.fetch_token(
            token_url=self.authentication_endpoint,
            username=organization_key,
            password=organization_key,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

    def get_binary(self, resource: str, headers: Dict[str, str] = None, **kwparams) -> Any:
        '''Make a GET request and return response as bytes'''
        self.is_configured()

        rsp = self.client.get(
            f'{self.api_endpoint}/{self.organization.Id}/{resource}',
            headers=headers,
            params=kwparams
        )
        rsp.raise_for_status()

        return rsp.content

    def get_json(self, resource: str, headers: Dict[str, str] = None, **kwparams) -> Any:
        '''Make a GET request and return response as json'''
        self.is_configured()

        rsp = self.client.get(
            f'{self.api_endpoint}/{self.organization.Id}/{resource}',
            headers=headers,
            params=kwparams
        )
        rsp.raise_for_status()

        return rsp.json()

    def get_json_paged(self, resource: str, **kwparams) -> Generator[Dict[str, Any], None, None]:
        '''Make paginated GET request and return a generator to json items'''
        page = 0
        count = 0

        while True:
            j = self.get_json(resource, page=page, **kwparams)
            collection = j.get('Collection', [])
            pagination = j.get('Pagination', {})

            for item in collection:
                yield item

            page  += 1
            count += pagination.get('Result')

            if count == pagination.get('ResultWithoutFilter'):
                break

    def post_json(self, resource: str, **kwparams) -> JSONType:
        '''Make a POST request and return response as json'''
        self.is_configured()

        rsp = self.client.post(f'{self.api_endpoint}/{self.organization.Id}/{resource}', json=kwparams)
        rsp.raise_for_status()

        return rsp.json() if rsp.content else None

    def put_json(self, resource: str, **kwparams) -> None:
        '''Make a PUT request and return response as json'''
        self.is_configured()

        rsp = self.client.put(f'{self.api_endpoint}/{self.organization.Id}/{resource}', json=kwparams)
        rsp.raise_for_status()

    def delete_json(self, resource: str, **kwparams) -> None:
        '''Make a DELETE request and return response as json'''
        self.is_configured()

        rsp = self.client.delete(f'{self.api_endpoint}/{self.organization.Id}/{resource}', json=kwparams)
        rsp.raise_for_status()

    def set_organization(self, organization_name: str = None, organization_id: int = None) -> None:
        self.is_authenticated()

        organizations = self.organizations.list()
        organizations_len = len(organizations)

        if len(organizations) == 0:
            raise ValueError('no organizations found')

        if organization_name and organization_id:
            organization = next(iter(o for o in organizations if o.Name == organization_name and o.Id == organization_id), None)
        elif organization_name:
            organization = next(iter(o for o in organizations if o.Nane == organization_name), None)
        elif organization_id:
            organization = next(iter(o for o in organizations if o.Name == organization_id), None)
        elif organizations_len > 1:
            raise ValueError('`organization_name` and/or `organization_id` must be given')
        elif organizations_len == 1:
            organization = organizations[0]

        if organization is None:
            raise ValueError(f'organization not found: Name: `{organization_name}`, Id: `{organization_id}`')

        self.organization = organization
