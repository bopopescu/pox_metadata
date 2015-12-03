'''
Created on 2015.8.27

@author: shengrulee
'''
from pox.core import core
from pox.lib.revent.revent import EventMixin
import pox.openflow.libpof_02 as of

log = core.getLogger()

def _handle_PacketIn(event):
    
    msg=of.ofp_flow_mod()
    msg.counter_id = 0
    msg.cookie = 0
    msg.cookie_mask = 0
    msg.table_id = 0
    msg.table_type = 0 #OF_MM_TABLE
    #msg.priority = 0
    msg.index = 0
  
    #matchx 1
    tempmatchx=of.ofp_matchx()
    tempmatchx.field_id=0
    tempmatchx.offset=0
    tempmatchx.length=48
    tempmatchx.set_value("70e284087574")  #Network Center PC MAC
    tempmatchx.set_mask("ffffffffffff")
    msg.matchx.append(tempmatchx)
 
    tempins=of.ofp_instruction_apply_actions()
    action = of.ofp_action_output()
    action.port_id = 6
    tempins.action_list.append(action)
    msg.instruction_list.append(tempins)
    

    event.connection.send(msg)

  
    packetout_msg = of.ofp_packet_out()
    packetout_msg.actions.append(of.ofp_action_output(portId = 255))
    packetout_msg.data = event.ofp
    packetout_msg.in_port = event.port
    event.connection.send(packetout_msg)


    msg1=of.ofp_flow_mod()
    msg1.counter_idd = 0
    msg1.cookie = 0
    msg1.cookie_mask = 0
    msg1.table_id = 0
    msg1.table_type = 0 #OF_MM_TABLE
    msg1.priority = 0
    msg1.index = 1
  
    #matchx 1
    tempmatchx1=of.ofp_matchx()
    tempmatchx1.fieldId=0
    tempmatchx1.offset=0
    tempmatchx1.length=48
    tempmatchx1.set_value("70e284088b30")  #Network Center PC MAC
    tempmatchx1.set_mask("ffffffffffff")
    msg1.matchx.append(tempmatchx1)
 
    tempins1=of.ofp_instruction_apply_actions()
    action1 = of.ofp_action_output()
    action1.port_id=7
    tempins1.action_list.append(action1)
    msg1.instruction_list.append(tempins1)
    

    event.connection.send(msg1)


    log.info("Get PacketIn")
    


def _handle_ConnectionUp(event):
    
    ofmatch20 =of.ofp_match20()
    ofmatch20.field_id=0
    ofmatch20.offset=0
    ofmatch20.length=48
    
    first_table = of.ofp_table_mod()
    first_table.flow_table.table_name='FirstTableEntry'
    first_table.flow_table.table_id = 0
    first_table.flow_table.command=0
    first_table.flow_table.table_type=0
    first_table.flow_table.table_size=128
    first_table.flow_table.key_length=48
    first_table.flow_table.match_field_num=1
    first_table.flow_table.match_field_list.append(ofmatch20)
    
    event.connection.send(first_table)
    
    
def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
