import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent, DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import Link from 'next/link';
import {Avatar, AvatarFallback} from "@/components/ui/avatar";
import {auth, signOut} from "@/lib/auth";


const userNavItems = [
    { title: "アカウント情報", href: "/account" },
    { title: "セキュリティ", href: "/account/security" },
    { title: "ログインサービス", href: "/account/login-provider" },
];

export default async function UserNav() {
    const session = await auth();
    const user = session?.user;

    return (
        <DropdownMenu>
            <DropdownMenuTrigger className="ml-auto" asChild>
                <Button
                    variant="outline"
                    size="icon"
                    className="overflow-hidden rounded-full"
                >
                    <Avatar className="h-8 w-8">
                        {/*<AvatarImage*/}
                        {/*    src={session.user?.image ?? ""}*/}
                        {/*    alt={session.user?.email ?? ""}*/}
                        {/*/>*/}
                        <AvatarFallback>{session?.user?.name?.substring(0, 2)}</AvatarFallback>
                    </Avatar>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                        <p className="text-sm font-medium leading-none">
                            {session?.user?.name}
                        </p>
                        <p className="text-xs leading-none text-muted-foreground">
                            {session?.user?.email}
                        </p>
                    </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                    {userNavItems.map((item) => (
                        <DropdownMenuItem key={item.href} asChild><Link href={item.href}>{item.title}</Link></DropdownMenuItem>
                    ))}
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                    <form action={async () => {
                        "use server"
                        await signOut({ redirectTo: '/auth/login', redirect: true });
                    }}>
                        <button type="submit">ログアウト</button>
                    </form>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}