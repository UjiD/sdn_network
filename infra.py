from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class CustomTreeTopo:
    @staticmethod
    def run():
        """Set up a custom tree-based Mininet topology."""
        net = Mininet(controller=RemoteController, link=TCLink)

        # Add the Ryu controller
        ryu_controller = net.addController(
            'ryuController',
            controller=RemoteController,
            ip='127.0.0.1',  # IP address of the Ryu controller
            port=6633  # Default OpenFlow port
        )

        # Core Layer
        core_switch = net.addSwitch('s1')

        # Aggregation Layer
        agg_switch1 = net.addSwitch('s2')
        agg_switch2 = net.addSwitch('s3')

        # Access Layer
        access_switch1 = net.addSwitch('s4')
        access_switch2 = net.addSwitch('s5')
        access_switch3 = net.addSwitch('s6')
        access_switch4 = net.addSwitch('s7')

        # Hosts
        hosts = []
        for i in range(1, 9):
            subnet = "10.0.0.0/24" if i <= 4 else "10.0.1.0/24"
            host_ip = f"10.0.{(i - 1) // 4}.{i % 4 + 1}/24"
            hosts.append(net.addHost(f'h{i}', ip=host_ip))

        # Connect core switch to aggregation layer switches
        net.addLink(core_switch, agg_switch1, bw=50, delay='2ms')
        net.addLink(core_switch, agg_switch2, bw=50, delay='2ms')

        # Connect aggregation switches to access switches
        net.addLink(agg_switch1, access_switch1, bw=30, delay='5ms')
        net.addLink(agg_switch1, access_switch2, bw=30, delay='5ms')
        net.addLink(agg_switch2, access_switch3, bw=30, delay='5ms')
        net.addLink(agg_switch2, access_switch4, bw=30, delay='5ms')

        # Connect hosts to access switches
        net.addLink(hosts[0], access_switch1)
        net.addLink(hosts[1], access_switch1)
        net.addLink(hosts[2], access_switch2)
        net.addLink(hosts[3], access_switch2)
        net.addLink(hosts[4], access_switch3)
        net.addLink(hosts[5], access_switch3)
        net.addLink(hosts[6], access_switch4)
        net.addLink(hosts[7], access_switch4)

        # Start the network
        net.start()
        print("Custom tree-based topology is up. Use 'pingall' in the CLI to test connectivity.")

        # Test connectivity
        net.pingAll()

        # Enter Mininet CLI
        CLI(net)

        # Stop the network
        net.stop()


if __name__ == '__main__':
    CustomTreeTopo.run()
