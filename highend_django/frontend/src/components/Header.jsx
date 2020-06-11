import React, { Component } from "react";
import { render } from "react-dom";

class BrandLink extends Component {
  constructor(props) {
    super(props);
    this.state = {
      brandName: '',
      productData: [],
      loaded: false,
      placeholder: "Loading"
    };

    this.fetchProducts = this.fetchProducts.bind(this);

  }


  render() {
    console.log("hello");
    return (<div className="header">
        <div></div> 
      </div>);
    
  }
}

export default BrandLink;