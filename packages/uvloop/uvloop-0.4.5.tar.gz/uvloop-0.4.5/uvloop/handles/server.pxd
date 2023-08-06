cdef class UVStreamServer(UVStream):
    cdef:
        object ssl
        object protocol_factory
        bint opened
        Server _server

    cdef _init(self, Loop loop, object protocol_factory, Server server,
               object ssl)

    cdef inline _mark_as_open(self)

    cdef listen(self, int backlog=?)
    cdef _on_listen(self)
    cdef UVTransport _make_new_transport(self, object protocol, object waiter)
