import {z} from "zod";

const Schema = z.object({
    username: z.string().min(1, {
       message: "ユーザー名を入力してください。"
    }),
    email: z.string().email({
        message: "メールアドレスを入力してください。",
    }),
    password: z.string().min(4, {
        message: "パスワードは4文字以上を入力してください。",
    })
});

export default Schema;