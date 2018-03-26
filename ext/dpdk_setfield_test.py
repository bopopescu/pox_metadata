'''
Created on Apr 18, 2016

@author: sqy output the fifth parameter is outputid
'''
from pox.core import core
from pox.lib.revent.revent import EventMixin
import pox.openflow.libpof_02 as of
from pox.lib.addresses import IPAddr,EthAddr
import time
'''
dpid_1 = 1
dpid_2 = 2
dpid_3 = 3
dpid_4 = 4
'''
def _add_protocol(protocol_name, field_list):
    """
    Define a new protocol, and save it to PMDatabase.
    
    protocol_name: string
    field_list:[("field_name", length)]
    """
    match_field_list = []
    total_offset = 0
    for field in field_list:
        field_id = core.PofManager.new_field(field[0], total_offset, field[1])   #field[0]:field_name, field[1]:length
        total_offset += field[1]
        match_field_list.append(core.PofManager.get_field(field_id))
    core.PofManager.add_protocol("protocol_name", match_field_list)

def add_protocol():
    field_list = [("DMAC",48), ("SMAC",48), ("Eth_Type",16), ("V_IHL_TOS",16), ("Total_Len",16),
                  ("ID_Flag_Offset",32), ("TTL",8), ("Protocol",8), ("Checksum",16), ("SIP_v4",32), ("DIP_v4",32),("S_Port",16),("D_Port",16 )]
    _add_protocol('ETH_IPv4', field_list)
    
    
class Test(EventMixin):
    def __init__ (self):
        add_protocol()
        core.openflow.addListeners(self, priority=0)
        
    def _handle_ConnectionUp (self, event):
        
        print "connection up!"
        for i in range(1,5):
            core.PofManager.set_port_of_enable(event.dpid, i, True)
            
        match_list=[]
        match_list.append(core.PofManager.get_field("Eth_Type")[0])
        table_id=core.PofManager.add_flow_table(event.dpid, 'FirstEntryTable', of.OF_MM_TABLE, 128, match_list)
            
	action_list=[]
        ofinstructions=[]
        matchx_list=[]
            
        match = core.PofManager.get_field("Eth_Type")[0]
        temp_matchx = core.PofManager.new_matchx(match, '0800', 'FFFF')
        matchx_list.append(temp_matchx)

        match = core.PofManager.get_field("DMAC")[0]
        temp_matchx = core.PofManager.new_matchx(match, '111000000000', 'FFFFFFFFFFFF')        
	action=core.PofManager.new_action_set_field(temp_matchx)
        action_list.append(action) 

        match = core.PofManager.get_field("DMAC")[0]
        temp_matchx = core.PofManager.new_matchx(match, '111000111000', 'FFFFFFFFFFFF')        
	action=core.PofManager.new_action_set_field(temp_matchx)
        action_list.append(action) 

        match = core.PofManager.get_field("DMAC")[0]
        temp_matchx = core.PofManager.new_matchx(match, '111111111111', 'FFFFFFFFFFFF')        
	action=core.PofManager.new_action_set_field(temp_matchx)
        action_list.append(action) 

        action=core.PofManager.new_action_output(0, 0, 0, 0, 1, 0)
        action_list.append(action) 
            
        ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
        ofinstructions.append(ofinstruction)
        flow_entry_id=core.PofManager.add_flow_entry(event.dpid,table_id,matchx_list,ofinstructions,1,1)

            
           
        
        
def launch ():
    core.registerNew(Test)
