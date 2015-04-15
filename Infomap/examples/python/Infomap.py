#!/usr/bin/env python
# import os, sys
# sys.path.append(os.path.abspath('infomap'))

from infomap import infomap

conf = infomap.init("--two-level -v -N2");

print "Creating network..."
network = infomap.Network(conf);

network.addLink(0, 1);
network.addLink(0, 2);
network.addLink(0, 3);
network.addLink(1, 0);
network.addLink(1, 2);
network.addLink(2, 1);
network.addLink(2, 0);
network.addLink(3, 0);
network.addLink(3, 4);
network.addLink(3, 5);
network.addLink(4, 3);
network.addLink(4, 5);
network.addLink(5, 4);
network.addLink(5, 3);

print "Num links:", network.numLinks()

network.finalizeAndCheckNetwork();

tree = infomap.HierarchicalNetwork(conf)

infomap.run(network, tree);

codelength = tree.codelength()

print "Codelength:", codelength
