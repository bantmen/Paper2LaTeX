import os, glob, sys
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/'

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

files = glob.glob('/YOUR/PATH/*')
for f in files:
    os.remove(f)

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    url = "http://www.personal.kent.edu/~bherzog/images/tao-dead.gif"
    files = glob.glob('static/*')
    for f in files:
      os.remove(f)
    img = request.files['img']
    if img:
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        return render_template('results.html', img=img.filename, placeholder=0)
    return render_template('results.html', img=url, placeholder=1)
    # return "hello"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)