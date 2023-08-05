import holoviews as hv

class _hv_enable(object):
    def __init__(self):
        self.enabled = False

    def __call__(self, backend = "matplotlib"):
        if self.enabled: return
        self.enabled = True
        hv.notebook_extension(backend)

hv_enable = _hv_enable()
