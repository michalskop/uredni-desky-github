"""Download Gazettes."""

# Stáhne aktuální úřední desky

from calendar import c
import requests
import sys

# URL of gazettes
# URL adresy úředních desek
gazettes = {
    "Test": "https://raw.githubusercontent.com/michalskop/uredni-deska-test/main/uredni-deska-test.json",
    "Kadaň": "https://www.mesto-kadan.cz/1ad1f16beff952576ae7ddd76a91e163"
}

# Download gazettes and save them
# Stáhne úřední desky a uloží je
# We use a simple heurystic approach later on to determine the newest piece of information
last_info = []

for name, url in gazettes.items():
    # download gazette
    r = requests.get(url)

    # if download failed
    if r.status_code != 200:
        print("Error {}".format(r.status_code))
        continue
    # save gazette
    with open("data/" + name + ".json", "w") as f:
        f.write(r.text)
    
    # get last info
    try:
        info = r.json()["informace"]
        info.sort(key=lambda x: x["vyvěšení"]["datum"], reverse=True)
        last_info.append({
            "name": name,
            "url": info[0]["url"],
            "title": info[0]["název"]["cs"],
            "date": info[0]["vyvěšení"]["datum"]
        })
    except:
        continue

# a simple heurystic approach to determine the newest piece of information
last_info.sort(key=lambda x: x["date"], reverse=True)

# output info about the newest piece of information
# výstup informací o nejnovějším oznámení
try:
    sys.stdout.write(name + ": " + last_info[0]["title"] + " ( " + last_info[0]["url"] + " )")
except:
    sys.stdout.write("Error")