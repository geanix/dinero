from libdinero import Dinero, Contact
import attr

def contacts_add_upd_arguments(parser):
    parser.add_argument('--Name')
    parser.add_argument('--Email')
    parser.add_argument('--ExternalReference')
    parser.add_argument('--VatNumber')
    parser.add_argument('--CountryKey', default='DK')
    parser.add_argument('--IsPerson', action='store_true')
    parser.add_argument('--UseCvr', action='store_true')
    parser.add_argument('--Street')
    parser.add_argument('--ZipCode')
    parser.add_argument('--City')
    parser.add_argument('--Phone')
    parser.add_argument('--Webpage')
    parser.add_argument('--AttPerson')
    parser.add_argument('--EanNumber')
    parser.add_argument('--PaymentConditionType')
    parser.add_argument('--PaymentConditionNumberOfDays', type=int)
    parser.add_argument('--IsMember', action='store_true')
    parser.add_argument('--MemberNumber')
    parser.add_argument('--CompanyTypeKey', default='PrivateLimitedCompany')

def contacts_arguments(subparsers, config, global_arguments):
    contacts_parser = subparsers.add_parser('contacts', help='list contacts')
    global_arguments(contacts_parser, config)
    contacts_parser.add_argument('--deletedOnly', action='store_true')
    contacts_parser.set_defaults(func=contacts_handler)
    contacts_subparsers = contacts_parser.add_subparsers(dest='contacts_subcommand')

    contacts_add_parser = contacts_subparsers.add_parser('add', help='add contact')
    contacts_add_upd_arguments(contacts_add_parser)

    contacts_upd_parser = contacts_subparsers.add_parser('update', help='update contact')
    contacts_upd_parser.add_argument('--ContactGuid', required=True)
    contacts_add_upd_arguments(contacts_upd_parser)

    contacts_del_parser = contacts_subparsers.add_parser('delete', help='delete contact')
    contacts_del_parser.add_argument('--ContactGuid', required=True)

    contacts_rst_parser = contacts_subparsers.add_parser('restore', help='restore contact')
    contacts_rst_parser.add_argument('--ContactGuid', required=True)

def contacts_handler(args):
    dinero = Dinero(
        args.client_id,
        args.client_secret,
        args.organization_key,
        args.organization_name,
        args.organization_id,
    )

    contacts_subcommand = args.contacts_subcommand

    if contacts_subcommand == 'add' or contacts_subcommand == 'update':
        contact = Contact(
              Name=args.Name,
              Email=args.Email,
              ExternalReference=args.ExternalReference,
              VatNumber=args.VatNumber,
              CountryKey=args.CountryKey,
              IsPerson=args.IsPerson,
              UseCvr=args.UseCvr,
              Street=args.Street,
              ZipCode=args.ZipCode,
              City=args.City,
              Phone=args.Phone,
              Webpage=args.Webpage,
              AttPerson=args.AttPerson,
              EanNumber=args.EanNumber,
              PaymentConditionType=args.PaymentConditionType,
              PaymentConditionNumberOfDays=args.PaymentConditionNumberOfDays,
              IsMember=args.IsMember,
              MemberNumber=args.MemberNumber,
              CompanyTypeKey=args.CompanyTypeKey,
        )

        if contacts_subcommand == 'add':
            contact = dinero.contacts.add(contact)
        elif contacts_subcommand == 'update':
            contact.ContactGuid = args.ContactGuid
            contact = dinero.contacts.update(contact)

        print(contact)

    elif contacts_subcommand == 'delete':
        dinero.contacts.delete(args.ContactGuid)

    elif contacts_subcommand == 'restore':
        dinero.contacts.restore(args.ContactGuid)

    else:
        for contact in dinero.contacts.list(deletedOnly=args.deletedOnly):
            print(contact)
