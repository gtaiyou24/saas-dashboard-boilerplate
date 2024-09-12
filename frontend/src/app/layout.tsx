import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import {clsx} from "clsx";
import Footer from "@/components/layout/footer";
import {Toaster} from "@/components/ui/toaster";
import Provider from "@/components/provider";
import {APP_NAME, BASE_URL} from "@/lib/constants";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL(BASE_URL),
  title: {
    default: `${APP_NAME} | チャット形式で誰でも簡単にデータ分析ができる AI`,
    template: `%s | ${APP_NAME}`
  },
  description: `${APP_NAME}はチャット形式で誰でも簡単にデータ分析できる AI サービスです`,
  applicationName: APP_NAME,
  alternates: {
    canonical: BASE_URL
  },
  icons: {
    apple: [
      {
        media: '(prefers-color-scheme: light)',
        url: '/favicon/light/apple-touch-icon.png',
        href: '/favicon/light/apple-touch-icon.png',
      },
      {
        media: '(prefers-color-scheme: dark)',
        url: '/favicon/dark/apple-touch-icon.png',
        href: '/favicon/dark/apple-touch-icon.png',
      },
    ],
    icon: [
      {
        media: '(prefers-color-scheme: light)',
        type: 'image/png',
        url: '/favicon/light/favicon-32x32.png',
        href: '/favicon/light/favicon-32x32.png',
      },
      {
        media: '(prefers-color-scheme: dark)',
        type: 'image/png',
        url: '/favicon/dark/favicon-32x32.png',
        href: '/favicon/dark/favicon-32x32.png',
      },
    ]
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className={clsx(inter.className, 'flex min-h-screen w-full flex-col')}>
        <Provider>
          <main className="flex-grow">
            {children}
          </main>
          <Toaster />
        </Provider>
      </body>
    </html>
  );
}
