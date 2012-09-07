#!usr/bin/env python

import desk
# from collections import Counter


def main():
    search_parameters = {
            'status': 'open,pending',
            'labels': 'Needs Update',
            'assigned_group': 'Customer Care',
            }

    search = desk.CaseSearch(**search_parameters)

    for case in search:
        print case.subject
        print case.created_at
        print '='*20
        for interaction in case:
            print interaction.created_at
            print dir(interaction.mail)
            raw_input('Press Enter to continue...')
        print 'end of case.'
        raw_input('Press Enter to continue...')
        print '\n\n'



if __name__ == '__main__':
    main()
