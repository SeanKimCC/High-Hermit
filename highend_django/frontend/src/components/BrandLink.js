import React, { Component } from "react";
import { render } from "react-dom";
import { trackPromise } from 'react-promise-tracker';


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

  fetchProducts() {
    console.log("does it get here", this.props.brandName);

    trackPromise(fetch("/api/products/?brandName="+encodeURI(this.props.brandName)+"&page="+this.props.pageNum)
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
            productData: [data],
            loaded: true
          };
        });
      }));
  }

  componentDidMount() {
    this.fetchProducts();
  }

  componentDidUpdate(prevProps) {
     console.log(prevProps, this.props);
     if (prevProps.brandName !== this.props.brandName) {
       this.fetchProducts();
     }
   }


  render() {
    console.log("hello");
    if(this.state.productData && this.state.productData[0]) {
      console.log(this.state);
      return (
        <ul>
          {this.state.productData[0].map(product => {
            return (
              <li key={product.unique_id}>
                {product.brand_name} <br/>
                {product.product_name} <br/>
                {product.sale_price} <br/>
              </li>
            );
          })}
        </ul>
      );
    } else {
      return (<div></div>);
    }
    
  }
}

export default BrandLink;