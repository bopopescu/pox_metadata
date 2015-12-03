from pox.core import core
from pox.lib.revent.revent import EventMixin
import pox.openflow.libpof_02 as of
from pox.lib.recoco import Timer
from time import sleep
flow_entry_id_2291=0
dpid_232=2215152370
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
            if i!=2 and event.dpid != dpid_232:
                core.PofManager.set_port_of_enable(event.dpid, i, True)
        if event.dpid==dpid_232:
            core.PofManager.set_port_of_enable(event.dpid, 3, True)
            core.PofManager.set_port_of_enable(event.dpid, 5, True)
            core.PofManager.set_port_of_enable(event.dpid, 6, True)
            core.PofManager.set_port_of_enable(event.dpid, 7, True)
            core.PofManager.set_port_of_enable(event.dpid, 8, True)
            #core.PofManager.set_port_of_enable(event.dpid, 2, True)
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
            matchx.value="abababababab"
            matchx_list.append(matchx)
            
            action_list=[]
            ofinstructions=[]
            reason=1
            action= core.PofManager.new_action_packetin(reason)
            action_list.append(action)
            
            ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
            ofinstructions.append(ofinstruction)
            table_id=0
            priority=11
            counter_enable=1
            flow_entry_id_2321=core.PofManager.add_flow_entry(event.dpid,table_id,matchx_list,ofinstructions,priority,counter_enable)

        if event.dpid==dpid_231:
            core.PofManager.set_port_of_enable(event.dpid, 2, True)
            core.PofManager.set_port_of_enable(event.dpid, 6, True)
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
            
            port_id_value_type=0
            port_id=6
            action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
            action_list.append(action)
            
            ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
            ofinstructions.append(ofinstruction)
            table_id=0
            priority=10
            counter_enable=1
            flow_entry_id_2291=core.PofManager.add_flow_entry(event.dpid,table_id,matchx_list,ofinstructions,priority,counter_enable)



        if event.dpid==dpid_229:
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


            matchx_list=[]
            match_field=core.PofManager.get_field(0)
            matchx=of.ofp_matchx()
            matchx.field_id=match_field.field_id
            matchx.field_name=match_field.field_name
            matchx.length=match_field.length
            matchx.offset=match_field.offset
            matchx.mask="ffffffffffff"
            matchx.value="abababababab"
            matchx_list.append(matchx)
            
            action_list=[]
            ofinstructions=[]
            reason=1
            action= core.PofManager.new_action_packetin(reason)
            action_list.append(action)
            
            ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
            ofinstructions.append(ofinstruction)
            table_id=0
            priority=11
            counter_enable=1
            flow_entry_id_2292=core.PofManager.add_flow_entry(event.dpid,table_id,matchx_list,ofinstructions,priority,counter_enable)
    def _handle_PacketIn (self, event):
        print "this is packet in~"
        dpid=event.connection.dpid
        packet=event.parsed
        print event.ofp
        udpp=packet.find('udp')
        if udpp:
            print "udp port:",udpp.dstport
            if udpp.dstport==8000:
                print "Get it!~~~!!!"
                match_field_list=[]
                match_field=core.PofManager.get_field(0)
                match_field_list.append(match_field)
                table={}
                table["name"]="FirstEntryTable"
                table["type"]=0
                table['size']=128
                core.PofManager.add_flow_table(dpid_230,  table['name'], table['type'], table['size'], match_field_list)
                
    
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
                
                port_id_value_type=0
                port_id=1
                action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
                action_list.append(action)
                
                ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
                ofinstructions.append(ofinstruction)
                table_id=0
                priority=10
                counter_enable=1
                flow_entry_id_2301=core.PofManager.add_flow_entry(dpid_230,table_id,matchx_list,ofinstructions,priority,counter_enable)

                '''229'''
                action_list=[]
                ofinstructions=[]
                
                port_id_value_type=0
                port_id=6
                action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
                action_list.append(action)
                
                port_id_value_type=0
                port_id=4
                action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
                action_list.append(action)
                
                ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
                ofinstructions.append(ofinstruction)
                table_id=0
                priority=20
                counter_enable=1
                flow_entry_id_2293=core.PofManager.add_flow_entry(dpid_229,table_id,matchx_list,ofinstructions,priority,counter_enable)
                
                '''232'''
                action_list=[]
                ofinstructions=[]
                
                port_id_value_type=0
                port_id=6
                action=core.PofManager.new_action_output(port_id_value_type, 0, 0, 0, port_id, 0)
                action_list.append(action)
                
                ofinstruction=core.PofManager.new_ins_apply_actions(action_list)
                ofinstructions.append(ofinstruction)
                table_id=0
                priority=10
                counter_enable=1
                flow_entry_id_2322=core.PofManager.add_flow_entry(dpid_232,table_id,matchx_list,ofinstructions,priority,counter_enable)

                
def launch ():
    core.registerNew(test)
    #Timer(25,change,recurring=False)