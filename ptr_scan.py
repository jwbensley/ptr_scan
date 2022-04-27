#!/usr/bin/env python3

import pprint
import re

in_file = "ipv4data_short"
inc_file = "include_data.txt"
exc_file = "exclude_data.txt"
unm_file = "unmatched_data.txt"
skip_file = "skipped_data.txt"


inc_regex = {
    # Interface names
    ".*1g": 0,
    ".*10g": 0,
    ".*25g": 0,
    ".*40g": 0,
    ".*50g": 0,
    ".*100g": 0,
    ".*400g": 0,
    ".*ae-?[0-9]": 0,
    "(.*as[0-9]+|^[0-9]+)": 0,
    ".*be-?[0-9]": 0,
    ".*bundle-?eth": 0,
    "^de-?cix": 0,
    ".*et?h?-?[0-9]": 0,
    "^eqix": 0,
    "(^|.*\.)f-?[0-9]": 0,
    ",*fourhundred": 0,
    ".*gi?g?-?[0-9]": 0,
    ".*gigabit": 0,
    ".*hu-?[0-9]": 0,
    ".*hundred": 0,
    ".*if-ae-?": 0,
    ".*if-be-?": 0,
    ".*if-et-?": 0,
    ".*if-xe-?": 0,
    ".*int-?[0-9]": 0,
    ".*irb-?[0-9]": 0,
    ".*lag-?[0-9]": 0,
    ".*-link": 0,
    ".*loo?p?-?[0-9]": 0,
    ".*po-?[0-9]": 0,
    ".*port-channel-?[0-9]": 0,
    ".*ten?g?i?g?a?-?[0-9]?": 0,
    ".*trunk-?[0-9]?": 0,
    ".*tun?-?[0-9]": 0,
    ".*tunnel-?[0-9]": 0,
    "(^|.*\.)v[0-9]": 0,
    ".*ve-?[0-9]": 0,
    ".*vla?n?-?[0-9]": 0,
    ".*xe-?[0-9]": 0,
    # Device names
    "(^|.*\.|.*\-)agg-?[0-9]": 0,
    ".*bar[0-9]": 0,
    "(^|.*\.|.*\-)bb-?[0-9]?": 0,
    "[a-z0-9]+bb[0-9]+": 0,
    "(^|.*\.|.*\-)boarder-?[0-9]": 0,
    "(^|.*\.|.*\-)br-?[0-9]": 0,
    "(^|.*\.|.*\-)cr-?[0-9]": 0,
    "[0-9a-z]+crs\.": 0,
    "(^|.*\.|.*\-)core-?[0-9]?\.": 0,
    "(^|.*\.|.*\-)ear-?[0-9]": 0,
    "(^|.*\.|.*\-)gw-?[0-9]?": 0,
    "[a-z0-9]+ip[0-9]+": 0,
    ".*mx-?(10k|240|480|960)": 0,
    ".*juniper": 0,
    ".*router-?[0-9a-z]+\.": 0,
    ".*router-?\.": 0,
    "(^|.*\.|.*\-|^[a-z0-9]+)rt?r?-?[0-9]": 0,
}

