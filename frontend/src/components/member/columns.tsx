"use client";

import { ColumnDef } from "@tanstack/react-table"
import {Member} from "@/lib/types";

export const columns: ColumnDef<Member>[] = [
    {
        accessorKey: "email",
        header: "メールアドレス",
    },
    {
        accessorKey: "username",
        header: "ユーザー名",
    },
    {
        accessorKey: "role",
        header: "ロール",
    }
]