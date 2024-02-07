# Lab3 Skeleton
from pox.core import core
import pox.openflow.libopenflow_01 as of
# from pox.lib.addresses import IPAddr
# from pox.lib.packet.ipv4 import ipv4
# from pox.lib.packet.tcp import tcp
# from pox.lib.packet.udp import udp
# from pox.lib.packet.icmp import icmp
# from pox.lib.packet.arp import arp

log = core.getLogger()

class Routing (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def accept(self, packet, packet_in, port_num):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.actions.append(of.ofp_action_output(port = port_num))
    msg.data = packet_in
    self.connection.send(msg)

  def drop(self, packet, packet_in):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match().from_packet(packet)
    msg.idle_timeout = 30  
    msg.hard_timeout = 30  
    msg.buffer_id = packet_in.buffer_id
    self.connection.send(msg)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here
    arp = packet.find("arp")
    tcp = packet.find("tcp")
    icmp = packet.find("icmp")
    ipv4 = packet.find("ipv4")
    udp = packet.find("udp")

    ot_sub = {'ws1':'200.20.3.4', 'ws2':'200.20.3.5'}
    it_sub = {'ws3':'200.20.4.7', 'ws4':'200.20.4.6'}
    ser_sub = {'ser2':'200.20.1.1', 'web':'200.20.1.2', 'dns':'200.20.1.3'}
    sal_sub = {'l1':'200.20.2.8', 'l2':'200.20.2.9','pri':'200.20.2.10'}

    if icmp is not None:
      # Coreswitch
      if switch_id == 5:
        if str(ipv4.srcip) in sal_sub.values() and str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 2)
        if str(ipv4.srcip) in it_sub.values() and str(ipv4.dstip) in sal_sub.values():
          self.accept(packet, packet_in, 4)

      # in IT
      elif switch_id == 2:
        if str(ipv4.dstip) in it_sub.values():
          if str(ipv4.dstip) == '200.20.4.6':
            self.accept(packet, packet_in, 1)
          if str(ipv4.dstip) == '200.20.4.7':
            self.accept(packet, packet_in, 2)
        
        if str(ipv4.dstip) in sal_sub.values():
          self.accept(packet, packet_in, 6)

      # in sales
      elif switch_id == 4:
        if str(ipv4.dstip) in sal_sub.values():
          if str(ipv4.dstip) == '200.20.2.8':
            self.accept(packet, packet_in, 1)
          if str(ipv4.dstip) == '200.20.2.9':
            self.accept(packet, packet_in, 3)
          if str(ipv4.dstip) == '200.20.2.10':
            self.accept(packet, packet_in, 2)
        if str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 8)
    
    # TCP traffic
    elif tcp is not None:
      # Coreswitch
      if switch_id == 5:
        if str(ipv4.srcip) in ser_sub.values() and str(ipv4.dstip) in ot_sub.values():
          self.accept(packet, packet_in, 1)
        if str(ipv4.srcip) in ser_sub.values() and str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 2)
        if str(ipv4.srcip) in ot_sub.values() and str(ipv4.dstip) in ser_sub.values():
          self.accept(packet, packet_in, 3)
        if str(ipv4.srcip) in ot_sub.values() and str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 2)
        if str(ipv4.srcip) in it_sub.values() and str(ipv4.dstip) in ser_sub.values():
          self.accept(packet, packet_in, 3)
        if str(ipv4.srcip) in it_sub.values() and str(ipv4.dstip) in ot_sub.values():
          self.accept(packet, packet_in, 1)

      # OT switch
      if switch_id == 1:
        if str(ipv4.dstip) in ot_sub.values():
          if str(ipv4.dstip) == '200.20.3.4':
            self.accept(packet, packet_in, 1)
          if str(ipv4.dstip) == '200.20.3.5':
            self.accept(packet, packet_in, 2)
        if str(ipv4.dstip) in ser_sub.values() or str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 5)
          
      # IT swtich
      if switch_id == 2:
        if str(ipv4.dstip) in it_sub.values():
          if str(ipv4.dstip) == '200.20.4.6':
            self.accept(packet, packet_in, 1)
          elif str(ipv4.dstip) == '200.20.4.7':
            self.accept(packet, packet_in, 2)
        if str(ipv4.dstip) in ser_sub.values() or str(ipv4.dstip) in ot_sub.values():
          self.accept(packet, packet_in, 6)

      # Data Switch
      if switch_id == 3:
        if str(ipv4.dstip) in ser_sub.values():
          if str(ipv4.dstip) == '200.20.1.1':
            self.accept(packet, packet_in, 1)
          elif str(ipv4.dstip) == '200.20.1.2':
            self.accept(packet, packet_in, 2)
          elif str(ipv4.dstip) == '200.20.1.3':
            self.accept(packet, packet_in, 3)
        #to the OT Department or IT Department
        if str(ipv4.dstip) in ot_sub.values() or str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 7)
        
    # UDP traffic
    elif udp is not None:
      # Coreswitch
      if switch_id == 5:
        if str(ipv4.srcip) in ser_sub.values() and str(ipv4.dstip) in ot_sub.values():
            self.accept(packet, packet_in, 1)
        elif str(ipv4.srcip) in ot_sub.values() and str(ipv4.dstip) in ser_sub.values():
          self.accept(packet, packet_in, 3)
        elif str(ipv4.srcip) in ser_sub.values() and str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 2)
        elif str(ipv4.srcip) in it_sub.values() and str(ipv4.dstip) in ser_sub.values():
          self.accept(packet, packet_in, 3)

      # OT Switch
      elif switch_id == 1:
          if str(ipv4.dstip) in ot_sub.values():
            if str(ipv4.dstip) == '200.20.3.4':
              self.accept(packet, packet_in, 1)
            elif str(ipv4.dstip) == '200.20.3.5':
              self.accept(packet, packet_in, 2)
          if str(ipv4.dstip) in ser_sub.values():
            self.accept(packet, packet_in, 5)

      # IT Switch
      elif switch_id == 2:
        if str(ipv4.dstip) in it_sub.values():
          if str(ipv4.dstip) == '200.20.4.6':
            self.accept(packet, packet_in, 1)
          if str(ipv4.dstip) == '200.20.4.7':
            self.accept(packet, packet_in, 2)
        
        if str(ipv4.dstip) in ser_sub.values():
          self.accept(packet, packet_in, 6)

      # Data Switch
      elif switch_id == 3:
        if str(ipv4.dstip) in ser_sub.values():
          if str(ipv4.dstip) == '200.20.1.1':
            self.accept(packet, packet_in, 1)
          if str(ipv4.dstip) == '200.20.1.2':
            self.accept(packet, packet_in, 2)
          if str(ipv4.dstip) == '200.20.1.3':
            self.accept(packet, packet_in, 3)
        #to the OT Department or IT Department
        if str(ipv4.dstip) in ot_sub.values() or str(ipv4.dstip) in it_sub.values():
          self.accept(packet, packet_in, 7)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)