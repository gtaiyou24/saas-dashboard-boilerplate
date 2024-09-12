import { Plus, Copy } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function InviteButton() {
    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button>
                    <Plus className="mr-2 h-4 w-4" /> メンバーを招待
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle>チームメンバーを招待する</DialogTitle>
                </DialogHeader>
                <div className="flex items-center space-x-4 my-4">
                    <div className="grid flex-1 gap-2">
                        <Label htmlFor="email" className="sr-only">メールアドレス</Label>
                        <Input id="email" type="email" placeholder="taro@example.com" />
                    </div>
                    <Select>
                        <SelectTrigger className="w-[150px]">
                            <SelectValue placeholder="ロールを選択" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel>ロール</SelectLabel>
                                <SelectItem value="admin">管理者</SelectItem>
                                <SelectItem value="editor">編集者</SelectItem>
                                <SelectItem value="reader">閲覧者</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
                <DialogFooter>
                    <DialogClose asChild>
                        <Button type="button" variant="secondary">キャンセル</Button>
                    </DialogClose>
                    <Button type="submit">招待する</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}