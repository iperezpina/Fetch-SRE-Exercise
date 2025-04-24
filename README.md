# Fetch-SRE-Exercise
Part of Fetch's SRE Take Home Assessment for job application.

## Overview

This project monitors the availability of HTTP endpoints using a YAML configuration file and performs health checks every 15 seconds, logs uptime by domain, and follows all the reliability and formatting rules required by spec sheet.


## How to use:

git clone https://github.com/iperezpina/Fetch-SRE-Exercise.git  
cd sre-take-home  
pip install -r req.txt  # only needs PyYAML and requests to import  



## Changes:
### Defaulted the method to GET
If method wasn’t in the YAML, the code originally threw an error. I added a fallback to "GET" to make sure it still works — the prompt says that's the expected default.

### Parsed the body string into a real JSON object
The body field comes in as a JSON string, but requests expects a dict when using json=. I added logic to parse it properly before sending.

### Measured how long each request takes
I used time.perf_counter() to time the request and made sure we only count the endpoint as UP if it responds in under 500ms, like the prompt asked for.

### Caught network-related errors
Wrapped the whole request in a try/except block using requests.RequestException. This prevents the whole script from crashing if an endpoint is down or flaky.

### Cleaned up domain parsing
Instead of doing string splits to get the domain (which could include ports), I used urlparse().hostname to get just the domain. Keeps things clean and accurate.

### Dropped decimals in availability percentages
Used int() instead of round() to drop anything after the decimal point, exactly as requested in the spec.

### Locked in the 15-second check window
The original script just slept for 15 seconds after each cycle, which could drift over time depending on how long the checks took. I fixed that so it always runs every 15 seconds, no matter how many endpoints there are.

### Cleaned up logs and output
I updated the print statements to make them easier to read and more consistent. Just helps with debugging and seeing what’s going on.

### Gave the functions better names and structure
Made everything a little cleaner and easier to follow. If someone else needs to read or extend it later, they won’t hate me.