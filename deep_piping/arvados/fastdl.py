import random
import arvados
from functools import lru_cache


class ArvadosFastDownload:
    def __init__(self, api, num_retries=3, disable_services=[]):
        self.api = api
        self.num_retries = num_retries
        
        keep_services = api.keep_services().list().execute()['items']
        keep_services = [ s for s in keep_services if s['service_type'] != 'proxy' ]
        keep_services = [ s for s in keep_services if s['service_host'] not in disable_services ]
        self.keep_services = keep_services
        
    @lru_cache()
    def get_block(self, locator):
        for _ in range(self.num_retries):
            svc = random.choice(self.keep_services)
            # print('Trying ', svc['service_host'], '...')
            c = arvados.http.client.HTTPConnection(svc['service_host'], svc['service_port'])
            headers={'Authorization': f'OAuth2 {self.api.api_token}', 'Host': svc['service_host']}
            c.request('GET', f'/{locator}', headers=headers)
            r = c.getresponse()
            if r.status != 200:
                continue
            try:
                data = r.read()
                return data
            except:
                continue
        raise RuntimeError(f'Unable to download {locator}')
        
    def get_file(self, f):
        data = []
        for seg in f.segments():
            block = self.get_block(seg.locator)
            data.append(block[seg.segment_offset:seg.segment_offset+(seg.range_size-seg.range_start)])
        return ( b''.join(data) )