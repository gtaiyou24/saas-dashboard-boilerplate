"use server";

import {postVerifyEmail} from "../../../lib/api";

export const newVerification = async (token: string): Promise<{success?: string; error?: string;}> => {
    try {
        await postVerifyEmail(token);
    } catch (e) {
        return { error: "メールアドレスの確認に失敗しました。ログインして再送信してください。" };
    }
    return { success: "メールアドレスの確認が完了しました！" };
};
