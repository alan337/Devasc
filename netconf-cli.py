from ncclient import manager
from ncclient.operations import RPCError

router_ip = "192.168.100.80"
router_port = 830  # Default NETCONF port
router_username = "admin"
router_password = "admin"

# NETCONF payload with static route configuration using ietf-routing.yang
netconf_payload = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
      <description>configured by netconf</description>
    </interface>
  </interfaces>
   <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
      <routing-instance>
         <name>default</name>
         <description>default-vrf [read-only]</description>
         <interfaces/>
         <routing-protocols>
            <routing-protocol>
               <type>static</type>
               <name>1</name>
               <static-routes>
                  <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing">
                     <route>
                        <destination-prefix>0.0.0.0/0</destination-prefix>
                        <next-hop>
                           <next-hop-address>192.168.100.1</next-hop-address>
                        </next-hop>
                     </route>
                  </ipv4>
               </static-routes>
            </routing-protocol>
         </routing-protocols>
      </routing-instance>
   </routing>
</config>
"""

def push_config():
    with manager.connect(
        host=router_ip,
        port=router_port,
        username=router_username,
        password=router_password,
        hostkey_verify=False,  # Disable key verification for simplicity
    ) as m:
        try:
            # Edit-config operation to push configuration
            m.edit_config(target="running", config=netconf_payload, format="xml")
            print("Configuration pushed successfully.")
        except RPCError as e:
            print(f"Failed to push configuration. Error: {e}")

if __name__ == "__main__":
    push_config()
