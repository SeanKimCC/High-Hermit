import React, { Component } from "react";
import {
  Link
} from "react-router-dom";
import '../../css/search-bar.css';


class SearchBar extends Component {
  
  render(){
    return(
      <div id="searchBarContainer">
        <input id="searchBar" type="text" name="fname"/>
      </div>
    );
  }
}

export default SearchBar;