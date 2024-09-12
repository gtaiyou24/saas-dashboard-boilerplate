import {auth} from "@/lib/auth";
import {createApiClient} from "@/lib/api/create-client";
import {components} from "@/lib/api/type";
import {TokenSet} from "next-auth";
import {ChatMessage, Dataset, DSItem, Field, Member, Project, Row, SemanticType, Tenant, User} from "@/lib/types";
import {TAGS} from "@/lib/constants";


export const postRegisterUser = async (username: string, email: string, password: string) =>  {
    const {error} = await createApiClient().POST("/auth/register", {
        cache: "no-cache",
        body: {
            username: username,
            email_address: email,
            password: password
        }
    });
    if (error) {
        console.log(error);
        throw Error('ユーザー登録に失敗しました。');
    }
}

export const postVerifyEmail = async (token: string): Promise<TokenSet> => {
    const { data, error } = await createApiClient().POST("/auth/verify-email/{token}", {
        headers: { 'Content-Type': 'application/json' },
        params: { path: { token: token } },
    })
    if (error) {
        throw Error();
    }
    return data as TokenSet;
}

export const postAuthToken = async (email: string, password: string): Promise<TokenSet>=> {
    const {data, error} = await createApiClient().POST("/auth/token", {
        cache: "no-cache",
        body: {
            email_address: email,
            password: password
        }
    });
    if (error?.type) {
        switch (error.type) {
            case 'USER_IS_NOT_VERIFIED':
                throw '確認メールを送信しました。メールをご確認してください。';
            case 'LOGIN_BAD_CREDENTIALS':
                throw 'メールアドレスまたはパスワードが間違っています';
            default:
                throw 'システムエラーが発生しました。しばらくお待ちください。';
        }
    }
    return data as TokenSet;
}

export const putAuthToken = async (token?: string): Promise<TokenSet> => {
    const {data, error} = await createApiClient().PUT("/auth/token", {
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `bearer ${token ? token : (await auth())?.refreshToken}`
        },
        cache: "no-cache",
    });
    if (error) {
        console.error(`トークンのリフレッシュに失敗しました。${error}`);
    }
    return data as TokenSet;
};

export async function postForgotPassword(email: string) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email_address: email
        })
    });
    if (res.status !== 200) {
        const errorJson = await res.json();
        switch (errorJson.type) {
            case 'USER_DOES_NOT_EXISTS':
                return 'メールアドレスが存在しません。';
            default:
                return 'システムエラーが発生しました。しばらくお待ちください。';
        }
    }
}


export async function postResetPassword(password: string, token: string) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            password: password,
            token: token
        })
    });
    if (res.status !== 200) {
        const errorJson = await res.json();
        switch (errorJson.type) {
            case 'VALID_TOKEN_DOES_NOT_EXISTS':
                return 'トークンの検証に失敗しました。トークンが存在しない、もしくは有効期限が切れています。';
            default:
                return 'システムエラーが発生しました。しばらくお待ちください。';
        }
    }
}


export const logout = async (token?: string) => {
    const { error } = await createApiClient().DELETE("/auth/token", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        cache: 'no-cache'
    });
    if (error) {
        console.error(error);
    }
}


export const getMe = async (token?: string): Promise<User> => {
    const { data, error } = await createApiClient().GET("/users/me", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        cache: 'no-cache'
    });
    if (error) {
        console.error(error);
    }
    return {
        username: data.username,
        emailAddress: data.email_address,
        tenants: data.tenants.map((tenant: components["schemas"]["Tenant"]) => {
            return {id: tenant.id, name: tenant.name};
        }),
        accounts: data.accounts.map((account: components["schemas"]["Account"]) => {
            return {provider: account.provider, providerAccountId: account.provider_account_id};
        })
    } as User;
}

export const getTenants = async (token?: string): Promise<Tenant[]> => {
    const {data, error} = await createApiClient().GET("/tenants/", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        next: {tags: [TAGS.tenants]},
        cache: 'no-cache'
    });
    if (!data) {
        throw Error("テナントの取得に失敗しました");
    }
    return data.tenants.map((tenant) => {
        return {id: tenant.id, name: tenant.name};
    });
}

export const getProjects = async (tenantId: string, token?: string): Promise<Project[]> => {
    const {data, error} = await createApiClient().GET("/tenants/{tenant_id}/projects", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        params: {path: {tenant_id: tenantId}},
        cache: 'no-cache'
    });
    if (!data) {
        throw Error("プロジェクトの取得に失敗しました");
    }
    return data.projects.map((project) => {
        return {id: project.id, name: project.name};
    });
}

export const getMembers = async (tenantId: string, token?: string): Promise<Member[]> => {
    const {data, error} = await createApiClient().GET("/tenants/{tenant_id}/members", {
        headers: { "Authorization": `bearer ${token ? token : (await auth())?.accessToken}` },
        params: {path: {tenant_id: tenantId}},
        cache: 'no-cache'
    });
    if (!data) {
        throw Error("プロジェクトの取得に失敗しました");
    }
    return data.members.map((member): Member => {
        return {
            userId: member.user_id,
            username: member.username,
            email: member.email_address,
            role: member.role.toLowerCase() as "admin" | "editor" | "reader"
        };
    });
}

export const fetchDateSet = async (messages: ChatMessage[]): Promise<DSItem> => {
    const {data, error} = await createApiClient().POST("/analytics/dataset", {
        headers: { "Content-Type": "application/json" },
        body: { messages: messages },
    });
    if (error) {
        throw Error("データセットの取得に失敗しました");
    }
    return {
        key: '1',
        name: '1',
        dataset: {
            fields: data.fields.map((field) => ({
                fid: field.name,
                name: field.name,
                semanticType: 'nominal'
            })),
            dataSource: data.data_source
        },
        type: "custom"
    };
}