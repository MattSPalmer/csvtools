import csvtools
from collections import Counter

report = csvtools.Report('ggdowntown.csv')

def avg(x): return round(sum(x) / len(x), 2)
def f(x):   return sum(report.toDict()[x])
def g(x):   return avg(report.toDict()[x])

tenderCount = report.toDict()['Payment Type']
tenders = dict(Counter(tenderCount)).keys()

categories = ['Total Price', 'Discount', 'Total Tax', 'Total']

for tender in tenders:
    print ''
    print tender.upper()
    print ''
    report.filter('Payment Type', tender)
    print 'Sums\n===='
    for category in categories:
        print category, ':', f(category)
    report.reset()


if __name__ == '__main__':
    pass
