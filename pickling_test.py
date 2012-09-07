#!usr/bin/env python

import cPickle as pickle
import desk
import os

def weCanPickleThat(data, filename):
    out_f = open(filename, 'wb')
    try:
        pickle.dump(data, out_f, protocol=2)
    finally:
        out_f.close()

def weCanUnpickleThat(filename):
    in_s = open(filename, 'rb')
    try:
        o = pickle.load(in_s)
    finally:
        in_s.close()
    return o

def getPickledCase(case_id, ext='.dat'):
    case_id = str(case_id)
    file_case_id = case_id
    while len(file_case_id) < 5:
        file_case_id = '0' + case_id
    filename = file_case_id + ext
    dirpath = '/'.join(list(str(case_id)))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = '/'.join([dirpath, filename])
    try:
        case = weCanUnpickleThat(filepath)
    except:
        case = desk.Case(id_num=case_id)
        weCanPickleThat(case, filepath)
    return case

def main():
    for i in range(3388, 3513):
        case = getPickledCase(i)
        if hasattr(case, 'subject'):
            print case.subject

if __name__ == '__main__':
    main()
