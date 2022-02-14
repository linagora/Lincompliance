import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, {useState} from 'react';
import { faFileExport } from '@fortawesome/free-solid-svg-icons'
import { useTranslation } from "react-i18next";
import UploadFile from "../utils/UploadFile";

function UploadForm(data: {upload: ((file: File) => void)}) {
    const [file, setFile] = useState<File | null>(null);

    const { t } = useTranslation('upload_form');

    // Events
    const launchUpload = (event: any) => {
        event.preventDefault();
        if (file) data.upload(file);
    }

    // Render
    return (
        <form onSubmit={launchUpload} className="w-75 m-auto">
            <UploadFile file={file} setFile={setFile}/>

            <button className="btn btn-primary btn-block m-0 mt-1" type="submit">
                <FontAwesomeIcon className="mx-1" icon={faFileExport}/> {t('launch')}
            </button>
        </form>
    );
}

export default UploadForm;
