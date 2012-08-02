import csvtools
from collections import Counter
 
denver      = csvtools.Report('others/Denver.csv')
littleton   = csvtools.Report('others/Littleton.csv')

selected = denver.headers()[2:]

for i in denver.selectColumns(*selected):
    print i[0], i[1]
