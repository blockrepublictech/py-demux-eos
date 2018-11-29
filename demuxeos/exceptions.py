# py-demux-eos - Deterministic event-sourced state and side effect handling for blockchain applications
# Copyright (C) 2018 BlockRepublic Pty Ltd
# Licenced under the Apache 2.0 Licence

class UnknownBlockError(Exception):
    # Raised when the API return status code 500 which means we asked for an unknown block
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
