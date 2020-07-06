import React, { Component } from "react";
import '../css/app.css';
import '../css/products.css';

import Header from "./Header";
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
    console.log("!!!");
    // console.log(this.state.data);

    trackPromise(fetch("/api/brands")
      .then(response => {
        if (response.status >= 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        console.log(response);
        return response.json();
      })
      .then(data => {
        console.log(data);
        this.setState(() => {
          return {
            brandData: [data],
            loaded: true
          };
        });
      }));
  }

  render() {
    console.log("!!!!");
    console.log(this.state.brandData, this.state.productData);
    if(this.state.brandData && this.state.brandData[0]) {
      return (
        <div id="root"> 

          <Router>
            <Header
              brandData={this.state.brandData}
            />

            <Switch>
              <Route path="/products/:brandName&pageNum=:pageNum" children={<BrandChild />} />
            </Switch>
            
          </Router>
          <LoadingIndicator/>
        </div>
      );
    } else {
      return (<div id="root"> 
                <div></div>
                <LoadingIndicator/>
              </div>);
    }
    
  }
}
function BrandChild() {
  let { brandName, pageNum } = useParams();
  console.log(brandName, pageNum);
  return (
    <BrandLink 
      brandName={brandName}
      pageNum={pageNum}
    />
  );
}
export default App;

// const container = document.getElementById("app");
// render(<App />, container);