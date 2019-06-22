#Author: Jmaes Grace

from flask import Flask, render_template, redirect #import module allowing python webpage
from Adafruit_IO import Client #MQTT sender to send mean to screen
from sense_hat import SenseHat #get onboard mtrix control
from time import sleep

sense = SenseHat()

ADAFRUIT_IO_USERNAME = "Jgsch"
ADAFRUIT_IO_KEY = "aabd69baf5a74a5fa8831b101d0ef1f3"

app = Flask(__name__)
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

sc=[]
means=[]

@app.route('/') #respond to <ip address>:5000 - index
def hello_world():
    return render_template('score.html') #return the score file of everything

@app.route('/score/<name>/<scr>/<ca>/<wa>/<ia>/<consa>/<exa>/<rea>/<coa>/<woa>/<ioa>/<constoa>/<expoa>/<rfloa>') #respond to <ip address>:5000/score/etc. - score string and attempts
def score(name, scr, ca, wa, ia, consa, exa, rea, coa, woa, ioa, constoa, expoa, rfloa):
    write = '<br><table style="width:100%"><p id="scr">Number of attempts taken to correctly position each stage and definition: </p> <tr id="row"><th></th><th>Stage</th><th>Definition</th></tr><tr><th>Connect</th><th>' + ca + '</th><th>'+coa+'</tr><tr><th>Wonder</th><th>'+wa+'</th><th> '+woa+'</th></tr><tr><th>Investigate</th><th>'+ia+'</th><th>'+ioa+'</th></tr><tr><th>Construct</th><th>'+consa+'</th><th>'+constoa+'</th></tr><tr><th>Express</th><th>'+exa+'</th><th>'+expoa+'</th></tr><tr><th>Reflect</th><th>'+rea+'</th><th>'+rfloa+'</th></tr></table><br>'
    means.append(int(scr)) #add the score to the mean list
    men = sum(means) / len(means) #calculate the mean of the whole list
    aio.send_data('mean', men) #send the mean across to the 64x64 matrix
    sc.append(name + ' scored: ' + scr + write) #add a string to the sc list
    sc.reverse() #switch it around so most recent first
    sense.show_message('You scored ' + scr) #show string on sensehat
    f=open('/home/pi/templates/score.html', 'w') #open the html file for index and rewrite it
    f.write("<head> <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet' type='text/css'> <style> #scr {font-size:20;} p {font-size: 30;} body {font-family: 'Montserrat';}</style></head>") #rewrite head
    f.write('<body>')
    f.write('<h1>Teacher Feedback</h1>')
    f.write('<h2>Current mean is ' + str(men) + '</h2>')
    for item in sc:
        f.write('<p><b>'+item+'</b><p>') #write all the scores
    f.write('</body>')
    f.close() 
    sc.reverse() #reverse it back to original
    return render_template('ys.html', score = scr, name = name, coni = ca, woni = wa, invi = ia, consti = consa, expi = exa, refli=rea, conti = coa, wonti = woa, invti=ioa, constiti = constoa, expti=expoa, reflt=rfloa) #return feedback
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
