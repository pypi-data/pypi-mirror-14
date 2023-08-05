import requests

class Popily:
    def __init__(self, token, url=None):
        self.auth_header = {'Authorization': 'Token ' + token}
        self.BASE_URL = 'https://popily.com'
        if url:
            self.BASE_URL = url


    def _pack_filters(self, filters):
        packed_str = ''
        for i,f in enumerate(filters):
            op = 'eq'
            if 'op' in f:
                op = f['op']

            filter_str = ''
            if i > 0:
                filter_str += '__'

            filter_str += f['column'] + '!' + op + '!' + ','.join(f['values'])
            packed_str += filter_str

        return packed_str


    def _assign_editables(self, data_dict, kwargs):
        editables = [
            'title',
            'x_label',
            'y_label',
            'z_label',
            'category_order',
            'time_interval',
            'refresh_rate',
            'swap'
        ]

        for key in editables:
            if key in kwargs:
                data_dict[key] = kwargs[key]

        return data_dict


    def add_source(self, **kwargs):
        endpoint = self.BASE_URL + '/api/sources/'

        post_data = {}
        for key in ['columns', 'title', 'description', 'created_by']:
            if key in kwargs:
                post_data[key] = kwargs[key]

        if 'url' in kwargs:
            post_data['url'] = kwargs['url']

            r = requests.post(endpoint, json=post_data, 
                    headers=self.auth_header)


        elif 'file_obj' in kwargs:
            r = requests.post(endpoint, data=post_data, 
                    files={'data': kwargs['file_obj']}, headers=self.auth_header)

        
        elif 'connection_string' in kwargs:
            post_data['connection_string'] = kwargs['connection_string']
            post_data['query'] = kwargs['query']
            
            r = requests.post(endpoint, json=post_data, 
                    headers=self.auth_header)

        else:
            raise('url or file_obj is required')

        return r.json()

    
    def get_sources(self):
        endpoint = self.BASE_URL + '/api/sources/'

        r = requests.get(endpoint, headers=self.auth_header)
        return r.json()


    def get_source(self, source_id):
        endpoint = self.BASE_URL + '/api/sources/' + str(source_id) + '/'
        r = requests.get(endpoint, headers=self.auth_header)
        return r.json()


    def get_insights(self, source_id, **kwargs):
        endpoint = self.BASE_URL + '/api/insights/'

        payload = {'source': source_id}

        for key in ['columns', 'insight_types', 'insight_actions']:
            if key in kwargs:
                payload[key] = ','.join(kwargs[key])

        if 'filters' in kwargs:
            payload['filters'] = self._pack_filters(kwargs['filters'])

        if 'full' in kwargs:
            payload['full'] = kwargs['full']

        if 'single' in kwargs:
            payload['single'] = kwargs['single']

        for key in ['full', 'height', 'width']:
            if key in kwargs:
                payload[key] = kwargs[key]

        payload = self._assign_editables(payload, kwargs)

        r = requests.get(endpoint, headers=self.auth_header,params=payload)

        return r.json()


    def get_insight(self, insight_id, **kwargs):
        endpoint = self.BASE_URL + '/api/insights/' + str(insight_id) + '/'

        payload = {}
        if 'filters' in kwargs:
            payload['filters'] = self._pack_filters(kwargs['filters'])

        for key in ['full', 'height', 'width']:
            if key in kwargs:
                payload[key] = kwargs[key] 

        payload = self._assign_editables(payload, kwargs)


        r = requests.get(endpoint, headers=self.auth_header, params=payload)
        return r.json()


    def customize_insight(self, insight_id, **kwargs):
        endpoint = self.BASE_URL + '/api/insights/' + str(insight_id) + '/'

        post_data = {}
        post_data = self._assign_editables(post_data, kwargs)


        if 'filters' in kwargs:
            post_data['filters'] = self._pack_filters(kwargs['filters'])


        r = requests.put(endpoint, json=post_data, headers=self.auth_header)
        return r.json()


    def add_user(self, **kwargs):
        endpoint = self.BASE_URL + '/api/users/'

        if 'username' not in kwargs:
            raise 'username is a required argument'

        post_data = {}
        post_data['username'] = kwargs['username']

        r = requests.post(endpoint, json=post_data, 
                    headers=self.auth_header)

        print r.text

        return r.json()


    def get_users(self):
        endpoint = self.BASE_URL + '/api/users/'

        r = requests.get(endpoint, headers=self.auth_header)
        return r.json()


    def get_user(self, user_id):
        endpoint = self.BASE_URL + '/api/users/' + str(user_id) + '/'
        r = requests.get(endpoint, headers=self.auth_header)
        return r.json()
