import React, { Component } from "react";
import {
  Link
} from "react-router-dom";
import '../../css/search-bar.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


class SearchBar extends Component {
  constructor(props){
  	super(props);
  	this.state = {
  		inputText: ''
  	};
  }

  componentDidUpdate(){
  	console.log(this.state.inputText);
  }

  handleInputTextChange(event){
  	this.setState({
  		inputText: event.target.value
  	});
  }

  handleInputSubmit(){

  }
  
  render(){
  	let inputBoxClass = "";
  	let containerClass = "";
  	if (this.props.searchbarLocation == "frontpage"){
  		containerClass = "frontpage-searchbar-container";
  		inputBoxClass = "frontpage-searchbar";
  	}else{
  		inputBoxClass = "header-searchbar";
  	}
    return(
      <div id="searchBarContainer" className={containerClass}>
      	<FontAwesomeIcon icon={faSearch} />
        <input id="searchBar" type="text" name="fname"
        	className={inputBoxClass}
        	onChange={(e) => {this.handleInputTextChange(e)}}
        	value={this.state.inputText}
        />
      </div>
    );
  }
}

export default SearchBar;