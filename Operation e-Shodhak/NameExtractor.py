
from PyPDF2 import PdfFileWriter,PdfFileReader
import re
import enchant

regex = re.compile("([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(\.|"
                    "\sdot\s))+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)")

def get_emails(s):
	a=re.findall(regex,s)
	b=list()
	for a1 in a:
		b.append(a1[0])
	modified_s = re.sub("[^;]*?([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+\/=?^_`""{|}~-]+)*(@|\sat\s)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(\.|""\sdot\s))+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?).*?;",' ',s)
	return b,modified_s;


def textToNames(textIn):

    listofemails,modifiedText = get_emails(textIn)
    list_of_proper_nouns = []
    modifiedText = modifiedText.replace(',',';')
    listText = modifiedText.split(';')
    d = enchant.Dict("en_US")

    nameListAmbar =[]

    for text in listText:
        if len(text.strip())==0:
            listText.remove(text)
            continue
        text = text.replace('\n',' ')
        text = text.strip()
        text_to_lower = text.lower()
        nameListAmbar.append(text)
       
    return list(set(nameListAmbar))#list_of_proper_nouns