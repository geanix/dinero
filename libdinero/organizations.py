import attr

@attr.s(auto_attribs=True)
class Organization(object):
    Name: str
    Id: int
    IsPro: bool
    IsPayingPro: bool
    IsVatFree: bool
    Email: str
    IsTaxFreeUnion: bool

class Organizations(object):
    def __init__(self,dinero):
        self.dinero = dinero

    def list(self):
        rsp = self.dinero.client.get(
            f'{self.dinero.api_endpoint}/organizations',
            params=dict(fields='Name,Id,IsPro,IsPayingPro,IsVatFree,Email,IsTaxFreeUnion')
        )

        return [Organization(**o) for o in rsp.json()]
