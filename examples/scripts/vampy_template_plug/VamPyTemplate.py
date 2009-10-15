'''VamPyTemplate.py - A simple VamPy plugin that doesn't
really do anything.

This is a really dumb plugin which returns the sum of the
magnitude spectrum of each processing block.
You need to have Python installed, the Vampy plugin wrapper
and a Vamp plugin host such as Sonic Visualiser to run this.

You can get them for (almost) any operating system at:
Vampy: http://www.vamp-plugins.org/vampy.html
Sonic Visualiser: http://www.sonicvisualiser.org/
Python: http://www.python.org/

Outputs: 
1) Output = sum(magnitudeSpectrum)

Created by Gyorgy Fazekas, QMUL.
'''

from numpy import *
from vampy import *

#this has to be the same as the script name
class VamPyTemplate: 
	
	def __init__(self,inputSampleRate):
		# meaning of flags: we use Numpy arrays to pass the audio
		# samples to the process() function, debug mode, use time stamps
		self.vampy_flags = vf_DEBUG | vf_ARRAY | vf_REALTIME
		self.m_inputSampleRate = inputSampleRate
		self.m_stepSize = 0
		self.m_blockSize = 0
		self.m_channels = 0
		self.threshold = 0.05
		return None
		
	def initialise(self,channels,stepSize,blockSize):
		self.m_channels = channels
		self.m_stepSize = stepSize		
		self.m_blockSize = blockSize
		return True
		
	def reset(self):
		# reset initial conditions (if any)
		return None
	
	def getMaker(self):
		return 'Enter your name here'
	
	def getName(self):
		return 'Enter the name of the plugin'
		
	def getIdentifier(self):
		return 'vampy-unique-ID'

	def getDescription(self):
		return 'Enter a short description of the plugin'
	
	def getMaxChannelCount(self):
		return 1
		
	def getInputDomain(self):
		# use TimeDomain or FrequencyDomain
		return FrequencyDomain 

			
	def getOutputDescriptors(self):
		# describe what the plugin's output will be like
		Generic = OutputDescriptor()
		Generic.identifier = 'vampy-unique-outputID'
		Generic.name = 'Output Name'
		Generic.description ='Short output description'
		# below: the output is a curve or more like a matrix ?
		Generic.hasFixedBinCount=True
		Generic.binCount=1
		Generic.hasKnownExtents=False
		Generic.isQuantized=False
		Generic.sampleType = OneSamplePerStep
		Generic.unit = ''		
		return OutputList(Generic)

	def getParameterDescriptors(self):
		# describe any parameters your algorithm is using
		threshold = ParameterDescriptor()
		threshold.identifier='threshold'
		threshold.name='Energy threshold'
		threshold.description='Energy threshold'
		threshold.unit='v'
		threshold.minValue=0
		threshold.maxValue=1
		threshold.defaultValue=0.05
		threshold.isQuantized=False
		return ParameterList(threshold)

	def setParameter(self,paramid,newval):
		if paramid == 'threshold' :
			self.threshold = newval
		return
		
	def getParameter(self,paramid):
		if paramid == 'threshold' :
			return self.threshold
		else:
			return 0.0

	def process(self,inputbuffers,timestamp):
		# this is where we compute the features
		fftsize = self.m_blockSize
		sampleRate = self.m_inputSampleRate

		complexSpectrum =  inputbuffers[0]
		magnitudeSpectrum = abs(complexSpectrum) / (fftsize*0.5)
		
		# return features in a FeatureSet()
		output_featureSet = FeatureSet()

		tpower = sum(magnitudeSpectrum)

		if tpower > self.threshold : 
			output_featureSet[0] = Feature(tpower)
		else :
			output_featureSet[0] = 0
			
		return output_featureSet
