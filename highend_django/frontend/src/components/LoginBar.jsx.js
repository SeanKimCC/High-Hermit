import React, { Component } from "react";
import {
  Link
} from "react-router-dom";

class LoginBar extends Component {
  
  render(){
    return(
      <div className="product_cell_container">
        <a href={`https://www.ssense.com/en-ca${this.props.productLink}`}>
          <picture>
            <img className="product_cell_image" src={this.props.pictureSrc} alt={this.props.productName}></img>
          </picture>
          <div className="product_cell_brand_name">{this.props.brand}</div>
          <div className="product_cell_name">{this.props.productName}</div>
          <div className="product_cell_price">{this.props.productPrice}</div>
        </a>
      </div>
    );
  }
}

export default LoginBar;