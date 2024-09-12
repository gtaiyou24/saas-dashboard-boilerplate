import {APP_NAME} from "@/lib/constants";
import Image from "next/image";


export default function Logo({
    width,
    height,
    className
}: {
    width: number;
    height: number;
    className?: string;
}) {
    return (
        <div className={className}>
            <Image src='/logo-dark.png' className={"rounded-lg hidden dark:block"} alt={APP_NAME} width={width} height={height} />
            <Image src='/logo-light.png' className={"rounded-lg block dark:hidden"} alt={APP_NAME} width={width} height={height} />
        </div>
    );
}