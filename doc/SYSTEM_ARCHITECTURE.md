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
    service dns(logos:aws-route53)[Route53]
    service cdn(logos:aws-cloudfront)[CloudFront]
    service cert(logos:aws-certificate-manager)[ACM]

    service storage(logos:aws-s3)[S3]

    group vpc(logos:aws-vpc)[VPC]

    service loadbalancer(logos:aws-elb)[ALB] in vpc

    group private_subnet1[Private Subnet 1] in vpc
    service appserver1(logos:aws-ec2)[EC2 Instance 1] in private_subnet1
    service db_primary(logos:aws-aurora)[Aurora Primary] in private_subnet1

    group private_subnet2[Private Subnet 2] in vpc
    service appserver2(logos:aws-ec2)[EC2 Instance 2] in private_subnet2
    service db_replica(logos:aws-aurora)[Aurora Replica] in private_subnet2

    junction asg_junction in vpc
    junction aurora_junction in vpc

    dns:R -- L:cdn
    cdn:R -- L:loadbalancer
    loadbalancer:R -- L:asg_junction
    asg_junction:T -- B:appserver1
    asg_junction:B -- T:appserver2
    appserver1:R -- L:db_primary
    appserver2:R -- L:db_replica
    cdn:T -- B:storage

    db_replica:T -- B:aurora_junction
    aurora_junction:T --> B:db_primary

    cert:B -- T:dns
```

**GCP**

```mermaid
architecture-beta
    group vpc(cloud)[VPC]

    service internet(cloud)[Internet]
    service alb(internet)[Application Load Balancer]
    service frontend(server)[Cloud Run Frontend]
    service backend(server)[Cloud Run Backend]
    service db(database)[Cloud SQL] in vpc
    service cdn(internet)[Cloud CDN]
    service storage(disk)[Cloud Storage]

    internet:T --> L:cdn
    internet:R --> L:alb
    
    cdn:R --> L:storage
    
    alb:R --> L:frontend
    frontend:R --> L:backend

    backend:R -- L:db
    backend:T --> R:storage
```

## 🛠️ フェーズ2 - API Gateway アーキテクチャ
モジュラモノリス構成のバックエンドシステムから一部モジュールをマイクロサービス化するフェーズ。 
この場合、最低2つ以上のマイクロサービスが存在するため、フロントエンドは各マイクロサービスエンドポイントの呼び出しを数多く処理する必要があります。 
また、サービスが進化して、新しいマイクロサービスが導入されたり既存のマイクロサービスが変更されたりすると、フロントエンドは膨大な数のエンドポイントを処理するのが大変になります。

したがって、マイクロサービスへ移行するにあたり、フロントエンドとバックエンドの間に間接層の API Gateway を導入するのが良いです。

 - [API ゲートウェイ パターンと、クライアントからマイクロサービスへの直接通信との比較 - .NET | Microsoft Learn](https://learn.microsoft.com/ja-jp/dotnet/architecture/microservices/architect-microservice-container-applications/direct-client-to-microservice-communication-versus-the-api-gateway-pattern)

## 🛠️️ フェーズ3 - マイクロサービスアーキテクチャ

WIP