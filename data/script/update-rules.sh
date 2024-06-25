#!/bin/sh
LC_ALL='C'

rm *.txt

wait
echo '创建临时文件夹'
mkdir -p ./tmp/

#添加补充规则
cp ./data/rules/adblock.txt ./tmp/rules01.txt
cp ./data/rules/whitelist.txt ./tmp/allow01.txt

cd tmp

#下载AdguardTeam_DNSFilter
curl https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt > rules001.txt
sed -i '/#/d' rules001.txt

#下载StevenBlack_UnifiedHosts
curl https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts > rules002.txt
sed -i '/0.0.0.0 /!d; s/0\.0\.0\.0 /||/; s/$/\^/' rules002.txt

#下载jdlingyu_ad-wars
curl https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts > rules003.txt
sed -i '/视频/d; /爱奇艺/d; /微信/d; /localhost/d; /127.0.0.1 /{s/127\.0\.0\.1 /||/; s/$/\^/}' rules003.txt

echo '下载规则'
rules=(
  "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt" #TG-Twilight_AWAvenue-Ads-Rule
  "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.adblock" #d3ward_Toolz
  "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh-online.txt" #malware-filter_Malicious-URL-Blocklist
  "https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt" #malware-filter_Phishing URL Blocklist
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt" #AdguardTeam_Base
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt" #AdguardTeam_Chinese
  "https://github.com/AdguardTeam/FiltersRegistry/raw/master/filters/filter_11_Mobile/filter.txt" #AdguardTeam_Mobile
  "https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt" #damengzhu_banad
  "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt" #xinggsf_MV
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_3_Spyware/filter.txt" #AdguardTeam_TrackingProtection
  "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_14_Annoyances/filter.txt" #AdguardTeam_Annoyances
  "https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt" #cjx82630_CJX-Annoyances
  "https://secure.fanboy.co.nz/fanboy-annoyance.txt" #ryanbr_Fanboy-Annoyances
  "https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt" #Noyllopa_NoAppDownload
  "https://easylist.to/easylist/easyprivacy.txt" #EasyList_EasyPrivacy
  "https://easylist-downloads.adblockplus.org/antiadblockfilters.txt" #EasyList_AdblockWarningRemovalList
 )

allow=(
)

for i in "${!rules[@]}" "${!allow[@]}"
do
  curl -m 60 --retry-delay 2 --retry 5 --parallel --parallel-immediate -k -L -C - -o "rules${i}.txt" --connect-timeout 60 -s "${rules[$i]}" |iconv -t utf-8 &
  curl -m 60 --retry-delay 2 --retry 5 --parallel --parallel-immediate -k -L -C - -o "allow${i}.txt" --connect-timeout 60 -s "${allow[$i]}" |iconv -t utf-8 &
done
wait
echo '规则下载完成'

# 添加空格
file="$(ls|sort -u)"
for i in $file; do
  echo -e '\n' >> $i &
done
wait

echo '处理规则中'

cat | sort -n| grep -v -E "^((#.*)|(\s*))$" \
 | grep -v -E "^[0-9f\.:]+\s+(ip6\-)|(localhost|local|loopback)$" \
 | grep -Ev "local.*\.local.*$" \
 | sed s/127.0.0.1/0.0.0.0/g | sed s/::/0.0.0.0/g |grep '0.0.0.0' |grep -Ev '.0.0.0.0 ' | sort \
 |uniq >base-src-hosts.txt &
wait
cat base-src-hosts.txt | grep -Ev '#|\$|@|!|/|\\|\*'\
 | grep -v -E "^((#.*)|(\s*))$" \
 | grep -v -E "^[0-9f\.:]+\s+(ip6\-)|(localhost|loopback)$" \
 | sed 's/127.0.0.1 //' | sed 's/0.0.0.0 //' \
 | sed "s/^/||&/g" |sed "s/$/&^/g"| sed '/^$/d' \
 | grep -v '^#' \
 | sort -n | uniq | awk '!a[$0]++' \
 | grep -E "^((\|\|)\S+\^)" & #Hosts规则转ABP规则

cat | sed '/^$/d' | grep -v '#' \
 | sed "s/^/@@||&/g" | sed "s/$/&^/g"  \
 | sort -n | uniq | awk '!a[$0]++' & #将允许域名转换为ABP规则

cat | sed '/^$/d' | grep -v "#" \
 |sed "s/^/@@||&/g" | sed "s/$/&^/g" | sort -n \
 | uniq | awk '!a[$0]++' & #将允许域名转换为ABP规则

cat | sed '/^$/d' | grep -v "#" \
 |sed "s/^/0.0.0.0 &/g" | sort -n \
 | uniq | awk '!a[$0]++' & #将允许域名转换为ABP规则

cat *.txt | sed '/^$/d' \
 |grep -E "^\/[a-z]([a-z]|\.)*\.$" \
 |sort -u > l.txt &

cat \
 | sed "s/^/||&/g" | sed "s/$/&^/g" &

cat \
 | sed "s/^/0.0.0.0 &/g" &


echo 开始合并

cat rules*.txt \
 |grep -Ev "^((\!)|(\[)).*" \
 | sort -n | uniq | awk '!a[$0]++' > tmp-rules.txt & #处理AdGuard的规则

cat \
 | grep -E "^[(\@\@)|(\|\|)][^\/\^]+\^$" \
 | grep -Ev "([0-9]{1,3}.){3}[0-9]{1,3}" \
 | sort | uniq > ll.txt &
wait


cat *.txt | grep '^@' \
 | sort -n | uniq > tmp-allow.txt & #允许清单处理
wait

cp tmp-allow.txt .././allow.txt
cp tmp-rules.txt .././rules.txt

echo 规则合并完成

# Python 处理重复规则
python .././data/python/rule.py
python .././data/python/filter-dns.py

# Start Add title and date
python .././data/python/title.py


wait
echo '更新成功'

exit
