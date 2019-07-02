from libdinero import Dinero

def organizations_arguments(subparsers, config, global_arguments):
    organizations_parser = subparsers.add_parser('organizations', help='list organizations')
    global_arguments(organizations_parser, config)
    organizations_parser.set_defaults(func=organizations_handler)

def organizations_handler(args):
    dinero = Dinero(
        args.client_id,
        args.client_secret,
        args.organization_key,
        args.organization_name,
        args.organization_id,
    )

    organizations = dinero.organizations.list()

    print('ID\tName')
    for organization in organizations:
        print(f'{organization.Id}\t{organization.Name}')
