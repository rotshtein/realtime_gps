# Realtime GPS-SDR-SIM

Realrtime GPS-SDR-SIM generates GPS baseband signal data streams, which can be converted 
to RF using software-defined radio (SDR) platforms, such as [HackRF](https://github.com/mossmann/hackrf/wiki).

### Prerequisites
    1. create fifo called gpssim.bin
       > nkfifo gpssim.bin
       
    2. install python wget module
       > sudo pip install wget
       
    3. Install socket.io for the nodejs
       > sudo npm install socket.io

    4. internet connection to the raspberry

    5. network connection between the Windows and the Linux/raspberry (you need to know the raspberry IP)
       
  # Linuxs build instructions
    > make
    > chmod +x realtime rt_gpssim transmit.sh
    
  # Windows    
    In order to run the map on windows please copy the "maps" directory to Windows    


### Runing
  # Linux/Raspberry side
    1. Connect the hackrf
    2. start the rt_gpssim by runing 
     > ./realtime
     
    3. run the hackrf transmit utility by
    > ./transmit.sh
    
    
  # Windows computrer 
    >  run_server <linux ip address> from the "maps" directory
    > browse to   https://127.0.0.1:4242/index.html
    
