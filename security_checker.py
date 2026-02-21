import requests
import ssl
import socket
import urllib.parse
import sys


def check_security_headers(url):
    """
    Checks for common security headers in the HTTP response.
    """
    results = []
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        # Define headers to check
        security_headers = {
            "Content-Security-Policy": {
                "desc": "Helps prevent XSS and data injection attacks.",
                "fix": "Implement a strong CSP header to restrict where resources can be loaded from."
            },
            "X-Frame-Options": {
                "desc": "Protects against Clickjacking.",
                "fix": "Set X-Frame-Options to DENY or SAMEORIGIN."
            },
            "X-Content-Type-Options": {
                "desc": "Prevents MIME type sniffing.",
                "fix": "Set X-Content-Type-Options to 'nosniff'."
            },
            "Strict-Transport-Security": {
                "desc": "Enforces HTTPS connections.",
                "fix": "Implement HSTS header (e.g., max-age=31536000; includeSubDomains)."
            }
        }

        for header, info in security_headers.items():
            if header in headers:
                results.append(
                    f"{header} -> Rank(10) -> Action: Nothing to do -> To do: It keep. It's already max security.")
            else:
                results.append(
                    f"{header} -> Rank(0) -> Action: Immediate action required -> To do: {info['fix']}")

    except Exception as e:
        results.append(f"Header Check Failed: {str(e)}")

    return results


def check_ssl(url):
    """
    Checks if the website is using a valid SSL certificate.
    """
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        return "SSL Check -> Rank(0) -> Action: Invalid URL -> To do: Please provide a valid URL."

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    return f"SSL Connection -> Rank(10) -> Action: Nothing to do -> To do: Your SSL setup is secure."
    except Exception as e:
        return f"SSL Connection -> Rank(0) -> Action: Immediate action required -> To do: Install or fix your SSL certificate. ({str(e)})"


def main():
    print("--- ညီမလေးရဲ့ Educational Security Checker ---")

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(
            "စမ်းသပ်ချင်တဲ့ URL ကို ရိုက်ထည့်ပေးပါ (e.g., https://google.com): ")

    if not target.startswith("http"):
        print("Error: URL must start with http:// or https://")
        return

    print(f"\nScanning: {target}...\n")

    print("1. Security Headers Analysis:")
    header_results = check_security_headers(target)
    for res in header_results:
        print(f" - {res}")

    print("\n2. SSL/TLS Status:")
    ssl_result = check_ssl(target)
    print(f" - {ssl_result}")


if __name__ == "__main__":
    main()
