"use client";

import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import {PlusCircle} from "lucide-react";
import React, {useEffect, useState} from "react";
import PromptForm from "@/components/chat/prompt-form";
import {ChatMessage, Dataset, DSItem} from "@/lib/types";
import {chatDateSet} from "@/components/chat/chat-completion";
import {toast} from "sonner";
import DataTable from "@/components/data-table/data-table";
import ChatMessages from "@/components/chat/chat-messages";


export default function CreateDatasetButton() {
    const [dataset, setDataset] = useState<Dataset | null>(null);
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
    const onSubmit = (message: string) => {
        const lastMessage: ChatMessage = {role: "user", content: message};

        chatDateSet([...chatMessages, lastMessage])
            .then((dsItem: DSItem) => {
                if (dsItem.type === "custom") {
                    setDataset(dsItem.dataset);
                }
                setChatMessages([...chatMessages, lastMessage]);
            })
            .catch((reason) => toast(reason.message))
    }

    useEffect(() => {
        setDataset(dataset);
    }, [dataset]);

    const deleteMessage = (message: ChatMessage, mIndex: number) => {
        if (message.role === "user") {
            setChatMessages((c) => {
                const newChat = [...c];
                newChat.splice(mIndex, 2);
                return newChat;
            });
        } else if (message.role === 'assistant') {
            setChatMessages((c) => {
                const newChat = [...c];
                newChat.splice(mIndex - 1, 2);
                return newChat;
            });
        }
    }

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button>
                    <PlusCircle className="mr-2 h-4 w-4"/> データセットを作成
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-screen-xl">
                <DialogHeader>
                    <DialogTitle>データセットを作成</DialogTitle>
                </DialogHeader>
                <div className="flex flex-col space-between">
                    {dataset && <DataTable
                        data={dataset.dataSource}
                        metas={dataset.fields}
                        onMetaChange={() => {
                            console.log("meta changed");
                        }}
                    />}
                    <PromptForm
                        onSubmit={onSubmit}
                        onClear={() => setChatMessages([])}/>
                </div>
            </DialogContent>
        </Dialog>
    );
}