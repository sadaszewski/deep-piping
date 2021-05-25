import arvados
import pandas as pd
from urllib.parse import urlparse
import io


class ArvadosDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return ArvadosDataFrame

    def __init__(self, source, *args, **kwargs):
        if isinstance(source, str):
            super().__init__()
            self._init_from_location(source)
        else:
            super().__init__(source, *args, **kwargs)

    def _init_from_location(self, location):
        #self.location = location

        loc = urlparse(location)
        uuid, *path = loc.path.split('/')
        path = '/'.join(path)
        c = arvados.collection.Collection(uuid)
        f = c.find(path)
        b = f.readfrom(0, f.size(), 3, exact=True)
        b = io.BytesIO(b)
        df = pd.read_csv(b)
        #self.df = df
        for k, v in df.items():
            self[k] = v

    def save_to_new_collection(self, name, owner_uuid):
        c = arvados.collection.Collection()
        with c.open(name, 'w') as writer:
            self.to_csv(writer)
        c.save_new(name=name, owner_uuid=owner_uuid)
        return c
