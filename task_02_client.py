import requests
import json
from pprint import pprint
from requests.exceptions import HTTPError
     
def main():
  
    data = """
      {"df": {"CPULoad5min": {"index": ["2020-09-02T00:01:49",
                                        "2020-09-02T00:06:37",
                                        "2020-09-02T00:11:36",
                                        "2020-09-02T00:16:54",
                                        "2020-09-02T00:21:35",
                                        "2020-09-02T00:26:32"],
                              "values": [123, 112, 78, 111, 111, 95]}},
       "graphs": [{"formula": "CPULoad5min*10"}],
       "rangeEnd": "2020-09-06T00:00:00",
       "rangeStart": "2020-09-02T00:00:00"}  


    """

    url = 'http://localhost:8080/cpuload'  
    #port = 8080
    json_req = json.loads(data)
    pprint(json_req)
    try:
        response = requests.post(url, data)  
        response.raise_for_status()
        json_response = response.json()
        
    except HTTPError as http_err:
        print('Server error:', str(http_err))
        return

    print('\n\n---Server response--\n\n')
    pprint(json_response)

  
if __name__ == '__main__':
    main()