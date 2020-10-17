## NRPE

check_multi is just a normal plugin and can be called via NRPE like all other plugins.\\
One remark: you also have to change the buffer sizes in common.h MAX_INPUT_BUFFER and MAX_PACKETBUFFER_LENGTH.

Caveat:\\
SSL implementation in NRPE only supports one buffer send per communication, and this is limited by PIPE_BUF (4096 bytes on Linux systems).


