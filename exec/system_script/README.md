## Holds the scripts required to be put into /etc/systemd/system/ for use by systemctl

# Step 1:
   Copy the script shelly-cardano.services to /etc/systemd/system (directory can vary based on system being linux or otherwise)

# Step 2:
   chmod +x shelly-cardano.services

# Step 3:
     To start this script use in linux ubuntu (debian systems): systemctl start shelly-cardano.services