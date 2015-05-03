import scrapy
from scrapy.http.request import Request
import json
import httplib
import Helpers

class DmozSpider(scrapy.Spider):
    name = "MehgansLaw"
    allowed_domains = ["meganslaw.ca.gov","api.parse.com"]
    start_urls = [
        "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=719389&searchby=CountyList&SelectCounty=ORANGE&SB=0&PageNo=%d" % page for page in xrange(1,25)]

    def parse(self, response):
        offenderList = []
        
        for links in response.xpath("//tr[@align='left']"):
            name = links.xpath('td[3]/a[1]/text()').extract()
            ID = links.xpath('td[3]/a[1]/@href').re("javascript: OpenDetail\('(.*?)'")

            offender={}

            nameString = ''.join(name)

            # Checks if valid path, valid path will have name
            if len(nameString)>1:
                offender['FullName'] = Helpers.fixName(nameString) 
                offender['FirstName'] = Helpers.firstName(offender['FullName'])
                offender['LastName'] = Helpers.lastName(offender['FullName'])
            
                IDString = ''.join(ID)
                offender['offenderID'] = IDString

                offender['link'] = "http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=719389&searchby=offender&id=" + IDString
                offenderList.append(offender)

        for offender in offenderList:
            # Checks if valid path, valid path will have name
            if len(nameString)>1:
                    yield scrapy.Request(offender['link'], meta={'person': offender}, callback=self.parse_offender)

    def parse_offender(self, response):

        predator = response.meta['person']

        AllCrimes = []
        for crimes in response.xpath('//td[@headers="descriptionColHdr"]'):
            NameOfCrime = crimes.xpath('text()').extract()
            NameOfCrimeString = ''.join(NameOfCrime)
            AllCrimes.append(NameOfCrimeString)
        predator['Crimes'] = AllCrimes

        image = response.xpath('//div[@class="photoBox"]/img/@src').extract()
        if Helpers.pictureAvailable(image):
            imageString = ''.join(image)
            predator['ImageLink'] = imageString

        DOB = response.xpath('//td[@headers="dobColHdr"]/text()').extract()
        DOBString = ''.join(DOB)
        predator['DOB'] = DOBString

        Gender = response.xpath('//td[@headers="genderColHdr"]/text()').extract()
        GenderString = ''.join(Gender)
        predator['Gender'] = GenderString

        Height = response.xpath('//td[@headers="heigthColHdr"]/text()').extract()
        TallnessString = ''.join(Height)
        predator['Tallness'] = TallnessString
        predator['Height'] = Helpers.heightToInches(TallnessString)

        Weight = response.xpath('//td[@headers="weigthColHdr"]/text()').extract()
        WeightString = ''.join(Weight)
        predator['Weight'] = WeightString

        eyeColor = response.xpath('//td[@headers="eyecolorColHdr"]/text()').extract()
        eyeColorString = ''.join(eyeColor)
        predator['EyeColor'] = eyeColorString

        hairColor = response.xpath('//td[@headers="haircolorColHdr"]/text()').extract()
        hairColorString = ''.join(hairColor)
        predator['HairColor'] = hairColorString

        ethnicity = response.xpath('//td[@headers="ethnicityColHdr"]/text()').extract()
        ethnicityString = ''.join(ethnicity)
        predator['Ethnicity'] = ethnicityString

        address = response.xpath('//td[@headers="lastKnwnAddrColHdr"]/text()').extract()
        addressString = ''.join(address)
        adjustedAddress = Helpers.fixAddress(addressString)
        predator['Address'] = adjustedAddress
        
        print predator
        Helpers.save_predator_to_database(predator)
        



        




        

        
        
