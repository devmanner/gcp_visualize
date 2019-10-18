#!/usr/bin/env python 

import sys
import json
from graphviz import Graph

def url2id(url):
    items = url.split("/")
    return items[9]+items[6]+items[8]+items[10]

def instance(graph, instance):
    instance_id = url2id(instance['selfLink'])
    name = instance['name']
    ipaddrs = []
    for iface in instance['networkInterfaces']:
        ipaddrs.append(iface['networkIP'])

    graph.node(instance_id, shape='box3d', label='''<<TABLE><TR><TD>'''+name+'''</TD></TR><TR><TD>'''+','.join(ipaddrs)+'''</TD></TR></TABLE>>''')

    for d in instance['disks']:
        disk_id = url2id(d['source'])
        disk_label = d['deviceName']
        add_disk(graph, disk_id, disk_label)
        graph.edge(instance_id, disk_id)

def disk(graph, disk):
    disk_id = url2id(disk['selfLink'])
    disk_label = disk['name']
    add_disk(graph, disk_id, disk_label)

def add_disk(graph, disk_id, disk_label):
    graph.node(disk_id, label=disk_label, shape='cylinder')


g = Graph('G', filename='cluster.gv')

with open(sys.argv[1]) as json_file:
	json = json.load(json_file)
	for proj in json:
		print proj['project']
		print proj['instances']	
		for i in proj['instances']:
			instance(g, i)
		for d in proj['disks']:
			disk(g, d)

g.view()

