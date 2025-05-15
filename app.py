from flask import Flask, request
from blocker import check_request

app = Flask(__name__)

@app.before_request
def before_request():
    result = check_request()
    if result:
        return result

@app.route("/")
def home():
    return "Добро пожаловать на защищённый сайт!"

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"Поиск по запросу: {query}"

if __name__ == "__main__":
    app.run(debug=True)


