export type User = {
    username: string;
    emailAddress: string;
    tenants: {
        id: string;
        name: string;
    }[];
    accounts: {
        provider: string;
        providerAccountId: string;
    }[];
}

export type Tenant = {
    id: string;
    name: string;
};

export type Project = {
    id: string;
    name: string;
};

export type Member = {
    userId: string;
    email: string;
    username: string;
    role: 'admin' | 'editor' | 'reader';
};


export type SemanticType = 'quantitative' | 'nominal' | 'ordinal' | 'temporal';

export interface Field {
    fid: string;
    name: string;
    semanticType: SemanticType;
}

export interface Row {
    [key: string]: any;
}

export interface Dataset {
    fields: Field[];
    dataSource: Row[];
}

export type DSItem =
    | {
        key: string;
        name: string;
        url: string;
        type: "demo";
      }
    | {
        key: string;
        name: string;
        dataset: Dataset;
        type: "custom";
    };


export interface ChatMessage {
    role: "user" | "assistant" | "system";
    content: string;
}
export interface ChatResponse {
    id: string;
    object: string;
    model: string;
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
    choices: { message: ChatMessage }[];
}