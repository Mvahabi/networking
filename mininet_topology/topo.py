#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    switch1 = self.addSwitch('s1')
    switch2 = self.addSwitch('s2')
    switch3 = self.addSwitch('s3')
    switch4 = self.addSwitch('s4')
    coreSwitch =  self.addSwitch('s5')

    # Data center
    Serv2 = self.addHost('Serv2',mac="00:00:00:00:00:01", ip='200.20.1.1/24',defaultRoute="Serv2-eth1") 
    ServWeb = self.addHost('ServWeb',mac="00:00:00:00:00:02", ip='200.20.1.2/24',defaultRoute="ServWeb-eth1") 
    ServDNS = self.addHost('ServDNS',mac="00:00:00:00:00:03", ip='200.20.1.3/24',defaultRoute="ServDNS-eth1")

    # Sales Department
    Laptop1 = self.addHost('Laptop1',mac="00:00:00:00:00:08", ip='200.20.2.8/24',defaultRoute="Laptop1-eth1") 
    Laptop2 = self.addHost('Laptop2',mac="00:00:00:00:00:09", ip='200.20.2.9/24',defaultRoute="Laptop2-eth1") 
    Printer = self.addHost('Printer',mac="00:00:00:00:00:10", ip='200.20.2.10/24',defaultRoute="Printer-eth1")

    # OT Department
    ws1 = self.addHost('ws1',mac="00:00:00:00:00:04", ip='200.20.3.4/24',defaultRoute="ws1-eth1") 
    ws2 = self.addHost('ws2',mac="00:00:00:00:00:05", ip='200.20.3.5/24',defaultRoute="ws2-eth1") 
    
    # IT Department
    ws4 = self.addHost('ws4',mac="00:00:00:00:00:06", ip='200.20.4.6/24',defaultRoute="ws4-eth1") 
    ws3 = self.addHost('ws3',mac="00:00:00:00:00:07", ip='200.20.4.7/24',defaultRoute="ws3-eth1") 
     
    # switch connections
    self.addLink(coreSwitch, switch1, port1=1 , port2=5) #ot
    self.addLink(coreSwitch, switch2, port1=2, port2=6) #it
    self.addLink(coreSwitch, switch3, port1=3, port2=7) #servers
    self.addLink(coreSwitch, switch4, port1=4, port2=8) #sales

    # sales connection
    self.addLink(Laptop1, switch4, port1=1, port2=1)
    self.addLink(Printer, switch4, port1=1, port2=2)
    self.addLink(Laptop2, switch4, port1=1, port2=3)

    # OT connection
    self.addLink(ws1, switch1, port1=1, port2=1)
    self.addLink(ws2, switch1, port1=1, port2=2)

    # IT connection
    self.addLink(ws3, switch2, port1=1, port2=2)
    self.addLink(ws4, switch2, port1=1, port2=1)

    # servers connection
    self.addLink(ServWeb, switch3, port1=1, port2=2)
    self.addLink(Serv2, switch3, port1=1, port2=1)
    self.addLink(ServDNS, switch3, port1=1, port2=3)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  # use static ARP
  net.staticArp() 
  CLI(net)
  
  net.stop()

if __name__ == '__main__':
  configure()