# Realtime GPS-SDR-SIM

Realrtime GPS-SDR-SIM generates GPS baseband signal data streams, which can be converted 
to RF using software-defined radio (SDR) platforms, such as 
[bladeRF](http://nuand.com/), [HackRF](https://github.com/mossmann/hackrf/wiki), and [USRP](http://www.ettus.com/).


### Prerequisites
    1. create fifo called gpssim.bin
       > nkfifo gpssim.bin
       
    2. install python wget module
       > sudo pip install wget
       
    3. Install socket.io for the nodejs
       > sudo npm install socket.io

       
       
### Linuxs build instructions
    > make
    
In order to run the map on windows please copy the   maps    directory to Windows    


### Runing
  1. start the rt_gpssim by runing 
     > python run.py -r
     
  2. run the hackrf transmit utility by
    > ./transmit.sh
    
    
  3. on the Windows computrer 
    >  run_server <linux ip address>
    > browse to   https://127.0.0.1:4242/index.html
    
