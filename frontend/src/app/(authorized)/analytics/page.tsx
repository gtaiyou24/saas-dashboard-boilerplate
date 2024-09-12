import Chat from "@/components/chat/chat";


export default function AnalyticsPage() {
    return (
        <div className="container mx-auto lg:px-48">
            <div className="text-5xl font-extrabold flex justify-center mt-8">
                <h1 className="bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-violet-500">
                    Analytics GPT
                </h1>
            </div>
            <p className="text-center my-2">
                表形式のデータセットからチャットインターフェイスを使ってコンテキストに沿ったデータの可視化を行います。
            </p>
            <Chat />
        </div>
    );
}