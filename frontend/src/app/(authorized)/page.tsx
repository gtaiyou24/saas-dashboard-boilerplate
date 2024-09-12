import Chat from "@/components/chat/chat";
import React from "react";
import CreateDatasetButton from "@/components/chat/create-dataset-button";


export default function HomePage() {
    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between">
                <h1 className="text-2xl font-bold">分析</h1>
                <CreateDatasetButton />
            </div>
            <Chat />
        </div>
    );
}