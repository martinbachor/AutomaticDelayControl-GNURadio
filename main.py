import numpy as np
from gnuradio import gr
import pmt
from collections import Counter


class delay_detection_block(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(self,
                               name="delay_detection_block",  # name of the block
                               in_sig=[np.float32, np.float32],  # Two input signals with type float32
                               out_sig=[]  # No output signals
                               )

        # Output message port
        self.message_port_register_out(pmt.intern("delay_out"))

        # Input message ports
        self.message_port_register_in(pmt.intern("start"))
        self.set_msg_handler(pmt.intern("start"), self.handle_start)

        self.message_port_register_in(pmt.intern("reset"))
        self.set_msg_handler(pmt.intern("reset"), self.handle_reset)

        # Buffer for number of delays can be changed as user needs
        self.delays_buffer = []
        self.buffer_size = 10

        # Internal state
        self.delay_sent = False
        self.calibrating = False

    def handle_start(self, msg):
        print("[INFO] Calibration started.")
        self.calibrating = True

    def handle_reset(self, msg):
        print("[INFO] Calibration reset.")
        self.calibrating = False
        self.delays_buffer = []
        self.delay_sent = False

        msg_zero = pmt.from_long(0)
        self.message_port_pub(pmt.intern("delay_out"), msg_zero)
        print("[INFO] Delay set to 0 and reset completed.")

    def work(self, input_items, output_items):

        # Do nothing until "start" msg is received 
        if not self.calibrating or self.delay_sent:
            return len(input_items[0])

        # Input signals    
        signal_1 = input_items[0]
        signal_2 = input_items[1]

        # computation of cross-correlation
        correlation = np.correlate(signal_1, signal_2, mode='full')
        delay = np.argmax(np.abs(correlation)) - (len(signal_1) - 1)

        print(f"[CALIBRATION] Detected delay: {delay}")
        self.delays_buffer.append(delay)

        # When enough samples are collected
        if len(self.delays_buffer) >= self.buffer_size:
            # modus of buffer
            modus = Counter(self.delays_buffer).most_common(1)[0][0]
            # Send calculated delay as pmt message
            msg = pmt.from_long(int(modus))
            self.message_port_pub(pmt.intern("delay_out"), msg)
            print(f"[AVG Delay] Final calculated delay: {modus} samples")
            self.delay_sent = True
            self.calibrating = False

        return len(input_items[0])