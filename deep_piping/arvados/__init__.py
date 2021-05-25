import arvados
import pandas as pd
from urllib.parse import urlparse
import io


class ArvadosDataFrame(pd.DataFrame):
    def __init__(self, location):
        super().__init__()
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
