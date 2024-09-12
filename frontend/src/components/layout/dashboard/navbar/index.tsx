import {Sheet, SheetContent, SheetTrigger} from "@/components/ui/sheet";
import {Button} from "@/components/ui/button";
import {　PanelLeft, Settings　} from "lucide-react";
import Link from "next/link";
import CurrentProjectNav from "@/components/layout/dashboard/current-project-nav";
import {APP_NAME, navItems} from "@/lib/constants";
import {Icons} from "@/components/icons";
import Logo from "@/components/logo";
import UserNav from "@/components/layout/dashboard/navbar/user-nav";

export default function Navbar() {
    return (
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
            <MobileNav />
            <CurrentProjectNav />
            <UserNav />
        </header>
    );
}

function MobileNav() {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button size="icon" variant="outline" className="sm:hidden">
                    <PanelLeft className="h-5 w-5" />
                    <span className="sr-only">Toggle Menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="sm:max-w-xs">
                <nav className="grid gap-6 text-lg font-medium">
                    <Link
                        href="/dashboard"
                        className="group flex h-10 w-10 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:text-base"
                    >
                        <Logo width={40} height={40} className="transition-all group-hover:scale-110" />
                        <span className="sr-only">{APP_NAME}</span>
                    </Link>

                    <CurrentProjectNav isGrid={true} />

                    {navItems.map((item, index) => {
                        const Icon = Icons[item.icon];
                        return (
                            <Link
                                key={index}
                                href={item.href}
                                className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                            >
                                <Icon className="h-5 w-5" />
                                {item.label}
                            </Link>
                        );
                    })}

                    <Link
                        href="#"
                        className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
                    >
                        <Settings className="h-5 w-5" />
                        設定
                    </Link>
                </nav>
            </SheetContent>
        </Sheet>
    );
}