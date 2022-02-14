import React from 'react';
import EC from "./EC";
import { useRoutes } from "react-router-dom";

function Body() {
    return useRoutes([
        {
            index: true,
            element: <EC/>
        }
    ]);
}

export default Body;
