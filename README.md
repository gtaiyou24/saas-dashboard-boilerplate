<h1 align="center">SaaS Dashboard</h1>

<div align="center">
  <a href="https://github.com/gtaiyou24/saas-dashboard-nextjs-fastapi/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/gtaiyou24/saas-dashboard-nextjs-fastapi/workflows/Test/badge.svg" alt="Test"></a>
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/gtaiyou24/saas-dashboard-nextjs-fastapi" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/gtaiyou24/saas-dashboard-nextjs-fastapi.svg" alt="Coverage"></a>
</div>

## ❓使い方
<details><summary><b>🏃 起動する</b></summary>

**Step.1** : Create a `.env` file at `./backend` folder.
```bash
cp backend/.env.local backend/.env
```

**Step.2** : Then run `docker-compose up` to start the server.
```bash
docker-compose up --build
```

 - [Front](http://localhost:3000)
 - [Swagger UI](http://localhost:8000/docs)
 - [MailHog](http://0.0.0.0:8025/)

</details>

<details><summary><b>🔌 ローカルDBに接続する</b></summary>

Connect to Redis
```bash
redis-cli
```

Connect to MySQL
```bash
mysql -h 127.0.0.1 -P 3306 -u user -p
# Enter password: pass
```

</details>

<details><summary><b>🛠️ OpenAPI から TypeScript のクライアントコードを生成する</b></summary>

```bash
cd frontend
npm run generate-client
```

Appendix

 - [openapi-typescript | OpenAPI TypeScript](https://openapi-ts.pages.dev/introduction)

</details>

<details><summary><b>✅ テストを実行する</b></summary>

```bash
pip install pytest pytest-env httpx
pytest -v ./test
```

</details>

---
## 🛠️ 技術スタック
### ⚡️ バックエンド

 - ⚙️ 開発言語: Python
 - ⚡️ フレームワーク: [FastAPI](https://fastapi.tiangolo.com/)
 - 🧰 ライブラリ: [SQLAlchemy](https://www.sqlalchemy.org/) / [PyTest](https://docs.pytest.org/en/stable/)
 - 💾 DB: MySQL / Redis
 - 🚀 CI: GitHub Ations

### 🚀 フロントエンド

 - ⚙️ 開発言語: TypeScript
 - ⚡️ フレームワーク: Next.js App Router
 - 🧰 ライブラリ: Auth.js(NextAuth V5)
 - 🎨 CSS: Tailwind / shadcn/ui / Headless UI
 - 🚀 CI: GitHub Ations

### ☁️ インフラ

 - ☁️ クラウドサービス: GCP Cloud Run / Neon / Upstash
 - 🚀 IaC: Terraform
 - 🐋 DevOps: [Docker Compose](https://www.docker.com)
 - 👀 エラー/ログ監視ツール: Sentry / New Relic
 - ✉️ メールサービス: Gmail

---

## 📋機能
### 🔐ユーザー認証


