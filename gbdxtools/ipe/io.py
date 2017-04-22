import rasterio
import numpy as np

def to_geotiff(arr, path='./output.tif', proj=None, dtype=None, bands=None):
    if dtype is not None:
        dtype = np.dtype(dtype)
    data = arr.read(bands=bands)
    c,h,w = data.shape
    meta = {
        'width': w,
        'height': h,
        'count': c,
        'dtype': data.dtype if dtype is None else dtype,
        'driver': 'GTiff'
    }
    if proj is not None:
        meta["crs"] = {'init': proj}
    with rasterio.open(path, "w", **meta) as dst:
        if dtype is not None:
            data = (data - data.min()) * (float(np.iinfo(dtype).max) * data.max())
            data = data.astype(dtype)
        dst.write(data)
    return path
