import json
import httplib
import urllib

def fixName(name):
    firstName=''
    lastName=''
    fullName=''
    for i, c in enumerate(name):
        if c == ",":
            firstName = name[i+1:]
            lastName = name[:i]
            fullName = firstName +' '+ lastName
    return fullName

def pictureAvailable(pictureLink):
    pictureLinkString = ''.join(pictureLink)
    if pictureLinkString == '../PhotoNotAvail.gif':
        return False
    else:
        return True

def heightToInches(height):
    heightList = list(height)
    length = len(heightList)
    heightList.pop(length-1)
    heightList.pop(1)
    
    if len(heightList) == 0:
      return 0
    elif len(heightList) == 3:
      firstNumber = int(heightList[0]) * 12
      totalHeight = firstNumber + 10 
      totalHeight = totalHeight + int(heightList[2])
      return totalHeight
    else:
      firstNumber = int(heightList[0]) * 12
      totalHeight = firstNumber + int(heightList[1])
      return totalHeight
    

def fixAddress(address):

    if address[0]=="," and not address.find('County'):
        return ''

    elif address[0]=="," and address.find('County'):
        addressList = list(address)
        addressList.pop(0)
        addressList.pop(0)
        adjustedAddress = "".join(addressList)
        locationOfComma = adjustedAddress.find(',')
        return adjustedAddress[:locationOfComma]

    else:
        locationOFCounty = address.find('County')
        newAddress = address[:locationOFCounty]
        return newAddress

def lastName(fullName):
    indexOfFirstCharacterOfLastName = 0
    for K in range(len(fullName), 0, -1):
        if fullName[K-1] == " ":
            indexOfFirstCharacterOfLastName = K
            break
    lastName = fullName[K:]
    return lastName

def firstName(fullName):
    indexOfFirstCharacterOfLastName = 0
    for K in range(0,len(fullName)):
        if fullName[K] == " ":
            indexOfFirstCharacterOfLastName = K
            break
    firstName = fullName[:K]
    return firstName

def save_predator_to_database(predator):
    if 'ImageLink' in predator:
        linkToImageSavedInDatabase = save_image_to_dabase(predator)
        save_predator_info_to_database_with_picture(predator,linkToImageSavedInDatabase)
    else:
        save_predator_info_to_database_without_picture(predator)

def save_image_to_dabase(predator):
    image = urllib.urlopen(predator['ImageLink'])
    jpgdata = image.read()

      # Save Image To Database
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/files/pic.jpg', jpgdata, {
    "X-Parse-Application-Id": "WhatEverMyX-Parse-Application-Id-IS",
    "X-Parse-REST-API-Key": "WhatEverMyX-Parse-REST-API-Key-IS",
    "Content-Type": "image/jpeg"
    })
    result = json.loads(connection.getresponse().read())
    imageLinkSavedInDatabase = result['name']
    return imageLinkSavedInDatabase

def save_predator_info_to_database_with_picture(predator,linkToImageSavedInDatabase):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/Predator', json.dumps({
       "FirstName": predator['FirstName'],
       "LastName": predator['LastName'],
       "Name": predator['FullName'],
       "PredatorID":predator['offenderID'],
       "DOB": predator['DOB'],
       "Gender": predator['Gender'],
       "Crimes": predator['Crimes'],
       "Height": predator['Height'],
       "Weight": predator['Weight'],
       "EyeColor": predator['EyeColor'],
       "HairColor": predator['HairColor'],
       "Ethnicity": predator['Ethnicity'],
       "Address": predator['Address'],

       "picture": {
         "name": linkToImageSavedInDatabase,
         "__type": "File"
       }
     }), {
       "X-Parse-Application-Id": "WhatEverMyX-Parse-Application-Id-IS",
       "X-Parse-REST-API-Key": "WhatEverMyX-Parse-REST-API-Key-IS",
       "Content-Type": "application/json"
     })
    Finalresult = json.loads(connection.getresponse().read())
    print Finalresult


def save_predator_info_to_database_without_picture(predator):
        # Save Predator Information To Database & Associate Image With Information
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/Predator', json.dumps({
       "FirstName": predator['FirstName'],
       "LastName": predator['LastName'],
       "Name": predator['FullName'],
       "PredatorID":predator['offenderID'],
       "DOB": predator['DOB'],
       "Gender": predator['Gender'],
       "Crimes": predator['Crimes'],
       "Height": predator['Height'],
       "Weight": predator['Weight'],
       "EyeColor": predator['EyeColor'],
       "HairColor": predator['HairColor'],
       "Ethnicity": predator['Ethnicity'],
       "Address": predator['Address']
     }), {
       "X-Parse-Application-Id": "WhatEverMyX-Parse-Application-Id-IS",
       "X-Parse-REST-API-Key": "WhatEverMyX-Parse-REST-API-Key-IS",
       "Content-Type": "application/json"
     })
    Finalresult = json.loads(connection.getresponse().read())
    print Finalresult









    