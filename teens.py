#Author: James Grace
import sys, time
from Adafruit_IO import MQTTClient #MQTT gets mean from scorer
from rgbmatrix import RGBMatrix, RGBMatrixOptions #matrix control
from PIL import ImageDraw,ImageFont,Image #matrix display

options = RGBMatrixOptions() #create option set
options.rows =64
options.cols=64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 90

matrix = RGBMatrix(options = options) #apply options to matrix
offset_canvas = matrix.CreateFrameCanvas() #apply frame to matrix

ADAFRUIT_IO_USERNAME = "" #MQTT authorization codes
ADAFRUIT_IO_KEY = "" 
FEED_ID = 'mean' #feed containing the mean

global mn
mn=0 #global value containing meamn
def connected(client): #action when connected
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    client.subscribe(FEED_ID) #connects to 'mean' feed

def disconnected(client): #action when disconnected
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload): #action when message received
    print('Success!')
    global mn #get global mean variable
    mn=int(payload) #set it to an integer from data received
    print(mn)
    
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY) #initialize MQTT
client.on_connect    = connected #setup connect action
client.on_disconnect = disconnected #setup disconnect action
client.on_message    = message #setup message action
client.connect() #connect to MQTT
client.loop_background() #continue a loop in background

while True: #forever loop
    mean =  mn * 4 #set variable mean to the actual mean times 4
    if mn > 7: #if actual mean is greater than seven, set colour to green
        r = 0
        g = 255
        b = 0
    else: #if not greater than seven, set colour to red
        r =255
        g=0
        b=0
    image = Image.new("RGB", (64,64)) #create new RGB image
    draw = ImageDraw.Draw(image) #draw on image
    draw.text((0,50),"Average:"+str(mn),(0,0,255)) #create text showing average
    draw.rectangle((0,0,mean,mean), fill=(r,g,b)) #create rectangle from 0,0 to mean,mean (mn*4,mn*4)
    matrix.Clear() #clear the matrix if value has decreased
    matrix.SetImage(image,0,0) #set the image on the matrix to the one just drawn
    time.sleep(60) #wait a minute



