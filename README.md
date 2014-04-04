StegoMinecraft
==============

Steganography in minecraft maps. Read "Kent - Project Research 63.pdf" presentations slides of the project.

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


# Technicals Ref :
chunks format : 
- http://minecraft.gamepedia.com/Chunk_format
commands :
- http://minecraft.gamepedia.com/Commands
Varint :
- https://gist.github.com/thinkofdeath/e975ddee04e9c87faf22
- https://developers.google.com/protocol-buffers/docs/encoding#varints
JSON Data :
- https://gist.github.com/thinkofdeath/e882ce057ed83bac0a1c

minecraft server packets : 
- http://minecraft.gamepedia.com/Classic_server_protocol
- http://www.minecraftforge.net/wiki/Packet_Handling
- http://wiki.vg/Protocol#Chat_Message_2

minecraft client :
- https://github.com/ORelio/Minecraft-Console-Client

interesting threads : 
- http://stackoverflow.com/questions/9520833/how-to-send-packets-to-a-remote-minecraft-classic-server-in-python
- http://wiki.vg/How_to_Write_a_Client
- http://www.minecraftforge.net/wiki/Packet_Handling
- http://greyminecraftcoder.blogspot.co.uk/2013/10/packets-from-client-to-server.html
- http://stackoverflow.com/questions/11498701/how-to-send-minecraft-server-packets-from-objective-c
- http://stackoverflow.com/questions/19758270/read-varint-from-linux-sockets

# Papers/Books Ref :
- Steganography in games: A general methodology and its application to the game of Go
http://www.seg.inf.uc3m.es/papers/2006cosec.pdf
- Steganography: Past, Present, Future :
https://www.sans.org/reading-room/whitepapers/stenganography/steganography-past-present-future-552
- A Game-Theoretic Approach to Content-Adaptive Steganography
http://www.ihconference.org/preproceedings/IH2012_07_Schoettle.pdf
- Noiseless Steganography: The Key to Covert Communications, By Abdelrahman Desoky
http://books.google.co.uk/books?id=GyPG-un1ivkC&printsec=frontcover&hl=fr#v=onepage&q&f=false
- Assured Supraliminal Steganography in Computer Games
http://pages.cpsc.ucalgary.ca/~asmosuno/WISA_2013.pdf
