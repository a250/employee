"""
Input POST request with JSON structure:

{'df': {'CPULoad5min': {'index': ['2020-09-02T00:01:49',
                                  '2020-09-02T00:06:37',
                                  '2020-09-02T00:11:36',
                                  '2020-09-02T00:16:54',
                                  '2020-09-02T00:21:35',
                                  '2020-09-02T00:26:32'],
                        'values': [123, 112, 78, 111, 111, 95]}},
 'graphs': [{'formula': 'CPULoad5min*10'}],
 'rangeEnd': '2020-09-06T00:00:00',
 'rangeStart': '2020-09-02T00:00:00'}

"""



from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import numpy as np


class S(BaseHTTPRequestHandler):
    def do_GET(self):

        content = "<h3>Try to make POST request for /cpuload</h3>"

        self.send_response(200)

        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_POST(self):

        # if POST-request not for http://.../cpuload/
        #
        # Return 404 if a file is not known.

        if self.path != "/cpuload/":
            self.send_response(404)
            content = "not found"
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

            return

        # get post data
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # processing the data
        err, responde = self.evaluate(post_data.decode("utf-8"))

        # if there is no errors return result
        if err is not None:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            content = json.dumps({"err": f"{err['type']}:{','.join(err['msg'])}"})
            self.wfile.write(content.encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(responde).encode("utf-8"))

    def evaluate(self, raw_data):

        try:
            data_in = json.loads(raw_data)
            formula = data_in["graphs"][0]["formula"]
            df_CPULoad5min = data_in["df"]["CPULoad5min"]
            CPULoad5min = np.array(df_CPULoad5min["values"])
            values = eval(formula)
            data_out = data_in.copy()
            data_out["df"]["CPULoad5min"]["values"] = [i.item() for i in values]
            return (None, data_out)

        except Exception as ex:
            # print(type(ex).__name__, ex.args)

            error = {"type": type(ex).__name__, "msg": ex.args}
            print("Error:\n", error)
            return (error, None)


def run(server_class=HTTPServer, handler_class=S, port=8000):

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("..stopping")
        pass
    httpd.server_close()


if __name__ == "__main__":
    run()
