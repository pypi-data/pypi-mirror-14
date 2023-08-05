"""
Video display for PCO Pixelfly CCD
"""

from pxlfly import PyPixelfly, CameraBuffer
import h5py
import numpy as np

from . import camdisp

  
class PixelflyDisplay(camdisp.CameraDisplay):
	"""Specialises :class:`camdisp,CameraDisplay` for the PCO Pixelfly camera."""
	def __init__(self, cam, master=None):
		"""
		:param cam: a PyPixelfly instance
		:param master: Tkinter parent widget
		"""
		self.cam = cam
		self.dyn = 2**cam.bitdepth - 1 # camera dynamic range (12 bits)
		self._rescale = (0, self.dyn)
		super(PixelflyDisplay, self).__init__(cam.framewidth, cam.frameheight, tk_window=master)
	
	def get_image_data(self):
		with CameraBuffer(self.cam): 
			self.imdata = self.cam.getframe().copy()
		rescaled_data = (((np.uint32(self.imdata) - self._rescale[0])*self.dyn)/(self._rescale[1]-self._rescale[0]))
		return np.uint8(rescaled_data/16)

	def title_string(self):
		s = 'Pixelfly | Max: {max: >4d} | Exposure: {exp} ms ({wheel:s})'
		return s.format(max=self.imdata.max(), exp=self.cam.exposure, wheel=self.wheel[self.count % 4])
