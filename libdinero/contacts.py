import attr

@attr.s(auto_attribs=True)
class Contact(object):
    ContactGuid: str = ''
    CreatedAt: str = ''
    UpdatedAt: str = ''
    DeletedAt: str = ''
    IsDebitor: bool = False
    IsCreditor: bool = False
    ExternalReference: str = ''
    Name: str = ''
    Street: str = ''
    ZipCode: str = ''
    City: str = ''
    CountryKey: str = 'DK'
    Phone: str = ''
    Email: str = ''
    Webpage: str = ''
    AttPerson: str = ''
    VatNumber: str = ''
    EanNumber: str = ''
    PaymentConditionType: str = ''
    PaymentConditionNumberOfDays: int = 0
    IsPerson: bool = False
    IsMember: bool = False
    MemberNumber: str = ''
    UseCvr: bool = False
    CompanyTypeKey: str = ''

class Contacts(object):

    def __init__(self,dinero):
        self.dinero = dinero

    def list(
        self,
        queryFilter: dict = {},
        changesSince: str = None,
        deletedOnly: bool = False,
        pageSize: int = 100,
    ):
        fields = attr.fields_dict(Contact).keys()

        contacts = self.dinero.get_json_paged(
            'contacts',
            fields=','.join(fields),
            queryFilter=queryFilter,
            changesSince=changesSince,
            deletedOnly=deletedOnly,
            pageSize=pageSize,
        )

        for contact in contacts:
            yield Contact(**contact)

    def get(self, guid):
        contact = self.dinero.get_json(f'contacts/{guid}')

        return Contact(**contact)

    def add(self, contact):
        contact_guid = self.dinero.post_json('contacts', **attr.asdict(contact))

        return self.get(contact_guid['ContactGuid'])

    def update(self, contact):
        self.dinero.put_json(f'contacts/{contact.ContactGuid}', **attr.asdict(contact))

        return self.get(contact.ContactGuid)

    def delete(self, guid):
        self.dinero.delete_json(f'contacts/{guid}')

    def restore(self, guid):
        self.dinero.post_json(f'contacts/{guid}/restore')

        return self.get(guid)
