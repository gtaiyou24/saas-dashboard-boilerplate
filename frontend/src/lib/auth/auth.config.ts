import type {NextAuthConfig, User} from "next-auth";
import Credentials from "next-auth/providers/credentials";
import {apiAuthPrefix, authRoutes, DEFAULT_LOGIN_REDIRECT, publicRoutes} from "@/route";
import {getMe, logout, postAuthToken} from "../api";

export default {
    providers: [
        Credentials({
            credentials: {
                email: { label: "メールアドレス", type: "email" },
                password: { label: "パスワード", type: "password" },
            },
            async authorize(credentials) {
                try {
                    const tokenSet = await postAuthToken(
                        credentials.email as string,
                        credentials.password as string
                    );
                    const user = await getMe(tokenSet.access_token);
                    return {
                        user: {
                            name: user.username,
                            email: user.emailAddress,
                            tenants: user.tenants,
                            accounts: user.accounts
                        },
                        accessToken: tokenSet.access_token,
                        refreshToken: tokenSet.refresh_token,
                        expiresAt: tokenSet.expires_at
                    } as User;
                } catch (e) {
                    return null;
                }
            },
        }),
    ],
    secret: process.env.AUTH_SECRET,
    pages: {
        signIn: '/auth/login',
        error: '/auth/error'
    },
    events: {
        async signOut() {
            await logout();
        }
    },
    callbacks: {
        authorized({ request, auth }) {
            // ログイン / 未ログイン時の画面遷移を制御する

            const { nextUrl } = request;
            const isLoggedIn = !!auth;

            const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix);
            const isPublicRoute = publicRoutes.includes(nextUrl.pathname);
            const isAuthRoute = authRoutes.includes(nextUrl.pathname);

            if (isApiAuthRoute) {
                // /api/auth は未認証でもアクセス可能
                return true;
            }

            if (isAuthRoute) {
                if (isLoggedIn) {
                    // すでにログイン済みの場合は、リダイレクトさせる
                    return Response.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl));
                }

                // 未ログインで認証ページの場合は、アクセス可能
                return true;
            }

            return isPublicRoute || isLoggedIn;
        },
        async jwt({ token, user, trigger, session }) {
            // 初回ログイン時のみ user が渡される
            if (user) {
                // 初回ログイン時
                token.user = user.user
                token.currentProject = { tenantId: user.user.tenants[0]?.id, projectId: undefined };
                token.accessToken = user.accessToken;
                token.refreshToken = user.refreshToken;
                token.expiresAt = user.expiresAt;
                return token;
            }
            if (trigger === "update" && session) {
                // update(); 実行時にセッションを更新する
                token.user = session.user;
                token.currentProject = session.currentProject;
            }
            return token;
        },
        async session({ session, token }) {
            if (token?.accessToken) {
                session.accessToken = token.accessToken;
                session.refreshToken = token.refreshToken;
                session.expiresAt = token.expiresAt;
            }
            if (token?.user || token?.currentProject) {
                session.user = token.user as any;
                session.currentProject = token.currentProject as any;
            }
            return session;
        },
    }
} satisfies NextAuthConfig;