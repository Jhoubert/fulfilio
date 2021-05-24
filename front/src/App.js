import React, { useEffect } from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import Login from "./components/login/Login";
import Product from "./components/product/Product"

function App() {

  useEffect(() => {
    console.log("EFFECT/")
  });


  return (<Router>
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light fixed-top">
        <div className="container">
          <Link className="navbar-brand" to={"/sign-in"}>Fulfil.io Products</Link>
          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">

          </div>
        </div>
      </nav>

          <Switch>
            <Route exact path='/' component={Login} />
            <Route path="/sign-in" component={Login} />
            <Route path="/products" component={Product} />
          </Switch>
          
    </div>
    </Router>
  );
}

export default App;