"use client";

import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PlusCircle, FileUp, Database } from "lucide-react";

// データセットの型定義
type Dataset = {
    id: string;
    name: string;
    type: 'file' | 'database';
    source: string;
    lastUpdated: string;
};

// ダミーデータ
const initialDatasets: Dataset[] = [
    { id: '1', name: '【デモ】車', type: 'file', source: 'sales_2023.csv', lastUpdated: '2023-12-31' },
    { id: '2', name: '顧客一覧', type: 'database', source: 'customers.json', lastUpdated: '2024-03-15' },
];

export default function DatasetPage() {
    const [datasets, setDatasets] = useState<Dataset[]>(initialDatasets);
    const [newDatasetName, setNewDatasetName] = useState('');
    const [newDatasetType, setNewDatasetType] = useState<'file' | 'database'>('file');

    const addDataset = () => {
        if (newDatasetName) {
            const newDataset: Dataset = {
                id: (datasets.length + 1).toString(),
                name: newDatasetName,
                type: newDatasetType,
                source: newDatasetType === 'file' ? 'Uploaded file' : 'Connected database',
                lastUpdated: new Date().toISOString().split('T')[0],
            };
            setDatasets([...datasets, newDataset]);
            setNewDatasetName('');
        }
    };

    return (
        <div className="p-6 space-y-6">
            <h1 className="text-2xl font-bold">データセット</h1>

            <div className="flex space-x-4">
                <Input
                    placeholder="データセット名"
                    value={newDatasetName}
                    onChange={(e) => setNewDatasetName(e.target.value)}
                    className="max-w-xs"
                />
                <Select value={newDatasetType} onValueChange={(value: 'file' | 'database') => setNewDatasetType(value)}>
                    <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="タイプを選択" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="file">ファイル</SelectItem>
                        <SelectItem value="database">データベース</SelectItem>
                    </SelectContent>
                </Select>
                <Button onClick={addDataset}>
                    <PlusCircle className="mr-2 h-4 w-4" /> データセット追加
                </Button>
            </div>

            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>名前</TableHead>
                        <TableHead>タイプ</TableHead>
                        <TableHead>ソース</TableHead>
                        <TableHead>最終更新日</TableHead>
                        <TableHead>アクション</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {datasets.map((dataset) => (
                        <TableRow key={dataset.id}>
                            <TableCell>{dataset.name}</TableCell>
                            <TableCell>{dataset.type === 'file' ? 'ファイル' : 'データベース'}</TableCell>
                            <TableCell>{dataset.source}</TableCell>
                            <TableCell>{dataset.lastUpdated}</TableCell>
                            <TableCell>
                                <Button variant="outline" size="sm">
                                    {dataset.type === 'file' ? (
                                        <><FileUp className="mr-2 h-4 w-4" /> アップロード</>
                                    ) : (
                                        <><Database className="mr-2 h-4 w-4" /> 接続</>
                                    )}
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};