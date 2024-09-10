# 🛠️ システムアーキテクチャ

 - フロントエンド / API Gateway / バックエンドの構成
 - 今後は、BFFを追加する想定
 - マイクロサービス化への転用も可能

## 📝 モジュラモノリス構成

```mermaid
architecture-beta
    group api(cloud)[API]

    service db(database)[Database] in api
    service disk1(disk)[Storage] in api
    service disk2(disk)[Storage] in api
    service server(server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
```

## 📝️ マイクロサービス構成
WIP
