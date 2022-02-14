import { createPackage, getPackage } from "./Package";

const functionMap: Record<string, Function> = {
    "createPackage": createPackage,
    "getPackage": getPackage,
}

export class HttpClient {
    private readonly host: string;

    constructor(host: string, port?: number) {
        this.host = host;
        if (port) {
            this.host += (':' + port);
        }
    }

    public async execFunction(functionName: string, args: any): Promise<any> {
        if (!functionMap[functionName]) throw Error("Api called function not found.");
        return await functionMap[functionName](this.host, args);
    }
}

export const apiClient = new HttpClient(process.env.REACT_APP_API_HOST || "");

