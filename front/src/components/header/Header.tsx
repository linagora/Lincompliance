import React from 'react';
import { Link } from 'react-router-dom';
import {useTranslation} from "react-i18next";

function Header() {
    const { t } = useTranslation('general');

    return (
        <nav className="Header navbar bg-light">
            <div className="w-75 m-auto text-left">
                <Link to="/" className="navbar-brand">{t('title')}</Link>
            </div>
        </nav>
    );
}

export default Header;
