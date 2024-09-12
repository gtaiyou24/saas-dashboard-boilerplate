"use client";

import {useEffect, useRef} from "react";
import embed, { vega } from 'vega-embed';
import {Row} from "@/lib/types";
import {useCurrentMediaTheme, VegaTheme} from "@/components/vega/theme";


export default function ReactVega({
    spec,
    data,
    width = 400,
    height = 400
}: {
    spec: any;
    data?: Row[];
    width?: number;
    height?: number;
}) {
    const container = useRef<HTMLDivElement>(null);

    const theme = useCurrentMediaTheme();

    useEffect(() => {
        if (container.current && data) {
            spec.data = {
                name: 'dataSource'
            }
            embed(container.current, spec, { actions: false, config: VegaTheme[theme] }).then(res => {
                res.view.change('dataSource', vega.changeset().remove(() => true).insert(data))
                res.view.resize();

                if (width) res.view.width(width);
                if (height) res.view.height(height);

                res.view.runAsync();
            })
        }
    }, [spec, data, theme])
    return <div ref={container} style={{ width: '100%', height: '100%' }}></div>
}