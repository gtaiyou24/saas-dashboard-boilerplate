import {ChatMessage, ChatResponse, Field} from "@/lib/types";
import { NextRequest, NextResponse } from 'next/server';


const TEMPERATURE = 0.05;


export async function POST(req: NextRequest) {
    const { messages, metas } = await req.json() as { messages: ChatMessage[], metas: Field[] };
    const systemMessage: ChatMessage = {
        role: "system",
        content: `You are a great assistant at vega-lite visualization creation. No matter what the user ask, you should always response with a valid vega-lite specification in JSON.

            You should create the vega-lite specification based on user's query.

            Besides, Here are some requirements:
            1. Do not contain the key called 'data' in vega-lite specification.
            2. If the user ask many times, you should generate the specification based on the previous context.
            3. You should consider to aggregate the field if it is quantitative and the chart has a mark type of react, bar, line, area or arc.
            4. Consider to use bin for field if it is a chart like heatmap or histogram.
            5. The available fields in the dataset and their types are:
            ${metas
                .map((field) => `${field.name} (${field.semanticType})`)
                .join(", ")}
            `,
    };

    if (messages.length === 0 || metas.length === 0) {
        return NextResponse.json({
            status: 400,
            success: false,
            message: `[error] メッセージまたはメタ情報がありません。`
        });
    }
    if (messages[messages.length - 1].role === "user") {
        messages[messages.length - 1].content = `
        Translate text delimited by triple backticks into vega-lite specification in JSON string.
        \`\`\`
        ${messages[messages.length - 1].content}
        \`\`\`
        `;
        //  If there is no valid vega-lite specification or the instruction is not clear, you can recommend a chart from the given dataset and print in vega-lite JSON string.
    }
    try {
        const data = await getCompletion([systemMessage, ...messages]);
        return NextResponse.json({
            status: 200,
            success: true,
            data: data,
        });
    } catch (error) {
        NextResponse.json({ status: 500, success: false, message: `[error] エラーが発生しました。` });
    }
}

async function getCompletion(messages: ChatMessage[]): Promise<ChatResponse> {
    const url = "https://api.openai.com/v1/chat/completions";
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${process.env.OPENAI_KEY}`
        },
        body: JSON.stringify({
            "model": "gpt-4o-mini",
            messages: messages,
            temperature: TEMPERATURE,
            n: 1,
        }),
    });

    const data = await response.json();
    return data as ChatResponse;
}