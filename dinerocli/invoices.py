from argparse import FileType
from libdinero import Dinero

def invoices_arguments(subparsers, config, global_arguments):
    invoices_parser = subparsers.add_parser('invoices', help='list invoices')
    global_arguments(invoices_parser, config)
    invoices_parser.add_argument('--deletedOnly', action='store_true')
    invoices_parser.set_defaults(func=invoices_handler)
    invoices_subparsers = invoices_parser.add_subparsers(dest='invoices_subcommand')

    invoices_add_parser = invoices_subparsers.add_parser('add', help='add invoice')
    invoices_get_parser = invoices_subparsers.add_parser('get', help='get invoice')
    invoices_get_parser.add_argument('--Format', default='json', choices=['json', 'pdf'])
    invoices_get_parser.add_argument('--Output', type=FileType('wb'), default='-')
    invoices_get_parser.add_argument('--Guid', required=True)

def invoices_handler(args):
    dinero = Dinero(
        args.client_id,
        args.client_secret,
        args.organization_key,
        args.organization_name,
        args.organization_id,
    )

    if args.invoices_subcommand == 'add':
        pass

    if args.invoices_subcommand == 'get':
        invoice = dinero.invoices.get(Format=args.Format, Guid=args.Guid)

        if args.Format == 'json':
            print(invoice)
        else:
            args.Output.write(invoice)

    else:
        for invoice in dinero.invoices.list(deletedOnly=args.deletedOnly):
            print(invoice)
