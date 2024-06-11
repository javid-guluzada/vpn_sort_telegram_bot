import requests
from bs4 import BeautifulSoup

base_url = "https://www.vpnjantit.com/"
countries_path = "free-wireguard"


def get_countries():
    countries = []
    response = requests.get(f"{base_url}{countries_path}")
    soup = BeautifulSoup(response.text, "html.parser")
    countries_a = soup.find_all("a", class_="btn btn-primary py-3")
    for country in countries_a:
        countries.append(
            {
                "name": country.text.replace("WireGuard", "").strip().replace(" ", "_"),
                "url": base_url + country["href"],
            }
        )
    return countries


def get_servers(country_url):
    servers = []
    response = requests.get(country_url)
    soup = BeautifulSoup(response.text, "html.parser")
    servers_div = soup.find_all("div", class_="block-7 text-center services border")
    servers = []
    for v in servers_div:
        vp = {}
        name = v.find_all("font")[0].text
        aviable = v.find_all("font")[0].text
        activeDays = v.find("ul").find_all("li")[4].contents[0][7]

        link = v.find("a", class_="btn btn-primary d-block px-3 py-3 mb-4")["href"]
        r = requests.get(base_url + link)
        s = BeautifulSoup(r.text, "html.parser")
        div = s.find_all("div", class_="media block-6 services border text-left")
        speed = div[1].find_all("h5")[5].text
        speed = speed.replace("Mbit/s", "").strip()
        vp["name"] = name
        vp["aviable"] = aviable
        vp["activeDays"] = activeDays
        vp["link"] = base_url + link
        vp["speed"] = float(speed)
        servers.append(vp)
    servers = sorted(servers, key=lambda x: x["speed"], reverse=True)
    return servers
