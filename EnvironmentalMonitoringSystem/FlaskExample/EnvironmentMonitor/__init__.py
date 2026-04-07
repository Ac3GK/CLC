from flask import Flask

app = Flask(__name__)
<<<<<<< HEAD
=======

>>>>>>> 68a49dc2f27aed555d635ec9141701a0817a0778
@app.route('/')
def hello_world():
    return 'Hello, World!'

<<<<<<< HEAD
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8000, debug=True)  
=======
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
>>>>>>> 68a49dc2f27aed555d635ec9141701a0817a0778
