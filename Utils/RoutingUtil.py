#!/usr/bin/env python
# -*- coding: utf-8 -*-

def isRouteExist(node, dist_ip):
    next = None
    hop = None
    for route_info in node.routing_table:
        if route_info['dist_ip'] == dist_ip:
            next = route_info['next_ip']
            hop = route_info['hop']
            return route_info['enable'], next, hop
            break
    else:
        return False, next, hop
