import requests
from bs4 import BeautifulSoup as bs
from .paralel_requests import multiURLFetcher
import logging

log = logging.getLogger(__name__)

base_url = "https://www.vpnjantit.com"
countries_path = "/free-wireguard"


def get_countries():
    log.info("Fetching countries")
    response = requests.get(f"{base_url}{countries_path}")
    soup = bs(response.text, "html.parser")
    countries_a = soup.find_all("a", class_="btn btn-primary py-3")
    countries = [
        {
            "name": country.text.replace("WireGuard", "").strip(),
            "url": base_url + "/" + country["href"],
        }
        for country in countries_a
    ]
    countries = sorted(countries, key=lambda x: x["name"])
    for i, country in enumerate(countries):
        country["id"] = i + 1
    return countries


async def get_servers(country_url):
    servers = []
    urls = []
    response = requests.get(country_url)
    soup = bs(response.text, "html.parser")
    servers_div = soup.find_all("div", class_="block-7 text-center services border")
    servers = []
    for v in servers_div:
        vp = {}
        name = v.find_all("font")[0].text.replace("FREE", "").strip()
        aviable = v.find_all("font")[1].text
        activeDays = v.find("ul").find_all("li")[4].contents[0][7]
        ip = v.find("ul").find_all("li")[1].contents[0]
        try:
            link = v.find("a", class_="btn btn-primary d-block px-3 py-3 mb-4")["href"]
        except:
            continue
        vp["name"] = name
        vp["aviable"] = aviable
        vp["activeDays"] = int(activeDays)
        vp["link"] = base_url + link
        vp["ip"] = ip.strip()
        # vp["speed"] = float(speed)
        servers.append(vp)
        urls.append(base_url + link)

    # responses = asyncio.get_event_loop().run_until_complete(main(urls))
    responses = await multiURLFetcher([server["link"] for server in servers])

    for r in responses:
        sp = bs(r, "html.parser")
        div = sp.find_all("div", class_="media block-6 services border text-left")
        speed = div[1].find_all("h5")[5].text
        speed = speed.replace("Mbit/s", "").strip()
        ip_ = div[1].find("input")["value"].strip()
        for server in servers:
            if server["ip"] == ip_:
                server["speed"] = float(speed)
                break
    # print(servers)
    servers = sorted(servers, key=lambda x: x["speed"], reverse=True)
    return servers
