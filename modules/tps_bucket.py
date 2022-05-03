import time
from multiprocessing import Process, Value


# Naive TPS regulation

# This class holds a bucket of tokens which are refilled every second based on the expected TPS
class TPSBucket:

    def __init__(self, expected_tps):
        self.number_of_tokens = Value('i', 0)
        self.expected_tps = expected_tps
        self.bucket_refresh_process = Process(
            target=self.refill_bucket_per_second)  # process to constantly refill the TPS bucket

    def refill_bucket_per_second(self):
        while True:
            print("refill")
            self.refill_bucket()
            time.sleep(1)

    def refill_bucket(self):
        self.number_of_tokens.value = self.expected_tps
        print('bucket count after refill', self.number_of_tokens)

    def start(self):
        self.bucket_refresh_process.start()

    def stop(self):
        self.bucket_refresh_process.kill()

    def get_token(self):
        response = False
        if self.number_of_tokens.value > 0:
            with self.number_of_tokens.get_lock():
                if self.number_of_tokens.value > 0:
                    self.number_of_tokens.value -= 1
                    response = True

        return response
