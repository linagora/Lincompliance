export interface Package {
    name: string,
    version: string,
    url?: string,
    description?: string,
    ifCrypto?: boolean,
    algoList?: string[],
    ifStrongEncryption?: boolean,
    score?: number,
    license?: string,
    code?: string
}
