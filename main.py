from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor

from soduku import get_sudoku, show_sudoku

app = Flask(__name__, static_url_path="", static_folder="templates")

executor = ThreadPoolExecutor(max_workers=10)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/generate", methods=["POST"])
def generate_sudoku():
    data = request.get_json()
    table_num, level = int(data["table_num"]), int(data["difficulty"])

    futures = []
    for _ in range(table_num):
        future = executor.submit(get_sudoku, level=level, clean_count=(18, 63))
        futures.append(future)

    results = [future.result() for future in futures]
    response = {
        "answers": [result[0] for result in results],
        "problems": [result[1] for result in results]
    }
    # for problem in response["problems"]:
    #     show_sudoku(problem)

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="localhost", port=5555, debug=True, threaded=False)
