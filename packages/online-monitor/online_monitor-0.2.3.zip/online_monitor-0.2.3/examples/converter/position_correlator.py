from online_monitor.converter.transceiver import Transceiver
import json
import logging
import numpy as np
from itertools import combinations

from online_monitor.utils import utils


def get_cartesian_combinations(array_one, array_two):
    ''' Creates all combinations of elements in array one against elements in array two.
    Parameters: array_one, array_two: array_like, 1 dimension
    e.g.: array_one = [1, 2, 3]; array_two = [4, 5, 6]
          result: [1, 2, 3, 1, 2, 3, 1, 2, 3], [4, 5, 6, 6, 4, 5, 5, 6, 4]
          '''
    array_one_comb = np.tile(array_one, array_two.shape[0])
    array_two_comb = np.tile(array_two, array_two.shape[0])

    array_two_comb_reshaped = array_two_comb.reshape(array_two_comb.shape[0] / array_two.shape[0], array_two.shape[0])
    for shifts in range(array_two_comb_reshaped.shape[1]):  # Shift each tile by shift vector [0, 1, 2, array_two_comb_reshaped.shape[1]]
        array_two_comb_reshaped[shifts] = np.roll(array_two_comb_reshaped[shifts], shifts)

    return array_one_comb, array_two_comb_reshaped.reshape(array_two_comb.shape)


class PositionCorrelator(Transceiver):

    def deserialze_data(self, data):
        return json.loads(data, object_hook=utils.json_numpy_obj_hook)

    def setup_interpretation(self):
        # The data with same time stamp does not have to arrive at the same receive command
        # since ZMQ buffers data and the DUT can have different timing behavior, thus the data is buffered for each
        # device in a FIFO data structure containing tuples of (time stamp, position data)
        self.data_buffer = {}  # A dict with the input addresses as keys and FIFO data as values
        for actual_receiver in self.receivers:
            self.data_buffer[actual_receiver[0]] = []
        self.correlation_histograms = {}  # Stores the actual correlation histograms for all combinations of 2 devices

    def interpret_data(self, data):
        # Fill the buffer with the actual received data
        for actual_device_data in data:  # Loop over all devices of actual received data
            for actual_data_type, actual_data in actual_device_data[1].items():  # Loop over the data from one device (time stamp, position data)
                if 'time_stamp' not in actual_data_type:
                    actual_position_data = actual_data
                else:
                    actual_time_stamp = actual_data

            # Check if the FIFO overflows and delete oldest data if needed
            fifo_size = len(self.data_buffer[actual_device_data[0]])
            max_fifo_size = int(self.config['max_buffer_size'])
            if fifo_size + 1 > max_fifo_size:
                logging.warning('Data buffer size is %d > %d for device at %s. Deleting oldest data!', fifo_size + 1, max_fifo_size, actual_device_data[0])
                self.data_buffer[actual_device_data[0]] = self.data_buffer[actual_device_data[0]][fifo_size + 1 - max_fifo_size:max_fifo_size]

            # Add the new data to the data fifo of the actual device
            self.data_buffer[actual_device_data[0]].append((actual_time_stamp, actual_position_data))

        print '______________________________________'
        # Correlate the data of all devices with the time stamp
        for (device_one_key, device_two_key) in combinations(self.data_buffer.keys(), 2):  # Loop over all combinations of two devices to correlate them
            device_one_data, device_two_data = self.data_buffer[device_one_key], self.data_buffer[device_two_key]  # Get the data of the actual two devices
            try:
                time_stamps_device_one = [i for (i, _) in device_one_data]
                time_stamps_device_two = [i for (i, _) in device_two_data]
                same_time_stamps = set(time_stamps_device_one) & set(time_stamps_device_two)
                if same_time_stamps:  # Check if there are same time stamps
                    max_same_time_stamps = max(same_time_stamps)
                    device_one_index, device_two_index = time_stamps_device_one.index(max_same_time_stamps), time_stamps_device_two.index(max_same_time_stamps)
                    device_one_max_ts_data, device_two_max_ts_data = device_one_data[device_one_index], device_two_data[device_two_index]

                    # Get hit dut_one_hits_x_combinations,y info from histogram
                    array_dut_one, array_dut_two = device_one_max_ts_data[-1], device_two_max_ts_data[-1]
                    hits_dut_one, hits_dut_two = np.where(array_dut_one != 0), np.where(array_dut_two != 0)

                    # Correlate position in dut_one_hits_x_combinations and y
                    combinations_x = get_cartesian_combinations(hits_dut_one[0], hits_dut_two[0])
                    combinations_y = get_cartesian_combinations(hits_dut_one[1], hits_dut_two[1])

                    print combinations_x[0]

#                     x_correlation = np.histogram2d(combinations_x[0], combinations_x[1], bins=[100, 100])
#                     y_correlation = np.histogram2d(combinations_y[0], combinations_y[1], bins=[100, 100])
# 
#                     self.correlation_histograms[device_one_key + '#' + device_two_key] = (x_correlation, y_correlation)
#                     correlated_data.append((device_one_key, device_two_key, device_one_max_ts_data, ))

                    # Delete all data of both devices up to maximum same time stamp
                    device_one_data = device_one_data[device_one_index + 1:]
                    device_two_data = device_two_data[device_two_index + 1:]
            except IndexError:  # Data not yet available for device
                pass

#         print self.correlation_histograms
#         return self.correlation_histograms
