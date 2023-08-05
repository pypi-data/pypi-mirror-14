from .holoviews_imports import hv, hv_enable
from yt.data_objects.derived_quantities import \
        DerivedQuantityCollection
import holoviews as hv
import numpy as np
import yt

class SliceViewer(object):
    _coord = 0.5
    _dirty = True
    _field = "density"
    _map = None
    _kdims = None
    def __init__(self, ds, x_field = "density", y_field = "temperature"):
        self.ds = ds
        self.x_field = x_field
        self.y_field = y_field
        hv_enable()
        
    @property
    def slice(self):
        if self._dirty:
            self._slice = self.ds.r[self.coord,:,:]
            if not hasattr(self._slice, "quantities"):
                self._slice.quantities = DerivedQuantityCollection(self._slice)
            self._dirty = False
        return self._slice

    @property
    def kdims(self):
        if self._kdims is not None:
            return self._kdims
        self._kdims = [#hv.Dimension('field', values=["density", "temperature"]),
                 hv.Dimension('coord', range=(0.45, 0.55)),
                 hv.Dimension('percentile', range=(50.0, 100.0)),
                 hv.Dimension('width', range=(0.05, 1.0))]
        return self._kdims

    @property
    def coord(self):
        return self._coord
    
    @coord.setter
    def coord(self, val):
        if self._coord == val:
            return
        self._dirty = True
        self._coord = val
    
    def image(self, coord, percentile, width):
        self.coord = coord
        frb = self.slice.to_frb(width, (512, 512))
        data = np.log10(frb[self.x_field].d)
        mi, ma = data.min(), data.max()
        xmi, xma, ymi, yma = frb.bounds
        im = hv.Image(data, vdims=[hv.Dimension(self.x_field, range=(mi, ma))],
                      kdims = [hv.Dimension("x", range=(xmi, xma)),
                               hv.Dimension("y", range=(ymi, yma))],
                      extents = (xmi, ymi, xma, yma),
                      bounds = (xmi, ymi, xma, yma),
                      )(style={'cmap':'viridis'})
        level = np.percentile(im.data, percentile)
        cont = hv.operation.contours(im, levels=[level], overlaid=True)
        return cont

    def profile(self, coord, percentile, width):
        self.coord = coord
        prof = yt.create_profile(self.slice, 
            [self.x_field, self.y_field], "cell_mass", weight_field=None)
        data = np.log10(prof["cell_mass"].d)
        mi, ma = data[prof.used].min(), data[prof.used].max()
        (xmi, xma), (ymi, yma) = np.log10(prof.bounds)
        im2 = hv.Image(data, vdims=[hv.Dimension("cell_mass", range=(mi, ma))],
                       kdims = [hv.Dimension(self.x_field, range=(xmi, xma)),
                                hv.Dimension(self.y_field, range=(ymi, yma))],
                       bounds = (xmi, ymi, xma, yma),
                       extents = (xmi, ymi, xma, yma),
                      style={'cmap':'jet'})
        return im2

    @property
    def map(self):
        if self._map is not None:
            return self._map
        self._map = hv.DynamicMap(self.image, kdims=self.kdims) + \
                    hv.DynamicMap(self.profile, kdims=self.kdims)
        return self._map
