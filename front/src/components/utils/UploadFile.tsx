import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';
import { faFileImport, faFileArchive } from '@fortawesome/free-solid-svg-icons'
import { useTranslation } from "react-i18next";

function UploadFile(data: {file: File | null, setFile: ((file: File) => void)}) {
    const { t } = useTranslation('uploader');

    // Events
    const onZipAdd = (event: any) => data.setFile(event.target.files[0])

    // Render
    return (
        <div className="UploadFile">
            <label className="btn btn-outline-primary btn-block m-0 mb-2" htmlFor="zipFile">
                <FontAwesomeIcon className="mx-1" icon={faFileImport}/> {t('import')}
            </label>
            <div className={"drop-zone m-auto w-100 " + (data.file === null ? "d-block" : "d-none")} id="uploader">
                <label>{t('drag_text')}</label>
                <input id="zipFile" className="m-0 p-0 w-100 h-100 input-file" type='file' accept=".zip" onChange={onZipAdd}/>
            </div>
            <div className={"file-upload " + (data.file === null ? "d-none" : "d-block")} id="file_upload">
                <FontAwesomeIcon icon={faFileArchive}/><br/>
                { data.file ? data.file.name : "" }
            </div>
        </div>
        );
}

export default UploadFile;