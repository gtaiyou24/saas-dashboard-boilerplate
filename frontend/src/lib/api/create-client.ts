import createClient from "openapi-fetch";
import {paths} from "@/lib/api/type";


export const createApiClient = () => {
    return createClient<paths>({ baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL! })
}