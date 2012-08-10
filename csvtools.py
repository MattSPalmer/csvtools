import csv
import mylogs
import time
import typeutil
from datetime import datetime

now = datetime.today()
currentDateString = '{0}-{1}-{2}'
currentDateString = currentDateString.format(str(now.year), str(now.month),
        str(now.day))


class Report:
    def __init__(self, reportFile, writeFile=None, date="%Y-%m-%d %H:%M:%S"):
        """Read in a CSV file."""
        with open(reportFile, 'rb') as readFile:
            self.fileRows = [row for row in csv.reader(readFile)]
            # self.fileRows = [map(typeutil.to_num, row)
            #         for row in csv.reader(readFile)]
            readFile.close()
        self.rowBuffer = self.fileRows
        self.dateFormat = date
        if writeFile == None:
            self.writeFile = '%s_write_%s.csv' % (reportFile[:-4],
                    currentDateString)
    
    def __str__(self):
        return str(self.rowBuffer)

    def __getitem__(self, index):
        return self.rowBuffer[index]

    def write(self, writeFileName=None):
        if not writeFileName:
            writeFileName = self.writeFile
        with open(writeFileName, 'wb') as writingFile:
            importWriter = csv.writer(writingFile)
            for row in self.rowBuffer:
                importWriter.writerow(row)
            writingFile.close()
        mylogs.log.info("Wrote file '%s', %s lines" % (writeFileName,
                len(self.rowBuffer)))

    def reset(self):
        del self.rowBuffer
        self.rowBuffer = self.fileRows
        return self

    def headers(self):
        return self.rowBuffer[0]

    def removeColumns(self, *args):
        for arg in args:
            index = self.headers().index(arg)
            for row in self.rowBuffer:
                row.pop(index)
        return self

    def filter(self, column, query=None, header=True, inverse=False):
        if column not in self.headers():
            print 'Error: invalid column header name.'
        else:
            columnIndex = self.headers().index(column)
            if inverse:
                self.scratchrows = [row for row in
                    self.rowBuffer if query not in row[columnIndex]]
            else:
                self.rowBuffer = [row for row in
                    self.rowBuffer if query in row[columnIndex]]
            if self.headers() != self.rowBuffer[0]:
                self.rowBuffer.insert(0, self.headers())
            return self

    def toDict(self):
        dictFromColumns = {}

        def toDate(datestr):
            return datetime.strptime(datestr, self.dateFormat)

        for i, elem in enumerate(self.rowBuffer[0]):
            if 'date' in elem:
                column = [toDate(row[i]) for row in self.rowBuffer[1:]]
            else:
                 column = [row[i] for row in self.rowBuffer[1:]]
            dictFromColumns[elem] = column
        return dictFromColumns
