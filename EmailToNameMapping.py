from nltk import metrics

def emailToNameMapping(emailList,nameList):
	dictOfEmails = dict() 
	name = ''
	finalEmailNameMapping = dict()
	
	for j in range(len(emailList)):
		editdistance = 1000 #initialize the editdistance to a large value
		mindistance = 1000  #initialize minimum editdistance for a compound
							#name's(eg: Sharanpreet Singh Lobana) individual components(eg Singh)

		#Filter the email for computing the editDistance by removing the digits 
		filteredEmail = ''.join([i for i in emailList[j].split('@')[0] if not i.isdigit()])
		
		for n in range(len(nameList)):
			if len(nameList[n].split())>1:  #if name consists of more than one component(eg Rahul Kashyap)
				subnames = nameList[n].split() #separate name into its components
				#Remove any dots from the subnames(eg [P.,Kumar] changes to [P,Kumar])
				subnames = [w.replace('.','') for w in subnames] 

				for m in range(len(subnames)):
					if(len(subnames[m])>2): #Compute the edit distance only if the subname is not an abbrevation(eg: Dr)
						distance = metrics.edit_distance(filteredEmail.lower(),subnames[m].lower())
						if distance < mindistance:
							#If the editDistance found is less than the mindistance so far
							mindistance = distance #Update the mindistance for the subnames
				
				if mindistance < editdistance:
					# if the editdistance for given name is minimum among all the names compared so far
					editdistance = mindistance # Update the minimum editdistance
					name = nameList[n]  #Current best match is the given name
				
				combinedname = nameList[n].replace(' ','') #Check editdistance for the combinedname as well
				combinedname = combinedname.replace('.','')#Remove all the dots in the combinedname
				distance = metrics.edit_distance(filteredEmail.lower(),combinedname.lower())
				if distance < editdistance:
					editdistance = distance #if editDistance is less than current minimum
					name = nameList[n]      #Current best mapping
			
			#if name contains a single character
			else:
				distance = metrics.edit_distance(filteredEmail.lower(),nameList[n].lower())
				if distance < editdistance:
					editdistance = distance
					name = nameList[n] #Current best mapping
		
		try:
			finalEmailNameMapping[emailList[j]] = name #Update the mapping frequency corresponding to given name
		except:
			"List index out of bounds error probably"

	return finalEmailNameMapping