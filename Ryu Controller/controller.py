# Import necessary modules from ryu library for the creation of the SDN controller
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.ofproto import inet

# Import necessary modules for database management and HTTP request handling
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from threading import Timer

Base = declarative_base()

# Define the database table
class MacAddress(Base):
    __tablename__ = 'mac_addresses'
    mac = Column(String, primary_key=True)

# Create engine for SQLite database
engine = create_engine('sqlite:////home/leandro/finalproject/whitelist.db')
Session = sessionmaker(bind=engine)
session = Session()


# Define the SDN application for the switch
class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'dpset': dpset.DPSet, 'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {} # Dictionary to keep track of MAC addresses and their corresponding ports
        self.datapaths = {} # Dictionary to keep track of datapaths (switches)


    # Event handler for switch features (invoked at the start of the connection)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Add default flow to send all packets to the controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        # Store the datapath instance
        self.datapaths[datapath.id] = datapath

    # Function to add flows to the switch
    def add_flow(self, datapath, priority, match, actions, hard_timeout=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        # If a hard_timeout is specified, add it to the flow
        if hard_timeout is not None:
            mod = parser.OFPFlowMod(datapath=datapath, hard_timeout=hard_timeout, priority=priority, match=match, instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)


