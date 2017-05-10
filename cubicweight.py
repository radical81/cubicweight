#pip install unirest
import threading, unirest, json, string, sys
from calculator import Calculator

API_ENDPOINT = "http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com"
FIRST_PAGE = "/api/products/1"

cubicWeightArray = []

def averageCubicWeight(list):
    return float(sum(list)) / len(list)

def getCubicWeight(obj):
    calc = Calculator()
    length = obj['size']['length']
    height = obj['size']['height']
    width = obj['size']['width']
    return calc.cubicWeight(length, height, width)

def displayItemDetails(obj):
    print 'Title: ' + obj['title']
    print 'Cubic Weight: ' + '{:,.2f}'.format(round(obj['cubic_weight'], 2)) + ' g'
    print 'Weight: ' + '{:,.2f}'.format(obj['weight']) + ' g'
    print 'Length: ' + str(obj['size']['length']) + ' cm'
    print 'Height: ' + str(obj['size']['height']) + ' cm'
    print 'Width: ' + str(obj['size']['width']) + ' cm'
    print("\n")

def extractItemsFromCategory(data, cat):
    objects = data['objects']
    catCount = 0
    for obj in objects:
        objCat = obj['category']
        if(objCat.strip().lower() == cat.strip().lower()):
            catCount = catCount + 1
            cubicWeight = getCubicWeight(obj)
            cubicWeightArray.append(cubicWeight)
            obj['cubic_weight'] = cubicWeight
            displayItemDetails(obj)

    if(catCount == 0):
        print 'No items for that category on this page'+'\n'

def fetchNextPage(page):
       print "NEXT PAGE: "+page+'\n'
       thread = unirest.get(API_ENDPOINT+page, headers={ "Accept": "application/json" }, callback=receiveObjects)

def showAverageCubicWeight():
    if(len(cubicWeightArray) > 0):
        print 'RESULTS:'
        print '\nCubic Weights of Items: ' + ', '.join('{:,.2f}'.format(round(c, 2)) + ' g' for c in cubicWeightArray)
        print '\nAverage Cubic Weight of Items: ' + '{:,.2f}'.format(round(averageCubicWeight(cubicWeightArray), 2))+ ' g'+'\n'
    else:
        print 'No items found.'

def processResponse(body):
   jsonStr = json.dumps(body) # The parsed response
   jsonRslt = json.loads(jsonStr)
   extractThread = threading.Thread(target=extractItemsFromCategory, args=[jsonRslt, sys.argv[1]])
   extractThread.start()
   if(jsonRslt['next']):
       fetchNextPage(jsonRslt['next'])
   else:
       showAverageCubicWeight()

def receiveObjects(response):
   response.code # The HTTP status code
   response.headers # The HTTP headers
   response.body # The parsed response
   response.raw_body # The unparsed response
   processResponse(response.body)

def runApp():
    print 'Retrieving Average Cubic Weights for Category '+ sys.argv[1]
    print 'FIRST PAGE: '+FIRST_PAGE+'\n'
    thread = unirest.get(API_ENDPOINT+FIRST_PAGE, headers={ "Accept": "application/json" }, callback=receiveObjects)

if(len(sys.argv) == 1):
    print "Please specify category name as an argument. Run using:"
    print "python cubicweight.py \"<category name>\""
else:
    runApp()
