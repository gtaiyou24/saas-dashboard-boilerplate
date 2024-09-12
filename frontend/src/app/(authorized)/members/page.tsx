import {MemberTable} from "@/components/member/member-table";
import {columns} from "@/components/member/columns";
import {getMembers} from "@/lib/api";
import {auth} from "@/lib/auth";
import {notFound} from "next/navigation";
import InviteButton from "@/components/member/invite-button";


export default async function MembersPage() {
    const session = await auth();
    if (!session) notFound();
    const members = await getMembers(session.currentProject?.tenantId ?? session.user.tenants[0].id);
    return (
        <div className="container mx-auto px-48">
            <div className="flex justify-between gap-4 my-8">
                <h1 className="text-2xl font-bold">チームメンバー</h1>
                <InviteButton />
            </div>
            <MemberTable columns={columns} data={members} />
        </div>
    );
}