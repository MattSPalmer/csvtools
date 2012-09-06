#!usr/bin/env python

import desk

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
            print '-'*20
            print interaction.incoming.email.body
            if interaction == case[-1]:
                continue
            raw_input('Press Enter to continue...')
        if case == search[-1]:
            continue
        raw_input('Press Enter to continue...')
        print '\n\n'



if __name__ == '__main__':
    main()
