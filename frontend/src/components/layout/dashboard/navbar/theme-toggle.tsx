"use client";

import { MoonIcon, SunIcon } from "@radix-ui/react-icons";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {LaptopMinimal} from "lucide-react";


export default function ThemeToggle({}: {}) {
    const { setTheme } = useTheme();
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                    <SunIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                    <MoonIcon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                    <span className="sr-only">Toggle theme</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem className="gap-1" onClick={() => setTheme("light")}>
                    <SunIcon className="h-4 w-4" /> Light
                </DropdownMenuItem>
                <DropdownMenuItem className="gap-1" onClick={() => setTheme("dark")}>
                    <MoonIcon className="h-4 w-4" /> Dark
                </DropdownMenuItem>
                <DropdownMenuItem className="gap-1" onClick={() => setTheme("system")}>
                    <LaptopMinimal className="h-4 w-4" /> System
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}