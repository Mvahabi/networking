Here is a topology where you create a network between devices on the same subnet and can view reachability between each other.

In another example, we have a similar topology but this time using a remote controller. When you start a Mininet network, each switch can be connected to a remote controller - which could be in the VM, outside the VM on your local machine, or anywhere in the world. By default, --controller=remote will use 127.0.0.1 and will try ports 6653 and 6633. I used the openflow controller ___ as an example.
