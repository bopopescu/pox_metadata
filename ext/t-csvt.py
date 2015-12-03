from pox.core import core
from pox.lib.revent.revent import EventMixin
import pox.openflow.libpof_02 as of
from pox.lib.recoco import Timer
from time import sleep
flow_entry_id_2291=0
dpid_231=2215152430
dpid_230=2215152298
dpid_229=2215146867
protocols={'ETH+IPv4': [('Dmac', 48, 0, 0), ('Smac', 48, 48, 1), ('Type', 16, 96, 2), ('V', 4, 112, 3), ('IHL', 4, 116, 4), 
                        ('TOS', 8, 120, 5), ('TotalLength', 16, 128, 6), ('ID', 16, 144, 7), ('Flag', 16, 160, 8), 
                        ('TTL', 8, 176, 9), ('Protocol', 8, 184, 10), ('checksum', 16, 192, 11), ('SIP', 32, 208, 12), 
                        ('DIP', 32, 240, 13)],
            'ETH+IPv6': [('Dmac', 48, 0, 14), ('Smac', 48, 48, 15), ('Type', 16, 96, 16),('V', 4, 112, 17), ('TC', 8, 116, 18), 
                         ('Label', 20, 124, 19), ('Totallength', 16, 144, 20), ('NH', 8, 160, 21), ('TTL', 8, 168, 22), 
                         ('SIP', 128, 176, 23), ('DIP', 128, 304, 24)],
           'FFC':[('Dmac', 20, 0, 25), ('Smac', 28, 20, 26)]}
class test(EventMixin):
    def __init__ (self):
        core.openflow.addListeners(self)
        for key in protocols.keys():
            match_field_list = []
            field_list=[]
            for field in protocols[key]:
                field_id = core.PofManager.new_field(field[0], field[2], field[1])
                match_field_list.append(core.PofManager.get_field(field_id))
                field_tuple=(field[0], field[1], field[2],field_id)
                field_list.append(field_tuple)
            core.PofManager.add_protocol(key,match_field_list)
            protocols[key]=field_list
        
    def _handle_ConnectionUp (self, event):
        print event.dpid
        for i in range(7):
            print i
            if i!=2 and event.dpid!=dpid_231:
                core.PofManager.set_port_of_enable(event.dpid, i, True)
        
        if event.dpid==dpid_229 :
            match_field_list=[]
            match_field=core.PofManager.get_field(0)
            match_field_list.append(match_field)
#             match_field=core.PofManager.get_field(2)
#             match_field_list.append(match_field)
            table={}
            table["name"]="FirstEntryTable"
            table["type"]=0
            table['size']=128
            core.PofManager.add_flow_table(event.dpid,  table['name'], table['type'], table['size'], match_field_list)
            

            matchx_list=[]
            match_field=core.PofManager.get_field(0)
            matchx=of.ofp_matchx()
            matchx.field_id=match_field.field_id
            matchx.field_name=match_field.field_name
            matchx.length=match_field.length
            matchx.offset=match_field.offset
            matchx.mask="ffffffffffff"
            matchx.value="605718a21714"
            matchx_list.append(matchx)
            
            action_list=[]
            ofinstructions=[]
                        
#             field_position=208
#             length_value=96
#             length_value_type=0
#             length_field=None
#             action = core.PofManager.new_action_delete_field(field_position, length_value_type, length_value, length_field)
#             action_list.append(action)
#             
#             field_position=176
#             length_value=16
#             length_value_type=0
#             length_field=None
#             action = core.PofManager.new_action_delete_field(field_position, length_value_type, length_value, length_field)
#             action_list.append(action)
#             
#             field_position=112
#             length_value=16
#             length_value_type=0
#             length_field=None
#             action = core.PofManager.new_action_delete_field(field_position, length_value_type, length_value, length_field)
#             action_list.append(action)
#             
#             field_setting=of.ofp_matchx()
#             field=core.PofManager.get_field(2)
#             field_setting.field_id=field.field_id
#             field_setting.field_name=field.field_name
#             field_setting.offset=field.offset
#             field_setting.length=field.length
#             field_setting.value="8850"
#             field_setting.mask="ffff"
#             action=core.PofManager.new_action_set_field(field_setting)
#             action_list.append(action)
#             
#             field_setting=of.ofp_matchx()
#             field=core.PofManager.get_field(0)
#             field_setting.field_id=field.field_id
#             field_setting.field_name=field.field_name
#             field_setting.offset=field.offset
#             field_setting.length=field.length
#             field_setting.value="200123000021"
#             field_setting.mask="ffffffffffff"
#             action=core.PofManager.new_action_set_field(field_setting)
#             action_list.append(action)
            
            port_id_value_type=0
            port_id=3
            action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
            action_list.append(action)
            
            port_id_value_type=0
            port_id=4
            action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
            action_list.append(action)
            
            ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
            ofinstructions.append(ofinstruction)
            table_id=0
            priority=10
            counter_enable=1
            flow_entry_id_2291=core.PofManager.add_flow_entry(event.dpid,table_id,matchx_list,ofinstructions,priority,counter_enable)


                
def launch ():
    core.registerNew(test)
    #Timer(25,change,recurring=False)