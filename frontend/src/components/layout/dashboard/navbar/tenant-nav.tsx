"use client"

import * as React from "react"
import {Check, ChevronsUpDown, CirclePlus} from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList, CommandSeparator,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {Tenant} from "@/lib/types";
import {useCallback, useEffect, useState} from "react";
import {useSession} from "next-auth/react";

export default function TenantNav({ tenants }: { tenants: Tenant[]; }) {
    const {data: session, update} = useSession();
    const tenantId = session?.currentProject?.tenantId;
    const setTenantId = useCallback((newTenantId: string) => {
        update({
            ...session,
            currentProject: {
                tenantId: newTenantId,
                projectId: session?.currentProject?.tenantId === newTenantId ? session?.currentProject.projectId : undefined
            }
        });
    }, [session]);
    const [open, setOpen] = useState(false);

    useEffect(() => {
        if (!session?.currentProject?.tenantId) {
            setTenantId(tenants[0].id);
        }
    }, []);

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[200px] justify-between"
                >
                    {tenants.find((tenant) => tenant.id === tenantId)?.name}
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
                <Command>
                    <CommandInput placeholder="チームを検索..." />
                    <CommandList>
                        <CommandEmpty>No framework found.</CommandEmpty>
                        <CommandGroup heading="チーム">
                            {tenants.map((tenant) => (
                                <CommandItem
                                    key={tenant.id}
                                    value={tenant.id}
                                    onSelect={(currentTenantId) => {
                                        setTenantId(currentTenantId)
                                        setOpen(false)
                                    }}
                                >
                                    <Check
                                        className={cn(
                                            "mr-2 h-4 w-4",
                                            tenantId === tenant.id ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                    {tenant.name}
                                </CommandItem>
                            ))}
                        </CommandGroup>
                        <CommandSeparator />
                        <CommandGroup>
                            <CommandItem>
                                <CirclePlus className="mr-2 h-4 w-4" />
                                <span>チームを新規作成</span>
                            </CommandItem>
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}