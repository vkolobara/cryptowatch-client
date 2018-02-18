from abc import ABC, abstractmethod
import csv
import os
import logging

class Writer(ABC):
    @abstractmethod
    def write(self, rows):
        pass

class CSVWriter(Writer):
    def __init__(self, out):
        self.out = out
        if not os.path.exists(self.out) or os.stat(self.out).st_size == 0:
            CSVWriter.write_header(self.out)

    @staticmethod
    def write_header(out):
        logging.info("Headers need to be created for %s" % out)
        with open(out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume'])
        logging.info("Headers created for %s" % out)

    def write(self, rows):
        logging.info("Writing rows to %s" % self.out)
        with open(self.out, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in rows:
                writer.writerow(row)
            with open(self.out + ".last_time", 'w') as f:
                f.write(str(row[0]))
        logging.info("%d rows written to %s" % (len(rows), self.out))
