import {ChatMessage, ChatResponse, DSItem, Field} from "@/lib/types";
import {fetchDateSet} from "@/lib/api";

export default async function chatCompletion(
    messages: ChatMessage[],
    metas: Field[]
): Promise<ChatResponse> {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            messages: messages,
            metas: metas
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

export async function chatDateSet(
    messages: ChatMessage[]
): Promise<DSItem> {
    const {dsItem} = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/dataset`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages: messages })
        })
        .then((value) => {
            return value.json() as Promise<{ dsItem: DSItem }>;
        })
        .catch((reason) => {
            throw new Error(reason.message ?? "Unknown error")
        });
    return dsItem;
}