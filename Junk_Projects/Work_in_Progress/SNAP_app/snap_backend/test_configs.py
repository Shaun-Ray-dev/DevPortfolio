from configs import add_config, list_configs

# Test adding a config
add_config(1, "interface Gig0/0\n ip address 192.168.1.1 255.255.255.0\n no shutdown")

# Test listing configs
configs = list_configs(1)
for c in configs:
    print(c)
