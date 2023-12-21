import psutil
import time
import matplotlib.pyplot as plt
from collections import deque

class BandwidthMonitor:
    def __init__(self, interval=1, history_size=60):
        self.interval = interval
        self.history_size = history_size
        self.history = deque(maxlen=history_size)
        self.timestamps = []
        self.alert_threshold = 1024 * 1024 * 2  # Set alert threshold to 2 MB/s

    def monitor_bandwidth(self):
        while True:
            # Get network usage statistics
            net_usage = psutil.net_io_counters()

            # Calculate the current network bandwidth in MB/s
            current_bandwidth = (net_usage.bytes_recv + net_usage.bytes_sent) / self.interval / (1024 * 1024)

            # Add current bandwidth to the history
            self.history.append(current_bandwidth)
            self.timestamps.append(time.strftime("%H:%M:%S"))

            # Display real-time bandwidth
            print(f"Current Bandwidth: {current_bandwidth:.2f} MB/s")

            # Check for abnormal usage and trigger alerts
            if current_bandwidth > self.alert_threshold:
                print(f"Alert! Abnormal Bandwidth Usage: {current_bandwidth:.2f} MB/s")

            time.sleep(self.interval)

    def plot_history(self):
        plt.plot(self.timestamps, self.history, marker='o', linestyle='-', color='b')
        plt.title('Network Bandwidth Over Time')
        plt.xlabel('Time')
        plt.ylabel('Bandwidth (MB/s)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    bandwidth_monitor = BandwidthMonitor()

    # Run bandwidth monitoring in the background
    monitor_thread = threading.Thread(target=bandwidth_monitor.monitor_bandwidth)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Plot historical data (press Ctrl+C to exit and display the plot)
    try:
        while True:
            bandwidth_monitor.plot_history()
            time.sleep(60)  # Update the plot every 60 seconds
    except KeyboardInterrupt:
        print("\nBandwidth Monitor terminated.")
