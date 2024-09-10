# 🛠️ システムアーキテクチャ

 - フロントエンド / API Gateway / バックエンドの構成
 - 今後は、BFFを追加する想定
 - マイクロサービス化への転用も可能

## 🛠️ Ph.1 - 3層アーキテクチャ

```mermaid
architecture-beta
    group api(cloud)[API]

    service rdb(database)[RDB / KVS] in api
    service kvs(database)[KVS] in api
    service storage(disk)[Storage] in api
    service backend(server)[Backend] in api
    
    junction jct

    backend:R -- L:jct
    jct:R --> L:rdb
    jct:B --> L:storage
```

## 🛠️ Ph.2 - API Gateway アーキテクチャ

 - [API ゲートウェイ パターンと、クライアントからマイクロサービスへの直接通信との比較 - .NET | Microsoft Learn](https://learn.microsoft.com/ja-jp/dotnet/architecture/microservices/architect-microservice-container-applications/direct-client-to-microservice-communication-versus-the-api-gateway-pattern)


## 🛠️️ Ph.3 - マイクロサービスアーキテクチャ
WIP
