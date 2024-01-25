# json
## ./data/installed_packges.json
|Value|描述|
|-------|-------|
|"version"|json版本|
|"last_check_date"|datetime.datetime.now().strftime('%Y-%m-%d')所获取的字符串，上次检查更新时间|
|data|数据|
*此为json最外层*

|data元组|描述|
|-------|-------|
|"packge_name"|插件包名|
|"check_url"|检查更新地址|
|"init_name"|文件根目录|