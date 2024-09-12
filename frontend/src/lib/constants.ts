import {Icons} from "@/components/icons";

export const BASE_URL = process.env.NODE_ENV === "production"
    ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}` ?? 'https://analyticsgpt.com'
    : 'http://localhost:3000';

export const APP_NAME = 'Analytics GPT';
export const X_CREATOR = '@tm_taiyo';

export const TAGS = {
    tenants: 'tenants'
}

export const STORAGES = {
    project: 'analyticsgpt/currentProj'
}

export const navItems: {href: string; label: string; icon: keyof typeof Icons}[] = [
    {href: '/', label: '分析', icon: 'lineChart'},
    // {href: '/', label: 'ホーム', icon: "home"},
    // {href: '/analytics', label: '分析', icon: 'lineChart'},

    {href: '/dashboard', label: 'ダッシュボード', icon: 'layoutDashboard'},
    {href: '/dataset', label: 'データセット', icon: 'database'},
    {href: '/members', label: 'メンバー', icon: 'users2'},
];