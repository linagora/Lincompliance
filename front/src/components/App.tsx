import React, {Suspense} from 'react';
import Header from "./header/Header";
import Body from './body/Body';
import Loader from "./utils/Loader";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
      <div className="App">
          <ToastContainer />
          <Suspense fallback={<Loader/>}>
              <Header />
              <Body />
          </Suspense>
      </div>
  );
}

export default App;
