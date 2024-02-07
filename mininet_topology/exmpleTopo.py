#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.link import TCLink
class MyTopology(Topo):
  """
  A basic topology
  """
  def __init__(self):
    Topo.__init__(self)
    # Set Up Topology Here
    switch1 = self.addSwitch('Switch1') ## Adds a Switch
    switch2 = self.addSwitch('Switch2') ## Adds a Switch
    switch3 = self.addSwitch('Switch3') ## Adds a Switch
    switch4 = self.addSwitch('Switch4') ## Adds a Switch
    host1 = self.addHost('Desktop', ip='10.0.0.1/24') ## Adds a Host
    host2 = self.addHost('Server', ip='10.0.0.2/24') ## Adds a Host
    host3 = self.addHost('smartTV', ip='10.0.0.3/24') ## Adds a Host
    host4 = self.addHost('Fridge', ip='10.0.0.4/24') ## Adds a Host
    host5 = self.addHost('Alexa', ip='10.0.0.5/24') ## Adds a Host
    host6 = self.addHost('Siri', ip='10.0.0.6/24') ## Adds a Host
    self.addLink(host1, switch2, delay="15ms") ## Add a link
    self.addLink(host5, switch3, delay="15ms") ## Add a link
    self.addLink(host6, switch3, delay="15ms") ## Add a link
    self.addLink(host2, switch4, delay="15ms") ## Add a link
    self.addLink(host4, switch1, delay="15ms") ## Add a link
    self.addLink(host3, switch1, delay="15ms") ## Add a link
    self.addLink(switch1, switch2, delay="15ms") ## Add a link
    self.addLink(switch2, switch3, delay="15ms") ## Add a link
    self.addLink(switch2, switch4, delay="15ms") ## Add a link


if __name__ == '__main__':
  """
  If this script is run as an executable (by chmod +x), this is
  what it will do
  """
  topo = MyTopology() ## Creates the topology
  net = Mininet( topo=topo, link = TCLink ) ## Loads the topology
  net.start() ## Starts Mininet
  # Commands here will run on the simulated topology
  CLI(net) 

  net.stop() ## Stops Mininet
