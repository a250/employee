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

from aiohttp import web
import json
from asyncio import sleep
#from pprint import pprint
import logging

def check_json_errors(jj):

    keys = jj.keys()

    # check ['graphs']
    lookup_key = 'graphs'
    if lookup_key not in jj.keys():
        return ('KeyError','There is no [{}] in request'.format(lookup_key))

    # check ['graphs'][0]   
    if not isinstance(jj['graphs'], list):
        return ('TypeError','Wrong structure for  request[graphs]. It should be List')

    # check ['graphs'][0]['formula']        
    lookup_key = 'formula'        
    if lookup_key not in jj['graphs'][0].keys():
        return ('KeyError','There is no [{}] in request'.format(lookup_key))

    # check ['df']
    lookup_key = 'df'
    if lookup_key not in jj.keys():
        return ('KeyError','There is no [{}] in request'.format(lookup_key))

    # check ['df']['CPULoad5min']
    lookup_key = 'CPULoad5min'
    if lookup_key not in jj['df'].keys():
        return ('KeyError','There is no [{}] in request'.format(lookup_key))

    # check ['df']['CPULoad5min']['values']
    lookup_key = 'values'
    if lookup_key not in jj['df']['CPULoad5min'].keys():
        return ('KeyError','There is no [{}] in request'.format(lookup_key))

    return None
  
def calculation(raw_data_in):
    error = {'type': '', 'msg': ''}

    try:                                     # request string -> json
        json_in = json.loads(raw_data_in)
        logging.debug('Info: Error occur: {}'.format(json_in))

    except json.JSONDecodeError as err:
        error = {'type':type(err).__name__, 'msg': err.msg}
        logging.warning('Warning! Error occur: {}, {}'.format(error['type'], error['msg']))
        return error, None

    err = check_json_errors(json_in)
    if err:
        error['type'], error['msg'] = err
        pprint(err)
        pprint(error)        
        logging.warning('Warning! Error occur: {}, {}'.format(error['type'], error['msg']))
        return error, None


    formula = json_in['graphs'][0]['formula']
    CPULoad5min = json_in['df']['CPULoad5min']['values']
    formula = '['+formula.replace('CPULoad5min','i')+' for i in {}]'.format(CPULoad5min)

    try:                                      # try evaluate formula
        values = eval(formula)

    except ValueError as err:
        error = {'type':type(err).__name__, 'msg': err.msg}
        logging.warning('Warning! Error occur: {}, {}'.format(error['type'], error['msg']))
        return error, None

    except SyntaxError as err:
        error = {'type':type(err).__name__, 'msg': err.msg}
        logging.warning('Warning! Error occur: {}, {}'.format(error['type'], error['msg']))
        return error, None

    json_out = json_in.copy()
    json_out['df']['CPULoad5min']['values'] = values

    logging.debug('Info: Error occur: {}'.format(json_out))

    return None, json_out
  

async def get_response(request):
  return web.Response(text = 'Ok, it works asynchronously!')
  

async def post_parse(request):
  #await sleep(10)  # to check asyncro 
  
  raw_data_in = await request.text()
  
  error, json_out = calculation(raw_data_in)
  
  if error:
    return web.json_response(error)    
  else:
    return web.json_response(json_out, text=None, body=None, status=200, reason=None,
              headers=None, content_type='application/json', dumps=json.dumps)
  
  
def main():
  log_file ='web_service.log'
  logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
  logging.info('Started')

  
  app = web.Application()
  app.add_routes([web.post('/cpuload', post_parse), 
                  web.get('/',get_response)])
  web.run_app(app)
  
  logging.info('Stoped')
  
  
if __name__ == "__main__":
  main()