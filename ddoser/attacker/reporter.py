class Reporter:

    def __init__(self,
                 pname,
                 num_requests=0,
                 failed_requests=0,
                 num_sessions=0
                 ):
        self.pname = pname
        self.num_requests = num_requests
        self.failed_requests = failed_requests
        self.num_sessions = num_sessions
