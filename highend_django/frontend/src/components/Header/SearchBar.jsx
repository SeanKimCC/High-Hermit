import React, { Component, useState, useEffect } from "react";
import { useDispatch } from 'react-redux';
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

import Select from 'react-select';

const customStyles = {
  container: (provided, state) => ({
    ...provided,
    width: '200px',
    fontSize: '15px',
    position: 'absolute',
    left: '180px',
    top: '11px',
  }),
}
 
const options = [
  { value: 'chocolate', label: 'Chocolate' },
  { value: 'strawberry', label: 'Strawberry' },
  { value: 'vanilla', label: 'Vanilla' },
];


function SearchBar(props){
	const [inputText, setInputText] = useState('');
  const [selectedOption, setSelectedOption] = useState(options[0]);

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

  const handleChangeOptions = (sOpt) => {
    setSelectedOption(sOpt);
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
    <React.Fragment>
      <Select
        styles={customStyles}
        value={selectedOption}
        onChange={handleChangeOptions}
        options={options}
      />
      <div id="searchBarContainer" className={containerClass}>
      	<FontAwesomeIcon className={searchIconClass} icon={faSearch} />
        <input id="searchBar" type="text" name="fname"
        	className={inputBoxClass}
        	onChange={(e) => {onInputTextChange(e)}}
        	onKeyPress={e => handleKeyPress(e)}
        	value={inputText}
        	onSubmit={handleInputSubmit}
        />
      </div>
    </React.Fragment>
  );
}
export default SearchBar;