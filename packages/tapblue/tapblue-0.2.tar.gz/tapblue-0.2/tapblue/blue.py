from pubnub import Pubnub 


pubnub = Pubnub(publish_key='', subscribe_key='sub-c-b09806ee-e056-11e3-8f83-02ee2ddab7fe', ssl_on=True ) 


class BlueBase(object):
  def __init__(
      self,
      channel,
  ) :
      self.channel = channel

class BlueCore(BlueBase):
  def __init__(
      self,
      channel,
  ) : 
    self.channel = channel
    
  def listen(self,function):
    def recieve(message,channel):
    	function(message)
    c = self.channel
    pubnub.subscribe(channels=self.channel,callback=recieve)
    
    #self.printChannel()
class Blue(BlueCore):
  def __init__(
      self,
      channel,
  ) :
      super(Blue, self).__init__(
          channel = channel,
  )