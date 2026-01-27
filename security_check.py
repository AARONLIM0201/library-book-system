import socket
import requests
import sys

ALB_DNS = "library-system-alb-1046206251.us-east-1.elb.amazonaws.com"
RDS_ENDPOINT = "terraform-20260126145823991100000001.c6f6sw2g8p4w.us-east-1.rds.amazonaws.com"
ALB_URL = f"http://{ALB_DNS}"

def check_port(host, port, expected_open=True):
    print(f"Checking {host}:{port}...", end=" ")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            status = "OPEN"
        else:
            status = "CLOSED/FILTERED"
            
        print(status)
        
        if expected_open and result == 0:
            return True
        elif not expected_open and result != 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_waf():
    print(f"\nTesting WAF on {ALB_URL}...")
    
    # 1. Normal Request
    try:
        print("Sending Normal Request...", end=" ")
        resp = requests.get(ALB_URL, timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("PASS: Normal request allowed.")
        else:
            print("FAIL: Normal request blocked or error.")
    except Exception as e:
        print(f"Error connecting: {e}")

    # 2. Malicious Request (XSS Simulation)
    try:
        print("Sending Malicious Request (<script>)...", end=" ")
        # AWS WAF Common Rule Set should block this
        params = {'q': '<script>alert(1)</script>'}
        resp = requests.get(ALB_URL, params=params, timeout=5)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 403:
            print("PASS: WAF blocked malicious request (403 Forbidden).")
        else:
            print(f"FAIL: Request was not blocked (Status: {resp.status_code}). WAF might not be active or configured correctly.")
            
    except Exception as e:
        print(f"Error connecting: {e}")

def main():
    print("=== SECURITY VALIDATION NOTEPAD ===")
    
    # Port Scans
    print("\n[PORT SCANNING]")
    check_port(ALB_DNS, 80, expected_open=True)
    check_port(ALB_DNS, 443, expected_open=False) # No HTTPS configured
    check_port(ALB_DNS, 22, expected_open=False)  # No SSH
    check_port(RDS_ENDPOINT, 5432, expected_open=False) # Should be private
    
    # WAF Test
    print("\n[WAF TESTING]")
    test_waf()
    
    print("\n=== END ===")

if __name__ == "__main__":
    main()
