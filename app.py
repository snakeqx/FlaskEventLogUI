from flask import Flask
from flask import render_template, request
import json
from flask_bootstrap import Bootstrap
from lib.EventLog import EventLog


app = Flask(__name__)
bootstrap = Bootstrap(app)


# item_list = []
# for i in range(0, 100):
#     dic1 = {
#         "severity": "severity",
#         "datetime": "datetime",
#         "messageid": i,
#         "messagetext": "message text",
#         "sbsb": "SBSB",
#     }
#     item_list.append(dic1)

event_log = EventLog(r"./ExampleData/a.gz")


@app.route("/", methods=['GET'])
def index():
    return render_template('base.html')


@app.route("/get_data", methods=['POST'])
def get_data():
    page = request.values.get('page')
    rows = request.values.get('rows')
    error_dict = {
                    "severity":     "Error in Server",
                    "datetime":     "Error in Server",
                    "messageid":    "Error in Server",
                    "messagetext":  "Error in Server", }
    # try to convert from string to int
    try:
        page = int(page)
        rows = int(rows)
    except Exception as e:
        print(str(e))
        return error_dict

    dic2 = {
        "total": event_log.ItemQuantity,
        "rows": event_log.DictList[(page-1)*rows: (page-1)*rows+rows]}
    json_str = json.dumps(dic2)
    return json_str


def main():

    app.run(debug=True)


if __name__ == '__main__':
    main()