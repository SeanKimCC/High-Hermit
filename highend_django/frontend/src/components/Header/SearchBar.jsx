import React, { Component, useState, useEffect } from "react";
import { useDispatch } from 'react-redux'
import {
  Link,
  withRouter,
  useHistory
} from "react-router-dom";
import '../../css/search-bar.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { connect } from "react-redux";
import { fetchProducts } from '../../js/actions/index';



function mapStateToProps(state) {
  return { products: state.products };
}  

function mapDispatchToProps(dispatch) {
  return {
    fetchProducts: (brandName, pageNum, searchQuery) => dispatch(fetchProducts(brandName, pageNum, searchQuery)),
  };
}


function SearchBar(props){
	const [inputText, setInputText] = useState('');
	let history = useHistory();
	const dispatch = useDispatch();

	const onInputTextChange = (e) => {
		console.log(e);
		setInputText(e.target.value);
	}

	const handleInputSubmit = () => {
		dispatch(fetchProducts(null, null, inputText));
		history.push(`/products`);
	}

	const handleKeyPress = (target) => {
		if(target.charCode==13){
			handleInputSubmit();
		}
	}

  	let inputBoxClass = "";
  	let containerClass = "";
  	let searchIconClass = "";
  	if (props.searchbarLocation == "frontpage"){
  		containerClass = "frontpage-searchbar-container";
  		inputBoxClass = "frontpage-searchbar";
  		searchIconClass = "frontpage-search-icon";

  	}else{
  		containerClass = "header-searchbar-container";
  		inputBoxClass = "header-searchbar";
  		searchIconClass = "header-search-icon";
  	}
    return(
      <div id="searchBarContainer" className={containerClass}>
      	<div></div>
      	<FontAwesomeIcon className={searchIconClass} icon={faSearch} />
        <input id="searchBar" type="text" name="fname"
        	className={inputBoxClass}
        	onChange={(e) => {onInputTextChange(e)}}
        	onKeyPress={e => handleKeyPress(e)}
        	value={inputText}
        	onSubmit={handleInputSubmit}
        />
      </div>
    );
}
export default SearchBar;