"use client";

import * as z from "zod";
import { useSearchParams } from "next/navigation";
import {useEffect, useState, useTransition} from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";

import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { CardWrapper } from "@/components/auth/card-wrapper";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/form-error";
import { FormSuccess } from "@/components/form-success";
import { login } from "@/components/auth/login/login";
import { LoginSchema } from "@/components/auth/login/login-schema";

export const LoginForm = () => {
    const searchParams = useSearchParams();
    const callbackUrl = searchParams.get("callbackUrl");

    const errorUrl =
        searchParams.get("error") === "OAuthAccountNotLinked"
            ? "Email already in use with a different provider"
            : "";

    const [error, setError] = useState<string | undefined>("");
    const [success, setSuccess] = useState<string | undefined>("");
    const [isPending, startTransition] = useTransition();

    const form = useForm<z.infer<typeof LoginSchema>>({
        resolver: zodResolver(LoginSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    useEffect(() => {
        const timeoutId = setTimeout(() => {
            const emailInput = document.querySelector('input[name="email"]') as HTMLInputElement;
            const passwordInput = document.querySelector('input[name="password"]') as HTMLInputElement;

            if (emailInput && emailInput.value) {
                form.setValue('email', emailInput.value);
            }
            if (passwordInput && passwordInput.value) {
                form.setValue('password', passwordInput.value);
            }
        }, 500);

        return () => clearTimeout(timeoutId);
    }, [form]);

    const onSubmit = (values: z.infer<typeof LoginSchema>) => {
        setError("");
        setSuccess("");

        startTransition(() => {
            login(values, callbackUrl)
                .then((data) => {
                    if (data?.error) {
                        form.reset();
                        setError(data.error);
                    }

                    if (data?.success) {
                        form.reset();
                        setSuccess(data.success);
                    }
                })
                .catch(() => setError("Something went wrong!"));
        });
    };

    return (
        <CardWrapper
            headerTitle="ログイン"
            backButtonLabel="初めてご利用ですか？ 新規登録はこちら"
            backButtonHref="/auth/register"
            showSocial
        >
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <div className="space-y-4">
                        <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="email">メールアドレス</FormLabel>
                                    <FormControl>
                                        <Input
                                            {...field}
                                            id="email"
                                            disabled={isPending}
                                            placeholder="メールアドレス"
                                            type="email"
                                            onBlur={(e) => {
                                                field.onBlur();
                                                form.setValue('email', e.target.value);
                                            }}
                                            autoComplete="username"
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="password"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="password">パスワード</FormLabel>
                                    <FormControl>
                                        <Input
                                            {...field}
                                            id="password"
                                            disabled={isPending}
                                            placeholder="パスワード"
                                            type="password"
                                            onBlur={(e) => {
                                                field.onBlur();
                                                form.setValue('password', e.target.value);
                                            }}
                                            autoComplete="current-password"
                                        />
                                    </FormControl>
                                    <FormMessage />
                                    <Button
                                        size="sm"
                                        variant="link"
                                        asChild
                                        className="px-0 font-normal flex justify-end"
                                    >
                                        <Link href="/auth/reset">パスワードをお忘れですか？</Link>
                                    </Button>
                                </FormItem>
                            )}
                        />
                    </div>
                    <FormError message={error || errorUrl} />
                    <FormSuccess message={success} />
                    <Button type="submit" disabled={isPending} className="w-full">ログイン</Button>
                </form>
            </Form>
        </CardWrapper>
    );
};