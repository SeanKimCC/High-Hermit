import React, { Component } from "react";
import { render } from "react-dom";
// import { trackPromise, usePromiseTracker } from 'react-promise-tracker';
import { fetchProducts, exitNavigationMenu } from '../js/actions/index';
import { connect } from "react-redux";
import ProductCell from './ProductCell';


function mapStateToProps(state) {
  return { showNavigation: state.showNavigationMenu, products: state.products };
}  

function mapDispatchToProps(dispatch) {
  return {
    exitNavigationMenu: () => dispatch(exitNavigationMenu()),
    fetchProducts: (brandName, pageNum) => dispatch(fetchProducts(brandName, pageNum)),
  };
}

class BrandLink extends Component {
  constructor(props) {
    super(props);
    this.state = {
      brandName: '',
      productData: [],
      loaded: false,
      placeholder: "Loading"
    };

    // this.fetchProducts = this.fetchProducts.bind(this);

  }

  // fetchProducts() {
  //   console.log("does it get here", this.props.brandName);

  //   trackPromise(fetch("/api/products/?brandName="+encodeURI(this.props.brandName)+"&page="+this.props.pageNum)
  //     .then(response => {
  //       if (response.status >= 400) {
  //         return this.setState(() => {
  //           return { placeholder: "Something went wrong!" };
  //         });
  //       }
  //       return response.json();
  //     })
  //     .then(data => {
  //       this.setState(() => {
  //         return {
  //           productData: [data],
  //           loaded: true
  //         };
  //       });
  //     }));
  // }

  componentDidMount() {
    // this.fetchProducts();
    console.log("line 58 of BrandLink.js", this);
    this.props.fetchProducts(this.props.brandName, this.props.pageNum, this.props.searchQuery);
  }

  componentDidUpdate(prevProps) {
     console.log(prevProps, this.props);
     if (prevProps.brandName !== this.props.brandName) {
       // this.fetchProducts();
       console.log("line 66 of BrandLink.js", this);
       this.props.fetchProducts(this.props.brandName, this.props.pageNum, this.props.searchQuery);
     }
   }


  render() {
    console.log("hello");
    // if(this.state.productData && this.state.productData[0]) {
    console.log(this, "72");
    const product_container_class = this.props.showNavigation ? 'product--container product--overlay' : 'product--container'; 
    if(this.props.products) {
      console.log(this.props, this.state);
      return (

        <div className={product_container_class} onMouseOver={this.props.exitNavigationMenu}>
          {this.props.products.map(product => {
            return (
              <ProductCell 
                key={product.unique_id}
                brand={product.brand_name}
                productName={product.product_name}
                productPrice={product.sale_price}
                pictureSrc={product.product_image}
                productLink={product.product_link}
              />
            );
          })}
        </div>
      );
    } else {
      return (<div></div>);
    }
    
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(BrandLink);