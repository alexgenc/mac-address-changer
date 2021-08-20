#https://docs.python.org/3/library/subprocess.html
#https://docs.python.org/3/library/optparse.html
#https://docs.python.org/3/library/re.html
import subprocess
import optparse
import re

def get_arguments():
    """Creates runtime argument options, and returns passed in user arguments."""

    parser = optparse.OptionParser()

    # Create runtime argument options
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (arguments, parameters) =  parser.parse_args()

    # Validate
    if not arguments.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not arguments.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    
    return arguments


def change_mac_address(interface, new_mac_address):
    """Changes current MAC address for the selected interface to the new mac address."""
    
    print(f"[+] Changing MAC address for {interface} to {new_mac_address}")

    # Kill interface process
    subprocess.call(["ifconfig", interface, "down"])
    # Change mac address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    # Start up interface process
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    """Returns current MAC address"""

    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")

arguments = get_arguments()
interface = arguments.interface
mac_address = arguments.new_mac

initial_mac = get_current_mac(interface)
print(f"Initial MAC address = {initial_mac}")

change_mac_address(interface, mac_address)

current_mac = get_current_mac(interface)
if current_mac == mac_address:
    print(f"[+] MAC address was successfully changed to {current_mac}.")
else:
    print("[-] Mac address couldn't be changed.")
