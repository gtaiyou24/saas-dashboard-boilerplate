'use client';

import Link from "next/link";
import {Button} from "@/components/ui/button";

export default function Error({ reset }: { reset: () => void }) {
    return (
        <div className="min-h-full text-center justify-center m-auto my-4 flex max-w-xl flex-col p-8 md:p-12">
            <h2 className="text-xl font-bold">システムエラーが発生しました</h2>
            <p className="my-2">
                恐れ入りますが、しばらく時間を置いてから再度お試しください。<br />
                問題が解決しない場合は<Link href="https://forms.gle/skqwe6iUnA8LQ7146" className="text-primary transition-colors" target="_blank">お問い合わせフォーム</Link>よりお問い合わせください。
            </p>
            <Button size="lg" onClick={() => reset()}>
                やり直す
            </Button>
        </div>
    );
}
