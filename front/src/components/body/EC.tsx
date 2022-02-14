import React, {useState} from 'react';
import {useTranslation} from "react-i18next";
import Loader from "../utils/Loader";
import UploadForm from "../package/UploadForm";
import PackageTable from "../package/PackageTable";
import {Package} from "../../models/Package";
import {apiClient} from "../../api/Client";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faRedo} from "@fortawesome/free-solid-svg-icons";
import {toast} from "react-toastify";


function EC() {
    enum State {
        start,
        uploading,
        resulted,
        error
    }

    // Variables
    const [state, setState] = useState<State>(State.start);
    const [filename, setFilename] = useState<string>();
    const [result, setResult] = useState<Package[]>([]);

    const { t } = useTranslation('ec');

    // Requests
    const onUpload = (data: Package[]) => {
        toast.success(t('analyse_success'))
        setResult(data);
        setState(State.resulted);
    }
    const onError = (error: Error) => {
        toast.success(t('error_prefix') + error.message);
        setState(State.error);
    }
    const upload = (file: File) => {
        let formData: FormData = new FormData();

        setState(State.uploading);
        setFilename(file.name);
        formData.append("file", file as Blob);
        apiClient.execFunction("createPackage", formData).then(onUpload).catch(onError);
    }

    // Render
    const fromState = (state: State): JSX.Element => {
        if (state === State.error) state = State.start
        switch (state) {
            case State.resulted:
                return <PackageTable packages={ result } filename={filename}/>;
            case State.uploading:
                return <Loader/>;
            case State.start:
                return <UploadForm upload={upload}/>;
        }
    }

    return (
        <div className="EC">
            <div className="flex-container">
                <h2>{t('title')}</h2>
                {
                    state !== State.start ?
                        <button className="ml-auto btn btn-light float-right" onClick={() => setState(State.start)}>
                            <FontAwesomeIcon className="mr-3" icon={faRedo}/>
                            { t('restart') }
                        </button> : <div/>

                }
            </div>
            <hr/>
            { fromState(state) }
        </div>
    );
}

export default EC;