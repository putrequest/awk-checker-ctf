from flask import Flask, request, render_template
import subprocess
import logging


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    def awk_reseponse(out: str):
        return render_template('index.html', output=out)

    if "input_data" not in request.form or "awk_command" not in request.form:
        return awk_reseponse("You have to supply both inputs")

    # If we are posting a form check for special cases
    input_data = request.form["input_data"]
    awk_command = request.form["awk_command"]

    # Decoys don't work on resilient minds, that would be too easy
    if len(awk_command) > 6 and awk_command[0:6] == "system":
        return awk_reseponse("You have to get more creative than that")

    # TODO: remove this, someone might be able to break something
    # if they have the debug pin
    if len(awk_command) > 5 and awk_command[0:5] == "2+2=5":
        raise ArithmeticError("2+2!=5")

    print(f"Got request: {input_data}, {awk_command}")
    return awk_reseponse(run_query(input_data, awk_command))


def run_query(input_data: str, awk_command: str) -> str:
    input_cmd = ["echo"] + input_data.split()
    echo = subprocess.Popen(input_cmd, stdout=subprocess.PIPE)
    # output = subprocess.check_output(
    #     awk_cmd, stdin=echo.stdout).decode("utf-8")[:-1]
    final_cmd = ('sudo', '-u', 'safe_awk', 'awk', "{"+awk_command+"}")
    output = subprocess.check_output(
        final_cmd, stdin=echo.stdout).decode("utf-8")[:-1]
    echo.wait()
    print(f'Returning computed output: {output}')
    return output


logging.basicConfig(filename="important.log", level=logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
