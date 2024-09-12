import {Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbSeparator} from "@/components/ui/breadcrumb";
import TenantNav from "@/components/layout/dashboard/navbar/tenant-nav";
import {Slash} from "lucide-react";
import ProjectNav from "@/components/layout/dashboard/navbar/project-nav";
import {getProjects, getTenants} from "@/lib/api";
import {auth} from "@/lib/auth";


export default async function CurrentProjectNav({ isGrid = false }: { isGrid?: boolean; }) {
    const session = await auth();
    const tenants = await getTenants();
    const projects = await getProjects(session?.currentProject?.tenantId ?? tenants[0].id);
    if (isGrid) {
        return (
            <div className="grid gap-2">
                <TenantNav tenants={tenants} />
                <ProjectNav projects={projects} />
            </div>
        );
    }
    return (
        <Breadcrumb className="hidden md:block">
            <BreadcrumbList>
                <BreadcrumbItem>
                    <TenantNav tenants={tenants} />
                </BreadcrumbItem>
                <BreadcrumbSeparator>
                    <Slash  />
                </BreadcrumbSeparator>
                <BreadcrumbItem>
                    <ProjectNav projects={projects} />
                </BreadcrumbItem>
            </BreadcrumbList>
        </Breadcrumb>
    );
}