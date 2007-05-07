# -*- coding: utf-8 -*-
"""
Project         :   HalfLife/counter-strike serverinfo module

Author          :   Guyon Morée <gumuz@looze.net>
Createdate      :   6 February 2005
Filename        :   hl_info.py

Description     :   Module to retireve server info from a Half Life / counter-strike server

                    **This will not work with the new source engine-type servers**

                    This module exports only *one* function:

                        - retrieve_info(host, port)

                    Given a hostname and a portnumber, this function will try
                    to retrieve the server details and a player list with fragcounts.

                    This data will be returned as a python dictionary. The dictionary will
                    have a structure like the following example details:

                    {'address': '62.212.75.45:27015',
                     'clientcount': 5,
                     'clientmax': 16,
                     'hostname': 'GameServers.net - Condition Zero (02) Dust Only',
                     'map': 'de_dust_cz',
                     'mod': 'czero',
                     'modname': 'Condition Zero',
                     'os': 'Linux',
                     'players': {1: {'fragtotal': 6, 'nickname': 'L3on'},
                                 2: {'fragtotal': 17, 'nickname': 'tjohoooo'},
                                 3: {'fragtotal': 6, 'nickname': 'marihuana'},
                                 4: {'fragtotal': 0, 'nickname': 'simon.be'},
                                 5: {'fragtotal': 2, 'nickname': '[XSS]Rex[DK]'}},
                     'protocol': 47,
                     'type': 'Dedicated'}

"""

import socket, struct


def retrieve_info(host, port):
    # first issue details command
    query = '\\xFF\\xFF\\xFF\\xFFdetails'.decode('string-escape')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.sendto(query, (host, int(port)))
    
    # receive & Parse data
    details = {}
    
    data = server.recv(2048)
    
    data = data[5:]             # cut off 5 bytes of rubbish :)
    details['address'] = data[:data.find(chr(0))]
    
    data = data[data.find(chr(0))+1:]
    details['hostname'] = data[:data.find(chr(0))]
    
    data = data[data.find(chr(0))+1:]
    details['map'] = data[:data.find(chr(0))]
    
    data = data[data.find(chr(0))+1:]
    details['mod'] = data[:data.find(chr(0))]
    
    data = data[data.find(chr(0))+1:]
    details['modname'] = data[:data.find(chr(0))]
    
    data = data[data.find(chr(0))+1:]
    
    details['clientcount'] = ord(data[0])
    details['clientmax'] = ord(data[1])
    details['protocol'] = ord(data[2])
    details['type'] = {'L':'Listen','D':'Dedicated'}[data[3].upper()]
    details['os'] = {'L':'Linux','W':'Windows'}[data[4].upper()]
    
    # now issue players command
    query = '\\xFF\\xFF\\xFF\\xFFplayers'.decode('string-escape')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.sendto(query, (host, int(port)))
    
    # receive & Parse data
    data = server.recv(2048)
    players = {}
    
    data = data[6:]             # cut off 6 bytes of rubbish :)
    
    for index in range(int(details['clientcount'])):
        playerid = ord(data[0])
        data = data[1:]
        players[playerid] = {'nickname':data[:data.find(chr(0))]}
        data = data[data.find(chr(0))+1:]
        players[playerid]['fragtotal'] = struct.unpack('@i', data[:4])[0]
        data = data[8:]
    
    details["players"] = players
    return details


if __name__ == '__main__':
    from pprint import pprint

    pprint(retrieve_info('62.212.75.45',27015))