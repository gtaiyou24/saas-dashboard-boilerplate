import {Field, ChatMessage, ChatResponse} from "@/lib/types";

export async function chatCompletion(messages: ChatMessage[], metas: Field[]): Promise<ChatResponse> {
    const url = `/api/analytics`;
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            messages,
            metas
        }),
    });
    const result = (await res.json()) as {
        data: ChatResponse;
        success: boolean;
        message?: string;
    };
    if (result.success) {
        return result.data;
    } else {
        throw new Error(result.message ?? "Unknown error");
    }
}
