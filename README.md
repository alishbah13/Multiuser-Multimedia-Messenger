# Multiuser-Multimedia-Messenger
The project is based on Socket programming on Python using TCP Sockets. The basic concept is to  allow clients to join usign unique aliases and establish a connection with any other peer. In order to accomplish this multithreading has been used. Each client is created as a thread and connected to the Host Server via <HOST> and <PORT>.

Aside from sending text, files of all types/extensions can be sent from one peer/client by typing //send<filename>.<ext> . The file being sent must be present in a folder (present in the working directory). The folder name must be equivalent to the sender's unique alias.
