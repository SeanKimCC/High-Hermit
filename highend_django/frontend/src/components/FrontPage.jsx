import React, { Component } from "react";
import {
  Link
} from "react-router-dom";
import SearchBar from "./Header/SearchBar";
import '../css/frontpage.css';


class FrontPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      productData: []
    }
  }
  
  render(){
    return(
      <div className="frontpage-container">
        <div className="frontpage-content-container centered">
          <Link to="/">
             <div className="frontpage-title borderbox">
               <img className="frontpage-logo" src={require("../resources/images/HH_logo_grey.svg")} alt="High Hermit"
                 onMouseOver={e => (e.currentTarget.src = require("../resources/images/HH_logo_green_and_grey.svg"))}
                 onMouseOut={e => (e.currentTarget.src = require("../resources/images/HH_logo_grey.svg"))}
               />
             </div>
          </Link>
          <SearchBar
            searchbarLocation="frontpage"
          />
          <div className="frontpage-category-menus">
            <div className="frontpage-category"><p className="category-text">Clothings</p></div>
            <div className="frontpage-category"><p className="category-text">Designers</p></div>
            <div className="frontpage-category"><p className="category-text">Shoes</p></div>
            <div className="frontpage-category"><p className="category-text">Essentials</p></div>
          </div>
        </div>
      </div>
    );
  }
}

export default FrontPage;