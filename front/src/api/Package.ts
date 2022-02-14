import httpStatus from "http-status";
import { Package } from "../models/Package";

export async function createPackage(host: string, file: FormData): Promise<Package> {
    const res = await fetch(`${host}/package`, {
        method: "POST",
        headers: new Headers({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Accept': '*/*'
        }),
        body: file
    });
    if (res.status !== httpStatus.CREATED && res.status !== httpStatus.OK)
        throw Error(await res.json().then((d: any) => d.message));
    return await res.json() as Package;
}

export async function getPackage(host: string, packageName: string): Promise<Package[]> {
    const res = await fetch(`${host}/package/${packageName}`);
    if (res.status !== httpStatus.OK) throw Error(await res.text());
    return await res.json() as Package[];
}