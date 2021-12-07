#!/bin/bash

FREQURENCY=300
WEBHOOK_URL=""

checkStock() {
    curl -s 'https://inv.mp.microsoft.com/v2.0/inventory/SG'\
    -H 'authority: inv.mp.microsoft.com' \
    -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"' \
    -H 'accept: */*' \
    -H 'content-type: application/json' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36' \
    -H 'sec-ch-ua-platform: "macOS"' \
    -H 'origin: https://www.microsoft.com' \
    -H 'sec-fetch-site: same-site' \
    -H 'sec-fetch-mode: cors' \
    -H 'sec-fetch-dest: empty' \
    -H 'referer: https://www.microsoft.com/' \
    -H 'accept-language: en-SG,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6,zh-TW;q=0.5,de;q=0.4' \
    --data-raw '[{"skuId":"RRT-00018","distributorId":"9000000013"}]' \
    | grep "\"inStock\":\"True\"" && curl \
        -H "Content-Type: application/json" \
        -d '{"username": "Microsoft Store (SG)", "content": "Xbox is in stock, go get it now! https://www.microsoft.com/en-sg/store/configure/Xbox-Series-S/8WJ714N3RBTL"}' \
        $WEBHOOK_URL
}

while true
do
    date
    checkStock
    echo "-----------------------------------------------------------------------------------------------"
    sleep $FREQURENCY
done