from __future__ import annotations

if False:
    from .dinero import Dinero

from typing import Generator, Union, List, Dict
import attr

@attr.s(auto_attribs=True)
class InvoiceFields(object):
      Guid: str = ''
      Number: int = 0
      UpdatedAt: str = ''
      Status: str = ''
      ContactName: str = ''
      Description: str = ''
      Date: str = ''
      Currency: str = ''
      TotalInclVat: int = 0
      TotalExclVat: int = 0
      TotalInclVatInDkk: int = 0
      TotalExclVatInDkk: int = 0
      ExternalReference: str = ''
      PaymentDate: str = ''
      Type: str = ''
      ContactGuid: str = ''
      MailOutStatus: str = ''
      CreatedAt: str = ''
      DeletedAt: str = ''

@attr.s(auto_attribs=True)
class Invoice(InvoiceFields):
      InvoiceTemplateId: str = ''
      TotalVatableAmount: int = 0
      TotalNonVatableAmount: int = 0
      TotalVat: int = 0
      TotalLines: List[Dict[str, Union[str, int]]] = []
      ShowLinesInclVat: bool = False
      PaymentStatus: str = ''
      PaymentConditionNumberOfDays: int = 0
      PaymentConditionType: str = ''
      FikCode: str = ''
      DepositAccountNumber: int = 0
      Status: str = ''
      TimeStamp: str = ''
      Language: str = ''
      Comment: str = ''
      Address: str = ''
      ProductLines: List[Dict[str, Union[str, int]]] = []

class Invoices(object):
    def __init__(self, dinero: Dinero):
        self.dinero = dinero

    def list(
        self,
        startDate: str = None,
        endDate: str = None,
        freeTextSearch: str = None,
        statusFilter: str = None,
        queryFilter: dict = {},
        changesSince: str = None,
        deletedOnly: bool = False,
        sort: str = None,
        sortOrder: str = None,
        pageSize: int = 100,
    ) -> Generator[Invoice, None, None]:
        fields = attr.fields_dict(InvoiceFields).keys()

        invoices = self.dinero.get_json_paged(
            'invoices',
            fields=','.join(fields),
            startDate=startDate,
            endDate=endDate,
            freeTextSearch=freeTextSearch,
            statusFilter=statusFilter,
            queryFilter=queryFilter,
            changesSince=changesSince,
            deletedOnly=deletedOnly,
            sort=sort,
            sortOrder=sortOrder,
            pageSize=pageSize,
        )

        for invoice in invoices:
            yield Invoice(**invoice)

    def get_pdf(self, Guid: str):
        invoice = self.dinero.get_binary(
            f'invoices/{Guid}',
            headers=dict(Accept='application/octet-stream'),
        )

        return invoice


    def get_json(self, Guid: str):
        invoice = self.dinero.get_json(
            f'invoices/{Guid}',
            headers=dict(Accept='application/json'),
        )

        return Invoice(**invoice)

    def get(
        self,
        Guid: str,
        Format: str = 'json',
    ) -> Union[Dict[str, Any], bytes]:
        if Format == 'json':
            return self.get_json(Guid)
        elif Format == 'pdf':
            return self.get_pdf(Guid)
        else:
            raise ValueError(f'Invalid Format: {Format}')

