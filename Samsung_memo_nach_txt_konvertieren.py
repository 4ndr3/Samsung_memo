import os
import re
import glob
import zipfile
import xmltodict
from datetime import datetime

MEMO_PATH = r'/Users/andre/Desktop/Memo'
RESULTS_PATH = r'/Users/andre/Desktop/ausgabe'

memos = glob.glob(MEMO_PATH + '/*.memo')

for i, memo in enumerate(memos):
    print('{}/{} - {}'.format(i+1, len(memos), memo))

    try:
        # Extract *.memo file and read the content
        archive = zipfile.ZipFile(memo, 'r')
        memo_content = archive.read('memo_content.xml').decode('utf-8')
        cleanr = re.compile('&.*?;')
        memo_content = re.sub(cleanr, '', memo_content)
        memo_content = xmltodict.parse(memo_content)
        text = memo_content['memo']['contents']['content']
        text = text.replace('/pp','\n')

        # Generate filename from memo timestamp
        #timestamp = int(memo_content['memo']['header']['meta'][2]['@createdTime'][:10])
        #date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H-%M-%S')
        #file_name = '{}.txt'.format(date)
        file_name = str(i)+'.txt'

        # Save file as a *.txt
        with open(os.path.join(RESULTS_PATH, file_name), 'w', encoding='utf-8') as file:
            file.write(text)

    except zipfile.BadZipFile:
        continue