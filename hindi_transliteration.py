letterOnly = {
    'a': 'ए',
    'b': 'बी',
    'c': 'सी',
    'd': 'डी',
    'e': 'ई',
    'f': 'एफ',
    'g': 'जी',
    'h': 'एच',
    'i': 'आई',
    'j': 'जे',
    'k': 'के',
    'l': 'एल',
    'm': 'एम',
    'n': 'एन',
    'o': 'ओ',
    'p': 'पी',
    'q': 'क्यू',
    'r': 'आर',
    's': 'एस',
    't': 'टी',
    'u': 'यू',
    'v': 'वी',
    'w': 'डब्ल्यू',
    'x': 'एक्स',
    'y': 'वाई',
    'z': 'ज़ेड',
}
letterInStart = {
    'a': 'अ',
    'aa':'आ',
    'e': 'ई',
    'i': 'इ',
    'o': 'ओ',
    'u': 'उ',
    'oo': 'ऊ',
    'ae': 'ऐ',
    'ie':'ए',
    'au': 'औ',
}
letterInAny= {
    'k': 'क्',
    'kh': 'ख्', 
    'g': 'ग्', 
    'gh': 'घ्', 
    'ch': 'च्', 
    'chh': 'छ्', 
    'j': 'ज्', 
    'jh': 'झ्', 
    't': ['ट्', 'त्'], 
    'th': 'थ्', 
    'd': ['ड्', 'द्'], 
    'dh': 'ढ्', 
    'dhh': 'ध्',
    'n': 'न्', 
    'p': 'प्', 
    'ph': 'फ्', 
    'b': 'ब्', 
    'bh': 'भ्', 
    'm': 'म्', 
    'y': 'य्', 
    'r': 'र्',
    'l': 'ल्', 
    'v': 'व्', 
    'sh': ['श्', 'ष्'],
    's': 'स्',
    'h': 'ह्',
    'ka': 'क',
    'c': 'क',
    'kha': 'ख',
    'ga': 'ग',
    'gha': 'घ',
    'cha': 'च',
    'chha': 'छ',
    'ja': 'ज',
    'z':'ज',
    'jha': 'झ',
    'ta': ['ट', 'त'],
    'tha': 'थ',
    'da': ['ड', 'द','ड़'],
    'dha': ['ढ','ध'],
    'dhha':'ध',
    'na': 'न',
    'pa': 'प',
    'pha': 'फ',
    'f': 'फ',
    'ba': 'ब',
    'bha': 'भ',
    'ma': 'म',
    'ya': 'य',
    'ra': 'र',
    'la': 'ल',
    'va': 'व',
    'wa': 'व',
    'sha': ['श', 'ष'],
    'sa': 'स',
    'ha': 'ह',
    'gya':'ज्ञा',
    #'ri':'ॠ',
    'ksha':'क्ष'
}
exceptionList=['f','c','z']
letterInMid={
    'a':'ा',
    'ai':'ै',
    'e': 'े',
    'ee':'ी',
    'i':'ि',
    'o': 'ो',
    'u': 'ु',
    'oo': 'ू',
    'au': 'ौ',
    'an':'ऺ',
}
letterInAnyKeys=letterInAny.keys()
letterInMidKeys=letterInMid.keys()
letterInStartKeys= letterInStart.keys()
#transliteration letter management system

#global variables
start=1
containerStr=""
container=[]
#checking call for known words and single word
def engToHindi(word):
    global container
    global containerStr
    word= word.strip().lower()
    if(len(word)==1):
        return letterOnly[word]
    #elif:
    #search for saved words in csv file using panda
    else:
        multiLetter(word)
        preProcess()
        output=assemble(process())
        container.clear()
        containerStr =""
        return output
#tranliterating multiLetter words
def multiLetter(word):
    global start
    global container
    global containerStr
    if(check(word[0])):
        containerStr= containerStr+word[0]
    for letter in range(1,len(word)):
        if not(check(containerStr+ word[letter])):
            container.append(containerStr)
            containerStr= word[letter]
            start=0
        else:
            containerStr= containerStr+word[letter]
    container.append(containerStr)
    return container
def check(letter):
    global start
    global container
    global containerStr
    if(start==1):
        #checking in letterInStart
        for req in letterInStartKeys:
            if(req.startswith(letter)):
                return True
    else:
        for req in letterInMidKeys:
            if(req.startswith(letter)):
                return True
    for req in letterInAnyKeys:
            if(req.startswith(letter)):
                return True
    return False
def preProcess():
    global container
    #preprocessing words for assembling
    for i in range(0,len(container)):
        #it checks for vowel consonant of hindi which can be overlapped
        try:
            result = (container[i+1]=='i' or container[i+1]=='u' or container[i+1]=='n')
        except IndexError:
            result= False
        if(container[i].endswith('a') and result ):
            if(container[i+1]=='i'):
                container[i+1]= "a"+ container[i+1]
                container[i]= (container[i])[:-1]
            elif(container[i+1]=='u'):
                container[i+1]= "a"+ container[i+1]
                container[i]= (container[i])[:-1]
            else:
                pass
                # print("report to programmer this word.This is potential bug.")
        #it corrects translation for vowel consonant in hindi telling previous letter that no '्' is required
        if(container[i] in letterInMidKeys and container[i]!='a' and i!=0 and container[i-1] not in exceptionList):
            container[i-1] =container[i-1]+'a'
    #ending word correction
    lastWord= container[len(container)-1]
    if(lastWord not in letterInMidKeys):
        if(lastWord.endswith('a')):
            container.append('a')
        else:
            container[len(container)-1]= container[len(container)-1]+'a'



def process():
    global container
    hindiWords=[]
    #assembling rule for splitteed word
    for i in range(0,len(container)):
        if(i==0):
            #starting phase recognition
            if(container[i] in letterInStartKeys):
                hindiWords.append(letterInStart[container[i]])
            elif(container[i] in letterInAnyKeys):
                hindiWords.append(letterInAny[container[i]])
        else:
            if(container[i] in letterInMidKeys):
                hindiWords.append(letterInMid[container[i]])
            elif(container[i] in letterInAnyKeys):
                hindiWords.append(letterInAny[container[i]])
    return hindiWords


def assemble(rawHindi):
    hindiWords=[""]
    for i in rawHindi:
        if(isinstance(i,str)):
            for j in range(0,len(hindiWords)):
                hindiWords[j] = hindiWords[j]+i
        else:
            initialLen= len(hindiWords)
            hindiWords= hindiWords*len(i)
            for j in range(len(i)):
                for k in range(initialLen*j,initialLen*(j+1)):
                    hindiWords[k]=hindiWords[k]+i[j]
            #for j in range(0,len(hindiWords)):
            #    hindiWords[j]= hindiWords[j]+ i[j]
    if(len(hindiWords)>1):
        for i in range(0,len(hindiWords)):
            print(i+1,".",hindiWords[i])
        inputChoice= int(input("Enter valid input:"))
        while(True):
            try:
                return hindiWords[inputChoice-1]
            except (IndexError,TypeError,ValueError):
                inputChoice= int(input("Enter valid input:"))
    else:
        return hindiWords[0]
        

#main program
userString= input("Enter :")
res=""
#handling multi world using a loop
userString=userString.strip()
splitWords= userString.split()
for i in splitWords:
    res = res+engToHindi(i)+' '
f = open("hindiPure.txt","w",encoding="utf-8")
f.write(res)
f.close()