exc_regex = {
    ".*FAIL\.": 0,
    ".*([0-9a-f]{1,4}(\-|\.)){7}[0-9a-f]{1,4}": 0,
    ".*([0-9]{1,4}(\-|\.)){3}[0-9]{1,4}": 0,
    "ah-ipv6": 0,
    "^autodiscover": 0,
    "^cpc.*cable\.virginm\.net": 0,
    "cpepool.*\.sanbrunocable\.com": 0,
    "^customer.*starlinkisp\.net": 0,
    "customer-static-.*\.iplannetworks\.net": 0,
    "dial-.*\.pool\.broadband44\.net": 0,
    ".*dns-?[0-9]": 0,
    "^dsl.*\.dsl\.speakeasy\.net": 0,
    ".*\.dyn\.optonline\.net": 0,
    "dyn.*\.pppoe\.tmb\.ru": 0,
    ".*\.dynamic\.bellmts\.net": 0,
    ".*\.dynamic\.kabel-deutschland\.de": 0,
    ".*\.dynamic\.medianet-world\.de": 0,
    ".*\.dynamic\.siol\.net": 0,
    "dynamic-cpe-pool\.orcon\.net\.nz": 0,
    "dynamic-ip.*\.cable\.net\.co": 0,
    "^ftip.*bt\.net": 0,
    "^host": 0,
    ".*\.in-addr.arpa": 0,
    ".*\.ip4\.static\.sl-reverse\.com": 0,
    "^ip[0-9]{1,3}\.ip.*\.(eu|us)": 0,
    "ip-address-pool-xxx\.fpt\.vn": 0,
    "js-ipv6": 0,
    "localhost.*": 0,
    "^mail[0-9]?\.": 0,
    "^p.*\.dip0\.t-ipconnect\.de": 0,
    ".*\.pool.*\.cwpanama\.net": 0,
    ".*\.pool\.baden\.net": 0,
    ".*\.pool\.tripleplugandplay\.com": 0,
    ".*\.ppp\.asahi-net\.or\.jp": 0,
    "pool.*\.unicom\.nat\.upenn\.edu": 0,
    "pool.*\.ptcomm\.ru": 0,
    "pool\.giga\.net\.ru": 0,
    "ppp.*\.access\.hol\.gr": 0,
    ".*\.ppp\.asahi-net\.or\.jp": 0,
    "rev-.*\.isp1\.alsatis\.net": 0,
    ".*\.skybroadband\.com": 0,
    "neu6\.edu\.cn": 0,
    ".*unassigned.*": 0,
    "static\.amc\.com\.ar": 0,
    "static\.cmcti\.vn": 0,
    "static\.kpn\.net": 0,
    "static\.rcn\.com": 0,
    "static\.reserve\.wtt\.net\.hk": 0,
    "static\.netnam\.vn": 0,
    "static\.velo\.net\.id": 0,
    "static\.vnpt\.vn": 0,
    "static\.vnpt-hanoi\.com\.vn": 0,
    "static.*\.itcsa\.net": 0,
    "static-.*\.gigacable.com.mx": 0,
    "static-.*\.poda\.cz": 0,
    "static-.*\.unet\.cz": 0,
    "static-broadband*\.gorge\.net": 0,
    "static-ip-.*\.cable\.net\.co": 0,
    "static-pool.*\.flagman\.zp\.ua": 0,
    ".*\.static\.movinet\.com\.uy": 0,
    ".*\.static\.123\.net": 0,
    ".*\.static\.kabel-deutschland\.de": 0,
    ".*\.static.ziggozakelijk.nl": 0,
    "undefined\.hostname\.localhost": 0,
    ".*uknown.*": 0,
    "[0-9a-f]{8}\.virtua\.com\.br": 0,
    "vmi.*\.contaboserver\.net": 0,
    ".*vps-?[0-9]": 0,
    "vnpt\.vn": 0,
    ".*\.wlan\.uni-bremen\.de": 0,
}

inc = open(inc_file, "w")
exc = open(exc_file, "w")
unm = open(unm_file, "w")
skip = open(skip_file, "w")

lines = 0
skipped = 0
excludes = 0
includes = 0
unmatched = 0

for line in open(in_file):
    vals = line.split()
    if len(vals) == 3:
        ptr = vals[2].strip()
    else:
        lines += 1
        skipped += 1
        skip.write(line)
        continue
    for regex in exc_regex:
        if re.match(regex, ptr):
            excludes += 1
            exc_regex[regex] += 1
            exc.write(ptr + "\n")
            break
    else:
        for regex in inc_regex:
            if re.match(regex, ptr):
                includes += 1
                inc_regex[regex] += 1
                inc.write(ptr + "\n")
                break
        else:
            unmatched += 1
            unm.write(ptr + "\n")
    lines += 1

inc.close()
exc.close()
unm.close()
skip.close()

print(
    f"Parsed {lines} lines\n"
    f"Excluded {excludes} lines\n"
    f"Included {includes} lines\n"
    f"Total excluded+included: {excludes+includes}\n"
    f"Unmatched {unmatched} lines\n"
    f"Skipped {skipped} lines\n"
    f"Remainder: {lines - (excludes + includes + unmatched)}\n"
)
print("Included by count:")
pprint.pprint(inc_regex)
print("Excluded by count:")
pprint.pprint(exc_regex)
