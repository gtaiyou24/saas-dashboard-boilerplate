"use client";

import {useCallback, useState} from "react";
import {PaperAirplaneIcon, TrashIcon} from "@heroicons/react/20/solid";
import {Spinner} from "@radix-ui/themes";
import {Button} from "@/components/ui/button";


export default function PromptForm({
    onSubmit,
    onClear
}: {
    onSubmit: (message: string) => void;
    onClear: () => void;
}) {
    const [userMessage, setUserMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const clearChat = useCallback(() => onClear(), []);
    const startQuery = useCallback(() => {
        setLoading(true);
        onSubmit(userMessage);
        setLoading(false);
        setUserMessage("");
    }, [userMessage]);

    return (
        <div className="right-0 py-8 flex">
            <button
                type="button"
                className="flex items-center grow-0 rounded-l-md border border-gray-300 dark:border-gray-500 px-2.5 py-1.5 text-sm text-gray-500 dark:text-gray-500 shadow-sm hover:bg-gray-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading}
                onClick={clearChat}
            >
                Clear
                {!loading && <TrashIcon className="w-4 ml-1" />}
            </button>
            <input
                type="text"
                className="block w-full border-0 px-2.5 py-1.5 text-gray-900 dark:text-gray-50 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-500 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-900"
                placeholder="データセットから何を可視化したいですか？"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter" && !loading && userMessage.length > 0) {
                        startQuery();
                    }
                }}
            />
            <Button className="rounded-l-none" disabled={loading || userMessage.length === 0} onClick={startQuery}>
                {!loading && (
                    <PaperAirplaneIcon className="w-4 ml-1" />
                )}
                {loading && <Spinner />}
            </Button>
        </div>
    );
}