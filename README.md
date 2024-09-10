# SaaS Dashboard
<a href="https://github.com/gtaiyou24/saas-dashboard/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/gtaiyou24/saas-dashboard/workflows/Test/badge.svg" alt="Test"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/gtaiyou24/saas-dashboard" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/gtaiyou24/saas-dashboard.svg" alt="Coverage"></a>

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
pytest -v ./backend/test
```

</details>

---
## 🛠️ 技術スタック
### 🔨 バックエンド

 - ⚙️ 開発言語: Python
 - ⚡️ フレームワーク: [FastAPI](https://fastapi.tiangolo.com/)
 - ✍️ 設計手法: [DDD(ドメイン駆動設計)](https://amzn.to/4gjk6AQ)
 - 🧰 ライブラリ:
   - 🗄 [SQLAlchemy](https://www.sqlalchemy.org/) : Python SQL DataBase interactions (ORM).
   - ✅ [PyTest](https://docs.pytest.org/en/stable/) : Python test.
   - 🖊️ [slf4py](https://pypi.org/project/slf4py/) : Logging.
   - 🔀 [di4injector](https://pypi.org/project/di4injector/) : DI injection.
 - 🗄️ DB: MySQL / Redis
 - 🔌 クライアント連携: GraphQL
 - 🚀 CI: [GitHub Actions](https://docs.github.com/ja/actions)
 - 📃 Doc: Markdown / [Mermaid](https://mermaid.js.org/)

### 🔧 フロントエンド

 - ⚙️ 開発言語: TypeScript
 - ⚡️ フレームワーク: [Next.js 14 App Router](https://nextjs.org/docs)
 - 🧰 ライブラリ:
   - 🔐 [Auth.js(NextAuth.js V5)](https://authjs.dev/)
 - 🎨 CSS: [Tailwind](https://tailwindcss.com/) / [shadcn/ui](https://ui.shadcn.com/) / [Headless UI](https://headlessui.com/)
 - 🚀 CI: [GitHub Actions](https://docs.github.com/ja/actions)

### ☁️ インフラ

 - ☁️ クラウドサービス: GCP Cloud Run / [Neon](https://neon.tech/) / [Upstash](https://upstash.com/)
 - 🌍️ IaC: [Terraform](https://www.terraform.io/)
 - 🐋 DevOps: [Docker Compose](https://www.docker.com)
 - 🚨 エラー/ログ監視ツール: [Sentry](https://sentry.io/welcome/) / [New Relic](https://newrelic.com/jp)
 - 📧 メールサービス: Gmail / SendGrid
