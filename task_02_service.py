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
 
 
Should return 'CPULoad5min*10', so...
  ...'values':[1230,1120,780,1110,1110,950]...


"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import numpy as np
import logging

class S(BaseHTTPRequestHandler):


    def do_GET(self):

        content = '<h3>Try to make POST request for /cpuload</h3>'

        self.send_response(200)

        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()        
        self.wfile.write(content.encode("utf-8"))
            
        
    def do_POST(self):
        
  
        # if POST-request not for http://.../cpuload/
        #
        # Return 404 if a file is not known.
        
        if self.path != '/cpuload/':
            self.send_response(404)
            content = "not found"
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
            logging.warning('Warning! Wrong URL: %s', self.path)
            
            return

        # get post data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  
        
        # processing the data
        err, res_content = self.evaluate(post_data.decode('utf-8'))
  
        # if there is no errors return result
        if err is not None:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            content = json.dumps({'err': f"{err['type']}: {err['msg']}"})
            self.wfile.write(content.encode("utf-8")) 
            logging.warning('Warning! Error occur: %s, %s', err['type'], err['msg'])            
            return
       
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(res_content.encode("utf-8"))       
       

    def check_json_errors(self, jj):
        
        keys = jj.keys()
        
        # check ['graphs']
        lookup_key = 'graphs'
        if lookup_key not in jj.keys():
            return ('KeyError',f'There is no [{lookup_key}] in request')

        # check ['graphs'][0]   
        if not isinstance(jj['graphs'], list):
            return ('TypeError',f'Wrong structure for  request[graphs]. It should be List')

        # check ['graphs'][0]['formula']        
        lookup_key = 'formula'        
        if lookup_key not in jj['graphs'][0].keys():
            return ('KeyError',f'There is no [{lookup_key}] in request')

        # check ['df']
        lookup_key = 'df'
        if lookup_key not in jj.keys():
            return ('KeyError',f'There is no [{lookup_key}] in request')

        # check ['df']['CPULoad5min']
        lookup_key = 'CPULoad5min'
        if lookup_key not in jj['df'].keys():
            return ('KeyError',f'There is no [{lookup_key}] in request')

        # check ['df']['CPULoad5min']['values']
        lookup_key = 'values'
        if lookup_key not in jj['df']['CPULoad5min'].keys():
            return ('KeyError',f'There is no [{lookup_key}] in request')

        return None
    
    def evaluate(self, raw_data_in):
        """
        Evaluate formula from json placed in ['graphs'][0]['formula'] on json data,.

        Input arguments:
          raw_data_in -- request as a string with specific structure
        
        Return:
          err -- None or (err['type'], err['msg']) if error occure 
          raw_data_out -- string contain json-structure
        
        """
        
        error = {'type': None, 'msg': None}
        
        try:                                     # request string -> json
            json_in = json.loads(raw_data_in)
            
        except json.JSONDecodeError as err:
            error = {'type':type(err).__name__, 'msg': err.msg}
            print(error)
            return (error, None)

        
        err = self.check_json_errors(json_in)
        if err:                                  # check json structure
            error['type'], error['msg'] = err
            return (error, None)
        
        formula = json_in['graphs'][0]['formula']
        CPULoad5min = np.array(json_in['df']['CPULoad5min']['values'])
        
        
        try:                                      # try evaluate formula
            values = eval(formula)
        except ValueError:
            error = {'type':type(err).__name__, 'msg': err.msg}
            return (error, None)            
        except SyntaxError as err:
            error = {'type':type(err).__name__, 'msg': err.msg}
            return (error, None)            


        json_out = json_in.copy()
        json_out['df']['CPULoad5min']['values'] = [i.item() for i in values]

        try:                                      # output json -> output string
            raw_data_out = json.dumps(json_out)
            
        except SyntaxError as err:
            error = {'type':type(err).__name__, 'msg': err.msg}
            return (error, None)    
        except TypeError as err:
            error = {'type':type(err).__name__, 'msg': 'Something went wrong'}
            return (error, None)    

        
        return (None, raw_data_out)        
        
def run(server_class=HTTPServer, handler_class=S, port=8000):    
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == "__main__":
    logging.basicConfig(filename='web_service.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')
    run()
    logging.info('Stoped')