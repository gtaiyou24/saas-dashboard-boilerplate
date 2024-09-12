"use client";

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"


export default function SelectDataset({
    items,
    selectedKey,
    onChange
}: {
    items: { key: string; name: string }[];
    selectedKey: string;
    onChange: (key: string) => void;
}) {
    const [open, setOpen] = React.useState(false)
    const [value, setValue] = React.useState(selectedKey)

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-[200px] justify-between bg-primary-foreground"
                >
                    {value
                        ? items.find((item) => item.key === value)?.name
                        : "データセットを選択..."}
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
                <Command>
                    <CommandInput placeholder="データセットを選択..." />
                    <CommandList>
                        <CommandEmpty>No framework found.</CommandEmpty>
                        <CommandGroup>
                            {items.map((item) => (
                                <CommandItem
                                    key={item.key}
                                    value={item.key}
                                    onSelect={(currentKey) => {
                                        onChange(currentKey);
                                        setValue(currentKey === value ? "" : currentKey)
                                        setOpen(false)
                                    }}
                                >
                                    <Check
                                        className={cn(
                                            "mr-2 h-4 w-4",
                                            value === item.key ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                    {item.name}
                                </CommandItem>
                            ))}
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}
