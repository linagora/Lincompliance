import React from 'react';
import {faExternalLinkAlt} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

function PackageTableRow(data: { package: any }) {
    // Render
    const displayLink = (link: string) => link !== "" ?
        <a href={link} className="ml-2" target="_blank" rel="noreferrer">
            <FontAwesomeIcon className="align-top" icon={faExternalLinkAlt}/>
        </a> :
        ""

    return (
        <tr className="PackageTableRow">
            <td>{data.package['name']}{displayLink(data.package['url'])}</td>
            <td>{data.package['version']}</td>
            <td>{data.package['licence']}</td>
            <td title={data.package['algoList']}>{data.package['score']}</td>
            <td>{data.package['code']}</td>
        </tr>
    );
}

export default PackageTableRow;