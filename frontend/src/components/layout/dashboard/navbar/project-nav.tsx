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
import {Project} from "@/lib/types";
import {useCallback, useState} from "react";
import {useSession} from "next-auth/react";

export default function ProjectNav({ projects }: { projects: Project[]; }) {
    const {data: session, update} = useSession();
    const projectId = session?.currentProject?.projectId;
    const setProjectId = useCallback((newProjectId: string) => {
        update({
            ...session,
            currentProject: {
                ...session?.currentProject,
                projectId: newProjectId
            }
        })
    }, [session]);
    if (!projectId) setProjectId(projects[0].id);
    const [open, setOpen] = useState(false)

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[200px] justify-between"
                >
                    {projects.find((project) => project.id === projectId)?.name}
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
                <Command>
                    <CommandInput placeholder="プロジェクトを検索..." />
                    <CommandList>
                        <CommandEmpty>プロジェクトが見つかりません</CommandEmpty>
                        <CommandGroup heading="プロジェクト">
                            {projects.map((project) => (
                                <CommandItem
                                    key={project.id}
                                    value={project.id}
                                    onSelect={(currentValue) => {
                                        setProjectId(currentValue)
                                        setOpen(false)
                                    }}
                                >
                                    <Check
                                        className={cn(
                                            "mr-2 h-4 w-4",
                                            projectId === project.id ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                    {project.name}
                                </CommandItem>
                            ))}
                        </CommandGroup>
                        <CommandSeparator />
                        <CommandGroup>
                            <CommandItem>
                                <CirclePlus className="mr-2 h-4 w-4" />
                                <span>プロジェクトを新規作成</span>
                            </CommandItem>
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}