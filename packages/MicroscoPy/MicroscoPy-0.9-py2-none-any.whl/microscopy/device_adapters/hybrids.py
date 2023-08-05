"""A hybrid adapters for systems that don't lend themselves to the Sensor/Actuator framework.

Instead we can wrap them directly into a Scan1D object.
"""

from .. import scan

class Scan1D_AIO(scan.Scan1D):
  """Wrapper to make the MCCDAQ Synchronous Analog Input/Output scan a valid Microscope scan."""
  def __init__(self, aioscan):
    self.aioscan = aioscan
    # don't need to call Scan1D.__init__()
    
  def run(self, scan_back=False, reverse_next=False):
    """Run the AIO scan.
    
    kwargs are ignored.
    """
    self.aioscan.run()
    # The position will be included in the data, so ignore pos array
    self.pos = [0]
    # aioscan.data is a Waveform, of which we want the data only:
    self.spec = self.aioscan.data.data
