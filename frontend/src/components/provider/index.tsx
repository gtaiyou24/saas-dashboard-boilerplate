'use client'

import { ReactNode } from 'react'
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import ThemeProvider from "@/components/provider/theme-provider";
import {SessionProvider} from "next-auth/react";
import {TooltipProvider} from "@/components/ui/tooltip";

export default function Provider({ children }: { children: ReactNode }) {
    const queryClient = new QueryClient();
    return (
        <SessionProvider>
            <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
                <TooltipProvider>
                    <QueryClientProvider client={queryClient}>
                        {children}
                    </QueryClientProvider>
                </TooltipProvider>
            </ThemeProvider>
        </SessionProvider>
    );
}