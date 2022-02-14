import React from 'react';
import { generateUniqueID } from "web-vitals/dist/modules/lib/generateUniqueID";
import {useTranslation} from "react-i18next";
import {ResourceKey} from "i18next";
import PackageTableRow from "./PackageTableRow";

function PackageTable(data: { packages: any[], filename: string | undefined }) {
    const { t } = useTranslation("package_table");

    // Variables
    const columns: string[] = ['name', 'version', 'licence', 'score', 'code'];

    // Render
    const headerRow = () => columns.map((column) => <th scope="col" key={generateUniqueID()}>{t(column as ResourceKey)}</th>)
    const rowContent = (p: any) => <PackageTableRow package={p} key={generateUniqueID()}/>
    const tableContent = () => data.packages.map(rowContent)

    return (
        <div className="table-responsive pb-5">
            <h4 className="text-center">{t('title_prefix')}{ data.filename }</h4>
            <table className="PackageTable table table-hover table-sm table-light text-secondary my-5-2 w-75 m-auto">
                <thead>
                    <tr>
                        {headerRow()}
                    </tr>
                </thead>
                <tbody>
                    {tableContent()}
                </tbody>
            </table>
        </div>
    );
}

export default PackageTable;