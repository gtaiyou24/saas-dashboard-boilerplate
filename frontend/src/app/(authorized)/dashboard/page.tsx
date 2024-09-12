"use client";

import React, {useEffect, useState} from 'react';
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import ReactVega from "@/components/vega/react-vega";
import {toast} from "sonner";
import {Dataset} from "@/lib/types";
import DataTable from "@/components/data-table/data-table";
import {produce} from "immer";
import {PlusCircle} from "lucide-react";
import {Button} from "@/components/ui/button";

export default function DashboardPage() {
    const [dataset, setDataset] = useState<Dataset | null>(null);

    useEffect(() => {
        fetch("/datasets/customers.json")
            .then((res) => res.json())
            .then((res) => {
                setDataset(res);
            })
            .catch(() => {
                toast("データセットが見つかりませんでした。");
            });
    }, []);

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between">
                <h1 className="text-2xl font-bold">ダッシュボード</h1>
                <Button>
                    <PlusCircle className="mr-2 h-4 w-4" /> データを追加
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-lg">顧客数</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">2,221</p>
                    </CardContent>
                </Card>
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-base">総購入金額</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">¥30,474,306</p>
                    </CardContent>
                </Card>
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-base">総分析回数</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">1,024</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-base">顧客一覧</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {dataset && (
                            <DataTable
                                data={dataset.dataSource}
                                metas={dataset.fields}
                                onMetaChange={(fid, fIndex, meta) => {
                                    const nextDataset = produce(
                                        dataset,
                                        (draft) => {
                                            draft.fields[fIndex] = {
                                                ...draft.fields[fIndex],
                                                ...meta,
                                            };
                                        }
                                    );
                                    setDataset(nextDataset);
                                }}
                            />
                        )}
                    </CardContent>
                </Card>
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-base">購入者数の推移</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {dataset && <ReactVega
                            spec={{
                                mark: "line",
                                encoding: {
                                    x: {
                                        field: "初回購入日",
                                        type: "temporal",
                                        title: "初回購入日"
                                    },
                                    y: {
                                        aggregate: "count",
                                        field: "顧客ID",
                                        type: "quantitative",
                                        title: "COUNT(顧客ID)"
                                    }
                                }
                            }}
                            data={dataset.dataSource ?? []} width={1500} />}
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card className="bg-primary-foreground">
                    <CardHeader>
                        <div className="flex justify-between">
                            <CardTitle className="text-base">購入回数</CardTitle>
                            <Button size="sm">
                                <PlusCircle className="mr-2 h-4 w-4" /> 編集
                            </Button>
                        </div>
                        <CardDescription>3日前</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {dataset && <ReactVega
                            spec={{
                                mark: "bar",
                                encoding: {
                                    x: {
                                        field: "購入回数",
                                        bin: { maxbins: 20 },
                                        type: "quantitative",
                                        title: "BIN(購入回数)"
                                    },
                                    y: {
                                        aggregate: "count",
                                        type: "quantitative"
                                    }
                                }
                            }}
                            data={dataset.dataSource ?? []} width={300} />}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};