import gzip
import logging
import json

try:
    import xml.etree.cElementTree as ElTree
except ImportError:
    import xml.etree.ElementTree as ElTree


class EventLog:
    def __init__(self, filename):
        self.DictList = []
        self.Node = []
        self.Severity = []
        self.DateTime = []
        self.Id = []
        self.MessageId = []
        self.ComponentName = []
        self.ComponentId = []
        self.MessageText = []
        self.Type = []
        self.AssemblyName = []
        self.ProcessName = []
        self.ProcessId = []
        self.ThreadName = []
        self.AppDomain = []
        self.ClusterId = []
        self.ItemQuantity = 0

        try:
            self.XmlStream = gzip.GzipFile(mode="rb",
                                           fileobj=open(filename, 'rb')
                                           ).read()
            self.parse()
            self.generate_dict()
        except Exception as e:
            logging.error(str(filename))
            logging.error(str(e))

    def parse(self):
        tree = ElTree.fromstring(self.XmlStream)
        for message in tree:
            for items in message:
                for item in items:
                    if item.tag == "Node":
                        self.Node.append(item.text)
                    if item.tag == "Severity":
                        self.Severity.append(item.text)
                    if item.tag == "DateTime":
                        self.DateTime.append(item.text)
                    if item.tag == "Id":
                        self.Id.append(item.text)
                    if item.tag == "MessageId":
                        self.MessageId.append(item.text)
                    if item.tag == "ComponentName":
                        self.ComponentName.append(item.text)
                    if item.tag == "ComponentId":
                        self.ComponentId.append(item.text)
                    if item.tag == "MessageText":
                        self.MessageText.append(item.text)
                    if item.tag == "Type":
                        self.Type.append(item.text)
                    if item.tag == "AssemblyName":
                        self.AssemblyName.append(item.text)
                    if item.tag == "ProcessName":
                        self.ProcessName.append(item.text)
                    if item.tag == "ProcessId":
                        self.ProcessId.append(item.text)
                    if item.tag == "ThreadName":
                        self.ThreadName.append(item.text)
                    if item.tag == "AppDomain":
                        self.AppDomain.append(item.text)
                    if item.tag == "ClusterId":
                        self.ClusterId.append(item.text)
                self.ItemQuantity += 1

    def generate_dict(self):
        for i in range(0, self.ItemQuantity):
            temp_dict = {
                "id":           i,
                "node":         self.Node[i],
                "severity":     self.Severity[i],
                "datetime":     self.DateTime[i],
                "messageid":    self.MessageId[i],
                "messagetext":  self.MessageText[i],
                "type":         self.Type[i],
            }
            self.DictList.append(temp_dict)

    def get_json(self, is_error, is_warn, is_info, is_sucess,
                 is_developer, is_service, page, rows):
        qty = 0
        filter_list = []
        result_list = []
        if is_error:
            filter_list.append("Error")
        if is_warn:
            filter_list.append("Warning")
        if is_info:
            filter_list.append("Information")
        if is_sucess:
            filter_list.append("Success")
        if is_developer:
            filter_list.append("Developer")
        if is_service:
            filter_list.append("Service")
        for i in self.DictList:
            if (i["severity"] in filter_list) and (i["type"] in filter_list):
                result_list.append(i)
                qty += 1
        dic2 = {
            "total": qty,
            "rows": result_list[(page - 1) * rows: (page - 1) * rows + rows]}
        json_str = json.dumps(dic2)
        return json_str




if __name__ == '__main__':
    print("please do not use it individually unless of debugging.")
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'./main.log',
                        filemode='w')
    # define a stream that will show log level > Warning on screen also
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
