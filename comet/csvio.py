import csv
import codecs

def leadAll():
    rows = []
    reader = None
    for path in glob.iglob(config.data_folder + '*.csv'):
        with codecs.open(path, 'r', encoding='latin1') as inFile:
            reader = csv.reader(inFile)
            for row in reader:
                if row not in rows:
                    rows.append(row)
    if reader is None:
        click.echo('No csv files found, nothing to do')
        exit(1)
    return rows;


def loadOne(path):
    rows = []
    with codecs.open(path, 'r', encoding='latin1') as inFile:
        reader = csv.reader(inFile)
        for row in reader:
            rows.append(row)
    return rows


def writeRows(rows, out_path):
    with open(out_path, 'w') as outFile:
        writer = csv.writer(outFile)
        for row in rows:
            writer.writerow(row)
