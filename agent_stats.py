#!usr/bin/env python

import desk
# from collections import Counter

def main():
    users = ['Stephen']
    search_parameters = {
            'status': 'open,pending',
            'labels': 'Needs Update'
            }
    case_blobs = {}

    for user in users:
        case_blobs[user] = desk.CaseSearch(assigned_user=user, **search_parameters)
        print '{}: {}'.format(user, case_blobs[user].total)
        print '='*40
        for case in case_blobs[user].itercases():
            total = case.getInteractions()['total']
            display_subj = (case.subject if len(case.subject) < 64
                    else case.subject[:64]+'...')
            print '[{}, {}] #{} - {}'.format(
                    case.status[0].upper(), total, case.id_num, display_subj)
            last_message = case.getLastInteraction()
            print last_message[0]
            print last_message[1]
        print


if __name__ == '__main__':
    main()


