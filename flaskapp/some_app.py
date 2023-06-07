print("Hello world")
from Flask import flask
app = flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"
if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000) 
