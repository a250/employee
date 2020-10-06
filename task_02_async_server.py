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
import asyncio 
import logging

  
def calculation(raw_data_in):

    json_in = json.loads(raw_data_in)
    logging.debug('Info. Received JSON: {}'.format(json_in))

    formula = json_in['graphs'][0]['formula']
    CPULoad5min = json_in['df']['CPULoad5min']['values']
    formula = '['+formula.replace('CPULoad5min','i')+' for i in {}]'.format(CPULoad5min)

    values = eval(formula)

    json_out = json_in.copy()
    json_out['df']['CPULoad5min']['values'] = values

    logging.debug('Info. Returned JSON: {}'.format(json_out))

    return json_out
  

async def get_response(request):
    return web.Response(text = 'Ok, it works asynchronously!')
  

async def post_parse(request):
  #await asyncio.sleep(10)  # to check asyncro 

    try:
        raw_data_in = await request.text()

        json_out = calculation(raw_data_in)

    except Exception as ex:
        error = {'type': type(ex).__name__, 'msg':str(ex)}
        
        return web.json_response(error, text=None, body=None, status=200, reason=None,              headers=None, content_type='application/json', dumps=json.dumps)


    return web.json_response(json_out, text=None, body=None, status=200, reason=None,              headers=None, content_type='application/json', dumps=json.dumps)
  
  
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