# 🛠️ システムアーキテクチャ
## 🛠️ フェーズ1 - 3層アーキテクチャ

```mermaid
architecture-beta
    group api(cloud)[cloud]

    service internet(cloud)[Internet]
    service frontend(server)[Frontend] in api
    service backend(server)[Backend] in api
    service db(database)[Database] in api
    service storage(disk)[Storage] in api
    
    junction fromBackend

    internet:R --> L:frontend
    frontend:R --> L:backend
    backend:R -- L:fromBackend
    fromBackend:R --> L:db
    fromBackend:B --> L:storage
```

**AWS**

```mermaid
architecture-beta
    group api(logos:aws-lambda)[API]

    service db(logos:aws-aurora)[Database] in api
    service disk1(logos:aws-glacier)[Storage] in api
    service disk2(logos:aws-s3)[Storage] in api
    service server(logos:aws-ec2)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db
```

**GCP**

WIP

## 🛠️ フェーズ2 - API Gateway アーキテクチャ
モジュラモノリス構成のバックエンドシステムから一部モジュールをマイクロサービス化するフェーズ。 
この場合、最低2つ以上のマイクロサービスが存在するため、フロントエンドは各マイクロサービスエンドポイントの呼び出しを数多く処理する必要があります。 
また、サービスが進化して、新しいマイクロサービスが導入されたり既存のマイクロサービスが変更されたりすると、フロントエンドは膨大な数のエンドポイントを処理するのが大変になります。

したがって、マイクロサービスへ移行するにあたり、フロントエンドとバックエンドの間に間接層の API Gateway を導入するのが良いです。

 - [API ゲートウェイ パターンと、クライアントからマイクロサービスへの直接通信との比較 - .NET | Microsoft Learn](https://learn.microsoft.com/ja-jp/dotnet/architecture/microservices/architect-microservice-container-applications/direct-client-to-microservice-communication-versus-the-api-gateway-pattern)

## 🛠️️ フェーズ3 - マイクロサービスアーキテクチャ

WIP