import HTMLParser
import optparse
import requests
from flask import Flask
from flask import request

from spelling_corrector.general_bare_corrector.corrector import GeneralBareCorrector
from spelling_corrector.domain_bare_corrector.corrector import DomainBareCorrector
app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


spelling_corrector = None

def init_model(is_general=False):
   global spelling_corrector
   if is_general:
      spelling_corrector = GeneralBareCorrector()
   else:
      spelling_corrector = DomainBareCorrector()
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route('/')
def start():
   #return render_template('index.html')
   return app.send_static_file('home.html')
@app.route('/fix',methods=['GET', 'POST'])
def fix():
   #data = request.data
   sen = request.form['sen']

   sen = HTMLParser.HTMLParser().unescape(sen)
   #sen = sen.decode("utf-8")
   fixed_res,accent_ref = spelling_corrector.fix(sen)
   return accent_ref

@app.route('/accent',methods=['GET','POST'])
def accent():
   sen = request.form['data']
   try:
       accent_request = requests.post("http://topica.ai:9339/accent",data={"data":sen}, timeout=30)
       return accent_request.content
   except:
        return "Unable to get accent result"

if __name__ == '__main__':
   optparser = optparse.OptionParser()
   optparser.add_option(
      "-R", "--port", default="9199",type="int"
   )
   optparser.add_option(
      "-M","--mode", default="general"
   )
   opts = optparser.parse_args()[0]
   port = opts.port

   mode = opts.mode
   is_genaral = False
   if mode == "general":
      is_genaral = True

   init_model(is_general=is_genaral)


   app.run(debug = False,host='0.0.0.0', port=port)