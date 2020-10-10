import React, { Component } from "react";
import '../css/app.css';
import '../css/products.css';

import Header from "./Header/Header";
import FrontPage from "./FrontPage";
import BrandLink from "./BrandLink";
import { HashRouter } from 'react-router-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams
} from "react-router-dom";
import LoadingIndicator from "./Loader";
import { trackPromise } from "react-promise-tracker";
import Loader from 'react-loader-spinner';
import SideCategoryBar from "./SideCategoryBar/SideCategoryBar"

import { library } from '@fortawesome/fontawesome-svg-core';
import { faCheckSquare, faCoffee, faCubes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
library.add(faCheckSquare, faCoffee, faCubes);


// const LoadingIndicator = props => {
//   const { promiseInProgress } = usePromiseTracker();
//   return (
//     promiseInProgress && 
//     <div
//       style={{
//         position: "absolute",
//         top: "0px",
//         left: "0px",
//         width: "100%",
//         height: "100%",
//         backgroundColor: "white",
//         display: "flex",
//         justifyContent: "center",
//         alignItems: "center"
//       }}
//     >
//       <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />
//     </div>
//   );  
// }

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      brandData: [],
      productData: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    // console.log(this.state.data);

    trackPromise(fetch("/api/brands")
      .then(response => {
        if (response.status >= 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            brandData: [data],
            loaded: true
          };
        });
      }));
  }

  render() {
    if(this.state.brandData && this.state.brandData[0]) {
      return (
        <div id="root"> 
          
          <Router>

            <Switch>
              <Route path="/products/:brandName?/:pageNum?" children={
                <BrandChild
                  brandData={this.state.brandData}
                />
              }/>
              <Route path="/" children={<FrontPage/>}/>
            </Switch>
            
          </Router>
          <LoadingIndicator/>
        </div>
      );
    } else {
      return (
        <div id="root"> 
          <div></div>
          <LoadingIndicator/>
        </div>);
    }
    
  }
}
function BrandChild(props) {
  console.log(props.brandData);
  let { brandName, pageNum } = useParams();
  console.log("116:", brandName, pageNum);
  return (
    <React.Fragment>
      <Header
        brandData={props.brandData}
      />
      <BrandLink 
        brandName={brandName}
        pageNum={pageNum}
      />
    </React.Fragment>
  );
}
export default App;

// const container = document.getElementById("app");
// render(<App />, container);