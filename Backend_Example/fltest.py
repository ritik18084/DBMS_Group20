from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def mainFile():
    return render_template('index.html')

@app.route('/getSum', methods = ['POST'])
def getsum():
    a = request.values.get('data')
    a = eval(a)
    o1 = int(a['first'])
    o2 = int(a['second'])
    ans = o1+o2
    return jsonify({'ans' : ans})

if __name__ == "__main__":
    app.run(host='0.0.0.0')