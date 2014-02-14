StegoMinecraft
==============

Steganography in minecraft maps 

Don't forget "--recursive" while cloning (ex : "git clone --recursive https://github.com/sebeq33/StegoMinecraft.git")

using :
- python 2.7
- PyQt4 
- pymclevel (need pyYaml and numpy (windows -> need a lousy Installation (maybe only in 64bits ?) : http://www.lfd.uci.edu/~gohlke/pythonlibs/)


Personal notes (and TODO):

- Create new map / take existing map
- Choose input file / type text input to insert
- Insert box (from pos1 to pos2) / Insert randomly (using key/seed)
- Choose which block = 1, which = 0 (default: Bedrock & !Bedrock)
- Output in a new copy / save in input

- Compression ?
- Open FileExplorer in Minecraft save directory
- Send a map to another ip ? (tcp ?)
- Command line version / graphical version (Qt)
- test on linux
- replace map creation seed


Ref :

chunks format : 
- http://minecraft.gamepedia.com/Chunk_format

minecraft server packets : 
- http://minecraft.gamepedia.com/Classic_server_protocol
- http://www.minecraftforge.net/wiki/Packet_Handling

minecraft python server independant project (2009 - too old) : 
- https://bitbucket.org/andrewgodwin/myne/src

interesting threads : 
- http://stackoverflow.com/questions/9520833/how-to-send-packets-to-a-remote-minecraft-classic-server-in-python
- http://wiki.vg/How_to_Write_a_Client
- http://www.minecraftforge.net/wiki/Packet_Handling
- http://greyminecraftcoder.blogspot.co.uk/2013/10/packets-from-client-to-server.html
- http://stackoverflow.com/questions/11498701/how-to-send-minecraft-server-packets-from-objective-c
