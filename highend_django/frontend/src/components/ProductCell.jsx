import React, { Component, useState } from "react";
import {
  Link
} from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

function StockBox() {

  const [showBox, setShowBox] = useState(false);

  // useEffect(() => {
  //   const tooltip;
  // }, [showBox]); // Only re-run the effect if count changes

  const handleBoxShow = () => {
    setShowBox(true);
    console.log("show");
  };

  const handleBoxHide = () => {
    setShowBox(false);
    console.log("hide");
  };

  return(
    <div className="product_stockbox" 
      onMouseOver={handleBoxShow}
      onMouseOut={handleBoxHide}
    >
      <FontAwesomeIcon icon="cubes"/>
      {showBox ? <div className="product_stock_tooltip">hello</div> : ''}
    </div>
  );

}
      // onMouseOver={}
      // onMouseOut={}
class ProductCell extends Component {

  handleStockBoxShow() {
    console.log("hello");
  }

  handleStockBoxHide() {

  }

  render(){
    return(
      <div 
        className="product_cell_container"
        onMouseOver={this.handleStockBoxShow}
        onMouseOut={this.handleStockBoxHide}
      >
        <a className="product_cell_link" href={`https://www.ssense.com/en-ca${this.props.productLink}`}>
          <picture>
            <img className="product_cell_image" src={this.props.pictureSrc} alt={this.props.productName}></img>
          </picture>
        </a>
        <a className="product_cell_description_link" href={`https://www.ssense.com/en-ca${this.props.productLink}`}>
          <div className="product_cell_description">
            <div className="product_cell_brand_name">{this.props.brand}</div>
            <div className="product_cell_name">{this.props.productName}</div>
            <div className="product_cell_price">${this.props.productPrice}</div>
          </div>
        </a>
        <div className="product_cell_stock_description"></div>
      </div>
    );
  }
}

export default ProductCell;