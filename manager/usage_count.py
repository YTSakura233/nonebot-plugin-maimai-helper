class UsageCount:
    handled_user_count = dict(unknown=0)

    def add(self, wxid="unknown"):
        if wxid not in self.handled_user_count:
            self.handled_user_count[wxid] = 0
        self.handled_user_count[wxid] += 1

    def get(self, wxid="unknown"):
        my_count = 0
        if wxid is not None:
            my_count = self.handled_user_count.get(wxid, 0)
        return len(self.handled_user_count.keys()) - 1, sum(self.handled_user_count.values()), my_count


class NetworkCount:
    average_delay = 0
    request_failed_count = 0
    request_count = 0
    zlib_compress_skip_count = 0

    def update_average_delay(self, delay: int):
        if self.request_count == 0:
            self.average_delay = delay
        else:
            self.average_delay = (self.average_delay * self.request_count + delay) / (self.request_count + 1)

    def add_request_count(self):
        self.request_count += 1

    def add_failed_request_count(self):
        self.request_count -= 1

    def add_zlib_compress_skip_count(self):
        self.zlib_compress_skip_count += 1

    def add_request_failed_count(self):
        self.request_failed_count += 1

    def get_network_status(self):
        return self.request_count, self.request_failed_count, self.zlib_compress_skip_count, self.average_delay
