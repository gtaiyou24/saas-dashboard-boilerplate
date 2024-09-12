import {NextRequest, NextResponse} from "next/server";
import {ChatMessage} from "@/lib/types";
import {fetchDateSet} from "@/lib/api";

export async function POST(req: NextRequest) {
    const { messages } = await req.json() as { messages: ChatMessage[] };
    const dsItem = await fetchDateSet(messages);
    return NextResponse.json({
        status: 200,
        dsItem: dsItem,
    });
}