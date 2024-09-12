import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import {encode, JWT} from "@auth/core/jwt";
import {TokenSet} from "next-auth";
import {RequestCookies} from "next/dist/compiled/@edge-runtime/cookies";
import {ApiError} from "next/dist/server/api-utils";
import {apiAuthPrefix, authRoutes, DEFAULT_LOGIN_REDIRECT, publicRoutes} from "@/route";
import {BASE_URL} from "@/lib/constants";
import {putAuthToken} from "@/lib/api";

async function refreshAccessToken(token: JWT): Promise<JWT> {
    return putAuthToken(token.refreshToken)
        .then((tokenSet: TokenSet) => {
            return {
                ...token,
                accessToken: tokenSet.access_token,
                refreshToken: tokenSet.refresh_token,
                expiresAt: tokenSet.expires_at
            };
        })
        .catch((error) => { throw error });
}

async function getToken(cookies: RequestCookies): Promise<JWT | undefined> {
    // NOTE: @auth/core/jwt の getToken でトークンが取得できないので /api/auth/session からデータを取得している
    return await fetch(
        `${BASE_URL}/api/auth/session`, {
            headers: {"Content-Type": "application/json", "Cookie": cookies.toString()},
            cache: "no-cache"
        })
        .then((res) => res.json())
        .catch((error) => {
            console.error(error);
            return undefined;
        });
}

const bufferSeconds = 600;

export async function middleware(request: NextRequest) {
    let response = NextResponse.next({ request });
    const token = await getToken(request.cookies);
    const isLoggedIn = token !== null;
    const { nextUrl } = request;
    const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix);
    const isPublicRoute = publicRoutes.filter((url) => nextUrl.pathname.match(url)).length > 0;
    const isAuthRoute = authRoutes.includes(nextUrl.pathname);

    const isTokenExpired = token?.expiresAt !== undefined && (Date.now() / 1000) > token.expiresAt - bufferSeconds;
    if (isTokenExpired) {
        // セッションを更新
        try {
            console.log(`refresh token ... ${nextUrl}`);
            const newSessionToken = await encode({
                salt: process.env.AUTH_SESSION_COOKIE_NAME!,
                secret: process.env.AUTH_SECRET!,
                token: await refreshAccessToken(token)
            });
            // 新しいセッションをクッキーにセット
            request.cookies.set(process.env.AUTH_SESSION_COOKIE_NAME!, newSessionToken);
            response = NextResponse.next({request: { headers: request.headers }});
            response.cookies.set({
                name: process.env.AUTH_SESSION_COOKIE_NAME!,
                value: newSessionToken,
                httpOnly: true,
                secure: process.env.NODE_ENV === "production",
                path: "/"
            });
        } catch (e) {
            if (e instanceof ApiError) {
                switch (e.statusCode) {
                    case 400:
                        console.info("リフレッシュトークンが無効なので強制ログアウトします");
                        request.cookies.delete(process.env.AUTH_SESSION_COOKIE_NAME!);
                        return NextResponse.next({request: {headers: request.headers}});
                }
            }
            console.error(e);
        }
    }

    if (isApiAuthRoute || isPublicRoute) {
        // /api/auth or 公開ページはアクセス可能
        return response;
    }

    if (isAuthRoute) {
        if (isLoggedIn) {
            // すでにログイン済みの場合は、リダイレクトさせる
            return Response.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl));
        }
        // 未ログインで認証ページの場合は、アクセス可能
        return response;
    }

    // 以降はログインが必要なページ
    if (isLoggedIn) {
        // ログイン済みの場合はアクセス可能
        return response;
    }

    // 以降はログインが必要なページなのでログイン画面へ遷移させる
    const url = new URL("/auth/login", nextUrl)
    url.searchParams.append("callbackUrl", nextUrl.pathname)
    return Response.redirect(url);
}

export const config = {
    matcher: [
        // "/((?!.+\\.[\\w]+$|_next).*)",
        // "/",
        // "/(api|trpc)(.*)",
        {
            /*
             * Match all request paths except for the ones starting with:
             * - api (API routes)
             * - _next/static (static files)
             * - _next/image (image optimization files)
             * - favicon.ico (favicon file)
             * Feel free to modify this pattern to include more paths.
             */
            source: '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
            // <Link>を使用していると、prefetchが行われるため、リストページなどでは大量にmiddlewareが実行される。
            // そのため、preFetchでは発火しないようにします
            missing: [
                { type: "header", key: "next-router-prefetch" },
                { type: "header", key: "purpose", value: "prefetch" },
            ],
        },
    ],
}